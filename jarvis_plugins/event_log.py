"""
Event Log Analyzer for JARVIS.
Parse Windows Security, System, and Application event logs.
Detect suspicious logins, service failures, crashes, audit failures.
"JARVIS, check security logs" / "JARVIS, recent login attempts"
"""
import subprocess
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path

_LOG_INSTANCE = None
_LOG_LOCK = threading.Lock()


class EventLogAnalyzer:
    def __init__(self):
        pass

    def _query_log(self, log_name, count=10, hours=24):
        """Query a Windows event log using PowerShell."""
        try:
            ps_cmd = (
                f"$start = (Get-Date).AddHours(-{hours}); "
                f"Get-WinEvent -LogName {log_name} -MaxEvents {count} | "
                "Select-Object TimeCreated, LevelDisplayName, ProviderName, Message | "
                "Sort-Object TimeCreated -Descending | ConvertTo-Json"
            )
            r = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True, text=True, timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if r.returncode == 0 and r.stdout.strip():
                try:
                    events = json.loads(r.stdout)
                    if isinstance(events, dict):
                        events = [events]
                    return events
                except:
                    pass
        except:
            pass
        return []

    def security_log(self, hours=24):
        """Show recent security events: logins, privilege use, audit failures."""
        events = self._query_log("Security", count=15, hours=hours)
        if not events:
            return "No security events in the last 24 hours."

        suspicious = []
        lines = [f"Security events (last {hours}h):"]
        for e in events:
            ts = str(e.get("TimeCreated", ""))[:16] if e.get("TimeCreated") else ""
            typ = e.get("LevelDisplayName", "?")
            src = str(e.get("ProviderName", "") or "")[:20]
            msg = (str(e.get("Message", "") or ""))[:100].replace("\n", " ")
            prefix = "[!]" if typ.lower() in ("failureaudit", "error") else " - "
            lines.append(f"{prefix} {ts} {typ}: {src} | {msg}")
            if typ.lower() == "failureaudit":
                suspicious.append(f"SUSPICIOUS: Failed login at {ts} - {msg[:80]}")

        result = "\n".join(lines[:20])
        if suspicious:
            result += "\n\nWARNINGS:\n" + "\n".join(suspicious[:5])
        return result

    def system_log(self, hours=24):
        """Show recent system events: crashes, service failures, driver issues."""
        events = self._query_log("System", count=20, hours=hours)
        if not events:
            return "No system events in the last 24 hours."

        errors = []
        lines = [f"System events (last {hours}h):"]
        for e in events:
            ts = e.get("TimeGenerated", "")[:16]
            typ = e.get("EntryType", "?")
            src = e.get("Source", "")[:25]
            if typ.lower() in ("error", "warning"):
                msg = (e.get("Message", "") or "")[:100].replace("\n", " ")
                prefix = "[!]" if typ.lower() == "error" else "[?]"
                lines.append(f"{prefix} {ts} {src} | {msg}")
                if typ.lower() == "error":
                    errors.append(f"ERROR: {src} at {ts} - {msg[:80]}")

        result = "\n".join(lines[:20])
        if errors:
            result += f"\n\nCRITICAL ({len(errors)}):\n" + "\n".join(errors[:5])
        return result

    def application_log(self, hours=24):
        """Show recent application events: crashes, hangs."""
        events = self._query_log("Application", count=20, hours=hours)
        if not events:
            return "No application events in the last 24 hours."

        errors = []
        lines = [f"Application events (last {hours}h):"]
        for e in events:
            ts = e.get("TimeGenerated", "")[:16]
            typ = e.get("EntryType", "?")
            src = e.get("Source", "")[:25]
            if typ.lower() in ("error", "warning"):
                msg = (e.get("Message", "") or "")[:100].replace("\n", " ")
                prefix = "[!]" if typ.lower() == "error" else "[?]"
                lines.append(f"{prefix} {ts} {src} | {msg}")
                if typ.lower() == "error":
                    errors.append(f"CRASH: {src} at {ts}")

        result = "\n".join(lines[:20])
        if errors:
            result += f"\n\nCRASHES ({len(errors)}):\n" + "\n".join(errors[:5])
        return result

    def login_attempts(self, hours=24):
        """Show recent login attempts (success + failures)."""
        events = self._query_log("Security", count=30, hours=hours)
        if not events:
            return "No login events found."

        logins = []
        for e in events:
            msg = (e.get("Message", "") or "").lower()
            if any(x in msg for x in ["logon", "login", "credential", "authenticate"]):
                ts = e.get("TimeGenerated", "")[:16]
                typ = e.get("EntryType", "?")
                detail = (e.get("Message", "") or "")[:120].replace("\n", " ")
                prefix = "[FAIL]" if "fail" in typ.lower() or "fail" in msg else "[OK]"
                logins.append(f"{prefix} {ts}: {detail}")

        if not logins:
            return "No login attempts in the last 24 hours."

        return f"Login attempts (last {hours}h):\n" + "\n".join(logins[:15])

    def full_audit(self):
        """Run a full audit: security, system, app errors."""
        sec = self.security_log(24)
        sys = self.system_log(24)
        app = self.application_log(24)
        logins = self.login_attempts(24)
        return f"SECURITY AUDIT\n{'='*40}\n{sec}\n\n{'='*40}\n{sys}\n\n{'='*40}\n{app}\n\n{'='*40}\n{logins}"


def get_log_analyzer():
    global _LOG_INSTANCE
    with _LOG_LOCK:
        if _LOG_INSTANCE is None:
            try:
                _LOG_INSTANCE = EventLogAnalyzer()
            except:
                _LOG_INSTANCE = False
    return _LOG_INSTANCE if _LOG_INSTANCE is not False else None
