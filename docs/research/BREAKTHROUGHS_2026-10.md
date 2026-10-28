# Local voice-agent breakthroughs + Apple Intelligence (research agent, 2026-10-28)

Mac: macOS 27.0.1 (26A434), M5, 24 GB.

## Apple Intelligence
- **What it is:** Foundation Models, one fixed ~3B on-device model. It can stand in for Ollama in the LLM slot, but it can't load other weights.
- **Bridges:**
  - apfel (Arthur-Ficial/apfel, MIT, about 6.5k stars, v1.16.0 2026-10-05) exposes it as an OpenAI-compatible server with streaming and tools.
  - Apple's own python-apple-fm-sdk (Apache-2) is Python bindings, not a server.
- **Limits:**
  - 8192-token context on macOS 27 with M3+.
  - Guardrails can refuse harmless prompts.
  - Apple Intelligence must be switched on.
  - `/usr/bin/fm` needs `sudo fm license` to be accepted (owner's call).
- **SpeechAnalyzer/SpeechTranscriber** (macOS 26+): on-device streaming STT with interim words. Swift only; no maintained Python wrapper.
- **Verdict:**
  - optional LLM backend via apfel (M7 bake-off)
  - SpeechTranscriber is a candidate for live words in M5, via a Swift sidecar
  - TTS: no

## What changed May–Oct 2026
- **Ollama:** MLX is the default runner since v0.40.0. qwen3.5:4b has `-mlx` and `-mtp` tags.
- **Pipecat 1.12–1.14:**
  - built-in Moonshine STT (segments only, no interim words), Pocket TTS, Piper
  - Whisper MLX event-loop fix
  - Smart Turn v3.2 bundled (still the latest)
- **Streaming STT:** Moonshine streaming (MIT), parakeet-mlx tdt-v3 (CC-BY), Voxtral-Mini-4B-Realtime (Apache, on MLX via mlx-audio).
- **TTS:** mlx-audio 0.6.3 runs Kokoro / Qwen3-TTS / Chatterbox on the GPU. Pocket TTS (CPU, CC-BY). Chatterbox-Flash (MIT).
- **Full-duplex:** NVIDIA NemotronLabs-VoiceChat-11B (4-bit MLX exists, OpenMDW licence). Watch.

## Plan changes
- **Adopt now:** Ollama ≥0.40 (done: 0.40.11, MLX runner confirmed), voice thinking off, log time to first token.
- **M5 bake-off adds:** Voxtral-Realtime (MLX) and Apple SpeechTranscriber (sidecar).
- **M7 bake-off:** qwen3.5:4b vs gemma4:e4b vs Apple on-device (apfel).
- **TTS bake-off:** kokoro-onnx (CPU) vs mlx-audio Kokoro (GPU), with Pocket TTS as a fallback.
- **Watch:** NemotronLabs-VoiceChat, Chatterbox-Flash, Smart Turn v4, Pipecat LLMWithBackend.

Sources: full list in the agent report, including github.com/Arthur-Ficial/apfel, github.com/apple/python-apple-fm-sdk, developer.apple.com/documentation/speech/speechanalyzer, github.com/ollama/ollama/releases, github.com/pipecat-ai/pipecat/releases, github.com/Blaizzy/mlx-audio, huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602.
