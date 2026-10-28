# Decisions

| ID | Date | Decision | Why | Verdict |
|---|---|---|---|---|
| D01 | 2026-10-28 | Fully local + free stack: Pipecat 1.14, SmallWebRTC, Silero + Smart Turn, MLX Whisper, Ollama qwen3.5:4b, Kokoro, Python 3.13 | Owner: "completely, fully hosted locally for free" | keep |
| D02 | 2026-10-28 | Engine only now; real site designed later on voice.js | Owner: "for now, we're just building the engine" | keep |
| D03 | 2026-10-28 | Blank slate: no branding or content from the reference site; agent named "Assistant" | Owner: "do not include those other people's branding" | keep |
| D04 | 2026-10-28 | Private repo, merges enforced by script/CI (no branch protection on free private) | Owner picked defaults | keep |
| D05 | 2026-10-28 | iPhone HTTPS via mkcert | Default; keeps traffic on the LAN | keep |
| D06 | 2026-10-28 | voice.js API milestone moved to M3 (right after M2); M5/M6 transcript kept separate | Contract settles before transcript work; shorter walks | keep |
| D07 | 2026-10-28 | Ollama: Homebrew service only; Ollama.app removed | Owner: "del app"; two installs fight over port 11434 | keep |
| D08 | 2026-10-28 | Test layers: make test / smoke / converse / e2e / verify-local; /dev console in M2 | Owner asked for testing harnesses and UI | keep |
| D09 | 2026-10-28 | Spiked huggingface/speech-to-speech v1.1.0 fully local: works (4/4 clips heard exactly, sensible replies), but 2.7–8.3 s to first sound, ~75% in the LLM; the 1.7B voice model holds the shared GPU lock 6–7 s per turn; Low Power Mode was on | Owner asked whether an existing repo already does this | keep notes (spikes/hf-s2s) |
| D10 | 2026-10-28 | Speed comes from moving compute to free/near-free cloud services; "fully local" becomes "local or cloud, by setting". Pending spikes T-M0-09/10, decided in T-M0-12 | Owner: "how to find free online compute that gets this done fast. Free or close to free" | pending |
