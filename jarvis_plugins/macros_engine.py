"""Command Macros + Media Summary for JARVIS. Quick workflows + video tools."""
import subprocess, threading, re, json
from pathlib import Path

_MACRO_INSTANCE = None
_MACRO_LOCK = threading.Lock()

MACROS = {
    "recording mode": [
        ("open_app", "obs"),
        ("mute_volume", "mute"),
    ],
    "coding mode": [
        ("open_app", "vscode"),
        ("open_url", "github.com"),
    ],
    "gaming mode": [
        ("open_app", "discord"),
        ("open_app", "spotify"),
    ],
    "cleanup": [
        ("run_powershell", "Clear-RecycleBin -Force"),
        ("run_powershell", "ipconfig /flushdns"),
        ("clear_temp_files", ""),
    ],
    "focus mode": [
        ("focus_mode", ""),
        ("mute_volume", "mute"),
    ],
}

class MacrosEngine:
    def __init__(self):
        self._macros = dict(MACROS)
        self._load_custom()

    def _load_custom(self):
        f = Path.home() / ".jarvis_macros.json"
        if f.exists():
            try:
                custom = json.loads(f.read_text())
                self._macros.update(custom)
            except: pass

    def _save_custom(self):
        custom = {k:v for k,v in self._macros.items() if k not in MACROS}
        if custom:
            (Path.home() / ".jarvis_macros.json").write_text(json.dumps(custom, indent=2))

    def run(self, name):
        name = name.lower().strip()
        if name not in self._macros:
            return f"No macro named '{name}'. Say list macros to see available."
        actions = self._macros[name]
        for action_name, arg in actions:
            try:
                if action_name == "open_app":
                    subprocess.Popen(["start", arg], shell=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                elif action_name == "open_url":
                    import webbrowser
                    webbrowser.open(arg if arg.startswith("http") else f"https://{arg}")
                elif action_name == "run_powershell":
                    subprocess.run(["powershell", "-Command", arg], capture_output=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                elif action_name == "mute_volume":
                    subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], capture_output=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            except: pass
        return f"Macro '{name}' executed: {len(actions)} actions."

    def list(self):
        names = list(self._macros.keys())
        return "Available macros: " + ", ".join(names) + ". Say 'run macro recording mode' to trigger."

    def add(self, name, actions_json):
        try:
            actions = json.loads(actions_json)
            self._macros[name.lower().strip()] = actions
            self._save_custom()
            return f"Macro '{name}' saved with {len(actions)} actions."
        except:
            return "Invalid JSON for macro actions."

    def delete(self, name):
        name = name.lower().strip()
        if name in MACROS:
            return "Cannot delete built-in macros."
        if name in self._macros:
            del self._macros[name]
            self._save_custom()
            return f"Macro '{name}' deleted."
        return f"Macro '{name}' not found."

    def summarize_media(self, url=""):
        """Extract info about a YouTube video or webpage."""
        if not url:
            return "Provide a URL to summarize."
        try:
            import requests
            hdrs = {"User-Agent":"Mozilla/5.0"}
            r = requests.get(url, headers=hdrs, timeout=8)
            title = re.search(r'<title>([^<]+)</title>', r.text, re.I)
            t = title.group(1).strip() if title else "Unknown"

            # YouTube specific
            if "youtube.com" in url or "youtu.be" in url:
                vid_id = None
                m = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
                if m: vid_id = m.group(1)
                if not vid_id:
                    m = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
                    if m: vid_id = m.group(1)

                if vid_id:
                    oembed = requests.get(f"https://www.youtube.com/oembed?url=https://youtube.com/watch?v={vid_id}&format=json", headers=hdrs, timeout=5)
                    if oembed.status_code == 200:
                        data = oembed.json()
                        return f"YouTube: '{data.get('title', t)}' by {data.get('author_name', '?')}. {t}"
                    return f"YouTube video: {t}"

            # Generic page
            desc = re.search(r'<meta name="description" content="([^"]+)"', r.text, re.I)
            d = desc.group(1)[:200] if desc else ""
            return f"Page: {t}" + (f" - {d}" if d else "")
        except:
            return f"Could not access {url}."


def get_macros():
    global _MACRO_INSTANCE
    with _MACRO_LOCK:
        if _MACRO_INSTANCE is None:
            try: _MACRO_INSTANCE = MacrosEngine()
            except: _MACRO_INSTANCE = False
    return _MACRO_INSTANCE if _MACRO_INSTANCE is not False else None
