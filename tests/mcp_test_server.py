#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor MCP de prueba - network.checkResonance (Nivel B)."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from mcp_network.resonance import check_node_resonance


class MCPTestHandler(BaseHTTPRequestHandler):
    """Minimal JSON-RPC 2.0 endpoint for local MCP integration tests."""

    def do_POST(self):
        if self.path != "/jsonrpc":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            post_data = self.rfile.read(content_length)
            request = json.loads(post_data.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error"},
                    }
                ).encode("utf-8")
            )
            return

        if request.get("method") == "network.checkResonance":
            node = request.get("params", {}).get("node")
            result = check_node_resonance(node)
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": result,
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32601, "message": "Method not found"},
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


if __name__ == "__main__":
    port = 8506
    server = HTTPServer(("127.0.0.1", port), MCPTestHandler)
    print(f"🚀 MCP Test Server escuchando en http://127.0.0.1:{port}/jsonrpc")
    print("Método expuesto: network.checkResonance")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
