# speech-vision-pipelines

`pipeline.py` combines a transcription call and an image question into one parcel-damage report, and `compose.yaml` starts the two local servers it targets.

## Goal

Show the wire formats for speech (`/v1/audio/transcriptions`, multipart) and vision (`/v1/chat/completions` with an `image_url` part) on OpenAI-compatible local servers, with the HTTP transport injectable so it can be checked offline.

## Run it

```
python3 pipeline.py
# against real servers (needs docker compose up -d and a pulled llava model):
python3 pipeline.py http://localhost:8001 http://localhost:11434 note.wav photo.png
```

Expected from the first command: `ok: pipeline wire formats and wiring {'customer_said': 'the box arrived crushed', 'photo_shows': 'yes, a corner is dented'}`.

Not run end to end: the containers were never started. The default run uses `fake_post`, which asserts the request format but not what the real servers return.

## What it proves

- `transcribe()` builds a multipart body with a `model` field and a `file` part, and reads `text` from the reply.
- `describe()` base64-encodes the image into a `data:image/png;base64,` URL inside a chat message.
- `damage_report()` joins both results into `{"customer_said": ..., "photo_shows": ...}`; `compose.yaml` pins `faster-whisper-server:0.4.1-cpu` on port 8001 and `ollama/ollama:0.5.7` on 11434.

## Trade-offs

- The stub validates only what `fake_post` asserts; real servers may reject details such as audio format.
- Whisper-tiny on CPU is fast but inaccurate; `llava` needs a manual `ollama pull`.
- Inputs are sent whole with a 120 s timeout, with no chunking of long audio or large images.

## When not to use it

- For real-time or streaming transcription: this is a single request per file.
- When the image is always the same kind of document, a dedicated OCR tool is cheaper than a vision model.
