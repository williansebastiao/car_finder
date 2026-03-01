"""
MCP Client — connects to the car-finder MCP server over stdio.

The server is started as a child process; communication happens via
stdin/stdout using the MCP protocol. Use as an async context manager:

    async with MCPClient() as client:
        vehicles = await client.search_vehicles(brand="Toyota", category="SUV")
"""

import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Project root so the server subprocess can resolve `src.*` imports
_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])


class MCPClient:
    def __init__(self) -> None:
        self._stdio_cm = None
        self._session_cm: ClientSession | None = None
        self.session: ClientSession | None = None

    async def __aenter__(self) -> "MCPClient":
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "src.server"],
            env={"PYTHONPATH": _PROJECT_ROOT},
        )

        self._stdio_cm = stdio_client(server_params)
        read_stream, write_stream = await self._stdio_cm.__aenter__()

        self._session_cm = ClientSession(read_stream, write_stream)
        self.session = await self._session_cm.__aenter__()
        await self.session.initialize()

        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        if self._session_cm is not None:
            await self._session_cm.__aexit__(*exc_info)
        if self._stdio_cm is not None:
            await self._stdio_cm.__aexit__(*exc_info)

    async def search_vehicles(self, **filters: Any) -> list[dict]:
        """Call the search_vehicles MCP tool with keyword filters.

        Filters are the same as VehicleFilters fields; None values are
        stripped before sending so the server uses its defaults.
        """
        if self.session is None:
            raise RuntimeError("MCPClient is not connected. Use 'async with'.")

        clean = {k: v for k, v in filters.items() if v is not None}
        result = await self.session.call_tool("search_vehicles", clean)

        if not result.content or result.isError:
            return []
        raw = result.content[0].text
        return json.loads(raw) if raw.strip() else []
