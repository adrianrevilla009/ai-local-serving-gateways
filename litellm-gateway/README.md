# litellm-gateway

A LiteLLM `config.yaml`, a `compose.yaml` that runs it next to Ollama, and `check_config.py`, which validates the config offline.

## Goal

Put one public model name, `chat`, in front of two local backends (Ollama and vLLM), with a fallback alias and a response cache, so callers never change their code when a backend changes.

## Run it

```
pip install pyyaml
python3 check_config.py
# full gateway (needs Docker and a pulled Ollama model):
docker compose up -d
```

Expected from the check: `ok: 2 aliases, 3 backends, fallback and cache configured`.

Not run end to end: the gateway container was never started here. The config is validated offline only. The compose file starts Ollama but not vLLM, so the vLLM backend of `chat` is unreachable there unless you add it.

## What it proves

- `config.yaml` lists two backends under the alias `chat` (`ollama_chat/llama3.2:1b` and `openai/Qwen/Qwen2.5-0.5B-Instruct`) with `simple-shuffle` routing and one retry.
- `router_settings.fallbacks` sends `chat` to `chat-fallback` (`qwen2.5:0.5b` on Ollama); the check fails if a fallback names an unknown alias or itself.
- The cache is on (`type: local`, `ttl: 300`) and the check rejects any `api_key` other than `none` or `os.environ/<VAR>`.

## Trade-offs

- The local cache lives in one process and is lost on restart; use Redis for several gateway replicas.
- `simple-shuffle` ignores backend load, so a slow CPU backend gets as much traffic as a fast GPU one.
- The check is a structural lint, not a LiteLLM parse; a wrong parameter name would pass it.

## When not to use it

- With a single backend and no need for fallback, call the server directly.
- When you need per-team budgets or auth, add LiteLLM's database-backed features; this config has none.
