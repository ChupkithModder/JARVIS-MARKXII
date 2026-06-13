"""
Process Watcher for JARVIS.
Real-time process creation/termination monitoring.
Detects suspicious processes, high CPU abusers, crypto miners.
"JARVIS, watch processes" / "JARVIS, what's eating my CPU?"
"""
import threading
import time
import psutil
from datetime import datetime
from pathlib import Path

_PROC_INSTANCE = None
_PROC_LOCK = threading.Lock()


class ProcessWatcher:
    def __init__(self):
        self._running = False
        self._thread = None
        self._alert_callback = None
        self._known_pids = set()
        self._suspicious_keywords = [
            "miner", "coin", "crypto", "xmrig", "nicehash", "phoenix",
            "keylog", "spy", "steal", "inject", "hook", "payload",
            "rat", "trojan", "backdoor", "shell", "reverse",
            "capture2text", "screenCapture", "stealth"
        ]
        self._high_cpu_pids = {}

    def start(self, alert_callback=None):
        if self._running:
            return "Process watcher already active."

        self._alert_callback = alert_callback
        self._known_pids = set(p.pid for p in psutil.process_iter())
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return "Process watcher active. Monitoring for suspicious activity."

    def stop(self):
        self._running = False
        return "Process watcher stopped."

    def _loop(self):
        while self._running:
            try:
                current_pids = set(p.pid for p in psutil.process_iter())

                # New processes
                new_pids = current_pids - self._known_pids
                for pid in new_pids:
                    try:
                        p = psutil.Process(pid)
                        name = p.name()
                        if any(kw in name.lower() for kw in self._suspicious_keywords):
                            msg = f"SUSPICIOUS PROCESS: {name} (PID {pid})"
                            if self._alert_callback:
                                self._alert_callback(msg)
                    except:
                        pass

                # High CPU processes
                for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
                    try:
                        proc.cpu_percent(interval=0.1)  # prime measurement
                    except:
                        pass
                time.sleep(0.5)
                for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
                    try:
                        cpu = proc.info["cpu_percent"] or 0
                        if cpu > 50:
                            pid = proc.info["pid"]
                            name = proc.info["name"]
                            if pid not in self._high_cpu_pids:
                                self._high_cpu_pids[pid] = {"name": name, "count": 0}
                            self._high_cpu_pids[pid]["count"] += 1
                            if self._high_cpu_pids[pid]["count"] >= 3:
                                msg = f"HIGH CPU: {name} at {cpu}% (PID {pid})"
                                if self._alert_callback:
                                    self._alert_callback(msg)
                                self._high_cpu_pids[pid]["count"] = 0
                    except:
                        pass

                self._known_pids = current_pids
            except:
                pass
            time.sleep(2)

    def top_processes(self, count=10):
        """Show top CPU-consuming processes."""
        procs = []
        for p in psutil.process_iter(["name", "cpu_percent", "memory_percent", "pid"]):
            try:
                procs.append(p.info)
            except:
                pass

        procs.sort(key=lambda x: x.get("cpu_percent", 0) or 0, reverse=True)
        lines = [f"Top {count} processes:"]
        for p in procs[:int(count)]:
            name = p.get("name", "?")[:25]
            cpu = p.get("cpu_percent", 0) or 0
            mem = p.get("memory_percent", 0) or 0
            pid = p.get("pid", "?")
            lines.append(f"  {name:25s} CPU:{cpu:5.1f}% MEM:{mem:5.1f}% PID:{pid}")
        return "\n".join(lines)

    def kill_suspicious(self):
        """Automatically kill processes matching suspicious keywords."""
        killed = []
        for p in psutil.process_iter(["name", "pid"]):
            try:
                name = p.info["name"].lower()
                if any(kw in name for kw in self._suspicious_keywords):
                    psutil.Process(p.info["pid"]).terminate()
                    killed.append(f"{p.info['name']} (PID {p.info['pid']})")
            except:
                pass

        if killed:
            return f"Terminated {len(killed)} suspicious processes: " + ", ".join(killed)
        return "No suspicious processes found."

    def status(self):
        state = "active" if self._running else "offline"
        procs = len(list(psutil.process_iter()))
        return f"Process watcher {state}. {procs} processes running."

    def process_info(self, name):
        """Get detailed info about a specific process."""
        found = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent",
                                       "create_time", "exe", "cmdline", "connections"]):
            try:
                if name.lower() in p.info["name"].lower():
                    info = {
                        "pid": p.info["pid"],
                        "name": p.info["name"],
                        "cpu": p.info.get("cpu_percent", 0),
                        "mem": p.info.get("memory_percent", 0),
                        "exe": p.info.get("exe", ""),
                        "cmdline": " ".join(p.info.get("cmdline", []) or [])[:100],
                    }
                    try:
                        ct = datetime.fromtimestamp(p.info.get("create_time", 0))
                        info["created"] = ct.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                    found.append(info)
            except:
                pass

        if not found:
            return f"No process matching '{name}' found."

        lines = [f"Processes matching '{name}' ({len(found)}):"]
        for f in found:
            lines.append(f"  PID:{f['pid']} | CPU:{f['cpu']:.1f}% | MEM:{f['mem']:.1f}%")
            if f.get("exe"):
                lines.append(f"    Path: {f['exe']}")
            if f.get("cmdline"):
                lines.append(f"    Args: {f['cmdline']}")
        return "\n".join(lines)


def get_proc_watcher():
    global _PROC_INSTANCE
    with _PROC_LOCK:
        if _PROC_INSTANCE is None:
            try:
                _PROC_INSTANCE = ProcessWatcher()
            except:
                _PROC_INSTANCE = False
    return _PROC_INSTANCE if _PROC_INSTANCE is not False else None
