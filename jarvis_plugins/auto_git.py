"""
Auto-Git for JARVIS.
Automatically commits and pushes JARVIS code to GitHub after updates.
"JARVIS, commit changes" / "JARVIS, push to github"
Also auto-commits when new features are added.
"""
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

_AUTOGIT_INSTANCE = None
_AUTOGIT_LOCK = threading.Lock()


class AutoGit:
    GIT_PATH = r"C:\Program Files\Git\bin\git.exe"
    DESKTOP = Path.home() / "Desktop"
    REMOTE = "origin"
    BRANCH = "master"

    def __init__(self):
        self._auto_enabled = False
        self._last_commit = ""
        self._pending = []
        self._lock = threading.Lock()

    def _git(self, *args, cwd=None):
        try:
            r = subprocess.run(
                [self.GIT_PATH] + list(args),
                capture_output=True, text=True, timeout=15,
                cwd=str(cwd or self.DESKTOP),
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return r.returncode == 0, r.stdout.strip(), r.stderr.strip()
        except Exception as e:
            return False, "", str(e)

    def status(self):
        ok, stdout, _ = self._git("status", "--short")
        if not ok:
            return "Git status check failed."
        if not stdout.strip():
            return "Working tree clean."
        changed = stdout.strip().split("\n")
        return f"{len(changed)} file(s) changed:\n{stdout[:500]}"

    def diff(self):
        ok, stdout, _ = self._git("diff", "--stat")
        if not ok:
            return "Git diff failed."
        return stdout or "No changes."

    def commit(self, message=""):
        msg = message or f"JARVIS update - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ok, stdout, stderr = self._git("add", "-A")
        if not ok:
            return f"Add failed: {stderr}"

        ok, stdout, stderr = self._git("commit", "-m", msg)
        if not ok and "nothing to commit" not in stderr.lower():
            return f"Commit failed: {stderr}"

        self._last_commit = msg
        return stdout or "Committed successfully."

    def push(self):
        ok, stdout, stderr = self._git("push", self.REMOTE, self.BRANCH)
        if not ok:
            return f"Push failed: {stderr}"
        return stdout or "Pushed successfully."

    def commit_and_push(self, message=""):
        msg = message or f"JARVIS auto-update - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        with self._lock:
            result = self.commit(msg)
            if "Committed" in result or "nothing to commit" in result.lower():
                push_result = self.push()
                self._last_commit = msg
                return f"{result}\n{push_result}"
            return result

    def enable_auto(self):
        self._auto_enabled = True
        return "Auto-commit enabled. JARVIS will push changes after feature additions."

    def disable_auto(self):
        self._auto_enabled = False
        return "Auto-commit disabled."

    def auto_status(self):
        state = "enabled" if self._auto_enabled else "disabled"
        return f"Auto-commit is {state}. Last commit: {self._last_commit or 'none'}."

    def log(self, count=5):
        ok, stdout, _ = self._git("log", f"-{count}", "--oneline")
        if not ok:
            return "Git log failed."
        return stdout or "No commits yet."

    def queue_commit(self, feature_name):
        """Queue a commit after a feature is added."""
        with self._lock:
            self._pending.append(f"Added {feature_name}")
            if self._auto_enabled:
                # Commit in background thread
                t = threading.Thread(target=self._auto_commit, daemon=True)
                t.start()

    def _auto_commit(self):
        time.sleep(2)  # small delay for file writes to settle
        with self._lock:
            if self._pending:
                msg = self._pending[-1]
                self._pending.clear()
                self.commit_and_push(f"JARVIS: {msg} - {datetime.now().strftime('%H:%M')}")

    def create_release(self, tag, notes=""):
        """Tag and push a release version."""
        msg = notes or f"JARVIS release {tag}"
        ok, stdout, stderr = self._git("tag", "-a", tag, "-m", msg)
        if not ok:
            return f"Tag failed: {stderr}"
        ok, stdout, stderr = self._git("push", self.REMOTE, tag)
        if not ok:
            return f"Push tag failed: {stderr}"
        return f"Release {tag} tagged and pushed."


def get_autogit():
    global _AUTOGIT_INSTANCE
    with _AUTOGIT_LOCK:
        if _AUTOGIT_INSTANCE is None:
            try:
                _AUTOGIT_INSTANCE = AutoGit()
            except:
                _AUTOGIT_INSTANCE = False
    return _AUTOGIT_INSTANCE if _AUTOGIT_INSTANCE is not False else None
