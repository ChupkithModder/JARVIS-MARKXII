"""
J.A.R.V.I.S Launcher v12.0 - MARK XII
- HTTP server on port 19847 with expanded API
- GPU monitoring, session logging, auto-restart
- Launches jarvis.py backend
- Opens HUD in Chrome/Edge app mode
"""
import sys, subprocess, os, threading, time, json, traceback, datetime, hashlib
from pathlib import Path

DESKTOP  = Path(__file__).parent
JARVIS   = DESKTOP / "jarvis.py"
HUD_HTML = DESKTOP / "jarvis_hud.html"
LOG      = DESKTOP / "jarvis_error.txt"
STATE_F  = Path.home() / ".jarvis_hud_state.json"
MEM_F    = Path.home() / ".jarvis_memory.json"
CHAT_F   = Path.home() / ".jarvis_chat_input.json"
PROJ_F   = DESKTOP / ".jarvis_projects.json"
SESSION_LOG = Path.home() / ".jarvis_session_log.json"
UPDATES_F = DESKTOP / ".jarvis_update_log.json"
VERSION = "12.0.0"
MARK = "MARK XV"

PY311 = Path(r"C:\Users\bdjaj\AppData\Local\Programs\Python\Python311\python.exe")
PY    = PY311 if PY311.exists() else Path(sys.executable)

sys.executable = str(PY)
sys.path.insert(0, str(DESKTOP))
os.chdir(str(DESKTOP))

_pending_commands = []
_backend_proc = None
_session_start = time.time()

# â”€â”€ Session Logging â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_session_events = []

def push_hud_command(cmd, arg=""):
    """Send a command to backend via state file and keep HUD queue mirror."""
    try:
        data = json.loads(STATE_F.read_text(encoding="utf-8")) if STATE_F.exists() else {}
    except:
        data = {}
    data["_hud_cmd"] = [cmd, arg]
    try:
        STATE_F.write_text(json.dumps(data), encoding="utf-8")
    except:
        pass
    try:
        _pending_commands.append((cmd, arg))
    except:
        pass


def latest_update_brief():
    try:
        if UPDATES_F.exists():
            data = json.loads(UPDATES_F.read_text(encoding="utf-8"))
            if data:
                e = data[0]
                changes = e.get("changes", [])
                return {
                    "title": e.get("label", "Update"),
                    "version": e.get("version", VERSION),
                    "summary": changes[0] if changes else "",
                    "date": e.get("date", "")
                }
    except:
        pass
    return {"title": "JARVIS MK 12", "version": VERSION, "summary": "", "date": ""}

def log_session_event(event_type, detail=""):
    """Log timestamped events for session analytics."""
    _session_events.append({
        "ts": datetime.datetime.now().isoformat(),
        "type": event_type,
        "detail": detail[:200]
    })
    # Keep last 500 events in memory
    if len(_session_events) > 500:
        _session_events.pop(0)

def save_session_log():
    """Persist session log to disk periodically."""
    while True:
        try:
            SESSION_LOG.write_text(json.dumps({
                "session_start": datetime.datetime.fromtimestamp(_session_start).isoformat(),
                "uptime_seconds": int(time.time() - _session_start),
                "events": _session_events[-100:]
            }, indent=2), encoding="utf-8")
        except: pass
        time.sleep(30)

# â”€â”€ System Info â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_sysinfo = {
    "cpu":0,"ram":0,"ram_used_gb":0,"ram_total_gb":0,
    "disk":0,"disk_free_gb":0,"tx_mb":0,"rx_mb":0,
    "top_proc":"","top_cpu":0,
    "bat_ok":False,"bat_pct":0,"bat_chg":False,
    "mem_rules":0,"mem_prefs":0,"mem_facts":0,"last_rule":"",
    "projects":[],"proj_done":0,"proj_active":0,
    "proc_count":0,"uptime":"",
    "gpu_name":"","gpu_util":0,"gpu_mem":0,"gpu_temp":0,
    "cpu_temp":0,"cpu_freq":0,
    "processes":[],
    "mission_title":"","mission_stage":"brief","mission_progress":0,"mission_confidence":0,
    "autonomy_mode":"guided"
}

def _get_gpu_info():
    """Get NVIDIA GPU stats via nvidia-smi."""
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if r.returncode == 0 and r.stdout.strip():
            parts = r.stdout.strip().split(",")
            if len(parts) >= 5:
                _sysinfo["gpu_name"] = parts[0].strip()[:20]
                _sysinfo["gpu_util"] = int(parts[1].strip())
                mem_used = float(parts[2].strip())
                mem_total = float(parts[3].strip())
                _sysinfo["gpu_mem"] = round(mem_used / mem_total * 100, 1) if mem_total > 0 else 0
                _sysinfo["gpu_temp"] = int(parts[4].strip())
    except: pass

def _update_sysinfo():
    try:
        import psutil, datetime as dt
        _sysinfo["cpu"] = round(psutil.cpu_percent(interval=0.5), 1)
        vm = psutil.virtual_memory()
        _sysinfo["ram"] = round(vm.percent, 1)
        _sysinfo["ram_used_gb"] = round(vm.used/1024**3, 1)
        _sysinfo["ram_total_gb"] = round(vm.total/1024**3, 1)

        try:
            du = psutil.disk_usage("C:\\")
            _sysinfo["disk"] = round(du.percent, 1)
            _sysinfo["disk_free_gb"] = round(du.free/1024**3, 1)
        except: pass

        net = psutil.net_io_counters()
        _sysinfo["tx_mb"] = net.bytes_sent // 1024 // 1024
        _sysinfo["rx_mb"] = net.bytes_recv // 1024 // 1024

        # CPU frequency
        try:
            freq = psutil.cpu_freq()
            if freq: _sysinfo["cpu_freq"] = round(freq.current, 0)
        except: pass

        # CPU temp (if available)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        _sysinfo["cpu_temp"] = round(entries[0].current, 1)
                        break
        except: pass

        try:
            top_procs = sorted(
                psutil.process_iter(["name","cpu_percent"]),
                key=lambda p: p.info.get("cpu_percent") or 0, reverse=True)
            if top_procs:
                _sysinfo["top_proc"] = top_procs[0].info["name"][:16]
                _sysinfo["top_cpu"] = round(top_procs[0].info.get("cpu_percent") or 0, 1)
            _sysinfo["proc_count"] = len(top_procs)
            # Top 15 processes for modal
            _sysinfo["processes"] = [
                [p.info["name"][:20], round(p.info.get("cpu_percent") or 0, 1)]
                for p in top_procs[:15] if p.info.get("name")
            ]
        except: pass

        try:
            bat = psutil.sensors_battery()
            if bat:
                _sysinfo.update(bat_ok=True, bat_pct=round(bat.percent,1), bat_chg=bat.power_plugged)
            else:
                _sysinfo["bat_ok"] = False
        except: _sysinfo["bat_ok"] = False

        # Uptime
        try:
            boot = dt.datetime.fromtimestamp(psutil.boot_time())
            up = dt.datetime.now() - boot
            h, rem = divmod(int(up.total_seconds()), 3600)
            _sysinfo["uptime"] = f"{h}h {rem//60:02d}m"
        except: pass

        # Memory counts
        try:
            if MEM_F.exists():
                mem = json.loads(MEM_F.read_text(encoding="utf-8"))
                _sysinfo["mem_rules"] = len(mem.get("rules",[]))
                _sysinfo["mem_prefs"] = len(mem.get("preferences",{}))
                _sysinfo["mem_facts"] = len(mem.get("facts",{}))
                rules = mem.get("rules",[])
                _sysinfo["last_rule"] = rules[-1].get("rule","")[:35] if rules else ""
        except: pass

        # Projects
        try:
            if PROJ_F.exists():
                reg = json.loads(PROJ_F.read_text(encoding="utf-8"))
                active = [{"name":k,"lang":v.get("language",""),"status":v.get("status","active"),
                           "notes":v.get("notes",[])}
                          for k,v in reg.items() if v.get("status","active")=="active"]
                done = sum(1 for v in reg.values() if v.get("status") in ("complete","archived"))
                _sysinfo["projects"] = active[:5]
                _sysinfo["proj_done"] = done
                _sysinfo["proj_active"] = len(active)
        except: pass

        # Mission telemetry from live HUD state file.
        try:
            if STATE_F.exists():
                st = json.loads(STATE_F.read_text(encoding="utf-8"))
                mission = st.get("mission", {}) or {}
                _sysinfo["mission_title"] = str(mission.get("title", ""))[:64]
                _sysinfo["mission_stage"] = str(mission.get("stage", "brief"))
                _sysinfo["mission_progress"] = int(mission.get("progress", 0) or 0)
                _sysinfo["mission_confidence"] = int(mission.get("confidence", 0) or 0)
                _sysinfo["autonomy_mode"] = str(st.get("autonomy_mode", "guided"))
        except:
            pass

    except: pass

def _sysinfo_loop():
    gpu_tick = 0
    while True:
        _update_sysinfo()
        # GPU every 3 cycles (slower since nvidia-smi is expensive)
        if gpu_tick % 3 == 0:
            _get_gpu_info()
        gpu_tick += 1
        time.sleep(1.5)

# â”€â”€ HTTP Handler â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
from http.server import HTTPServer, BaseHTTPRequestHandler

class HUDHandler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Cache-Control","no-store")

    def _json_response(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self._cors(); self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_GET(self):
        if self.path == "/state":
            try: data = json.loads(STATE_F.read_text()) if STATE_F.exists() else {}
            except: data = {}
            if _pending_commands:
                data["_hud_cmd"] = list(_pending_commands.pop(0))
            self._json_response(data)

        elif self.path == "/sysinfo":
            self._json_response(_sysinfo)

        elif self.path == "/memory":
            try:
                data = json.loads(MEM_F.read_text(encoding="utf-8")) if MEM_F.exists() else {}
            except: data = {}
            self._json_response(data)

        elif self.path == "/projects":
            try:
                data = json.loads(PROJ_F.read_text(encoding="utf-8")) if PROJ_F.exists() else {}
            except: data = {}
            self._json_response(data)

        elif self.path == "/session":
            self._json_response({
                "uptime": int(time.time() - _session_start),
                "events_count": len(_session_events),
                "recent_events": _session_events[-20:]
            })

        elif self.path == "/health":
            upd = latest_update_brief()
            self._json_response({
                "status": "online",
                "uptime_seconds": int(time.time() - _session_start),
                "backend_alive": _backend_proc is not None and _backend_proc.poll() is None,
                "sysinfo_fresh": True,
                "version": VERSION,
                "mark": MARK,
                "latest_update": upd
            })

        elif self.path in ("/","/hud"):
            try:
                html = HUD_HTML.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type","text/html; charset=utf-8")
                self._cors(); self.end_headers()
                self.wfile.write(html)
            except:
                self.send_response(404); self.end_headers()
        elif self.path == "/deep-dive-report":
            try:
                report = Path.home() / ".jarvis_deep_dive_report.json"
                if report.exists():
                    data = json.loads(report.read_text(encoding="utf-8"))
                    self._json_response(data)
                else:
                    self._json_response({"error": "No report available"})
            except:
                self._json_response({"error": "Failed to load report"})
        elif self.path == "/kill":
            self._json_response({"ok":True,"killing":"jarvis processes only"})
            import subprocess as _sp
            _sp.Popen(
                ["powershell","-Command",
                 "$targets = Get-CimInstance Win32_Process | Where-Object { "
                 "($_.Name -match 'pythonw?\\.exe' -or $_.Name -match 'wscript\\.exe') -and "
                 "($_.CommandLine -match 'jarvis|JARVIS') }; "
                 "foreach ($p in $targets) { try { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue } catch {} }"],
                creationflags=getattr(_sp, 'CREATE_NO_WINDOW', 0)
            )
            os._exit(0)
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path == "/command":
            try:
                length = int(self.headers.get("Content-Length",0))
                body = json.loads(self.rfile.read(length))
                cmd = body.get("cmd","")
                arg = body.get("arg","")
                if cmd == "enter_project":
                    push_hud_command("enter_project", arg)
                    log_session_event("project_enter", arg)
                elif cmd == "quick_action":
                    qa = str(arg or action)
                    push_hud_command("quick_action", qa)
                    log_session_event("quick_action", qa)
                elif cmd == "chat_message":
                    try:
                        CHAT_F.write_text(json.dumps({"message": arg}), encoding="utf-8")
                    except: pass
                    log_session_event("chat", arg)
                elif cmd == "chat_mode":
                    push_hud_command("chat_mode", arg or "toggle")
                    log_session_event("chat_mode", str(arg or "toggle"))
                self._json_response({"ok":True})
            except Exception as e:
                self.send_response(500); self.end_headers()

        elif self.path == "/chat":
            try:
                length = int(self.headers.get("Content-Length",0))
                body = json.loads(self.rfile.read(length))
                text = body.get("text","")
                if text:
                    try:
                        CHAT_F.write_text(json.dumps({"message": text}), encoding="utf-8")
                    except: pass
                    log_session_event("chat", text)
                self._json_response({"ok":True})
            except:
                self.send_response(500); self.end_headers()
        else:
            self.send_response(404); self.end_headers()

def _start_server():
    server = HTTPServer(("127.0.0.1", 19847), HUDHandler)
    log_session_event("server_start", "HTTP server on port 19847")
    server.serve_forever()

# â”€â”€ Backend with Auto-Restart â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def _launch_backend():
    global _backend_proc
    max_restarts = 5
    restarts = 0

    while restarts < max_restarts:
        try:
            log_session_event("backend_start", f"Attempt {restarts+1}")
            _backend_proc = subprocess.Popen(
                [str(PY), str(JARVIS)],
                cwd=str(DESKTOP),
                stderr=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            # Wait for early crash
            for _ in range(150):
                time.sleep(0.1)
                if _backend_proc.poll() is not None:
                    stderr = _backend_proc.stderr.read().decode("utf-8", errors="replace")
                    LOG.write_text(f"Backend crashed (code {_backend_proc.returncode}):\n{stderr}", encoding="utf-8")
                    log_session_event("backend_crash", stderr[:200])
                    restarts += 1
                    time.sleep(2)
                    break
            else:
                # No early crash â€” monitor
                _backend_proc.stderr.close()
                log_session_event("backend_online", "Backend running")
                # Wait for process to exit
                _backend_proc.wait()
                log_session_event("backend_exit", f"Code {_backend_proc.returncode}")
                restarts += 1
                time.sleep(3)
                continue
        except Exception as e:
            LOG.write_text(f"Backend error:\n{e}\n{traceback.format_exc()}", encoding="utf-8")
            log_session_event("backend_error", str(e)[:200])
            restarts += 1
            time.sleep(3)

    log_session_event("backend_exhausted", f"Max restarts ({max_restarts}) reached")
    # Reset HUD status so it doesn't stay stuck on SHUTDOWN
    try:
        if STATE_F.exists():
            sd = json.loads(STATE_F.read_text(encoding="utf-8"))
            sd["status"] = "standby"
            sd["text"] = "Backend offline - restart JARVIS"
            STATE_F.write_text(json.dumps(sd), encoding="utf-8")
    except: pass

# â”€â”€ Open HUD â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def _open_hud():
    time.sleep(0.8)
    url = "http://127.0.0.1:19847/hud"
    chrome = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    edge   = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    for browser, flag_prefix in [(chrome,"--app"), (edge,"--app")]:
        if browser.exists():
            subprocess.Popen([
                str(browser),
                f"{flag_prefix}={url}",
                "--window-size=1000,640",
                "--window-position=50,50",
                "--disable-infobars",
                "--no-first-run",
                "--disable-extensions",
            ])
            log_session_event("hud_open", str(browser.name))
            return
    import webbrowser
    webbrowser.open(url)
    log_session_event("hud_open", "default browser")

# â”€â”€ Main â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
log_session_event("launcher_start", f"JARVIS {MARK} v{VERSION}")

threading.Thread(target=_sysinfo_loop, daemon=True).start()
threading.Thread(target=_start_server, daemon=True).start()
threading.Thread(target=_launch_backend, daemon=True).start()
threading.Thread(target=_open_hud, daemon=True).start()
threading.Thread(target=save_session_log, daemon=True).start()

while True:
    time.sleep(60)
