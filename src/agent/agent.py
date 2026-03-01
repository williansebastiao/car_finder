"""
CarFinderAgent — conversational Claude agent backed by MCP.

The agent maintains conversation history across turns. When it decides
it has enough context to run a search, it calls the `search_vehicles`
MCP tool via Claude's native tool-use mechanism, then presents the
results to the user in natural language.
"""

import json
from typing import Any

import anthropic

from src.core.settings import settings
from src.integrations.mcp import MCPClient

_MODEL = "claude-sonnet-4-6"

_SYSTEM_PROMPT = """\
Você é um assistente simpático especializado em ajudar pessoas a encontrarem \
o carro ideal. Converse de forma natural, sem transformar a conversa em um \
formulário rígido. Faça perguntas relevantes sobre preferências do usuário \
(marca, modelo, ano, combustível, câmbio, cor, condição, categoria, faixa \
de preço, quilometragem máxima) mas só quando fizer sentido no diálogo.

Quando tiver informações suficientes para realizar uma busca, use a ferramenta \
`search_vehicles`. Pode realizar múltiplas buscas se necessário (ex.: ampliar \
a faixa de preço ou remover um filtro quando não houver resultados).

Ao apresentar os resultados, seja claro e amigável. Para cada veículo mostre: \
marca, modelo, ano, cor, quilometragem e preço (em reais). Se não encontrar \
nenhum veículo, sugira relaxar algum filtro e ofereça uma nova busca.

Responda sempre em português do Brasil.
"""

_SEARCH_TOOL: dict[str, Any] = {
    "name": "search_vehicles",
    "description": (
        "Busca veículos no banco de dados com base nos filtros informados. "
        "Todos os parâmetros são opcionais. Retorna até 10 veículos ordenados "
        "pelo menor preço."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "brand": {
                "type": "string",
                "description": "Marca do veículo (ex.: Toyota, Honda, Fiat).",
            },
            "model": {
                "type": "string",
                "description": "Modelo do veículo (ex.: Corolla, HB20).",
            },
            "year_min": {
                "type": "integer",
                "description": "Ano mínimo de fabricação.",
            },
            "year_max": {
                "type": "integer",
                "description": "Ano máximo de fabricação.",
            },
            "fuel": {
                "type": "string",
                "description": (
                    "Tipo de combustível: Flex, Gasoline, Diesel, "
                    "Electric, Hybrid, Natural Gas."
                ),
            },
            "transmission": {
                "type": "string",
                "description": (
                    "Câmbio: Manual, Automatic, CVT, "
                    "Automated Manual, Dual Clutch."
                ),
            },
            "color": {
                "type": "string",
                "description": "Cor do veículo (ex.: White, Black, Red).",
            },
            "condition": {
                "type": "string",
                "description": "Estado: New, Semi-new ou Used.",
            },
            "category": {
                "type": "string",
                "description": (
                    "Categoria: Hatch, Sedan, SUV, Pickup, "
                    "Minivan, Coupe, Convertible, Wagon, Van."
                ),
            },
            "min_price": {
                "type": "number",
                "description": "Preço mínimo em reais.",
            },
            "max_price": {
                "type": "number",
                "description": "Preço máximo em reais.",
            },
            "max_mileage": {
                "type": "integer",
                "description": "Quilometragem máxima.",
            },
        },
        "required": [],
    },
}


class CarFinderAgent:
    def __init__(self, mcp_client: MCPClient) -> None:
        self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self._mcp = mcp_client
        self._history: list[dict[str, Any]] = []

    async def chat(self, user_message: str) -> str:
        """Process one user turn and return the assistant's reply."""
        self._history.append({"role": "user", "content": user_message})

        while True:
            response = self._client.messages.create(
                model=_MODEL,
                max_tokens=1024,
                system=_SYSTEM_PROMPT,
                messages=self._history,
                tools=[_SEARCH_TOOL],
            )

            # Append assistant turn (may contain text + tool_use blocks)
            self._history.append(
                {"role": "assistant", "content": response.content}
            )

            if response.stop_reason == "end_turn":
                return self._extract_text(response.content)

            if response.stop_reason == "tool_use":
                tool_results = await self._handle_tool_calls(response.content)
                self._history.append({"role": "user", "content": tool_results})
                # Loop: let Claude compose its final reply with the results
                continue

            # Unexpected stop reason — surface the last text block
            return self._extract_text(response.content)

    async def _handle_tool_calls(
        self, content: list[Any]
    ) -> list[dict[str, Any]]:
        tool_results = []

        for block in content:
            if block.type != "tool_use":
                continue

            if block.name == "search_vehicles":
                vehicles = await self._mcp.search_vehicles(**block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(vehicles, ensure_ascii=False),
                    }
                )

        return tool_results

    @staticmethod
    def _extract_text(content: list[Any]) -> str:
        for block in content:
            if hasattr(block, "text"):
                return block.text
        return ""
