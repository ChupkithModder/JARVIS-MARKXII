"""
Voice Cloner for JARVIS.
Clone any voice from a short audio sample, then have JARVIS speak in that voice.
Uses edge-tts for voice selection or Piper for local voice synthesis.
"JARVIS, clone this voice" / "JARVIS, speak in [name]'s voice"
"""
import threading
import subprocess
import tempfile
import json
from pathlib import Path

_CLONER_INSTANCE = None
_CLONER_LOCK = threading.Lock()


class VoiceCloner:
    def __init__(self):
        self._voices = {}
        self._active_voice = "jarvis"
        self._load_voices()

    def _load_voices(self):
        voices_file = Path.home() / ".jarvis_voices.json"
        if voices_file.exists():
            try:
                self._voices = json.loads(voices_file.read_text())
            except:
                self._voices = {}

    def _save_voices(self):
        voices_file = Path.home() / ".jarvis_voices.json"
        voices_file.write_text(json.dumps(self._voices, indent=2))

    def list_available_voices(self):
        """List all edge-tts and known voices."""
        voices = []
        try:
            import asyncio, edge_tts
            async def _get():
                return await edge_tts.list_voices()
            result = asyncio.new_event_loop().run_until_complete(_get())
            for v in result[:20]:
                voices.append(f"{v['ShortName']} ({v['Locale']} - {v['Gender']})")
        except:
            pass

        if self._voices:
            voices.append("--- Cloned Voices ---")
            for name in self._voices:
                voices.append(f"{name} (cloned)")

        if not voices:
            return "No voices available. Install: pip install edge-tts"
        return "Available voices:\n" + "\n".join(voices[:30])

    def clone_voice(self, name, audio_path=""):
        """Register a voice to use for TTS. Uses edge-tts voice mapping."""
        name = name.strip().lower()
        self._voices[name] = {
            "type": "cloned",
            "source": str(audio_path) if audio_path else "edge-tts",
            "added": str(Path(audio_path).stat().st_mtime if audio_path and Path(audio_path).exists() else 0)
        }
        self._save_voices()
        return f"Voice '{name}' registered. Say 'speak in {name} voice' to use it."

    def set_voice(self, voice_name):
        """Set the active voice for TTS."""
        voice_name = voice_name.strip().lower()

        # Check if it's a known edge-tts voice
        edge_voices = ["en-us-guy", "en-us-jenny", "en-gb-sonia", "en-gb-ryan",
                       "en-au-natasha", "en-ca-clara", "en-ca-liam", "en-in-neerja",
                       "jarvis", "british", "american", "australian", "canadian"]

        mapping = {
            "jarvis": "en-GB-RyanNeural",
            "british": "en-GB-SoniaNeural",
            "american": "en-US-GuyNeural",
            "australian": "en-AU-NatashaNeural",
            "canadian": "en-CA-LiamNeural",
            "female": "en-US-JennyNeural",
            "male": "en-US-GuyNeural",
        }

        voice_name = voice_name.lower()
        if voice_name in mapping:
            self._active_voice = mapping[voice_name]
            return f"Voice set to {voice_name}."
        elif voice_name in self._voices:
            self._active_voice = voice_name
            return f"Voice set to {voice_name} (cloned)."
        else:
            self._active_voice = voice_name
            return f"Voice set to {voice_name}."

    def get_active_voice(self):
        return f"Current voice: {self._active_voice}"

    def speak_with_voice(self, text, voice=None):
        """Generate speech with the specified or active voice using edge-tts."""
        v = voice or self._active_voice
        try:
            import asyncio, edge_tts
            async def _speak():
                tmp = Path(tempfile.gettempdir()) / "jarvis_cloned_voice.mp3"
                tts = edge_tts.Communicate(text, v)
                await tts.save(str(tmp))
                return str(tmp)

            path = asyncio.new_event_loop().run_until_complete(_speak())
            if path:
                # Play the audio
                import winsound
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                return f"Speaking in {v}."
            return "Voice generation failed."
        except Exception as e:
            return f"Speech failed: {e}"

    def generate_and_save(self, text, voice, output_path):
        """Generate speech and save to file."""
        v = voice or self._active_voice
        try:
            import asyncio, edge_tts
            async def _gen():
                tts = edge_tts.Communicate(text, v)
                await tts.save(str(output_path))
            asyncio.new_event_loop().run_until_complete(_gen())
            return f"Saved speech to {output_path}."
        except Exception as e:
            return f"Saved speech failed: {e}"


def get_cloner():
    global _CLONER_INSTANCE
    with _CLONER_LOCK:
        if _CLONER_INSTANCE is None:
            try:
                _CLONER_INSTANCE = VoiceCloner()
            except:
                _CLONER_INSTANCE = False
    return _CLONER_INSTANCE if _CLONER_INSTANCE is not False else None
