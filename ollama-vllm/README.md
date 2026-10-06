# ollama-vllm

A compose file for Ollama and vLLM, one OpenAI-style client (`client.py`), and a mock server (`mock_server.py`) to run the client without a model.

## Goal

Show that Ollama (port 11434) and vLLM (port 8000) both expose the OpenAI API under `/v1`, so one client works against either. The default run uses a mock so it needs no GPU or download.

## Run it

```
python3 client.py
# against a real server (after docker compose up -d ollama and pulling the model):
python3 client.py http://localhost:11434 llama3.2:1b
```

Expected from the first command: `ok: OpenAI-compatible round trip: echo: ping`.

Not run end to end: the containers were never started here, so the Ollama and vLLM calls are untested. Only the mock round trip was run.

## What it proves

- `chat()` in `client.py` calls `GET /v1/models` and `POST /v1/chat/completions`, the same two requests for both servers.
- `mock_server.py` answers both routes and echoes the last message, so the check asserts `echo: ping`.
- `compose.yaml` pins `ollama/ollama:0.5.7` and puts `vllm/vllm-openai:v0.6.6` behind the `gpu` profile with one NVIDIA device reserved.

## Trade-offs

- The mock only proves the request and response shape, not model behaviour or latency.
- Ollama on CPU is slow; vLLM is fast but needs a GPU and a model download.
- The client does not stream, set timeouts or retry.

## When not to use it

- When you need streaming, tool calls or token usage: the mock and client cover only plain chat.
- For production serving: this is a single-node setup with no auth.
