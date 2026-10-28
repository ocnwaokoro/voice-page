# Spike: huggingface/speech-to-speech v1.1.0 (2026-10-28)

**Setup**
- Isolated venv (Python 3.13); `pip install speech-to-speech==1.1.0`.
- Config `mac.yaml`: Silero VAD + Smart Turn v3.2 → Parakeet TDT 0.6B v3 (MLX) → Qwen3.5-4B 4-bit (mlx-lm) → Qwen3-TTS 1.7B 6-bit (mlx-audio).
- Port 8799, because 8765 was already in use on this Mac.
- First run downloads all four models. A warm start takes ~35 s.

**Bench**
- `bench.py`: say-generated 16 kHz clips over the Realtime WebSocket, paced in real time, followed by silence.
- STT accuracy: 4/4 transcripts exact.
- Replies: short, sensible, and correct (Abuja).
- Server-side latency, last speech → first audio:

| run | vad | stt | llm | tts first audio | e2e |
|---|---|---|---|---|---|
| 1 | 0.10 | 0.09 | 3.98 | 0.19 | 4.70 |
| 2 | 0.10 | 0.06 | 3.94 | 0.33 | 4.53 |
| 3 | 0.10 | 0.11 | 2.04 | 0.32 | 2.72 |
| 4 | 0.10 | 0.18 | 5.30 | 0.36 | 6.16 |
| 5 | 0.10 | 0.09 | 2.94 | 0.38 | 3.63 |

**Caveat: the Mac was throttled during these runs**
- Low Power Mode was ON (`pmset -g`: lowpowermode 1), and the load average was 10–14 from other sessions.
- Plain Ollama read a 19-token prompt in 3.95 s and generated at 14.3 tok/s.
- So the LLM column is not representative. Rerun with Low Power Mode off.

**Notes**
- One session slot by default: a second client gets `session_limit_reached` until the first disconnects.
- Server latency logs are excellent (per-stage, MLX lock wait/hold).
- It has progressive (interim) STT built in, plus Realtime events: `conversation.item.input_audio_transcription.delta`, `response.output_audio_transcript.delta`, `input_audio_buffer.speech_started` (barge-in).
