"""Clipboard History for JARVIS - SQLite-backed searchable clipboard."""
import threading, time, sqlite3, json
from datetime import datetime
from pathlib import Path

_CLIP_INSTANCE = None
_CLIP_LOCK = threading.Lock()

class ClipboardHistory:
    def __init__(self):
        self._db = Path.home() / ".jarvis_clipboard.db"
        self._running = False
        self._thread = None
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(str(self._db))
        conn.execute("CREATE TABLE IF NOT EXISTS clips (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, length INTEGER, timestamp TEXT, app TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_clips_ts ON clips(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_clips_content ON clips(content)")
        conn.commit()
        conn.close()

    def start(self):
        if self._running: return "Clipboard monitor already active."
        try:
            import pyperclip
        except ImportError:
            return "Install pyperclip: pip install pyperclip"
        self._running = True
        self._last = ""
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return "Clipboard monitor active. Every copy is remembered."

    def stop(self):
        self._running = False
        return "Clipboard monitor stopped."

    def _loop(self):
        import pyperclip
        while self._running:
            try:
                txt = pyperclip.paste()
                if txt and txt != self._last and len(txt) > 1:
                    self._last = txt
                    conn = sqlite3.connect(str(self._db))
                    conn.execute("INSERT INTO clips (content, length, timestamp) VALUES (?,?,?)",
                                (txt[:5000], len(txt), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
            except: pass
            time.sleep(1.5)

    def search(self, query, limit=5):
        conn = sqlite3.connect(str(self._db))
        rows = conn.execute(
            "SELECT id, content, length, timestamp FROM clips WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
            (f"%{query}%", limit)
        ).fetchall()
        conn.close()
        if not rows:
            return f"No clipboard items matching '{query}'."
        lines = [f"{len(rows)} matches:"]
        for rid, content, length, ts in rows:
            preview = content[:80].replace("\n"," ").replace("\r","")
            lines.append(f"[{ts}] {preview}...")
        return "\n".join(lines)

    def recent(self, count=5):
        conn = sqlite3.connect(str(self._db))
        rows = conn.execute("SELECT content, length, timestamp FROM clips ORDER BY id DESC LIMIT ?", (count,)).fetchall()
        conn.close()
        if not rows:
            return "No clipboard history yet."
        lines = ["Recent clipboard:"]
        for content, length, ts in rows:
            preview = content[:100].replace("\n"," ").replace("\r","")
            lines.append(f"[{ts}] ({length} chars) {preview}")
        return "\n".join(lines)

    def get_by_id(self, clip_id):
        conn = sqlite3.connect(str(self._db))
        row = conn.execute("SELECT content FROM clips WHERE id=?", (clip_id,)).fetchone()
        conn.close()
        if row:
            import pyperclip
            pyperclip.copy(row[0])
            return f"Copied clip #{clip_id} back to clipboard."
        return f"Clip #{clip_id} not found."

    def stats(self):
        conn = sqlite3.connect(str(self._db))
        count = conn.execute("SELECT COUNT(*) FROM clips").fetchone()[0]
        conn.close()
        state = "active" if self._running else "offline"
        return f"Clipboard monitor {state}. {count} items stored."

    def clear(self):
        conn = sqlite3.connect(str(self._db))
        conn.execute("DELETE FROM clips")
        conn.commit()
        conn.close()
        return "Clipboard history cleared."


def get_clipboard():
    global _CLIP_INSTANCE
    with _CLIP_LOCK:
        if _CLIP_INSTANCE is None:
            try: _CLIP_INSTANCE = ClipboardHistory()
            except: _CLIP_INSTANCE = False
    return _CLIP_INSTANCE if _CLIP_INSTANCE is not False else None
