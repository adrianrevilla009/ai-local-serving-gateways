"""Same client code for Ollama (:11434) and vLLM (:8000): both speak the OpenAI API under /v1."""
import json
import sys
import threading
import urllib.request

from mock_server import serve


def chat(base_url, model, prompt):
    models = json.load(urllib.request.urlopen(f"{base_url}/v1/models"))
    assert models["data"], "server lists no models"
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(f"{base_url}/v1/chat/completions", body, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))["choices"][0]["message"]["content"]


if __name__ == "__main__":
    if len(sys.argv) > 1:  # e.g. client.py http://localhost:11434 llama3.2:1b
        print(chat(sys.argv[1], sys.argv[2], "Say hi in five words."))
    else:  # offline self-check against the mock
        server = serve()
        threading.Thread(target=server.serve_forever, daemon=True).start()
        out = chat(f"http://127.0.0.1:{server.server_port}", "mock-model", "ping")
        assert out == "echo: ping", out
        print("ok: OpenAI-compatible round trip:", out)
