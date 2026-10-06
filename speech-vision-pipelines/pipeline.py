"""Speech + vision pipeline against OpenAI-compatible local servers, with an injectable transport.

speech:  POST /v1/audio/transcriptions (multipart; e.g. faster-whisper-server)
vision:  POST /v1/chat/completions with an image_url part (e.g. Ollama llava, vLLM VLMs)
"""
import base64
import json
import sys
import urllib.request
import uuid


def http_post(url, body, content_type):
    req = urllib.request.Request(url, body, {"Content-Type": content_type})
    return json.load(urllib.request.urlopen(req, timeout=120))


def transcribe(post, base, audio_bytes, model="Systran/faster-whisper-tiny"):
    boundary = uuid.uuid4().hex
    parts = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\n{model}\r\n"
             f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.wav\"\r\n"
             "Content-Type: audio/wav\r\n\r\n").encode() + audio_bytes + f"\r\n--{boundary}--\r\n".encode()
    return post(f"{base}/v1/audio/transcriptions", parts, f"multipart/form-data; boundary={boundary}")["text"]


def describe(post, base, image_bytes, question, model="llava"):
    url = "data:image/png;base64," + base64.b64encode(image_bytes).decode()
    body = {"model": model, "messages": [{"role": "user", "content": [
        {"type": "text", "text": question}, {"type": "image_url", "image_url": {"url": url}}]}]}
    out = post(f"{base}/v1/chat/completions", json.dumps(body).encode(), "application/json")
    return out["choices"][0]["message"]["content"]


def damage_report(post, speech_base, vision_base, audio, image):
    """Voice note + photo of a parcel -> one structured line for an order ticket."""
    said = transcribe(post, speech_base, audio)
    seen = describe(post, vision_base, image, "Is the parcel damaged? Answer briefly.")
    return {"customer_said": said, "photo_shows": seen}


def fake_post(url, body, content_type):
    """Stub servers: checks the wire format the real servers expect."""
    if url.endswith("/audio/transcriptions"):
        assert content_type.startswith("multipart/form-data; boundary=") and b'name="file"' in body
        return {"text": "the box arrived crushed"}
    payload = json.loads(body)
    part = payload["messages"][0]["content"][1]
    assert part["image_url"]["url"].startswith("data:image/png;base64,")
    return {"choices": [{"message": {"content": "yes, a corner is dented"}}]}


if __name__ == "__main__":
    if len(sys.argv) == 5:  # pipeline.py SPEECH_URL VISION_URL audio.wav image.png
        audio, image = open(sys.argv[3], "rb").read(), open(sys.argv[4], "rb").read()
        print(damage_report(http_post, sys.argv[1], sys.argv[2], audio, image))
    else:
        report = damage_report(fake_post, "http://speech", "http://vision", b"RIFFfake", b"\x89PNGfake")
        assert report == {"customer_said": "the box arrived crushed", "photo_shows": "yes, a corner is dented"}, report
        print("ok: pipeline wire formats and wiring", report)
