"""Tiny OpenAI-compatible stand-in so the client can be verified without a GPU or model download."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def _send(self, body):
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send({"object": "list", "data": [{"id": "mock-model", "object": "model"}]})

    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        last = req["messages"][-1]["content"]
        self._send({"object": "chat.completion", "model": req["model"],
                    "choices": [{"index": 0, "finish_reason": "stop",
                                 "message": {"role": "assistant", "content": f"echo: {last}"}}]})

    def log_message(self, *args):
        pass


def serve(port=0):
    return HTTPServer(("127.0.0.1", port), Handler)
