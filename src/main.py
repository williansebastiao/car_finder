import asyncio
import sys

from src.agent.agent import CarFinderAgent
from src.integrations.mcp import MCPClient

_BANNER = """
╔══════════════════════════════════════════╗
║  Car Finder                              ║
║  Digite 'sair' ou Ctrl+C para encerrar   ║
╚══════════════════════════════════════════╝
"""

_EXIT_COMMANDS = {"sair", "exit", "quit", "q"}


async def _run() -> None:
    print(_BANNER)

    async with MCPClient() as mcp_client:
        agent = CarFinderAgent(mcp_client)

        # Kick off the conversation with a greeting
        greeting = await agent.chat(
            "Olá! Estou aqui para ajudar a encontrar o carro ideal."
        )
        print(f"Agente: {greeting}\n")

        while True:
            try:
                user_input = (await asyncio.to_thread(input, "Você: ")).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nAgente: Até mais! Boa sorte na busca pelo seu carro.")
                break

            if not user_input:
                continue

            if user_input.lower() in _EXIT_COMMANDS:
                print("\nAgente: Até mais! Boa sorte na busca pelo seu carro.")
                break

            response = await agent.chat(user_input)
            print(f"\nAgente: {response}\n")


def main() -> None:
    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
