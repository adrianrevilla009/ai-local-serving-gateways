# ai-local-serving-gateways

Six small examples of serving models on your own hardware: OpenAI-compatible local servers, a routing gateway in front of them, in-process ONNX inference from Java, Kubernetes serving manifests, speech and vision calls, and a decision note on fine-tuning vs RAG vs prompting. The shared Orders domain shows up in the scorer and the parcel-damage pipeline.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`ollama-vllm`](./ollama-vllm) | One client for Ollama and vLLM through the OpenAI API, checked against a local mock server | `python3 client.py` |
| [`litellm-gateway`](./litellm-gateway) | LiteLLM config with one alias over two backends, a fallback alias and caching, validated offline | `python3 check_config.py` |
| [`ml-serving-onnx`](./ml-serving-onnx) | A hand-built ONNX linear model scored from Java 21 with ONNX Runtime | `python3 make_model.py && mvn -B test` |
| [`kserve-triton-serving`](./kserve-triton-serving) | KServe InferenceService plus Triton model repository, checked for consistency | `python3 validate.py` |
| [`speech-vision-pipelines`](./speech-vision-pipelines) | Transcription and image questions over OpenAI-style endpoints, with a stubbed transport | `python3 pipeline.py` |
| [`fine-tuning-vs-rag-notes`](./fine-tuning-vs-rag-notes) | The fine-tuning vs RAG vs prompting decision written as testable rules | `python3 decide.py` |

## Prerequisites

- Python 3.10+, plus PyYAML for `litellm-gateway` and `kserve-triton-serving`
- Java 21 and Maven 3.9+ for `ml-serving-onnx`
- Docker, only to start the real servers from the compose files (vLLM also needs an NVIDIA GPU)
- A Kubernetes cluster with KServe, only to apply the manifest

## How to read it

Start with `ollama-vllm`, then `litellm-gateway`, which routes to the same backends. `ml-serving-onnx` and `kserve-triton-serving` belong together: the Triton config describes the model the Java folder builds.
