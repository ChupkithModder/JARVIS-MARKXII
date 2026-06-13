"""
Screen Ghost for JARVIS.
Continuously OCRs everything on screen, stores in searchable SQLite DB.
Windrecorder-style: "JARVIS, what was I looking at 10 minutes ago?"
"JARVIS, search screen history for 'password'"
"""
import threading
import time
import sqlite3
import json
from datetime import datetime
from pathlib import Path

_GHOST_INSTANCE = None
_GHOST_LOCK = threading.Lock()


class ScreenGhost:
    def __init__(self):
        self._running = False
        self._thread = None
        self._db_path = Path.home() / ".jarvis_screen_ghost.db"
        self._interval = 5  # capture every N seconds

    def _init_db(self):
        conn = sqlite3.connect(str(self._db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS screens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                text TEXT,
                active_window TEXT,
                summary TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ts ON screens(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_text ON screens(text)")
        conn.commit()
        return conn

    def start(self, interval=5):
        if self._running:
            return "Screen ghost already running."
        self._interval = int(interval)

        try:
            import mss
            import pytesseract
            import pygetwindow as gw
            import numpy as np
        except ImportError as e:
            return f"Missing dependency: {e}. Install: pip install mss pytesseract pygetwindow"

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return f"Screen ghost active. Capturing every {self._interval}s."

    def stop(self):
        self._running = False
        return "Screen ghost stopped."

    def _loop(self):
        import mss
        import pytesseract
        import pygetwindow as gw
        import numpy as np

        conn = self._init_db()

        while self._running:
            try:
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    img = sct.grab(monitor)
                    # Convert to PIL
                    from PIL import Image
                    pil_img = Image.frombytes("RGB", img.size, img.rgb)
                    # OCR
                    text = pytesseract.image_to_string(pil_img, timeout=5)[:5000]
                if not text.strip():
                    time.sleep(self._interval)
                    continue

                # Get active window title
                try:
                    win = gw.getActiveWindow()
                    active = win.title if win else "unknown"
                except:
                    active = "unknown"

                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn.execute(
                    "INSERT INTO screens (timestamp, text, active_window) VALUES (?,?,?)",
                    (ts, text, active)
                )
                conn.commit()
            except:
                pass
            time.sleep(self._interval)

        conn.close()

    def search(self, query, limit=10):
        conn = sqlite3.connect(str(self._db_path))
        conn.create_function("REGEXP", 2, lambda p, s: __import__("re").search(p, s, __import__("re").I) is not None)
        try:
            rows = conn.execute(
                "SELECT timestamp, active_window, text FROM screens WHERE text LIKE ? ORDER BY timestamp DESC LIMIT ?",
                (f"%{query}%", int(limit))
            ).fetchall()
        except:
            rows = []
        finally:
            conn.close()

        if not rows:
            return "No screen history matches that query."

        results = []
        for ts, win, text in rows:
            snippet = text[:200].replace("\n", " ")
            results.append(f"[{ts}] {win}: {snippet}")
        return f"Found {len(rows)} matches:\n" + "\n".join(results)

    def recent(self, minutes=5):
        conn = sqlite3.connect(str(self._db_path))
        cutoff = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Simple time check - get last N entries
        rows = conn.execute(
            "SELECT timestamp, active_window, text FROM screens ORDER BY id DESC LIMIT ?",
            (max(1, int(minutes) * 12),)
        ).fetchall()
        conn.close()

        if not rows:
            return "No recent screen history."

        windows = {}
        for ts, win, _ in rows:
            windows[win] = windows.get(win, 0) + 1

        top_windows = sorted(windows.items(), key=lambda x: -x[1])[:5]
        win_summary = " | ".join(f"{w}: {c}s" for w, c in top_windows)
        return f"Screen history ({len(rows)} captures): {win_summary}"

    def status(self):
        conn = sqlite3.connect(str(self._db_path))
        count = conn.execute("SELECT COUNT(*) FROM screens").fetchone()[0]
        conn.close()
        state = "active" if self._running else "offline"
        return f"Screen ghost {state}. {count} captures in database."

    def clear(self):
        conn = sqlite3.connect(str(self._db_path))
        conn.execute("DELETE FROM screens")
        conn.commit()
        conn.close()
        return "Screen history cleared."


def get_ghost():
    global _GHOST_INSTANCE
    with _GHOST_LOCK:
        if _GHOST_INSTANCE is None:
            try:
                _GHOST_INSTANCE = ScreenGhost()
            except:
                _GHOST_INSTANCE = False
    return _GHOST_INSTANCE if _GHOST_INSTANCE is not False else None
