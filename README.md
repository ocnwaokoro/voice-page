# voice-page

Press a mic and talk live with an AI agent, with a live transcript. Everything runs locally on a Mac for free; moving to a server later is a configuration change, not a rewrite.

**Status:** M0 (engines working on the Mac). See [plan/tickets.yaml](plan/tickets.yaml) and the GitHub milestones.

## Stack

| Part | Choice |
|---|---|
| Framework | [Pipecat](https://github.com/pipecat-ai/pipecat) 1.14 |
| Connection | SmallWebRTC (browser ↔ Mac peer-to-peer) |
| End of speech | Silero VAD + Smart Turn v3 |
| Speech to text | MLX Whisper large-v3-turbo, plus a streaming engine for live words (M5) |
| LLM | Ollama, `qwen3.5:4b` by default |
| Voice | Kokoro-82M |
| Python | 3.13 via uv |

Each engine is chosen by an environment variable (`STT_PROVIDER`, `LLM_PROVIDER`, `LLM_MODEL`, `TTS_PROVIDER`), so the same code runs with Linux/GPU engines or a hosted LLM later.

## Layout

```
server/   Pipecat bot + FastAPI server        (M1–M2)
web/      voice.js + a blank test page        (M2–M3)
config/   persona, topics, knowledge (YAML)   (M7)
e2e/ evals/ scripts/ deploy/
plan/     tickets.yaml: source of truth for issues
```

## Milestones

| | Milestone | You can… |
|---|---|---|
| M0 | Engines working on the Mac | hear the local voice say what the local model wrote |
| M1 | First real conversation | talk and interrupt in Pipecat's test page |
| M2 | Our server, voice.js, blank test page | talk from our own page |
| M3 | voice.js as a real API | drive the engine from a second page using only the docs |
| M4 | On the iPhone | talk from your phone over Wi-Fi |
| M5 | Live words as you speak | watch your words appear while you talk |
| M6 | Transcript and turn states | read a clean transcript with interruptions marked |
| M7 | Topics, persona, knowledge from config | tap a topic; the agent sticks to what it knows |
| M8 | Safe to leave running | the 6th caller gets "busy"; one command checks everything |
| M9 | Server-ready, still $0 | run the server build on the Mac and pass its tests |

Later phases: designing the real site (on voice.js) and going live on a rented server.

## Working rules

- Milestones run strictly in order.
- A ticket is done when its named tests pass **and** a real audio round-trip is observed with a number (for example, time to first audio). Proof is linked in the PR.
- Bug fixes start with a failing `[BUG-n]` test.
- PR bodies: What / Why / Proof, plus `Closes #n` once per issue.
