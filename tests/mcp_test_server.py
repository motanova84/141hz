#!/usr/bin/env python3
"""Minimal MCP test server exposing network.checkResonance via JSON-RPC."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict

from mcp_network.resonance import check_node_resonance

HOST = "127.0.0.1"
PORT = 8506
PATH = "/jsonrpc"
METHOD = "network.checkResonance"


class MCPTestHandler(BaseHTTPRequestHandler):
    def _write_json(self, status_code: int, payload: Dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_POST(self) -> None:  # noqa: N802
        if self.path != PATH:
            self._write_json(404, {"error": "Not Found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)

        try:
            request = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._write_json(
                400,
                {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                },
            )
            return

        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method != METHOD:
            self._write_json(
                200,
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": "Method not found"},
                },
            )
            return

        node = params.get("node") if isinstance(params, dict) else None
        if not node:
            self._write_json(
                200,
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": "Invalid params: node is required"},
                },
            )
            return

        result = check_node_resonance(str(node))
        self._write_json(200, {"jsonrpc": "2.0", "id": req_id, "result": result})


def main() -> None:
    server = HTTPServer((HOST, PORT), MCPTestHandler)
    print(f"🚀 MCP Test Server escuchando en http://{HOST}:{PORT}{PATH}")
    print(f"Método expuesto: {METHOD}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
