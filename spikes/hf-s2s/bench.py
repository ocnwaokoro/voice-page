"""Spike bench: send a wav to the HF speech-to-speech Realtime server, time the reply.

Usage: .venv/bin/python bench.py clips/q1.wav [...]
Clock starts when the last speech chunk is sent (mouth stops), then silence keeps flowing like a live mic.
"""

import asyncio
import base64
import json
import sys
import time
import wave

import websockets
from speech_to_speech.api.openai_realtime.audio_client import RealtimeAudioClientConfig, build_session_update

URL = "ws://127.0.0.1:8799/v1/realtime"
CHUNK_MS = 20


async def run(path: str) -> dict:
    with wave.open(path) as w:
        assert w.getframerate() == 16000 and w.getnchannels() == 1
        pcm = w.readframes(w.getnframes())
    step = 16000 * 2 * CHUNK_MS // 1000
    marks: dict = {}
    heard, said = "", ""
    async with websockets.connect(URL, max_size=None) as ws:
        await ws.send(json.dumps(build_session_update(RealtimeAudioClientConfig())))

        async def sender():
            for i in range(0, len(pcm), step):
                await ws.send(json.dumps({"type": "input_audio_buffer.append",
                                          "audio": base64.b64encode(pcm[i:i + step]).decode()}))
                await asyncio.sleep(CHUNK_MS / 1000)
            marks["speech_end"] = time.perf_counter()
            silence = base64.b64encode(b"\0" * step).decode()
            for _ in range(int(8000 / CHUNK_MS)):
                await ws.send(json.dumps({"type": "input_audio_buffer.append", "audio": silence}))
                await asyncio.sleep(CHUNK_MS / 1000)

        task = asyncio.create_task(sender())
        try:
            while True:
                ev = json.loads(await asyncio.wait_for(ws.recv(), timeout=30))
                t, now = ev["type"], time.perf_counter()
                if t == "input_audio_buffer.speech_stopped":
                    marks.setdefault("vad_stop", now)
                elif t == "conversation.item.input_audio_transcription.completed":
                    marks.setdefault("stt_done", now)
                    heard = ev.get("transcript", "")
                elif t == "response.output_audio_transcript.delta":
                    marks.setdefault("first_text", now)
                    said += ev.get("delta", "")
                elif t == "response.output_audio.delta":
                    marks.setdefault("first_audio", now)
                elif t == "response.done":
                    marks["done"] = now
                    break
                elif t == "error":
                    print("ERROR", ev)
                    break
        finally:
            task.cancel()
    end = marks.get("speech_end")
    ms = {k: round((v - end) * 1000) for k, v in marks.items() if end and k != "speech_end"}
    return {"clip": path, "heard": heard, "said": said.strip(), "ms_after_speech_end": ms}


async def main():
    for p in sys.argv[1:]:
        print(json.dumps(await run(p), indent=1))
        await asyncio.sleep(4)


asyncio.run(main())
