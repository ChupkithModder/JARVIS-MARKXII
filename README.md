# J.A.R.V.I.S - MARK XV

> *"Just A Rather Very Intelligent System"*

Iron Man-style personal AI assistant for Windows. Voice-controlled, HTML HUD, local LLM. 8 plugin modules.

## Architecture

```
jarvis.py            → Core backend (LLM, voice, tools, mission control)
JARVIS.pyw           → Launcher (HTTP server, HUD bridge, auto-restart)
jarvis_hud.html      → HTML/JS holographic interface (1900 lines)
launch.bat           → One-click launcher with dependency auto-check
jarvis_plugins/      → Plugin system (8 modules)
jarvis_skills/       → Custom skill scripts
```

## Features

### Voice & AI
- Wake word activation ("JARVIS")
- Local LLM via OpenAI-compatible API (LM Studio/Ollama)
- Speech-to-text (Whisper) + Text-to-speech (Piper/pyttsx3/edge-tts)
- 0 preset responses — everything generated fresh by the LLM
- Interruptible speech (say "JARVIS" while JARVIS is talking)

### HUD Interface
- Arc reactor animation with spinning rings
- System vitals (CPU, RAM, GPU, disk, network)
- Mission control board with progress tracking
- Intel bulletin board
- Threat assessment gauges
- Chat input for text commands

### Plugins

| Plugin | Capability | File |
|--------|-----------|------|
| Deep Dive | 104-site OSINT + breach check + people search | `deep_dive.py` |
| Browser Agent | Playwright-controlled Chrome browser | `browser_agent.py` |
| Surveillance | Webcam motion + face detection | `surveillance.py` |
| Gesture Control | MediaPipe hand → mouse/keyboard | `gesture_control.py` |
| Screen Ghost | OCR + searchable screen history | `screen_ghost.py` |
| Network Ghost | ARP/port scan, WiFi recon, DNS | `network_ghost.py` |
| Telegram OSINT | Phone → Telegram account lookup | `telegram_osint.py` |
| Voice Cloner | Clone any voice from 10s audio | `voice_cloner.py` |

### Built-in Tools (100+)
File ops, system info, processes, network, Spotify, Discord, 3D printing, calendar, notes, clipboard, code gen, git, security, weather, news, crypto...

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Launch
launch.bat
# OR
pythonw JARVIS.pyw
```

## Voice Commands

```
"JARVIS"                              — wake word
"deep dive on username"               — OSINT reconnaissance
"scan my network"                     — discover devices
"start screen recording"              — begin screen OCR
"gesture mode"                        — hand control via webcam
"enable surveillance"                 — webcam motion detection
"open browser"                        — launch controlled Chrome
"search YouTube for X"                — browser automation
"check telegram user"                 — phone/username lookup
"system status"                       — diagnostics
"what's the time"                     — casual chat
```

## Configuration

Config file: `%USERPROFILE%\.jarvis_config.json`

Key settings:
- `local_model_url` — LLM endpoint (default: `http://169.254.83.107:1234/v1`)
- `mic_device` — audio input device index
- `wake_words` — activation phrases

## License

MIT
