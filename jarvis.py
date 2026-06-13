#!/usr/bin/env python3
"""
J.A.R.V.I.S - Just A Rather Very Intelligent System
Full featured personal AI assistant.
"""

import os, sys, json, time, threading, subprocess, platform
import shutil, datetime, random, webbrowser, socket, hashlib, re
import winreg
from pathlib import Path


def check_and_install(package, import_name=None):
    import_name = import_name or package
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package, "-q"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

check_and_install("anthropic")
check_and_install("openai")
check_and_install("vosk")
check_and_install("speechrecognition", "speech_recognition")
check_and_install("sounddevice")
check_and_install("openai-whisper", "whisper")
check_and_install("pyttsx3")
check_and_install("requests")
check_and_install("psutil")
check_and_install("colorama")
check_and_install("numpy")
check_and_install("scipy")

import anthropic
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import pyttsx3
import psutil
import requests
import tkinter as tk
import math
import math as _math
from colorama import init, Fore, Style

DEEP_DIVE_ENGINE = None
def _get_deep_dive():
    global DEEP_DIVE_ENGINE
    if DEEP_DIVE_ENGINE is None:
        try:
            from jarvis_plugins.deep_dive import DeepDiveEngine
            DEEP_DIVE_ENGINE = DeepDiveEngine()
        except Exception as e:
            print(f"[JARVIS] Deep dive engine unavailable: {e}")
            DEEP_DIVE_ENGINE = False
    return DEEP_DIVE_ENGINE if DEEP_DIVE_ENGINE is not False else None

BROWSER_AGENT = False
def _get_browser():
    global BROWSER_AGENT
    if BROWSER_AGENT is False:
        try:
            from jarvis_plugins.browser_agent import get_agent
            BROWSER_AGENT = get_agent()
        except Exception as e:
            print(f"[JARVIS] Browser agent unavailable: {e}")
    return BROWSER_AGENT if BROWSER_AGENT is not False else None

SURVEILLANCE_ENGINE = False
def _get_surveillance():
    global SURVEILLANCE_ENGINE
    if SURVEILLANCE_ENGINE is False:
        try:
            from jarvis_plugins.surveillance import get_surveillance
            SURVEILLANCE_ENGINE = get_surveillance()
        except Exception as e:
            print(f"[JARVIS] Surveillance unavailable: {e}")
    return SURVEILLANCE_ENGINE if SURVEILLANCE_ENGINE is not False else None

GESTURE_CONTROLLER = False
def _get_gesture():
    global GESTURE_CONTROLLER
    if GESTURE_CONTROLLER is False:
        try:
            from jarvis_plugins.gesture_control import get_gesture
            GESTURE_CONTROLLER = get_gesture()
        except Exception as e:
            print(f"[JARVIS] Gesture control unavailable: {e}")
    return GESTURE_CONTROLLER if GESTURE_CONTROLLER is not False else None

SCREEN_GHOST = False
def _get_ghost():
    global SCREEN_GHOST
    if SCREEN_GHOST is False:
        try:
            from jarvis_plugins.screen_ghost import get_ghost
            SCREEN_GHOST = get_ghost()
        except Exception as e:
            print(f"[JARVIS] Screen ghost unavailable: {e}")
    return SCREEN_GHOST if SCREEN_GHOST is not False else None

NETWORK_GHOST = False
def _get_netghost():
    global NETWORK_GHOST
    if NETWORK_GHOST is False:
        try:
            from jarvis_plugins.network_ghost import get_netghost
            NETWORK_GHOST = get_netghost()
        except Exception as e:
            print(f"[JARVIS] Network ghost unavailable: {e}")
    return NETWORK_GHOST if NETWORK_GHOST is not False else None

TELEGRAM_INTEL = False
def _get_tg():
    global TELEGRAM_INTEL
    if TELEGRAM_INTEL is False:
        try:
            from jarvis_plugins.telegram_osint import get_telegram_intel
            TELEGRAM_INTEL = get_telegram_intel()
        except Exception as e:
            print(f"[JARVIS] Telegram intel unavailable: {e}")
    return TELEGRAM_INTEL if TELEGRAM_INTEL is not False else None

VOICE_CLONER = False
def _get_cloner():
    global VOICE_CLONER
    if VOICE_CLONER is False:
        try:
            from jarvis_plugins.voice_cloner import get_cloner
            VOICE_CLONER = get_cloner()
        except Exception as e:
            print(f"[JARVIS] Voice cloner unavailable: {e}")
    return VOICE_CLONER if VOICE_CLONER is not False else None

USB_SENTINEL = False
def _get_usb():
    global USB_SENTINEL
    if USB_SENTINEL is False:
        try:
            from jarvis_plugins.usb_sentinel import get_usb_sentinel
            USB_SENTINEL = get_usb_sentinel()
        except Exception as e:
            print(f"[JARVIS] USB sentinel unavailable: {e}")
    return USB_SENTINEL if USB_SENTINEL is not False else None

LOG_ANALYZER = False
def _get_logs():
    global LOG_ANALYZER
    if LOG_ANALYZER is False:
        try:
            from jarvis_plugins.event_log import get_log_analyzer
            LOG_ANALYZER = get_log_analyzer()
        except Exception as e:
            print(f"[JARVIS] Event log analyzer unavailable: {e}")
    return LOG_ANALYZER if LOG_ANALYZER is not False else None

PROC_WATCHER = False
def _get_procwatch():
    global PROC_WATCHER
    if PROC_WATCHER is False:
        try:
            from jarvis_plugins.process_watcher import get_proc_watcher
            PROC_WATCHER = get_proc_watcher()
        except Exception as e:
            print(f"[JARVIS] Process watcher unavailable: {e}")
    return PROC_WATCHER if PROC_WATCHER is not False else None

AUTO_GIT = False
def _get_autogit():
    global AUTO_GIT
    if AUTO_GIT is False:
        try:
            from jarvis_plugins.auto_git import get_autogit
            AUTO_GIT = get_autogit()
        except Exception as e:
            print(f"[JARVIS] Auto-git unavailable: {e}")
    return AUTO_GIT if AUTO_GIT is not False else None

MACROS_ENGINE = False
def _get_macros():
    global MACROS_ENGINE
    if MACROS_ENGINE is False:
        try:
            from jarvis_plugins.macros_engine import get_macros
            MACROS_ENGINE = get_macros()
        except Exception as e:
            print(f"[JARVIS] Macros engine unavailable: {e}")
    return MACROS_ENGINE if MACROS_ENGINE is not False else None

CLIPBOARD_HISTORY = False
def _get_clipboard():
    global CLIPBOARD_HISTORY
    if CLIPBOARD_HISTORY is False:
        try:
            from jarvis_plugins.clipboard_history import get_clipboard
            CLIPBOARD_HISTORY = get_clipboard()
        except Exception as e:
            print(f"[JARVIS] Clipboard history unavailable: {e}")
    return CLIPBOARD_HISTORY if CLIPBOARD_HISTORY is not False else None

REACT_AGENT = False
def _get_react():
    global REACT_AGENT
    if REACT_AGENT is False:
        try:
            from jarvis_plugins.react_agent import get_react
            REACT_AGENT = get_react()
        except Exception as e:
            print(f"[JARVIS] ReAct agent unavailable: {e}")
    return REACT_AGENT if REACT_AGENT is not False else None

init(autoreset=True)

JARVIS_PATH = Path(__file__).resolve()



HUD_STATE_FILE = Path.home() / ".jarvis_hud_state.json"
PROJECTS_FILE  = Path.home() / "Desktop" / "Jarvis MARK 15" / ".jarvis_projects.json"
MISSION_STAGES = ["brief", "plan", "execute", "verify", "complete"]

def _write_hud(status="standby", text="", tool="", hud_mode="", hud_data=None, active_project="", mission=None, trace=None, blockers=None, autonomy_mode=""):
    """Write status to HUD state file."""
    try:
        import json as _j, time as _t
        f = Path.home() / ".jarvis_hud_state.json"
        existing = {}
        try: existing = _j.loads(f.read_text()) if f.exists() else {}
        except: pass
        d = {
            "status": status, "text": text, "tool": tool, "ts": _t.time(),
            "active_project": active_project or existing.get("active_project",""),
            "hud_mode": hud_mode or existing.get("hud_mode",""),
            "hud_data":  hud_data or existing.get("hud_data",{}),
            "mission": mission or existing.get("mission", {}),
            "trace": trace if trace is not None else existing.get("trace", []),
            "blockers": blockers if blockers is not None else existing.get("blockers", []),
            "autonomy_mode": autonomy_mode or existing.get("autonomy_mode", ""),
            "_hud_cmd": existing.get("_hud_cmd"),
        }
        f.write_text(_j.dumps(d))
    except: pass


class MissionControlEngine:
    """Persistent mission timeline + guided autonomy state."""
    def __init__(self, memory, pc):
        self.memory = memory
        self.pc = pc
        self._trace = []
        self._ensure_schema()
        self.autonomy_mode = (self.memory.data.get("operator_profile", {}) or {}).get("autonomy_mode", "guided")
        if self.autonomy_mode not in ("guided", "manual", "autopilot"):
            self.autonomy_mode = "guided"
        self._save_profile("autonomy_mode", self.autonomy_mode)

    def _ensure_schema(self):
        d = self.memory.data
        if "missions" not in d or not isinstance(d.get("missions"), dict):
            d["missions"] = {"active": None, "history": []}
        d["missions"].setdefault("active", None)
        d["missions"].setdefault("history", [])
        if "operator_profile" not in d or not isinstance(d.get("operator_profile"), dict):
            d["operator_profile"] = {}
        if "decision_log" not in d or not isinstance(d.get("decision_log"), list):
            d["decision_log"] = []
        self._save_memory()

    def _save_memory(self):
        try:
            if hasattr(self.memory, "_save_json"):
                self.memory._save_json()
            elif hasattr(self.memory, "_save"):
                self.memory._save()
        except Exception:
            pass

    def _save_profile(self, key, value):
        self.memory.data.setdefault("operator_profile", {})[key] = value
        self._save_memory()

    def _iso_now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def _new_mission(self, goal):
        txt = (goal or "").strip()
        mission_id = "msn-" + hashlib.sha1((txt + str(time.time())).encode("utf-8", "ignore")).hexdigest()[:8]
        actions = self._seed_actions(txt)
        blockers = self._seed_blockers(txt)
        eta = "today"
        if any(x in txt.lower() for x in ["week", "large", "full"]):
            eta = "2-3 days"
        return {
            "id": mission_id,
            "title": txt[:80] or "Untitled mission",
            "goal": txt[:160],
            "stage": "brief",
            "progress": 8,
            "confidence": 78,
            "eta": eta,
            "next_actions": actions,
            "blockers": blockers,
            "mode": "architect",
            "status": "active",
            "created": self._iso_now(),
            "updated": self._iso_now(),
        }

    def _seed_actions(self, goal):
        g = (goal or "").lower()
        if any(x in g for x in ["flappy", "pygame", "python game", "game", "arcade"]):
            return [
                "Create Python game scaffold with main loop and scene state",
                "Implement player physics, collision, and score tracking",
                "Add obstacle spawning, difficulty ramp, and restart flow",
                "Run playtest pass and tune controls/performance",
            ]
        if any(x in g for x in ["python script", "automation script", "cli script", "script"]):
            return [
                "Define script inputs, outputs, and usage contract",
                "Build Python script skeleton with argparse and logging",
                "Implement core logic and error handling paths",
                "Run validation cases and package runnable command",
            ]
        if any(x in g for x in ["api", "backend", "server"]):
            return [
                "Define endpoint contract and payload shape",
                "Scaffold service and health checks",
                "Implement core business logic + tests",
                "Run verification and produce ship checklist",
            ]
        if any(x in g for x in ["ui", "hud", "frontend", "design"]):
            return [
                "Draft visual direction and key interaction states",
                "Implement base layout and component shell",
                "Add animation pass and responsive tuning",
                "Run polish + regression sweep",
            ]
        return [
            "Clarify outcome and acceptance criteria",
            "Build v1 skeleton and core workflow",
            "Validate behavior with real usage path",
            "Harden and ship",
        ]

    def _seed_blockers(self, goal):
        blockers = ["Dependencies not yet verified", "Final acceptance criteria not locked"]
        g = (goal or "").lower()
        if any(x in g for x in ["flappy", "pygame", "python game", "game", "arcade"]):
            blockers[0] = "Game library and asset pipeline not validated"
        elif any(x in g for x in ["python script", "automation script", "cli script", "script"]):
            blockers[0] = "Runtime dependencies and target environment not validated"
        if "calendar" in g:
            blockers[0] = "Calendar source freshness check pending"
        if "spotify" in g:
            blockers[0] = "Playback context handshake pending"
        return blockers

    def _active(self):
        return (self.memory.data.get("missions", {}) or {}).get("active")

    def _set_active(self, mission):
        self.memory.data.setdefault("missions", {})["active"] = mission
        self._save_memory()

    def start_mission(self, goal):
        mission = self._new_mission(goal)
        self._set_active(mission)
        self.append_decision(f"Mission started: {mission['title']}")
        self.trace("MISSION", "start", f"Initialized mission {mission['id']}", fallback=False)
        self.sync_hud(status="thinking", text=f"Mission started: {mission['title']}", tool="mission")
        return f"Mission initialized: {mission['title']}."

    def clear_mission(self, reason="cleared by operator"):
        m = self._active()
        if not m:
            self.trace("MISSION", "clear", "No active mission to clear", fallback=False)
            self.sync_hud(status="standby", text="No active mission.", tool="mission")
            return "No active mission to clear sir."
        title = m.get("title", "mission")
        m["status"] = "cancelled"
        m["updated"] = self._iso_now()
        m["cancel_reason"] = str(reason or "cleared by operator")[:120]
        self.memory.data.setdefault("missions", {}).setdefault("history", []).insert(0, dict(m))
        self.memory.data["missions"]["history"] = self.memory.data["missions"]["history"][:30]
        self.memory.data["missions"]["active"] = None
        self.append_decision(f"Mission cleared: {title}")
        self.trace("MISSION", "clear", f"Cleared mission {title}", fallback=False)
        self._save_memory()
        self.sync_hud(status="standby", text=f"Mission cleared: {title}", tool="mission")
        return f"Mission cleared sir: {title}."

    def apply_template(self, template_name, goal=""):
        m = self._active()
        if not m:
            return "No active mission sir. Start one first."
        tn = str(template_name or "").strip().lower()
        g = str(goal or m.get("goal", "")).lower()
        if tn in ("python_game", "game", "pygame", "flappy"):
            m["mode"] = "architect"
            m["stage"] = "plan"
            m["progress"] = max(int(m.get("progress", 0) or 0), 20)
            m["next_actions"] = [
                "Scaffold game loop, state machine, and asset folders",
                "Implement player controls, gravity, and collision",
                "Add obstacle generation, scoring, and restart logic",
                "Playtest difficulty ramp and package run command",
            ]
            m["blockers"] = [
                "Pygame dependency and FPS stability not validated",
                "Art/audio placeholders not finalized",
            ]
            m["eta"] = "today"
        elif tn in ("python_script", "script", "cli"):
            m["mode"] = "architect"
            m["stage"] = "plan"
            m["progress"] = max(int(m.get("progress", 0) or 0), 18)
            m["next_actions"] = [
                "Define input/output contract and arguments",
                "Build argparse/logging skeleton and core module layout",
                "Implement happy path plus error handling",
                "Run examples and package runnable usage docs",
            ]
            m["blockers"] = [
                "Runtime/dependency target not validated",
                "Acceptance examples not finalized",
            ]
            m["eta"] = "today"
        else:
            return "Unknown template. Use python_game or python_script."
        if g:
            m["goal"] = str(goal)[:160]
            m["title"] = str(goal)[:80]
        m["updated"] = self._iso_now()
        self.append_decision(f"Template applied: {tn}")
        self.trace("MISSION", "template", f"Applied {tn}", fallback=False)
        self._save_memory()
        self.sync_hud(status="thinking", text=f"Template applied: {tn}", tool="mission")
        return f"Applied {tn} template to mission {m.get('title','')}."

    def set_stage(self, stage, progress=None):
        m = self._active()
        if not m:
            return "No active mission sir."
        if stage not in MISSION_STAGES:
            return "Unknown mission stage sir."
        m["stage"] = stage
        if progress is not None:
            m["progress"] = max(0, min(100, int(progress)))
        else:
            stage_idx = max(0, MISSION_STAGES.index(stage))
            m["progress"] = max(m.get("progress", 0), min(100, stage_idx * 24 + 8))
        m["updated"] = self._iso_now()
        if stage == "complete":
            m["status"] = "complete"
            self.memory.data.setdefault("missions", {}).setdefault("history", []).insert(0, dict(m))
            self.memory.data["missions"]["history"] = self.memory.data["missions"]["history"][:30]
            self.memory.data["missions"]["active"] = None
        self._save_memory()
        self.sync_hud()
        return f"Mission stage set to {stage.upper()}."

    def mission_status(self):
        m = self._active()
        if not m:
            return "No active mission. Say start mission and your goal."
        nx = m.get("next_actions", [])
        nxt = nx[0] if nx else "No queued actions"
        return (
            f"Mission {m.get('title','')} is in {m.get('stage','brief').upper()} at {m.get('progress',0)} percent. "
            f"Confidence {m.get('confidence',0)} percent. Next action: {nxt}."
        )

    def next_action(self):
        m = self._active()
        if not m:
            return "No active mission sir."
        nx = m.get("next_actions", [])
        if not nx:
            return "No queued action. Say mission status to refresh priorities."
        return "Next action: " + nx[0] + "."

    def why_this(self):
        m = self._active()
        if not m:
            return "No active mission context yet sir."
        reasons = []
        reasons.append(f"Current stage is {m.get('stage','brief').upper()} and progress is {m.get('progress',0)} percent.")
        if m.get("blockers"):
            reasons.append("Primary blocker: " + m["blockers"][0] + ".")
        if getattr(self.pc, "_active_proj_path", None):
            reasons.append("Active project context is loaded, so actions are scoped to current workspace.")
        if self.memory.data.get("operator_profile", {}).get("coding_stack"):
            reasons.append("Using your saved coding stack preference.")
        return " ".join(reasons)

    def set_autonomy(self, mode):
        md = (mode or "").strip().lower()
        if md not in ("guided", "manual", "autopilot"):
            return "Autonomy mode must be guided, manual, or autopilot."
        self.autonomy_mode = md
        self._save_profile("autonomy_mode", md)
        self.sync_hud()
        return f"Autonomy mode set to {md}."

    def set_supermode(self, mode):
        m = self._active()
        if not m:
            return "No active mission. Start one first."
        md = (mode or "").strip().lower()
        if md not in ("architect", "ship", "debug"):
            return "Unknown mode."
        m["mode"] = md
        m["updated"] = self._iso_now()
        if md == "architect":
            m["stage"] = "plan"
            m["progress"] = max(m.get("progress", 0), 22)
            m["next_actions"] = [
                "Map architecture boundaries and interfaces",
                "Generate scaffold and dependency blueprint",
                "Create implementation slices with risk notes",
            ]
        elif md == "ship":
            m["stage"] = "verify"
            m["progress"] = max(m.get("progress", 0), 72)
            m["next_actions"] = [
                "Run validation checks and smoke tests",
                "Resolve blockers and finalize release notes",
                "Execute ship checklist and close mission",
            ]
        else:
            m["stage"] = "execute"
            m["progress"] = max(m.get("progress", 0), 48)
            m["next_actions"] = [
                "Reproduce failure and isolate minimal failing path",
                "Apply smallest fix-first patch",
                "Verify regression and stability",
            ]
        self._save_memory()
        self.trace("MODE", "set", f"Supermode -> {md}", fallback=False)
        self.sync_hud()
        return f"{md.capitalize()} mode engaged."

    def append_decision(self, note):
        log = self.memory.data.setdefault("decision_log", [])
        log.insert(0, {"ts": self._iso_now(), "note": str(note)[:180]})
        self.memory.data["decision_log"] = log[:120]
        self._save_memory()

    def trace(self, intent, tool, result, fallback=False):
        entry = {
            "ts": datetime.datetime.now().strftime("%H:%M:%S"),
            "intent": str(intent or "TASK")[:48],
            "tool": str(tool or "brain")[:48],
            "result": str(result or "")[:140],
            "fallback": bool(fallback),
        }
        if self._trace and self._trace[0] == entry:
            return
        self._trace.insert(0, entry)
        self._trace = self._trace[:20]

    def hud_payload(self):
        m = self._active() or {}
        mission = {
            "id": m.get("id", ""),
            "title": m.get("title", "NO ACTIVE MISSION"),
            "stage": m.get("stage", "brief"),
            "progress": int(m.get("progress", 0) or 0),
            "confidence": int(m.get("confidence", 0) or 0),
            "mode": m.get("mode", "architect"),
            "eta": m.get("eta", ""),
        }
        blockers = list((m.get("blockers", []) or []))[:4]
        return mission, list(self._trace)[:10], blockers

    def sync_hud(self, status="standby", text="", tool="mission"):
        mission, trace, blockers = self.hud_payload()
        _write_hud(status=status, text=text, tool=tool, mission=mission, trace=trace, blockers=blockers, autonomy_mode=self.autonomy_mode)


# â”€â”€ Config â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CONFIG_FILE = Path.home() / ".jarvis_config.json"
MEMORY_FILE = Path.home() / ".jarvis_memory.json"
# Unique injection markers â€” never appear in tool descriptions or prompts
_INJECT_METHODS = "    # @@INJECT_METHODS@@"
_INJECT_TOOLS   = "    # @@TOOLS_INJECT_HERE@@"
_INJECT_METHODS = "    # @@INJECT_METHODS@@"
DEFAULT_CONFIG = {
    "anthropic_api_key": "",
    "vosk_model_path": str(Path.home() / "Desktop" / "vosk-model-small-en-us-0.15"),
    "voice_rate": 155,
    "voice_volume": 0.95,
    "home_dir": str(Path.home()),
    "workspace_dir": str(Path.home() / "Desktop" / "Jarvis MARK 15"),
    "mic_device": 1,
    "session_timeout": 20,
    "listen_timeout": 10,
    "listen_phrase_limit": 24,
    "listen_silence_seconds": 1.6,
    "use_preset_commands": False,
    "skills_dir": str(Path.home() / "Desktop" / "Jarvis MARK 15" / "jarvis_skills"),
    "whisper_model": "base",
    "whisper_language": "en",
    "interrupt_on_speech": True,
    "speech_interrupt_min_words": 2,
    "use_local_model": True,
    "local_model_url": "http://169.254.83.107:1234/v1",
    "local_model_name": "gemma-4-e4b-uncensored-hauhaucs-aggressive",
    "local_model_api_key": "lm-studio",
    "use_openclaw": False,
    "openclaw_token": "",
    "openclaw_url": "http://127.0.0.1:18789",
    "openclaw_agent": "main",
    "tts_engine": "piper",
    "voice_gender": "male",
    "wake_words": ["jarvis","javis","travis","davis","harris","charles","j.a.r.v.i.s"],
    "context_window": 30,
    "max_tokens_local": 500,
    "school_calendar_ics": "https://calendar.google.com/calendar/ical/0frjpl08d72hetlk4ci2vioqms%40group.calendar.google.com/public/basic.ics",
    "auto_compact_tokens": 28000,
    "ambient_monitoring": True,
    "screen_time_tracking": True,
    "health_reminders": True,
    "health_reminder_interval": 60,
    "water_reminder_interval": 30,
    "email_user": "",
    "email_pass": "",
    "email_smtp": "smtp.gmail.com",
    "email_port": 587,
    "weather_city": "Toronto",
    "weather_api_key": "",
    "news_sources": ["bbc-news","techcrunch","the-verge"],
    "vision_model_url": "http://localhost:1234/v1",
    "vision_model_name": "gemma-3-4b-it",
    "vision_model_api_key": "lm-studio",
}


# â”€â”€ HUD â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# â”€â”€ Palette â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BG      = "#000810"
C1      = "#00c8ff"   # main cyan
C2      = "#0077bb"   # mid blue
C3      = "#004488"   # dark blue
C4      = "#00ffcc"   # teal accent
C5      = "#e8f8ff"   # near white
DIM     = "#001e33"
DIMMER  = "#000f1a"
BLUE_DIM = "#001e33"
RED     = "#ff3333"
AMBER   = "#ffaa00"
GREEN   = "#00ff88"

def _hex(r, g, b):
    return f"#{max(0,min(255,r)):02x}{max(0,min(255,g)):02x}{max(0,min(255,b)):02x}"

def _lerp(a, b, t):
    return a + (b - a) * t

class JarvisHUD:
    W_BASE, H_BASE = 920, 580
    W_TALK, H_TALK = 1100, 660

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S")
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        try: self.root.overrideredirect(True)
        except: pass

        self.W, self.H = self.W_BASE, self.H_BASE
        self.W_target, self.H_target = self.W_BASE, self.H_BASE
        self.root.geometry(f"{self.W}x{self.H}+60+60")

        self.canvas = tk.Canvas(self.root, width=self.W, height=self.H,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", lambda e: setattr(self,'_ox',e.x) or setattr(self,'_oy',e.y))
        self.canvas.bind("<B1-Motion>", lambda e: self.root.geometry(f"+{self.root.winfo_x()+e.x-self._ox}+{self.root.winfo_y()+e.y-self._oy}"))
        self.canvas.bind("<Button-3>", lambda e: self.root.destroy())

        # Core state
        self.tick        = 0
        self.phase       = 0.0
        self.ring_angle  = 0.0
        self.pulse       = 0.0
        self.talking     = False
        self._talk_end   = 0.0
        self.status      = "standby"
        self.last_text   = ""
        self.last_tool   = ""
        self._active_project_badge = ""
        self.hud_mode      = ""   # "project", "file", "scan", "alert"
        self.hud_mode_data = {}
        self.hud_mode_ts   = 0.0
        self.hud_overlay_alpha = 0.0

        # â”€â”€ Slow data cache â€” refreshed every 500ms, not every frame â”€â”€â”€â”€â”€â”€â”€â”€â”€
        self._cache = {
            "cpu": 0, "ram": 0, "disk": 0, "bat_pct": 100, "bat_chg": False, "bat_ok": False,
            "net_tx": 0, "net_rx": 0,
            "projects": [], "proj_active": 0, "proj_done": 0,
            "mem_rules": 0, "mem_prefs": 0, "mem_facts": 0, "mem_last_rule": "",
            "top_proc": "", "top_cpu": 0, "proc_count": 0, "uptime": "",
            "goal": "", "tick": 0,
        }
        self._cache_tick = 0
        self._start_bg_thread()

        # Boot
        self.boot_phase  = 0.0
        self.boot_done   = False
        self.boot_lines  = [{"y": random.uniform(0,self.H_TALK),"speed":random.uniform(3,8),
                              "alpha":random.uniform(0.4,1.0),"w":random.uniform(1,3)} for _ in range(12)]

        # Ring scale
        self._ring_scale = 1.0

        # Particles
        self.particles = [self._new_particle() for _ in range(8)]

        # Waveform
        self.wave_buf = [0.0]*120

        self._watch_state()
        self._animate()
        self.root.mainloop()

    # â”€â”€ drag / close â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _drag_start(self, e): self._ox, self._oy = e.x, e.y
    def _drag_move(self, e):
        self.root.geometry(f"+{self.root.winfo_x()+e.x-self._ox}+{self.root.winfo_y()+e.y-self._oy}")

    def _new_particle(self, x=None, y=None):
        return {"x": x or random.uniform(30,self.W_TALK-30),
                "y": y or self.H_TALK,
                "vx": random.uniform(-0.3,0.3),
                "vy": random.uniform(-0.3,-0.7),
                "r":  random.uniform(0.8,2.0),
                "life": random.random(),
                "max_life": random.uniform(250,700),
                "age": 0}

    # â”€â”€ background data thread â€” runs forever, never touches main thread â”€â”€â”€â”€â”€â”€â”€â”€
    def _start_bg_thread(self):
        """Single persistent background thread â€” updates cache continuously."""
        import threading as _t
        def _loop():
            slow_tick = 0
            while True:
                c = self._cache
                # Fast refresh: cpu/ram/net every 800ms
                try:
                    c["cpu"] = psutil.cpu_percent(interval=None)
                    c["ram"] = psutil.virtual_memory().percent
                except: pass
                try:
                    net = psutil.net_io_counters()
                    c["net_tx"] = net.bytes_sent  // 1024 // 1024
                    c["net_rx"] = net.bytes_recv  // 1024 // 1024
                except: pass

                # Medium refresh: disk/battery/files every 4s
                if slow_tick % 5 == 0:
                    try: c["disk"] = psutil.disk_usage("/").percent
                    except: pass
                    pass  # calendar removed
                    try:
                        bat = psutil.sensors_battery()
                        if bat:
                            c["bat_pct"] = bat.percent
                            c["bat_chg"] = bat.power_plugged
                            c["bat_ok"]  = True
                    except: pass
                    try:
                        pf = PROJECTS_FILE
                        if pf.exists():
                            reg = json.loads(pf.read_text(encoding="utf-8"))
                            active = [(k,v) for k,v in reg.items() if v.get("status","active")=="active"]
                            done   = [(k,v) for k,v in reg.items() if v.get("status") in ("complete","archived")]
                            c["projects"]    = active
                            c["proj_active"] = len(active)
                            c["proj_done"]   = len(done)
                    except: pass
                    try:
                        mf = Path.home() / ".jarvis_memory.json"
                        if mf.exists():
                            mem = json.loads(mf.read_text(encoding="utf-8"))
                            rules = mem.get("rules",[])
                            c["mem_rules"] = len(rules)
                            c["mem_prefs"] = len(mem.get("preferences",{}))
                            c["mem_facts"] = len(mem.get("facts",{}))
                            c["mem_last_rule"] = rules[-1].get("rule","")[:24] if rules else ""
                    except: pass
                    try:
                        gf = Path.home() / ".jarvis_goals.json"
                        if gf.exists():
                            goals = json.loads(gf.read_text())
                            today = datetime.datetime.now().strftime("%Y-%m-%d")
                            c["goal"] = goals.get(today,{}).get("goal","")[:22]
                    except: pass

                # Slow refresh: process list every 10s â€” this is the expensive one
                if slow_tick % 12 == 0:
                    try:
                        procs = sorted(
                            psutil.process_iter(["name","cpu_percent"]),
                            key=lambda p: p.info.get("cpu_percent") or 0, reverse=True)
                        if procs:
                            c["top_proc"] = procs[0].info["name"][:16]
                            c["top_cpu"]  = procs[0].info.get("cpu_percent",0)
                        c["proc_count"] = len(procs)
                    except: pass
                    try:
                        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
                        up = datetime.datetime.now() - boot
                        h2, rem = divmod(int(up.total_seconds()), 3600)
                        c["uptime"] = f"{h2}h {rem//60:02d}m"
                    except: pass

                slow_tick += 1
                time.sleep(0.8)  # 800ms base interval

        _t.Thread(target=_loop, daemon=True).start()

    def _refresh_cache(self): pass  # kept for compat, no longer used

    # â”€â”€ state polling â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _watch_state(self):
        try:
            sf = Path.home() / ".jarvis_hud_state.json"
            if sf.exists():
                d = json.loads(sf.read_text())
                age = time.time() - d.get("ts", 0)
                if age < 8:
                    st = d.get("status","standby")
                    self.status = st
                    if d.get("text"): self.last_text = d["text"]
                    if d.get("tool"): self.last_tool = d["tool"]
                    if st == "shutdown":
                        self.root.after(400, self.root.destroy); return
                    if st in ("speaking","thinking"):
                        self._talk_end = time.time() + 9.0
                    # HUD display mode
                    hm = d.get("hud_mode","")
                    if hm and hm != self.hud_mode:
                        self.hud_mode = hm
                        self.hud_mode_data = d.get("hud_data", {})
                        self.hud_mode_ts   = time.time()
                else:
                    self.status = "standby"
                    if time.time() - self.hud_mode_ts > 30:
                        self.hud_mode = ""  # auto-clear after 30s
                self._active_project_badge = d.get("active_project","")
        except: pass
        self.talking = time.time() < self._talk_end
        self.root.after(100, self._watch_state)

    # â”€â”€ animate â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _animate(self):
        self.tick  += 1

        # Standby: only redraw every 4th frame (7.5fps) to save CPU
        if (self.status == "standby" and not self.talking and
                self.boot_done and not self.hud_mode):
            if self.tick % 4 != 0:
                self.root.after(80 if self.talking else 250, self._animate)
                return

        self.phase += 0.055
        self.ring_angle += 2.6 if self.talking else 1.0
        self.pulse = (math.sin(self.tick*0.05)+1)/2

        if not self.boot_done:
            self.boot_phase = min(1.0, self.boot_phase + 0.007)
            if self.boot_phase >= 1.0: self.boot_done = True

        # Window resize
        self.W_target, self.H_target = (self.W_TALK, self.H_TALK) if self.talking else (self.W_BASE, self.H_BASE)
        nW = int(_lerp(self.W, self.W_target, 0.10))
        nH = int(_lerp(self.H, self.H_target, 0.10))
        if abs(nW-self.W)>1 or abs(nH-self.H)>1:
            self.W, self.H = nW, nH
            self.root.geometry(f"{self.W}x{self.H}")
            self.canvas.config(width=self.W, height=self.H)

        # Ring scale
        self._ring_scale = _lerp(self._ring_scale, 1.85 if self.talking else 1.0, 0.09)

        # Waveform
        amp = 26 if self.talking else 4
        # Update waveform every other frame
        if self.tick % 2 == 0:
            for i in range(len(self.wave_buf)):
                t2 = amp*math.sin(self.phase*2.5+i*0.22)*math.sin(i*math.pi/len(self.wave_buf))
                noise = random.uniform(-1.5,1.5) if self.talking else 0
                self.wave_buf[i] += (t2+noise-self.wave_buf[i])*0.22

        # Particles â€” update every 2 frames
        if self.tick % 2 == 0:
            for i,p in enumerate(self.particles):
                p["x"]+=p["vx"]; p["y"]+=p["vy"]; p["age"]+=1
                if p["age"]>p["max_life"] or p["y"]<0:
                    self.particles[i] = self._new_particle()

        # Skip expensive full redraw if in standby and nothing has changed
        self._idle_frames = getattr(self, '_idle_frames', 0)
        if (self.status == "standby" and not self.talking and
                not self.hud_mode and self.boot_done):
            self._idle_frames += 1
            # In standby: redraw every 3rd frame (10fps) â€” saves 66% CPU
            if self._idle_frames % 3 != 0:
                self.root.after(80 if self.talking else 250, self._animate)
                return
        else:
            self._idle_frames = 0

        # Draw
        c = self.canvas
        c.delete("all")
        cx, cy = self.W//2, self.H//2

        self._draw_grid(c)
        if self.talking: self._draw_particles(c)
        self._draw_glow_core(c, cx, cy)
        self._draw_rings(c, cx, cy)
        self._draw_waveform(c, cx, cy)
        self._draw_left_panel(c, cx, cy)
        self._draw_right_panel(c, cx, cy)
        self._draw_text_overlay(c, cx, cy)
        self._draw_center_bottom_panel(c, cx, cy)
        if self.tick % 10 == 0: self._draw_corners(c)
        self._draw_scanline(c)
        # HUD mode overlay
        if self.hud_mode:
            self._draw_hud_overlay(c, cx, cy)
        if not self.boot_done:
            self._draw_boot_anim(c, cx, cy)

        self.root.after(80 if self.talking else 250, self._animate)

    # â”€â”€ grid â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_grid(self, c): pass  # disabled for performance

    def _draw_particles(self, c):
        for p in self.particles:
            t = min(1.0, p["age"]/p["max_life"])
            fade = math.sin(t*math.pi)
            a = int(160*fade)
            col = _hex(0, int(a*0.6), a)
            r = p["r"]*fade
            if r > 0.3:
                c.create_oval(p["x"]-r,p["y"]-r,p["x"]+r,p["y"]+r, fill=col, outline="")

    # â”€â”€ arc reactor â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_glow_core(self, c, cx, cy):
        sc_rgb = {"standby":(0,140,210),"listening":(0,220,170),
                  "thinking":(210,140,0),"speaking":(0,190,255)}.get(self.status,(0,140,210))
        sr,sg,sb = sc_rgb
        glow_r = 56 + 8*self.pulse + (14 if self.talking else 0)
        # Soft glow layers â€” more layers, smaller steps = smoother
        for i in range(10,0,-1):
            gr = glow_r + i*6
            al = int(16*(1-i/10)*(0.5+0.5*self.pulse))
            c.create_oval(cx-gr,cy-gr,cx+gr,cy+gr,
                          fill=_hex(sr*al//100,sg*al//100,sb*al//100), outline="")
        c.create_oval(cx-glow_r,cy-glow_r,cx+glow_r,cy+glow_r, fill=_hex(0,16,32), outline="")
        # Segments â€” smoother with more segments
        n = 16
        for i in range(n):
            a1 = math.radians(i*(360/n)+self.ring_angle*0.4)
            a2 = math.radians((i+0.6)*(360/n)+self.ring_angle*0.4)
            ri, ro = 28, 46
            col = C1 if i%2==0 else C2
            pts = [cx+ri*math.cos(a1),cy+ri*math.sin(a1),
                   cx+ro*math.cos(a1),cy+ro*math.sin(a1),
                   cx+ro*math.cos(a2),cy+ro*math.sin(a2),
                   cx+ri*math.cos(a2),cy+ri*math.sin(a2)]
            c.create_polygon(*pts, fill=col, outline="")
        # Center glow
        dr = 16+4*self.pulse
        for gi in range(5,0,-1):
            gr2 = dr+gi*3; al2 = int(50*(1-gi/5))
            c.create_oval(cx-gr2,cy-gr2,cx+gr2,cy+gr2, fill=_hex(0,al2,al2*2), outline="")
        c.create_oval(cx-dr,cy-dr,cx+dr,cy+dr, fill=_hex(sr,sg,sb), outline="")
        c.create_oval(cx-8,cy-8,cx+8,cy+8, fill="#e8f8ff", outline="")

    # â”€â”€ rings â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_rings(self, c, cx, cy):
        sc = min(self._ring_scale, (min(self.W,self.H)//2-22)/118)
        spd = 1.8 if self.talking else 1.0
        bases = [(118,0.55,2,C3,C1,75),(94,-0.9,2,C3,C4,52),(72,1.7,1,DIMMER,C2,38)]
        for base_r,rspd,w,bg,arc_col,arc_ext in bases:
            r = int(base_r*sc)

            c.create_oval(cx-r,cy-r,cx+r,cy+r, outline=bg, width=w)
            ang = self.ring_angle*rspd*spd
            ext = arc_ext+12*self.pulse+(52 if self.talking else 0)
            lw  = w+1+(2 if self.talking else 0)
            # Draw arc with smooth end caps by using multiple thin arcs
            c.create_arc(cx-r,cy-r,cx+r,cy+r, start=ang, extent=ext,
                         outline=arc_col, width=lw, style=tk.ARC)
            c.create_arc(cx-r,cy-r,cx+r,cy+r, start=ang+180, extent=ext//2,
                         outline=arc_col, width=w, style=tk.ARC)


    # â”€â”€ waveform â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_waveform(self, c, cx, cy):
        wy = self.H-72; n=len(self.wave_buf)
        tw = min(self.W-100,580); step=tw/n; x0=cx-tw//2
        # Glow
        pts_g=[x0+i*step for i in range(n)]
        pts_glow=[]
        for i in range(n): pts_glow+=[x0+i*step, wy+self.wave_buf[i]]
        if len(pts_glow)>=4:
            c.create_line(*pts_glow, fill=C3, width=5, smooth=True)
            c.create_line(*pts_glow, fill=C2, width=3, smooth=True)
            c.create_line(*pts_glow, fill=C1, width=1.5, smooth=True)
        c.create_line(x0,wy,x0+tw,wy, fill=DIM, width=1)
        c.create_oval(cx-4,wy-4,cx+4,wy+4, fill=C5, outline="")

    # â”€â”€ left panel â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_bar(self, c, x, y, w, frac, label, val):
        col = GREEN if frac<0.6 else (AMBER if frac<0.85 else RED)
        c.create_text(x, y, text=label, fill=C2, font=("Courier",9,"bold"), anchor="w")
        # Background
        c.create_rectangle(x, y+13, x+w, y+18, fill=DIM, outline="")
        # Fill with gradient effect (3 rectangles)
        fw = max(2, w*frac)
        c.create_rectangle(x, y+13, x+fw, y+18, fill=col, outline="")
        c.create_rectangle(x, y+13, x+fw, y+15, fill=_hex(255,255,255), outline="", stipple="gray25")
        c.create_text(x+w+8, y, text=val, fill=C5, font=("Courier",9), anchor="w")

    def _draw_left_panel(self, c, cx, cy):
        C = self._cache
        lx = 14
        c.create_text(lx, cy-100, text="SYSTEM", fill=C2, font=("Courier",7,"bold"), anchor="w")
        c.create_line(lx, cy-92, lx+155, cy-92, fill=DIM, width=1)
        self._draw_bar(c, lx, cy-84, 115, C["cpu"]/100,  "CPU", f"{C['cpu']:.0f}%")
        self._draw_bar(c, lx, cy-57, 115, C["ram"]/100,  "RAM", f"{C['ram']:.0f}%")
        self._draw_bar(c, lx, cy-30, 115, C["disk"]/100, "DSK", f"{C['disk']:.0f}%")
        if C.get("proj_active",0):
            c.create_text(lx, cy+10, text=f"{C['proj_active']} projects active", fill=C3, font=("Courier",8), anchor="w")


    def _draw_right_panel(self, c, cx, cy):
        C = self._cache
        rx = self.W - 14
        now = datetime.datetime.now()
        c.create_text(rx, cy-130, text=now.strftime("%I:%M %p"), fill=C1, font=("Courier",18,"bold"), anchor="e")
        c.create_text(rx, cy-110, text=now.strftime("%A %B %d"), fill=C3, font=("Courier",8), anchor="e")
        c.create_line(rx-160,cy-98,rx,cy-98, fill=DIM, width=1)
        c.create_text(rx, cy-88, text=f"CPU  {C['cpu']:.0f}%", fill=C2, font=("Courier",9), anchor="e")
        c.create_text(rx, cy-74, text=f"RAM  {C['ram']:.0f}%", fill=C2, font=("Courier",9), anchor="e")
        c.create_text(rx, cy-60, text=f"UP   {C.get('uptime','--')}", fill=C2, font=("Courier",9), anchor="e")
        if C.get("goal"):
            c.create_text(rx, cy-40, text=f"â–º {C['goal'][:24]}", fill=C4, font=("Courier",8), anchor="e")


    def _draw_text_overlay(self, c, cx, cy):
        c.create_text(cx, 22, text="J . A . R . V . I . S", fill=C1, font=("Courier",17,"bold"))
        c.create_text(cx, 40, text="JUST A RATHER VERY INTELLIGENT SYSTEM", fill=C2, font=("Courier",7))
        # Active project badge
        ap = getattr(self, "_active_project_badge","")
        if ap:
            bw = len(ap)*7+22
            c.create_rectangle(cx-bw//2,50,cx+bw//2,64, fill=DIM, outline=C4, width=1)
            c.create_text(cx, 57, text=f"â—ˆ {ap.upper()} â—ˆ", fill=C4, font=("Courier",7,"bold"))

        # â”€â”€ Status bar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        STATUS_MAP = {
            "standby":  ("STANDBY",  C3,   3.5),
            "listening":("LISTENING", C4,   5+2*self.pulse),
            "thinking": ("PROCESSING",AMBER,5+2*self.pulse),
            "speaking": ("RESPONDING",C1,   6+3*self.pulse),
        }
        label, col, dr = STATUS_MAP.get(self.status, ("STANDBY", C3, 3.5))

        # Status bar background
        bar_y = cy + 74
        c.create_rectangle(cx-180, bar_y-14, cx+180, bar_y+14,
                           fill=_hex(0,8,16), outline=DIM, width=1)

        # Pulsing dot with glow
        dx, dy = cx-158, bar_y
        try:
            ri = int(int(col[1:3],16)); gi2 = int(int(col[3:5],16)); bi = int(int(col[5:7],16))
            for gi in range(4,0,-1):
                fa = gi/4
                c.create_oval(dx-(dr+gi*3),dy-(dr+gi*3),dx+(dr+gi*3),dy+(dr+gi*3),
                              fill=_hex(int(ri*fa*0.5),int(gi2*fa*0.5),int(bi*fa*0.5)), outline="")
        except: pass
        c.create_oval(dx-dr,dy-dr,dx+dr,dy+dr, fill=col, outline="")

        # Label
        c.create_text(dx+dr+6, dy, text=label, fill=col,
                      font=("Courier",10,"bold"), anchor="w")

        # Tool indicator
        if self.last_tool and self.talking:
            c.create_text(cx+20, dy, text=f"[ {self.last_tool.upper()} ]",
                          fill=C4, font=("Courier",9,"bold"), anchor="w")

        # Last spoken text â€” shown below status bar
        if self.last_text and self.talking:
            disp = self.last_text[:88]+("â€¦" if len(self.last_text)>88 else "")
            c.create_text(cx, bar_y+28, text=disp, fill=C5,
                          font=("Courier",9), width=self.W-140)

        c.create_text(self.W-14, self.H-10, text="right-click to close",
                      fill=DIM, font=("Courier",7), anchor="e")

    # â”€â”€ corners â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_center_bottom_panel(self, c, cx, cy):
        """Draw a centre status strip at the bottom with live info."""
        # Jarvis response text â€” clean scrolling display
        if self.last_text and self.talking:
            # Background strip
            c.create_rectangle(cx-350, self.H-55, cx+350, self.H-30,
                               fill=_hex(0,6,14), outline=DIM, width=1)
            disp = self.last_text[:100] + ("â€¦" if len(self.last_text)>100 else "")
            c.create_text(cx, self.H-42, text=disp, fill=C5,
                          font=("Courier",8), width=680)

        # Network indicator dots
        C2_ = self._cache
        tx_mb = C2_.get("net_tx",0)
        rx_mb = C2_.get("net_rx",0)
        # Pulse when active
        net_active = tx_mb > 0 or rx_mb > 0
        dot_col = C4 if net_active else DIM
        c.create_oval(cx-295, self.H-22, cx-289, self.H-16, fill=dot_col, outline="")
        c.create_text(cx-284, self.H-19, text="NET", fill=C3, font=("Courier",7), anchor="w")

        # Session timer
        if not hasattr(self, '_session_start'):
            self._session_start = time.time()
        elapsed = int(time.time() - self._session_start)
        h2,rem = divmod(elapsed,3600); m2=rem//60; s2=rem%60
        sess_str = f"{h2:02d}:{m2:02d}:{s2:02d}"
        c.create_text(cx+180, self.H-19, text=f"SESSION  {sess_str}",
                      fill=C3, font=("Courier",7), anchor="w")

    def _draw_corners(self, c):
        s = 24
        for x,y,dx,dy in [(14,14,1,1),(self.W-14,14,-1,1),(14,self.H-14,1,-1),(self.W-14,self.H-14,-1,-1)]:
            c.create_line(x,y,x+dx*s,y, fill=C1, width=1.5)
            c.create_line(x,y,x,y+dy*s, fill=C1, width=1.5)
            c.create_oval(x-2,y-2,x+2,y+2, fill=C1, outline="")
        # Hex data
        for ci, bx in enumerate([30, self.W-108]):
            for ri in range(7):
                seed = (self.tick//5+ci*13+ri*9)%256
                c.create_text(bx, 58+ri*16,
                              text=f"{seed:02X} {(seed*7+13)%256:02X} {(seed*3+ri)%256:02X}",
                              fill=DIMMER, font=("Courier",8), anchor="w")

    # â”€â”€ scanline â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_scanline(self, c): pass  # disabled for performance

    def _draw_hud_overlay(self, c, cx, cy):
        """Full-screen HUD overlay for project/file/scan displays."""
        mode = self.hud_mode
        data = self.hud_mode_data
        age  = time.time() - self.hud_mode_ts

        # Fade in
        alpha = min(1.0, age * 3)
        dim_a = int(200 * alpha)

        # Translucent dark overlay
        c.create_rectangle(0, 0, self.W, self.H,
                           fill=_hex(0, 4, 10), outline="", stipple="gray75")

        if mode == "project":
            name = data.get("name","Unknown")
            path = data.get("path","")
            lang = data.get("language","")
            desc = data.get("description","")
            files= data.get("files",[])

            # Header
            c.create_text(cx, 80, text="PROJECT CONTEXT LOADED",
                          fill=C4, font=("Courier",10,"bold"))
            c.create_text(cx, 100, text=name.upper(),
                          fill=C1, font=("Courier",20,"bold"))
            c.create_line(cx-200, 118, cx+200, 118, fill=C3, width=1)

            # Info row
            c.create_text(cx-180, 134, text=f"LANG: {lang.upper()}", fill=C2,
                          font=("Courier",9), anchor="w")
            c.create_text(cx, 134, text=f"FILES: {len(files)}", fill=C2,
                          font=("Courier",9), anchor="center")
            c.create_text(cx+100, 134, text="STATUS: ACTIVE", fill=GREEN,
                          font=("Courier",9), anchor="w")

            # Description
            if desc:
                c.create_text(cx, 155, text=desc[:70], fill=C3,
                              font=("Courier",8), anchor="center")

            # File tree â€” animated, files appear one by one
            max_show = min(len(files), int(age * 8))
            cols = 2
            col_w = 260
            for i, fname in enumerate(files[:max_show]):
                col = i % cols
                row = i // cols
                fx = cx - 240 + col * col_w
                fy = 178 + row * 16
                if fy > self.H - 100: break
                # Icon by extension
                ext = fname.rsplit(".",1)[-1] if "." in fname else ""
                icon_col = {"py":C4,"js":"#f7df1e","ts":"#3178c6","rs":RED,
                           "md":C2,"json":AMBER,"txt":DIM}.get(ext, C2)
                c.create_text(fx, fy, text=f"{'ðŸ“„' if ext else 'ðŸ“'} {fname[:32]}",
                              fill=icon_col, font=("Courier",8), anchor="w")

            # Scanning line animation
            scan_y = 178 + ((int(age * 60)) % max(1, len(files)//cols + 1)) * 16
            c.create_line(cx-240, scan_y, cx+240, scan_y,
                          fill=_hex(0,40,80), width=1)

            # Close hint
            c.create_text(cx, self.H-30, text='say "close project" to exit context',
                          fill=C3, font=("Courier",8))

        elif mode == "scan":
            title = data.get("title","SCANNING")
            items = data.get("items",[])
            c.create_text(cx, 90, text=title, fill=C1, font=("Courier",16,"bold"))
            for i,item in enumerate(items[:14]):
                fy = 130 + i*24
                bar_w = random.randint(80,280) if age < 1 else 200
                c.create_rectangle(cx-200, fy-6, cx-200+bar_w, fy+6, fill=DIM, outline="")
                c.create_rectangle(cx-200, fy-6, cx-200+int(bar_w*(age/(i+1))), fy+6, fill=C1 if i%2==0 else C4, outline="")
                c.create_text(cx+100, fy, text=item[:28], fill=C2, font=("Courier",9), anchor="w")

        elif mode == "alert":
            msg = data.get("message","ALERT")
            lvl = data.get("level","warning")
            col = RED if lvl=="critical" else AMBER
            c.create_text(cx, cy-20, text="âš  " + msg.upper() + " âš ",
                          fill=col, font=("Courier",14,"bold"))

    # â”€â”€ boot animation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _draw_boot_anim(self, c, cx, cy):
        t = self.boot_phase
        if t < 0.85:
            fade = max(0.0,1.0-t/0.5); al = int(235*fade)
            c.create_rectangle(0,0,self.W,self.H, fill=_hex(0,int(8*fade),int(16*fade)), outline="")
        if t < 0.5:
            for bl in self.boot_lines:
                bl["y"] = (bl["y"]+bl["speed"]) % self.H
                a = int(160*bl["alpha"]*(1-t/0.5))
                c.create_line(0,bl["y"],self.W,bl["y"], fill=_hex(0,a//2,a), width=bl["w"])
        if 0.1<t<0.5:
            prog=(t-0.1)/0.4; lw2=int(self.W*prog)
            c.create_line(cx-lw2//2,cy,cx+lw2//2,cy, fill=_hex(0,80,160), width=2)
        if 0.2<t<0.6:
            prog=min(1.0,(t-0.2)/0.3); sv=int(24*prog)
            for x,y,dx,dy in [(14,14,1,1),(self.W-14,14,-1,1),(14,self.H-14,1,-1),(self.W-14,self.H-14,-1,-1)]:
                c.create_line(x,y,x+dx*sv,y, fill=C1, width=2)
                c.create_line(x,y,x,y+dy*sv, fill=C1, width=2)
        if t>0.35:
            rp=min(1.0,(t-0.35)/0.45)
            for ii,(r,col) in enumerate([(118,C1),(94,C4),(72,C2)]):
                dp=ii*0.15; p2=max(0.0,min(1.0,(rp-dp)/0.5))
                if p2>0:
                    ext=p2*359
                    c.create_arc(cx-r,cy-r,cx+r,cy+r, start=90,extent=ext,
                                 outline=col, width=2, style=tk.ARC)
                    aa=math.radians(90-ext)
                    c.create_oval(cx+r*math.cos(aa)-3,cy+r*math.sin(aa)-3,
                                  cx+r*math.cos(aa)+3,cy+r*math.sin(aa)+3, fill=col, outline="")
        if t>0.75:
            ft=(t-0.75)/0.25
            if ft<0.4:
                br=int(220*ft/0.4)
                c.create_oval(cx-88,cy-88,cx+88,cy+88, fill=_hex(0,br//3,br), outline="")
        if 0.25<t<0.92:
            br=int(180*math.sin((t-0.25)/0.67*math.pi))
            msgs=[(0.25,"INITIALIZING SYSTEMS..."),(0.38,"LOADING AI CORE..."),
                  (0.51,"CALIBRATING SENSORS..."),(0.64,"VOICE SYSTEMS ONLINE..."),(0.77,"J.A.R.V.I.S READY")]
            for thr,msg in reversed(msgs):
                if t>=thr:
                    c.create_text(cx,cy+130, text=msg, fill=_hex(0,br//2,br),
                                  font=("Courier",11,"bold"))
                    break
        if t>0.88:
            fo=(t-0.88)/0.12; ov=int(200*(1-fo))
            if ov>0:
                c.create_rectangle(0,0,self.W,self.H, fill=_hex(0,0,ov//10),
                                   outline="", stipple="gray50")

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                raw = f.read()
            cfg = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[JARVIS] WARNING: config has a JSON syntax error ({e}). Auto-repairing...")
            try:
                # Simple fix: add missing commas between adjacent "value"\n  "key" pairs
                import re as _re
                fixed = _re.sub(r'("(?:[^"\\\\]|\\\\.)*"\s*:\s*[^,{\[\n]+)\n(\s*")',
                                lambda m: m.group(1) + ",\n" + m.group(2), raw)
                cfg = json.loads(fixed)
                print("[JARVIS] Config auto-repaired. Saving...")
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, indent=2)
            except Exception:
                print("[JARVIS] Could not auto-repair config. Using defaults.")
                cfg = {}
        for k, v in DEFAULT_CONFIG.items():
            cfg.setdefault(k, v)
        # Fill in any missing local model settings with defaults.
        if cfg.get("use_local_model", False):
            if not cfg.get("local_model_url"):
                cfg["local_model_url"] = DEFAULT_CONFIG["local_model_url"]
            if not cfg.get("local_model_name"):
                cfg["local_model_name"] = DEFAULT_CONFIG["local_model_name"]
            if not cfg.get("local_model_api_key"):
                cfg["local_model_api_key"] = DEFAULT_CONFIG["local_model_api_key"]
        # Respect user max_tokens_local — allow up to 4096 for local models.
        try:
            cfg["max_tokens_local"] = int(min(max(int(cfg.get("max_tokens_local", 512)), 80), 4096))
        except Exception:
            cfg["max_tokens_local"] = 512
        return cfg
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

# â”€â”€ Persistent Memory â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

# â”€â”€ Vector Memory & Ontology Graph â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class JarvisOntologyGraph:
    """
    Persistent knowledge graph. Uses networkx if available, pure-dict fallback otherwise.
    """
    def __init__(self):
        self.db_path = Path.home() / ".jarvis_ontology.db"
        self._has_nx = False
        try:
            import networkx as nx
            self.G = nx.DiGraph()
            self._has_nx = True
        except:
            self.G = None  # fallback: use DB only
        self._load()

    def _conn(self):
        import sqlite3
        c = sqlite3.connect(str(self.db_path))
        c.execute("""CREATE TABLE IF NOT EXISTS triples
                     (subject TEXT, predicate TEXT, object TEXT,
                      added TEXT, PRIMARY KEY(subject, predicate, object))""")
        return c

    def _load(self):
        try:
            c = self._conn()
            for row in c.execute("SELECT subject, predicate, object FROM triples"):
                s, p, o = row
                if self._has_nx and self.G is not None:
                    self.G.add_edge(s, o, predicate=p)
            c.close()
        except: pass

    def add(self, subject, predicate, obj):
        subject = subject.strip().lower()
        obj     = obj.strip().lower()
        predicate = predicate.strip().lower()
        if self._has_nx and self.G is not None:
            self.G.add_edge(subject, obj, predicate=predicate)
        try:
            c = self._conn()
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT OR REPLACE INTO triples VALUES (?,?,?,?)",
                      (subject, predicate, obj, ts))
            c.commit(); c.close()
        except: pass

    def query(self, subject=None, predicate=None, obj=None):
        """Find triples matching any combination of subject/predicate/object."""
        results = []
        try:
            c = self._conn()
            q = "SELECT subject, predicate, object FROM triples WHERE 1=1"
            params = []
            if subject:   q += " AND subject LIKE ?";   params.append(f"%{subject.lower()}%")
            if predicate: q += " AND predicate LIKE ?"; params.append(f"%{predicate.lower()}%")
            if obj:       q += " AND object LIKE ?";    params.append(f"%{obj.lower()}%")
            results = c.execute(q, params).fetchall()
            c.close()
        except: pass
        return results

    def what_do_i_know_about(self, topic):
        """Return all facts about a topic as a spoken string."""
        topic = topic.strip().lower()
        results = self.query(subject=topic) + self.query(obj=topic)
        if not results:
            return f"Nothing recorded about {topic} sir."
        parts = []
        for s, p, o in results[:8]:
            parts.append(f"{s} {p} {o}")
        return "Here is what I know about " + topic + ": " + ". ".join(parts) + "."

    def connections(self, topic, depth=2):
        """Find all nodes connected to a topic within N hops."""
        topic = topic.strip().lower()
        if not self._has_nx or self.G is None or topic not in self.G:
            # Fallback: return DB-based connections
            results = self.query(subject=topic) + self.query(obj=topic)
            return list(set([r[0] for r in results] + [r[2] for r in results]))
        import networkx as nx
        nodes = nx.single_source_shortest_path(self.G, topic, cutoff=depth)
        return list(nodes.keys())

    def add_project(self, name, language, description, path):
        """Auto-populate graph when a project is created."""
        n = name.lower()
        self.add(n, "is_a", "project")
        self.add(n, "uses", language.lower() if language else "unknown")
        self.add(n, "located_at", path)
        if description:
            words = [w.lower() for w in description.split() if len(w) > 4]
            for w in words[:5]:
                self.add(n, "relates_to", w)
        self.add("user", "owns", n)

    def remove_node(self, name):
        n = name.lower()
        if self._has_nx and self.G is not None and n in self.G:
            self.G.remove_node(n)
        try:
            c = self._conn()
            c.execute("DELETE FROM triples WHERE subject=? OR object=?", (n, n))
            c.commit(); c.close()
        except: pass


class JarvisVectorMemory:
    """
    Hybrid memory: ChromaDB for semantic vector search + JSON fallback.
    Falls back to plain JarvisMemory if chromadb/sentence-transformers not installed.
    """
    VECTOR_DB = Path.home() / ".jarvis_vectordb"
    JSON_FILE = Path.home() / ".jarvis_memory.json"

    def __init__(self):
        self.data = self._load_json()   # always keep JSON as ground truth
        self._vec_ok = False
        self._embed  = None
        self._chroma = None
        self._col    = None
        self.graph   = JarvisOntologyGraph()
        self._init_vector()

    def _init_vector(self):
        """Initialise vector backend â€” tries chromadb+fastembed, falls back to SQLite+TF-IDF."""
        caps_file = Path.home() / ".jarvis_memory_caps.json"
        caps = {}
        try:
            caps = json.loads(caps_file.read_text()) if caps_file.exists() else {}
        except: pass

        self._backend = "none"

        # Try chromadb + fastembed
        if caps.get("chromadb") and caps.get("fastembed"):
            try:
                import chromadb
                from fastembed import TextEmbedding
                self._embed = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
                self.VECTOR_DB.mkdir(exist_ok=True)
                self._chroma = chromadb.PersistentClient(path=str(self.VECTOR_DB))
                self._col = self._chroma.get_or_create_collection("memories")
                self._vec_ok = True
                self._backend = "chromadb"
                count = self._col.count()
                print(f"{Fore.GREEN}Vector memory: ChromaDB+fastembed ({count} memories){Style.RESET_ALL}")
                return
            except Exception as e:
                print(f"{Fore.YELLOW}ChromaDB init failed: {e}{Style.RESET_ALL}")

        # Try SQLite + TF-IDF fallback
        try:
            import sqlite3 as _sq
            self._sqlite_db = Path.home() / ".jarvis_vectordb.db"
            conn = _sq.connect(str(self._sqlite_db))
            conn.execute("""CREATE TABLE IF NOT EXISTS memories
                            (id TEXT PRIMARY KEY, document TEXT, metadata TEXT, added TEXT)""")
            conn.commit(); conn.close()
            self._vec_ok = True
            self._backend = "sqlite_tfidf"
            # Count existing memories
            conn2 = _sq.connect(str(self._sqlite_db))
            count = conn2.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            conn2.close()
            print(f"{Fore.GREEN}Vector memory: SQLite+TF-IDF ({count} memories){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}Vector memory offline: {e}. Run setup_memory.py{Style.RESET_ALL}")

    # â”€â”€ JSON layer (source of truth) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _load_json(self):
        if self.JSON_FILE.exists():
            try:
                with open(self.JSON_FILE) as f:
                    return json.load(f)
            except: pass
        return {
            "preferences": {},
            "rules": [],
            "facts": {},
            "shortcuts": {},
            "episodes": [],
            "missions": {"active": None, "history": []},
            "operator_profile": {},
            "decision_log": [],
        }

    def _save_json(self):
        with open(self.JSON_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    # â”€â”€ Vector layer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _embed_text(self, text):
        """Get embedding using available backend."""
        if self._backend == "chromadb":
            return list(self._embed.embed([text]))[0].tolist()
        return None

    def _vec_add(self, doc_id, text, metadata=None):
        if not self._vec_ok: return
        try:
            if self._backend == "chromadb":
                emb = self._embed_text(text)
                existing = self._col.get(ids=[doc_id])
                if existing["ids"]:
                    self._col.update(ids=[doc_id], embeddings=[emb],
                                     documents=[text], metadatas=[metadata or {}])
                else:
                    self._col.add(ids=[doc_id], embeddings=[emb],
                                  documents=[text], metadatas=[metadata or {}])
            elif self._backend == "sqlite_tfidf":
                import sqlite3 as _sq, json as _jj
                conn = _sq.connect(str(self._sqlite_db))
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                conn.execute("INSERT OR REPLACE INTO memories VALUES (?,?,?,?)",
                             (doc_id, text, _jj.dumps(metadata or {}), ts))
                conn.commit(); conn.close()
        except: pass

    def _vec_search(self, query, n=5):
        if not self._vec_ok: return []
        try:
            if self._backend == "chromadb":
                emb = self._embed_text(query)
                count = self._col.count()
                if count == 0: return []
                res = self._col.query(query_embeddings=[emb],
                                      n_results=min(n, count))
                docs  = res.get("documents", [[]])[0]
                metas = res.get("metadatas",  [[]])[0]
                return list(zip(docs, metas))

            elif self._backend == "sqlite_tfidf":
                # TF-IDF keyword search via SQLite FTS-style scoring
                import sqlite3 as _sq
                conn = _sq.connect(str(self._sqlite_db))
                rows = conn.execute("SELECT document FROM memories").fetchall()
                conn.close()
                if not rows: return []
                # Simple TF-IDF: score each doc by query word overlap
                q_words = set(query.lower().split())
                scored = []
                for (doc,) in rows:
                    d_words = set(doc.lower().split())
                    score = len(q_words & d_words) / max(len(q_words), 1)
                    if score > 0:
                        scored.append((score, doc))
                scored.sort(reverse=True)
                return [(doc, {}) for _, doc in scored[:n]]
        except: return []

    # â”€â”€ Public API (mirrors old JarvisMemory) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def remember(self, category, key, value):
        if category not in self.data:
            self.data[category] = {} if category != "rules" else []
        if isinstance(self.data[category], list):
            self.data[category].append({"key": key, "value": value})
        else:
            self.data[category][key] = value
        self._save_json()
        # Add to vector store
        doc_id = f"{category}_{key}".replace(" ","_")
        self._vec_add(doc_id, f"{key}: {value}", {"category": category, "key": key})
        # Add to graph
        self.graph.add("user", f"has_{category}", key)
        self.graph.add(key, "means", str(value))
        return f"Remembered {key} sir."

    def add_rule(self, rule):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {"rule": rule, "added": ts}
        self.data["rules"].append(entry)
        self._save_json()
        doc_id = f"rule_{len(self.data['rules'])}"
        self._vec_add(doc_id, rule, {"category": "rule", "added": ts})
        self.graph.add("user", "follows_rule", rule[:40])
        return "Rule saved sir."

    def store_episode(self, user_text, assistant_text):
        """Persist compact user/assistant interaction for continuity across restarts."""
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        ep = {
            "ts": ts,
            "user": str(user_text or "")[:180],
            "assistant": str(assistant_text or "")[:220],
        }
        episodes = self.data.setdefault("episodes", [])
        if episodes and episodes[-1].get("user") == ep["user"] and episodes[-1].get("assistant") == ep["assistant"]:
            return
        episodes.append(ep)
        self.data["episodes"] = episodes[-150:]
        self._save_json()
        self._vec_add(f"episode_{int(time.time())}", f"{ep['user']} -> {ep['assistant']}", {"category": "episode", "ts": ts})

    def forget(self, key):
        removed = False
        for section in self.data.values():
            if isinstance(section, dict) and key in section:
                del section[key]; removed = True; break
            elif isinstance(section, list):
                before = len(section)
                section[:] = [x for x in section if key.lower() not in str(x).lower()]
                if len(section) < before: removed = True
        self._save_json()
        # Remove from vector store
        if self._vec_ok:
            try:
                all_ids = self._col.get()["ids"]
                to_del = [i for i in all_ids if key.lower() in i.lower()]
                if to_del: self._col.delete(ids=to_del)
            except: pass
        self.graph.remove_node(key)
        return "Forgotten." if removed else f"Nothing found for {key} sir."

    def recall(self, key=""):
        """Semantic recall â€” finds relevant memories even without exact match."""
        if not key:
            parts = []
            if self.data.get("rules"):    parts.append(f"{len(self.data['rules'])} rules")
            if self.data.get("preferences"): parts.append(f"{len(self.data['preferences'])} preferences")
            if self.data.get("facts"):    parts.append(f"{len(self.data['facts'])} facts")
            return "Memory contains " + ", ".join(parts) + "." if parts else "Memory is empty sir."

        # Try semantic vector search first
        if self._vec_ok:
            try:
                hits = self._vec_search(key, n=4)
            except Exception:
                hits = []
            if hits:
                results = [doc for doc, meta in hits]
                return f"Relevant memories for {key}: " + ". ".join(results[:3]) + "."

        # Fallback to keyword search
        results = []
        for section, items in self.data.items():
            if isinstance(items, dict):
                for k, v in items.items():
                    if key.lower() in k.lower() or key.lower() in str(v).lower():
                        results.append(f"{k}: {v}")
            elif isinstance(items, list):
                for item in items:
                    if key.lower() in str(item).lower():
                        results.append(str(item.get("rule", item)))
        return ". ".join(results) if results else f"Nothing in memory about {key} sir."

    def recall_semantic(self, query, n=5):
        """Pure semantic search â€” finds conceptually related memories."""
        hits = self._vec_search(query, n=n)
        if not hits: return self.recall(query)
        docs = [doc for doc, _ in hits]
        return "Here is what I know related to that: " + ". ".join(docs) + "."

    def list_rules(self):
        rules = self.data.get("rules", [])
        if not rules: return "No rules set sir."
        return "Your rules: " + ". ".join(r["rule"] for r in rules)

    def graph_query(self, topic):
        return self.graph.what_do_i_know_about(topic)

    def to_context(self):
        parts = []
        rules = self.data.get("rules", [])
        if rules:
            parts.append("PERSISTENT RULES â€” always follow these:")
            for r in rules: parts.append("  - " + r["rule"])
        prefs = self.data.get("preferences", {})
        if prefs:
            parts.append("USER PREFERENCES:")
            for k, v in prefs.items(): parts.append(f"  - {k}: {v}")
        facts = self.data.get("facts", {})
        if facts:
            parts.append("KNOWN FACTS:")
            for k, v in facts.items(): parts.append(f"  - {k}: {v}")
        episodes = self.data.get("episodes", [])
        if episodes:
            parts.append("RECENT PERMANENT EPISODES:")
            for ep in episodes[-6:]:
                u = str(ep.get("user", ""))[:120]
                a = str(ep.get("assistant", ""))[:120]
                parts.append(f"  - [{ep.get('ts','')}] U: {u} | A: {a}")
        mission = (self.data.get("missions", {}) or {}).get("active")
        if mission:
            parts.append("ACTIVE MISSION:")
            parts.append(f"  - {mission.get('title','')} [{mission.get('stage','brief')} {mission.get('progress',0)}%]")
            for nx in (mission.get("next_actions", []) or [])[:2]:
                parts.append(f"  - next: {nx}")
        op = self.data.get("operator_profile", {})
        if op:
            parts.append("OPERATOR PROFILE:")
            for k, v in list(op.items())[:6]:
                parts.append(f"  - {k}: {v}")
        dlog = self.data.get("decision_log", [])
        if dlog:
            parts.append("RECENT DECISIONS:")
            for it in dlog[:4]:
                parts.append(f"  - {it.get('ts','')}: {it.get('note','')}")
        return "\n".join(parts)

    def sync_projects_to_graph(self):
        """Sync all known projects into the ontology graph."""
        pf = Path.home() / "Desktop" / ".jarvis_projects.json"
        if not pf.exists(): return
        try:
            reg = json.loads(pf.read_text(encoding="utf-8"))
            for name, info in reg.items():
                self.graph.add_project(
                    name=name,
                    language=info.get("language",""),
                    description=info.get("description",""),
                    path=info.get("path","")
                )
        except: pass

class JarvisMemory:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE) as f:
                    return json.load(f)
            except:
                pass
        return {
            "preferences": {},
            "rules": [],
            "facts": {},
            "shortcuts": {},
            "episodes": [],
            "missions": {"active": None, "history": []},
            "operator_profile": {},
            "decision_log": [],
        }

    def _save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def remember(self, category, key, value):
        if category not in self.data:
            self.data[category] = {}
        if isinstance(self.data[category], list):
            self.data[category].append({"key": key, "value": value})
        else:
            self.data[category][key] = value
        self._save()
        return "Remembered " + key + " sir."

    def add_rule(self, rule):
        self.data["rules"].append({"rule": rule, "added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
        self._save()
        return "Rule saved sir."

    def store_episode(self, user_text, assistant_text):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        ep = {
            "ts": ts,
            "user": str(user_text or "")[:180],
            "assistant": str(assistant_text or "")[:220],
        }
        episodes = self.data.setdefault("episodes", [])
        if episodes and episodes[-1].get("user") == ep["user"] and episodes[-1].get("assistant") == ep["assistant"]:
            return
        episodes.append(ep)
        self.data["episodes"] = episodes[-150:]
        self._save()

    def forget(self, key):
        removed = False
        for section in self.data.values():
            if isinstance(section, dict) and key in section:
                del section[key]; removed = True; break
            elif isinstance(section, list):
                before = len(section)
                section[:] = [x for x in section if key.lower() not in str(x).lower()]
                if len(section) < before:
                    removed = True
        self._save()
        return "Forgotten." if removed else "Nothing found for " + key + " sir."

    def recall(self, key=""):
        if not key:
            parts = []
            if self.data.get("rules"): parts.append(str(len(self.data["rules"])) + " rules")
            if self.data.get("preferences"): parts.append(str(len(self.data["preferences"])) + " preferences")
            if self.data.get("facts"): parts.append(str(len(self.data["facts"])) + " facts")
            if self.data.get("shortcuts"): parts.append(str(len(self.data["shortcuts"])) + " shortcuts")
            return "Memory contains " + ", ".join(parts) + "." if parts else "Memory is empty sir."
        results = []
        for section, items in self.data.items():
            if isinstance(items, dict):
                for k, v in items.items():
                    if key.lower() in k.lower() or key.lower() in str(v).lower():
                        results.append(k + ": " + str(v))
            elif isinstance(items, list):
                for item in items:
                    if key.lower() in str(item).lower():
                        results.append(str(item.get("rule", item)))
        return ". ".join(results) if results else "Nothing in memory about " + key + " sir."

    def list_rules(self):
        rules = self.data.get("rules", [])
        if not rules: return "No rules set sir."
        return "Your rules: " + ". ".join(r["rule"] for r in rules)

    def to_context(self):
        parts = []
        rules = self.data.get("rules", [])
        if rules:
            parts.append("PERSISTENT RULES â€” always follow these:")
            for r in rules: parts.append("  - " + r["rule"])
        prefs = self.data.get("preferences", {})
        if prefs:
            parts.append("USER PREFERENCES:")
            for k, v in prefs.items(): parts.append("  - " + k + ": " + str(v))
        facts = self.data.get("facts", {})
        if facts:
            parts.append("KNOWN FACTS:")
            for k, v in facts.items(): parts.append("  - " + k + ": " + str(v))
        shortcuts = self.data.get("shortcuts", {})
        if shortcuts:
            parts.append("SHORTCUTS:")
            for k, v in shortcuts.items(): parts.append("  - '" + k + "' means: " + str(v))
        episodes = self.data.get("episodes", [])
        if episodes:
            parts.append("RECENT PERMANENT EPISODES:")
            for ep in episodes[-6:]:
                u = str(ep.get("user", ""))[:120]
                a = str(ep.get("assistant", ""))[:120]
                parts.append(f"  - [{ep.get('ts','')}] U: {u} | A: {a}")
        mission = (self.data.get("missions", {}) or {}).get("active")
        if mission:
            parts.append("ACTIVE MISSION:")
            parts.append("  - " + str(mission.get("title","")) + " [" + str(mission.get("stage","brief")) + " " + str(mission.get("progress",0)) + "%]")
        op = self.data.get("operator_profile", {})
        if op:
            parts.append("OPERATOR PROFILE:")
            for k, v in list(op.items())[:6]:
                parts.append("  - " + str(k) + ": " + str(v))
        dlog = self.data.get("decision_log", [])
        if dlog:
            parts.append("RECENT DECISIONS:")
            for it in dlog[:4]:
                parts.append("  - " + str(it.get("ts","")) + ": " + str(it.get("note","")))
        return "\n".join(parts)

# â”€â”€ Response pools â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_ERR_FALLBACK = "Let me know when you need something sir."


PROTOCOLS = {
    "alpha":      ("ALPHA PROTOCOL",     "Full system diagnostics. All sensors active."),
    "beta":       ("BETA PROTOCOL",      "Reduced power mode. Non-essential systems offline."),
    "lockdown":   ("LOCKDOWN PROTOCOL",  "Locking workstation and securing the perimeter."),
    "ghost":      ("GHOST PROTOCOL",     "Silent mode. Going dark sir."),
    "overdrive":  ("OVERDRIVE PROTOCOL", "Maximum performance. All resources to primary task."),
    "reboot":     ("REBOOT SEQUENCE",    "Controlled restart in 30 seconds. Save your work sir."),
    "blackout":   ("BLACKOUT PROTOCOL",  "Displays off. You were never here sir."),
    "cleanup":    ("CLEANUP PROTOCOL",   "Purging temp files, flushing DNS, emptying recycle bin."),
    "focus":      ("FOCUS PROTOCOL",     "All windows minimized. Deep work mode engaged."),
    "nightwatch": ("NIGHTWATCH PROTOCOL","Setting 0800 alarm and initiating sleep mode."),
    "deploy":     ("DEPLOY SEQUENCE",    "Pushing commits. Stand by sir."),
    "stealth":    ("STEALTH PROTOCOL",   "Windows minimized, audio muted. Invisible mode active."),
    "recovery":   ("RECOVERY PROTOCOL",  "Running cleanup and DNS flush."),
    "omega":      ("OMEGA PROTOCOL",     "Complete shutdown in 60 seconds. Save everything now sir."),
    "sandbox":    ("SANDBOX PROTOCOL",   "Isolating network adapters. Air gap engaged."),
    "sentinel":   ("SENTINEL PROTOCOL",  "Initiating background monitoring. Watching all systems."),
    "purge":      ("PURGE PROTOCOL",     "Clearing all temporary data, logs, and cache files."),
    "hibernate":  ("HIBERNATE PROTOCOL", "Saving system state and entering hibernation."),
    "revelations":("PROTOCOL REVELATIONS","All Jarvis processes terminating. Goodbye sir."),
}



QUICK_ACTIONS = {
    'screenshot':  'take_screenshot',
    'health':      'system_health_report',
    'lock':        'lock_pc',
    'processes':   'list_processes',
    'notes':       'read_notes',
    'weather':     'get_weather',
    'enter_architect_mode': 'enter_architect_mode',
    'enter_ship_mode': 'enter_ship_mode',
    'enter_debug_hunt': 'enter_debug_hunt',
    'daily_briefing': 'daily_briefing',
}

def rand(lst): return random.choice(lst)

def tts_clean(text):
    text = re.sub(r'<think>[\s\S]*?</think>', '', str(text), flags=re.I)
    text = re.sub(r'^\s*(thought|thinking|reasoning)\s*:\s*.*$', '', text, flags=re.I|re.M)
    text = re.sub(r'^\s*(analysis|chain of thought)\s*:\s*.*$', '', text, flags=re.I|re.M)
    text = re.sub(r'\[THOUGHT[^\]]*\].*', '', text, flags=re.I)
    text = re.sub(r'^\s*(i think|i believe|my reasoning|my thought process)\b[^\n]*', '', text, flags=re.I|re.M)
    text = re.sub(r'^\s*as an ai[^\n]*', '', text, flags=re.I|re.M)
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'`+', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[|â€¢â†’â†â†‘â†“â–ªâ—¦]', '', text)
    text = re.sub(r'[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF]+', '', text)
    text = text.encode("ascii", errors="ignore").decode("ascii")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# â”€â”€ Voice â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class JarvisVoice:
    def __init__(self, rate=155, volume=0.95):
        self.rate = rate
        self.volume = volume
        self._lock = threading.Lock()
        self._interrupted = threading.Event()
        self.is_speaking = False
        self._voice_id = self._find_voice()
        self._on_wake = None
        self._on_enough = None
        self._mic_device = 1
        self._vosk_path = ""
        self._piper_model = None
        self._piper_config = None
        self._piper_voice_obj = None
        self._use_piper = False
        self._interrupt_thread = None
        self._interrupt_model = None
        self._last_interrupt_ts = 0.0
        self._interrupt_on_speech = True
        self._speech_interrupt_min_words = 2
        try:
            cfg_file = Path.home() / ".jarvis_config.json"
            if cfg_file.exists():
                import json as _jj
                self._mic_device = int(_jj.loads(cfg_file.read_text()).get("mic_device", 1))
        except:
            self._mic_device = 1
        self._init_piper()

    def _init_piper(self):
        """Try to load Piper TTS with JARVIS voice model. Loads voice object immediately."""
        MODEL_FILE  = "en/en_GB/jarvis/medium/jarvis-medium.onnx"
        CONFIG_FILE = "en/en_GB/jarvis/medium/jarvis-medium.onnx.json"
        try:
            from piper import PiperVoice
            from huggingface_hub import hf_hub_download
            import warnings, sounddevice as _sd, numpy as _np
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model_path  = hf_hub_download("jgkawell/jarvis", MODEL_FILE)
                config_path = hf_hub_download("jgkawell/jarvis", CONFIG_FILE)
            self._piper_model  = model_path
            self._piper_config = config_path
            # Load the voice object NOW so any errors surface at startup
            self._piper_voice_obj = PiperVoice.load(
                model_path, config_path=config_path, use_cuda=False)
            self._use_piper = True
            print(f"{Fore.GREEN}Voice: Piper JARVIS model ready (sr={self._piper_voice_obj.config.sample_rate}){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}Voice: Piper unavailable ({type(e).__name__}: {e}), using pyttsx3{Style.RESET_ALL}")
            self._use_piper = False
            self._piper_voice_obj = None

    def _speak_piper(self, text):
        """Speak using Piper TTS JARVIS voice with interruptible async playback."""
        import wave as _wave, io as _io, tempfile as _tmp, os as _os
        voice = self._piper_voice_obj
        if voice is None:
            raise RuntimeError("Piper voice not loaded")
        if self._interrupted.is_set():
            return
        # Synthesise to buffer
        buf = _io.BytesIO()
        wav_file = _wave.open(buf, 'wb')
        voice.synthesize_wav(text, wav_file)
        wav_file.close()
        if self._interrupted.is_set():
            return
        wav_bytes = buf.getvalue()
        duration_s = 1.5
        try:
            with _wave.open(_io.BytesIO(wav_bytes), "rb") as wf:
                frames = max(1, int(wf.getnframes()))
                rate = max(1, int(wf.getframerate()))
                duration_s = float(frames) / float(rate)
        except Exception:
            pass
        # Write to temp file and play asynchronously so interrupt can cut speech instantly.
        tmp = _tmp.mktemp(suffix=".wav")
        with open(tmp, 'wb') as f:
            f.write(wav_bytes)
        try:
            import time as _time
            import winsound
            if not self._interrupted.is_set():
                winsound.PlaySound(tmp, winsound.SND_FILENAME | winsound.SND_ASYNC)
                end_at = _time.time() + duration_s + 0.25
                while _time.time() < end_at:
                    if self._interrupted.is_set():
                        winsound.PlaySound(None, winsound.SND_PURGE)
                        break
                    _time.sleep(0.03)
        finally:
            try:
                import winsound
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass
            try: _os.unlink(tmp)
            except: pass

    def _find_voice(self):
        try:
            e = pyttsx3.init()
            voices = e.getProperty("voices")
            chosen = None
            for v in voices:
                if any(x in v.name.lower() for x in ["david","mark","george","male"]):
                    chosen = v.id; break
            if not chosen and voices:
                chosen = voices[0].id
            e.stop()
            return chosen
        except:
            return None

    def stop(self): 
        self._interrupted.set()
        try:
            import sounddevice as _sd
            _sd.stop()
        except Exception:
            pass
        try:
            import winsound
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

    def speak(self, text):
        text = tts_clean(text)
        if not text: return
        print(f"{Fore.CYAN}Jarvis: {text}{Style.RESET_ALL}")
        _write_hud("speaking", text=text)
        self._interrupted.clear()
        self.is_speaking = True
        if self._vosk_path and self._on_wake is not None:
            self.start_interrupt_listener(
                self._mic_device, self._vosk_path,
                self._on_wake, self._on_enough)
        # Split into sentences so nothing gets cut off
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        if not sentences or sentences == ['']: sentences = [text]
        with self._lock:
            try:
                if self._use_piper and self._piper_voice_obj is not None:
                    try:
                        if not self._interrupted.is_set():
                            self._speak_piper(text)
                    except Exception as pe:
                        import traceback
                        print(f"{Fore.RED}Piper error: {pe}{Style.RESET_ALL}")
                        traceback.print_exc()
                        self._use_piper = False
                        self._speak_pyttsx3(sentences)
                else:
                    if self._use_piper:
                        print(f"{Fore.YELLOW}Piper voice obj missing, falling back{Style.RESET_ALL}")
                        self._use_piper = False
                    self._speak_pyttsx3(sentences)
            except Exception as ex:
                import traceback
                print(f"{Fore.RED}TTS error: {ex}{Style.RESET_ALL}")
                traceback.print_exc()
            finally:
                self.is_speaking = False
                _write_hud("standby")

    def _speak_pyttsx3(self, sentences):
        """Speak sentences using pyttsx3, one engine instance, no truncation."""
        try:
            e = pyttsx3.init()
            e.setProperty("rate", self.rate)
            e.setProperty("volume", self.volume)
            if self._voice_id:
                e.setProperty("voice", self._voice_id)
            for sentence in sentences:
                if self._interrupted.is_set(): break
                sentence = sentence.strip()
                if not sentence: continue
                e.say(sentence)
            e.runAndWait()
            e.stop()
        except Exception as ex:
            print(f"{Fore.RED}pyttsx3: {ex}{Style.RESET_ALL}")


    def interrupt(self):
        """Stop speaking immediately."""
        self._interrupted.set()

    def stop(self):
        self._interrupted.set()
        try:
            import sounddevice as _sd
            _sd.stop()
        except Exception:
            pass
        try:
            import winsound
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass

    def start_interrupt_listener(self, mic_device, vosk_path, on_wake, on_enough):
        """Background thread: listen while Jarvis speaks, interrupt on trigger words."""
        if self._interrupt_thread is not None and self._interrupt_thread.is_alive():
            return self._interrupt_thread

        def _listen():
            try:
                from vosk import Model, KaldiRecognizer
                import logging; logging.disable(logging.CRITICAL)
                m = Path(vosk_path)
                if not m.exists(): return
                if self._interrupt_model is None:
                    self._interrupt_model = Model(str(m))
                model = self._interrupt_model
                rec = KaldiRecognizer(model, 16000)
                chunk = int(16000 * 0.1)
                wake_hits = 0
                enough_hits = 0
                speech_hits = 0
                noise_floor = 0.0
                with sd.InputStream(samplerate=16000, channels=1, dtype="int16",
                                    blocksize=chunk, device=mic_device) as s:
                    while self.is_speaking and not self._interrupted.is_set():
                        data, _ = s.read(chunk)
                        raw = data.flatten().tobytes()
                        vol = float(np.abs(data).mean())
                        noise_floor = vol if noise_floor == 0 else (noise_floor * 0.93 + vol * 0.07)
                        text = ""
                        if rec.AcceptWaveform(raw):
                            text = json.loads(rec.Result()).get("text","").lower()
                        else:
                            text = json.loads(rec.PartialResult()).get("partial","").lower()
                        # More robust phrase gating to avoid accidental interruption.
                        enough_detected = any(
                            x in text for x in [
                                "thats enough", "that's enough", "enough jarvis", "be quiet",
                                "stop talking", "shut up", "cancel speech", "stop now"
                            ]
                        )
                        wake_detected = any(re.search(r"\b" + w + r"\b", text) for w in ["jarvis","javis","travis","davis"])
                        words = re.findall(r"[a-z']+", text)
                        loud_voice = vol > max(120.0, noise_floor * 2.2)
                        speech_detected = bool(
                            self._interrupt_on_speech and loud_voice and
                            len([w for w in words if len(w) > 1]) >= int(max(1, self._speech_interrupt_min_words))
                        )
                        enough_hits = (enough_hits + 1) if enough_detected else max(0, enough_hits - 1)
                        wake_hits = (wake_hits + 1) if wake_detected else max(0, wake_hits - 1)
                        speech_hits = (speech_hits + 1) if speech_detected else max(0, speech_hits - 1)
                        now_ts = time.time()

                        if enough_hits >= 2 and (now_ts - self._last_interrupt_ts) > 0.8:
                            self._last_interrupt_ts = now_ts
                            self.interrupt()
                            if on_enough: on_enough()
                            return
                        if wake_hits >= 2 and (now_ts - self._last_interrupt_ts) > 0.8:
                            self._last_interrupt_ts = now_ts
                            self.interrupt()
                            if on_wake: on_wake()
                            return
                        if speech_hits >= 3 and (now_ts - self._last_interrupt_ts) > 0.8:
                            self._last_interrupt_ts = now_ts
                            self.interrupt()
                            if on_wake: on_wake()
                            return
            except Exception:
                pass
        self._interrupt_thread = threading.Thread(target=_listen, daemon=True)
        self._interrupt_thread.start()
        return self._interrupt_thread




class ConversationState:
    def __init__(self,flow,steps): self.flow=flow;self.steps=steps;self.data={};self.current=0
    def next_question(self): return self.steps[self.current][0] if self.current<len(self.steps) else None
    def store_answer(self,ans): self.data[self.steps[self.current][1]]=ans;self.current+=1
    def is_complete(self): return self.current>=len(self.steps)

# â”€â”€ PC Tools â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class PCTools:
    def __init__(self, workspace, home):
        self.workspace = Path(workspace)
        self.home = Path(home)
        self._reminder_cb = None
        self._active_proj = ""
        self._school_ics_cache_ts = 0.0
        self._school_ics_cache = []
        self._last_school_off = {}
        self._updates_file = self.workspace / ".jarvis_update_log.json"
        self._ensure_update_log()

    def _load_updates(self):
        try:
            if self._updates_file.exists():
                return json.loads(self._updates_file.read_text(encoding="utf-8"))
        except Exception:
            pass
        return []

    def _save_updates(self, entries):
        try:
            self._updates_file.write_text(json.dumps(entries, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _ensure_update_log(self):
        entries = self._load_updates()
        mk12 = {
            "version": "12.0.0",
            "label": "JARVIS MK 12",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "changes": [
                    "Persistent episode memory and semantic recall improvements",
                    "Calendar follow-up reasoning now answers why a day is off",
                    "Follow-up question context update for school calendar queries",
                    "Threat-removal intent executes Defender remediation flow",
                    "HUD upgraded with MK12 status and update brief panel",
                    "Project framework mode with roadmap, task board, checkpoints, and build status"
                ]
            }
        found = False
        for i, e in enumerate(entries):
            if e.get("version") == "12.0.0":
                entries[i] = mk12
                found = True
                break
        if not found:
            entries.insert(0, mk12)
        self._save_updates(entries[:80])

    def get_update_log(self, limit=5):
        entries = self._load_updates()[:max(1, int(limit))]
        if not entries:
            return "No update log entries yet sir."
        lines = []
        for e in entries:
            ver = e.get("version", "unknown")
            label = e.get("label", "Update")
            date = e.get("date", "")
            changes = e.get("changes", [])[:3]
            lines.append(f"{label} v{ver} ({date}): " + "; ".join(changes))
        return " | ".join(lines)

    def latest_update_brief(self):
        entries = self._load_updates()
        if not entries:
            return "No update entries available."
        e = entries[0]
        ver = e.get("version", "unknown")
        title = e.get("label", "Update")
        ch = e.get("changes", [])
        return {
            "version": ver,
            "title": title,
            "date": e.get("date", ""),
            "summary": ch[0] if ch else ""
        }

    def _r(self, path):
        """Resolve path with common shortcut aliases."""
        # If a project is active, resolve relative paths within it
        if hasattr(self, "_active_proj_path") and self._active_proj_path:
            p_str = str(path).strip()
            p = Path(p_str)
            if not p.is_absolute():
                # Check if it names a subfolder of project
                proj_candidate = self._active_proj_path / p
                if proj_candidate.exists() or not (self.workspace / p).exists():
                    return proj_candidate
        aliases = {
            "desktop":   self.home / "Desktop",
            "downloads": self.home / "Downloads",
            "documents": self.home / "Documents",
            "pictures":  self.home / "Pictures",
            "music":     self.home / "Music",
            "videos":    self.home / "Videos",
            "home":      self.home,
            "workspace": self.workspace,
        }
        p_str = str(path).strip()
        lower = p_str.lower().strip("/")
        if lower in aliases:
            return aliases[lower]
        p = Path(p_str)
        if p.is_absolute():
            return p
        # Try workspace first, then home
        if (self.workspace / p).exists():
            return self.workspace / p
        if (self.home / p).exists():
            return self.home / p
        return self.workspace / p

    def _sh(self, cmd, cwd=None):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                               timeout=30, cwd=cwd or str(self.workspace))
            return r.stdout.strip() or r.stderr.strip() or "Done."
        except subprocess.TimeoutExpired: return "Command timed out."
        except Exception as e: return "Error: " + str(e)

    def _ps(self, cmd):
        return self._sh('powershell -WindowStyle Hidden -NonInteractive -Command "' + cmd + '"')


    def _send_media_key(self, key):
        import tempfile
        ps = '$wsh=New-Object -ComObject WScript.Shell\n$wsh.SendKeys("' + key + '")'
        tmp = Path(tempfile.gettempdir()) / "jmk.ps1"
        tmp.write_text(ps, encoding="utf-8")
        subprocess.Popen(
            ["powershell", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", str(tmp)],
            creationflags=subprocess.CREATE_NO_WINDOW
        )


    def _set_clipboard(self, text):
        import tempfile
        tmp = Path(tempfile.gettempdir()) / "jclip.txt"
        tmp.write_text(text, encoding="utf-8")
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command",
             "Get-Content -Raw '" + str(tmp) + "' | Set-Clipboard"],
            capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW
        )


    def _send_keys(self, keys):
        import tempfile
        script = '$wsh = New-Object -ComObject WScript.Shell\n$wsh.SendKeys("' + keys + '")'
        tmp = Path(tempfile.gettempdir()) / "jarvis_keys.ps1"
        tmp.write_text(script, encoding="utf-8")
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(tmp)],
                       capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)


    # â”€â”€ Files â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def create_file(self, path, content=""):
        p = self._r(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return "Created " + p.name + " sir."

    def read_file(self, path):
        p = self._r(path)
        return p.read_text(encoding="utf-8") if p.exists() else "File not found: " + str(path)

    def write_file(self, path, content):
        p = self._r(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return "Written to " + p.name + " sir."

    def append_file(self, path, content):
        p = self._r(path)
        with open(p, "a", encoding="utf-8") as f: f.write(content)
        return "Appended to " + p.name + " sir."

    def delete_file(self, path):
        p = self._r(path)
        if p.is_file(): p.unlink(); return "Deleted " + p.name + " sir."
        return "File not found."

    def rename_file(self, path, new_name):
        p = self._r(path); p.rename(p.parent / new_name)
        return "Renamed to " + new_name + " sir."

    def move_file(self, src, dst):
        shutil.move(str(self._r(src)), str(self._r(dst))); return "Moved sir."

    def copy_file(self, src, dst):
        shutil.copy2(str(self._r(src)), str(self._r(dst))); return "Copied sir."

    def file_exists(self, path):
        return "Yes, it exists." if self._r(path).exists() else "No, it does not exist."

    def file_size(self, path):
        p = self._r(path)
        if not p.exists(): return "File not found."
        s = p.stat().st_size
        return p.name + " is " + (f"{s/1024:.1f} kilobytes" if s < 1024**2 else f"{s/1024**2:.1f} megabytes") + " sir."

    def count_lines(self, path):
        p = self._r(path)
        if not p.exists(): return "File not found."
        return p.name + " has " + str(p.read_text(encoding="utf-8", errors="ignore").count("\n")) + " lines sir."

    def list_directory(self, path="."):
        p = self._r(path)
        if not p.is_dir(): return "Not a directory."
        items = [("folder: " if i.is_dir() else "file: ") + i.name for i in sorted(p.iterdir())]
        return ", ".join(items) if items else "Empty directory."


    def newest_file(self, directory="downloads", extension=""):
        """Find the most recently downloaded/modified file in a directory."""
        p = self._r(directory)
        if not p.is_dir(): return f"Directory not found: {directory}"
        files = [f for f in p.iterdir() if f.is_file()]
        if extension:
            files = [f for f in files if f.suffix.lower() == "." + extension.lower().strip(".")]
        if not files: return f"No files found in {p.name}."
        newest = max(files, key=lambda f: f.stat().st_mtime)
        return str(newest)

    def open_newest_file(self, directory="downloads", extension=""):
        """Open the most recently modified file in a directory."""
        path = self.newest_file(directory, extension)
        if path.startswith("No files") or path.startswith("Directory"):
            return path
        p = Path(path)
        import os
        os.startfile(str(p))
        return f"Opened {p.name} sir."

    def read_pdf(self, path):
        """Extract text from a PDF and return it for summarization."""
        p = self._r(path)
        if not p.exists():
            # Try downloads folder
            p = self.home / "Downloads" / Path(path).name
        if not p.exists(): return f"PDF not found: {path}"
        try:
            import subprocess as _sp
            # Use powershell to extract PDF text via .NET
            ps = (
                f"Add-Type -Path '{p}' -ErrorAction SilentlyContinue; "
                f"$r=New-Object iTextSharp.text.pdf.PdfReader('{p}');"
                "$t='';1..$r.NumberOfPages|%{$t+=[iTextSharp.text.pdf.parser.PdfTextExtractor]::GetTextFromPage($r,$_)};$t"
            )
            # Simpler approach: use pdfminer or just open it
            try:
                import subprocess
                _si2 = subprocess.STARTUPINFO()
                _si2.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                _si2.wShowWindow = 0
                result = subprocess.run(
                    ['powershell', '-Command',
                     f"(Get-Content '{p}' -Raw -Encoding Byte | ForEach-Object {{[System.Text.Encoding]::UTF8.GetString($_)}})[:3000]"],
                    capture_output=True, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW
                )
                text = result.stdout.strip()[:3000]
            except:
                text = ""
            if not text or len(text) < 50:
                # Just return path so Claude can open and describe
                return f"PDF found at {p}. Opening now."
            return f"PDF content from {p.name}: " + text
        except Exception as e:
            return f"Could not read PDF {p.name}: {e}. Try opening it instead."

    def create_directory(self, path):
        p = self._r(path); p.mkdir(parents=True, exist_ok=True)
        return "Directory " + p.name + " created sir."

    def delete_directory(self, path):
        p = self._r(path)
        if p.is_dir(): shutil.rmtree(p); return "Deleted directory " + p.name + " sir."
        return "Not a directory."

    def search_files(self, pattern, directory="."):
        p = self._r(directory)
        matches = list(p.rglob(pattern))[:20]
        if not matches: return "No files matching " + pattern + " found."
        return ", ".join(m.name for m in matches)

    def zip_directory(self, path, output=""):
        p = self._r(path)
        out = self._r(output) if output else self.workspace / (p.name + ".zip")
        shutil.make_archive(str(out).replace(".zip", ""), "zip", str(p.parent), p.name)
        return "Zipped to " + out.name + " sir."

    def get_file_info(self, path):
        p = self._r(path)
        if not p.exists(): return "File not found."
        s = p.stat()
        mod = datetime.datetime.fromtimestamp(s.st_mtime).strftime("%B %d at %I:%M %p")
        return p.name + ", " + f"{s.st_size/1024:.1f} KB" + ", modified " + mod + " sir."

    def find_duplicates(self, directory="."):
        p = self._r(directory)
        hashes = {}
        for f in p.rglob("*"):
            if f.is_file():
                h = hashlib.md5(f.read_bytes()).hexdigest()
                hashes.setdefault(h, []).append(f.name)
        dups = {h: v for h, v in hashes.items() if len(v) > 1}
        if not dups: return "No duplicate files found sir."
        return ". ".join(v[0] + " and " + v[1] + " are duplicates" for v in list(dups.values())[:5])

    # â”€â”€ System â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def system_info(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        return (f"CPU at {cpu} percent. RAM {mem.percent} percent used, "
                f"{mem.used//1024**3} of {mem.total//1024**3} gigabytes. "
                f"Disk {disk.percent} percent used, {disk.free//1024**3} gigabytes free.")

    def cpu_info(self):
        freq = psutil.cpu_freq()
        return f"CPU at {psutil.cpu_percent(interval=1)} percent, {psutil.cpu_count(logical=False)} cores, {freq.current:.0f} megahertz."

    def memory_info(self):
        m = psutil.virtual_memory()
        return f"RAM: {m.used//1024**3} of {m.total//1024**3} gigabytes used, {m.percent} percent."

    def disk_info(self):
        parts = []
        for p in psutil.disk_partitions():
            try:
                u = psutil.disk_usage(p.mountpoint)
                parts.append(p.device + ": " + str(u.used//1024**3) + " of " + str(u.total//1024**3) + " gigabytes used")
            except: pass
        return ". ".join(parts)

    def network_info(self):
        s = psutil.net_io_counters()
        return f"Sent {s.bytes_sent//1024**2} megabytes, received {s.bytes_recv//1024**2} megabytes."

    def list_processes(self, count=10):
        procs = sorted(psutil.process_iter(["pid","name","cpu_percent","memory_percent"]),
                       key=lambda x: x.info["cpu_percent"] or 0, reverse=True)[:int(count)]
        return ". ".join(p.info["name"] + " at " + str(p.info["cpu_percent"]) + " percent CPU" for p in procs)

    def kill_process(self, pid):
        try:
            p = psutil.Process(int(pid)); name = p.name(); p.terminate()
            return "Terminated " + name + " sir."
        except Exception as e: return "Could not terminate: " + str(e)

    def kill_process_by_name(self, name):
        killed = 0
        for p in psutil.process_iter(["name"]):
            if name.lower() in p.info["name"].lower():
                try: p.terminate(); killed += 1
                except: pass
        return "Terminated " + str(killed) + " process" + ("es" if killed != 1 else "") + " named " + name + "." if killed else "No process named " + name + " found."

    def get_time(self):
        return datetime.datetime.now().strftime("It is %I:%M %p on %A, %B %d, %Y.")

    def get_uptime(self):
        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        up = datetime.datetime.now() - boot
        h, rem = divmod(int(up.total_seconds()), 3600); m = rem // 60
        return f"System running for {h} hours and {m} minutes sir."

    def get_battery(self):
        b = psutil.sensors_battery()
        if not b: return "No battery detected sir."
        return f"Battery at {b.percent:.0f} percent, {'charging' if b.power_plugged else 'discharging'} sir."

    def get_hostname(self): return "This machine is named " + socket.gethostname() + " sir."
    def get_username(self): return "You are logged in as " + os.getlogin() + " sir."

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close()
            return "Local IP is " + ip + " sir."
        except: return "Could not determine local IP."

    def get_public_ip(self):
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=5)
            return "Public IP is " + r.json()["ip"] + " sir."
        except: return "Could not retrieve public IP."

    def ping(self, host):
        r = self._sh("ping -n 2 " + host)
        if "Average" in r:
            return "Ping to " + host + ": average " + r.split("Average = ")[-1].strip() + "."
        return "Ping to " + host + " failed."

    def check_internet(self):
        try: requests.get("https://www.google.com", timeout=3); return "Internet connection is active sir."
        except: return "No internet connection detected sir."

    def list_drives(self):
        drives = []
        for p in psutil.disk_partitions():
            try:
                u = psutil.disk_usage(p.mountpoint)
                drives.append(p.device + " with " + str(u.total//1024**3) + " gigabytes")
            except: pass
        return ". ".join(drives)

    def list_open_ports(self):
        conns = [c for c in psutil.net_connections() if c.status == "LISTEN"][:10]
        return "Listening on ports: " + ", ".join(str(c.laddr.port) for c in conns) if conns else "No listening ports found."

    def list_startup_programs(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run")
            items = []
            i = 0
            while True:
                try: name, _, _ = winreg.EnumValue(key, i); items.append(name); i += 1
                except: break
            return "Startup programs: " + ", ".join(items) if items else "No startup programs found."
        except: return "Could not read startup programs."

    def watch_cpu(self, seconds=5):
        readings = [psutil.cpu_percent(interval=1) for _ in range(int(seconds))]
        return f"Over {seconds} seconds: average {sum(readings)/len(readings):.0f} percent, peak {max(readings):.0f} percent."

    def daily_briefing(self):
        t = self.get_time()
        try: w = self.get_weather()
        except: w = "weather unavailable"
        try: tasks = self.read_todo()
        except: tasks = "no tasks"
        return t + " " + w + " " + tasks

    # â”€â”€ Shell / Apps â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def run_command(self, command): return self._sh(command)
    def run_powershell(self, command): return self._ps(command)

    def open_file(self, path):
        p = self._r(path)
        if platform.system() == "Windows": os.startfile(str(p))  # os.startfile handles spaces fine
        else: subprocess.Popen(["xdg-open", str(p)])
        return "Opened " + p.name + " sir."

    def open_url(self, url):
        if not url.startswith("http"): url = "https://" + url
        webbrowser.open(url); return "Opened " + url + " sir."

    def open_app(self, app_name):
        """Launch an app by name, trying multiple strategies."""
        import shutil as _shutil, glob as _glob
        lname = app_name.lower().strip()
        appdata = os.environ.get("APPDATA","")
        localdata = os.environ.get("LOCALAPPDATA","")
        uname = os.getlogin()

        # Known aliases â€” checked first
        aliases = {
            "steam":         "C:/Program Files (x86)/Steam/steam.exe",
            "discord":       localdata + "/Discord/Update.exe --processStart Discord.exe",
            "chrome":        "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "google chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "firefox":       "C:/Program Files/Mozilla Firefox/firefox.exe",
            "edge":          "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            "spotify":       appdata + "/Spotify/Spotify.exe",
            "vscode":        localdata + "/Programs/Microsoft VS Code/Code.exe",
            "vs code":       localdata + "/Programs/Microsoft VS Code/Code.exe",
            "visual studio code": localdata + "/Programs/Microsoft VS Code/Code.exe",
            "obs":           "C:/Program Files/obs-studio/bin/64bit/obs64.exe",
            "vlc":           "C:/Program Files/VideoLAN/VLC/vlc.exe",
            "notepad++":     "C:/Program Files/Notepad++/notepad++.exe",
            "word":          "C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE",
            "excel":         "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE",
            "powerpoint":    "C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE",
            "paint":         "mspaint.exe",
            "calculator":    "calc.exe",
            "notepad":       "notepad.exe",
            "task manager":  "taskmgr.exe",
            "terminal":      "wt.exe",
            "explorer":      "explorer.exe",
            "file explorer": "explorer.exe",
            "cmd":           "cmd.exe",
            "powershell":    "powershell.exe",
            "snipping tool": "snippingtool.exe",
        }

        # 1. Alias table
        if lname in aliases:
            target = aliases[lname]
            if " --" in target:
                exe, args = target.split(" ", 1)
                if Path(exe).exists():
                    subprocess.Popen(exe + " " + args, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    return "Launching " + app_name + " sir."
            p = Path(target)
            if p.exists():
                subprocess.Popen([str(p)], creationflags=subprocess.CREATE_NO_WINDOW)
                return "Launching " + app_name + " sir."

        # 2. shutil.which â€” finds anything on PATH
        found = _shutil.which(app_name) or _shutil.which(app_name + ".exe")
        if found:
            subprocess.Popen([found], creationflags=subprocess.CREATE_NO_WINDOW)
            return "Launching " + app_name + " sir."

        # 3. Windows start verb â€” works for installed apps by display name
        r = subprocess.run('start "" "' + app_name + '"', shell=True, capture_output=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
        if r.returncode == 0:
            return "Launching " + app_name + " sir."

        # 4. Search Program Files
        for d in ["C:/Program Files", "C:/Program Files (x86)", appdata, localdata]:
            matches = _glob.glob(d + "/**/" + app_name + "*.exe", recursive=True)
            if matches:
                subprocess.Popen([matches[0]], creationflags=subprocess.CREATE_NO_WINDOW)
                return "Launching " + Path(matches[0]).name + " sir."

        # 5. Last resort
        subprocess.Popen('start "" "' + app_name + '"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return "Attempted to open " + app_name + " sir. If nothing appeared, try giving me the full path."


    def close_app(self, app_name): return self.kill_process_by_name(app_name)

    def search_web(self, query):
        webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))
        return "Searching Google for " + query + " sir."

    def search_youtube(self, query):
        webbrowser.open("https://www.youtube.com/results?search_query=" + query.replace(" ", "+"))
        return "Searching YouTube for " + query + " sir."

    def open_calculator(self): subprocess.Popen("calc.exe", creationflags=subprocess.CREATE_NO_WINDOW); return "Calculator opened sir."
    def open_notepad(self, path=""): subprocess.Popen(('notepad "' + str(self._r(path)) + '"') if path else "notepad", shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Notepad opened sir."
    def open_task_manager(self): subprocess.Popen("taskmgr.exe", creationflags=subprocess.CREATE_NO_WINDOW); return "Task manager opened sir."
    def open_file_explorer(self, path="."): subprocess.Popen('explorer "' + str(self._r(path)) + '"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "File explorer opened sir."
    def open_settings(self): subprocess.Popen("ms-settings:", shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Settings opened sir."
    def open_control_panel(self): subprocess.Popen("control", creationflags=subprocess.CREATE_NO_WINDOW); return "Control panel opened sir."
    def open_device_manager(self): subprocess.Popen("devmgmt.msc", shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Device manager opened sir."
    def open_github(self): webbrowser.open("https://github.com"); return "Opening GitHub sir."

    # -- Discord --
    def open_discord(self):
        return self.open_app("discord")

    def discord_toggle_mute(self):
        self.open_discord()
        time.sleep(0.35)
        self._send_keys("^+m")
        return "Discord mute toggled sir."

    def discord_toggle_deafen(self):
        self.open_discord()
        time.sleep(0.35)
        self._send_keys("^+d")
        return "Discord deafen toggled sir."

    def discord_open_channel(self, target):
        """Open Discord quick switcher and jump to a channel/server/user."""
        q = str(target or "").strip()
        if not q:
            return "Provide a Discord target sir."
        self.open_discord()
        time.sleep(0.45)
        self._send_keys("^k")
        time.sleep(0.2)
        self._set_clipboard(q)
        self._send_keys("^v")
        time.sleep(0.15)
        self._send_keys("{ENTER}")
        return f"Opening Discord target {q} sir."

    def discord_quick_dm(self, user, message=""):
        """Open Discord DM to user and optionally send a message."""
        u = str(user or "").strip()
        msg = str(message or "").strip()
        if not u:
            return "Provide a Discord user or DM target sir."
        self.open_discord()
        time.sleep(0.45)
        self._send_keys("^k")
        time.sleep(0.2)
        self._set_clipboard(u)
        self._send_keys("^v")
        time.sleep(0.15)
        self._send_keys("{ENTER}")
        if msg:
            time.sleep(0.25)
            self._set_clipboard(msg)
            self._send_keys("^v")
            time.sleep(0.1)
            self._send_keys("{ENTER}")
            return f"Discord message sent to {u} sir."
        return f"Opened DM with {u} sir."

    # â”€â”€ Spotify â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def _spotify_running(self):
        return any("spotify" in p.name().lower() for p in psutil.process_iter(["name"]))

    def _launch_spotify_bg(self):
        exe = Path(os.environ.get("APPDATA", "")) / "Spotify" / "Spotify.exe"
        if exe.exists() and not self._spotify_running():
            subprocess.Popen([str(exe)], creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(4)

    def _minimize_spotify(self):
        ps = ("$p=Get-Process spotify -EA SilentlyContinue;if($p){"
              "Add-Type -TypeDefinition 'using System;using System.Runtime.InteropServices;"
              "public class W{[DllImport(\"user32.dll\")]public static extern bool ShowWindow(IntPtr h,int n);}'"
              ";$p|%{[W]::ShowWindow($_.MainWindowHandle,6)}}")
        subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps],
                         creationflags=subprocess.CREATE_NO_WINDOW)

    def spotify_search_play(self, query):
        import urllib.parse
        raw = (query or "").strip()
        q = raw.lower()
        if any(x in q for x in ["my favorite song", "my favourite song"]):
            fav = ""
            try:
                if hasattr(self, "_memory_ref") and self._memory_ref:
                    fav = str(self._memory_ref.data.get("preferences", {}).get("favorite_song", "")).strip()
            except Exception:
                fav = ""
            if fav:
                raw = fav
                q = raw.lower()
            else:
                return self.spotify_play_liked()

        if q in ["", "song", "a song", "some music", "music", "something", "anything", "play a song", "play music", "liked songs", "my liked songs"]:
            return self.spotify_play_liked()
        self._launch_spotify_bg()
        subprocess.Popen("start spotify:search:" + urllib.parse.quote(raw),
                         shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2)
        self._minimize_spotify()
        return "Playing " + raw + " on Spotify sir."

    def spotify_play_liked(self):
        """Open Spotify liked songs collection and start playback."""
        self._launch_spotify_bg()
        subprocess.Popen("start spotify:collection:tracks", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2)
        self._spotify_key(0xB3)  # play/pause media key
        time.sleep(0.4)
        self._spotify_key(0xB0)  # next track once to avoid stale paused item
        self._minimize_spotify()
        return "Playing your liked songs on Spotify sir."

    def _spotify_key(self, vk_code):
        """Send virtual key code directly via Windows API â€” works regardless of focus."""
        import tempfile as _tf
        # keybd_event approach â€” sends to whole system not just focused window
        script = (
            "Add-Type -TypeDefinition @\"\n"
            "using System;\n"
            "using System.Runtime.InteropServices;\n"
            "public class KB {\n"
            "    [DllImport(\"user32.dll\")]\n"
            "    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);\n"
            "    public static void Press(byte key) {\n"
            "        keybd_event(key, 0, 0, UIntPtr.Zero);\n"
            "        System.Threading.Thread.Sleep(50);\n"
            "        keybd_event(key, 0, 2, UIntPtr.Zero);\n"
            "    }\n"
            "}\n"
            "\"@ \n"
            "[KB]::Press(" + str(vk_code) + ")"
        )
        tmp = Path(_tf.gettempdir()) / "jvk.ps1"
        tmp.write_text(script, encoding="utf-8")
        subprocess.run(
            ["powershell", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", str(tmp)],
            capture_output=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW
        )

    def spotify_pause(self):
        """Toggle Spotify play/pause using VK_MEDIA_PLAY_PAUSE (0xB3)."""
        self._spotify_key(0xB3)
        return "Toggled Spotify sir."

    def spotify_next(self):
        """Skip to next track using VK_MEDIA_NEXT_TRACK (0xB0)."""
        self._spotify_key(0xB0)
        return "Next track sir."

    def spotify_prev(self):
        """Go to previous track using VK_MEDIA_PREV_TRACK (0xB1)."""
        self._spotify_key(0xB1)
        return "Previous track sir."

    # â”€â”€ Images â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def fetch_and_show_image(self, query, index=0):
        import urllib.parse, urllib.request, tempfile
        hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        try:
            q = urllib.parse.quote(query)
            html = urllib.request.urlopen(
                urllib.request.Request("https://www.bing.com/images/search?q=" + q, headers=hdrs),
                timeout=10).read().decode("utf-8", errors="ignore")
            urls = re.findall(r'murl&quot;:&quot;(https?://[^&]+)&quot;', html)
            if not urls:
                urls = re.findall(r'https?://[^\s<>"]+\.(?:jpg|jpeg|png)', html)
            if not urls:
                webbrowser.open("https://www.bing.com/images/search?q=" + q)
                return "Opened Bing Images for " + query + " sir."
            picked = urls[min(int(index), len(urls) - 1)]
            ext = ".png" if "png" in picked.lower() else ".jpg"
            tmp = Path(tempfile.gettempdir()) / ("jarvis_img" + ext)
            data = urllib.request.urlopen(
                urllib.request.Request(picked, headers=hdrs), timeout=12).read()
            if len(data) < 500: raise ValueError("too small")
            tmp.write_bytes(data)
            os.startfile(str(tmp))
            return "Image displayed sir."
        except Exception:
            webbrowser.open("https://www.bing.com/images/search?q=" + urllib.parse.quote(query))
            return "Opened Bing Images for " + query + " sir."

    def image_search_browser(self, query):
        webbrowser.open("https://www.bing.com/images/search?q=" + query.replace(" ", "+"))
        return "Opening Bing Images for " + query + " sir."

    # ── 3D Printing ──────────────────────────────────────────────────────

    _ORCASLICER_PATHS = [
        r"C:\Program Files\OrcaSlicer\orca-slicer.exe",
        r"C:\Program Files (x86)\OrcaSlicer\orca-slicer.exe",
        r"C:\Users\{user}\AppData\Local\OrcaSlicer\orca-slicer.exe",
        r"C:\Program Files\Bambu Studio\bambu-studio.exe",
    ]

    def _find_orcaslicer(self):
        """Locate OrcaSlicer or Bambu Studio executable."""
        import glob
        user = os.environ.get("USERNAME", "")
        for p in self._ORCASLICER_PATHS:
            resolved = p.replace("{user}", user)
            if Path(resolved).exists():
                return resolved
        try:
            out = subprocess.run(
                ["where", "/R", r"C:\Program Files", "orca-slicer.exe"],
                capture_output=True, text=True, timeout=8,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = [l.strip() for l in (out.stdout or "").splitlines() if l.strip()]
            if lines:
                return lines[0]
        except:
            pass
        for pattern in [r"C:\Program Files\*\orca-slicer.exe",
                        r"C:\Program Files (x86)\*\orca-slicer.exe"]:
            hits = glob.glob(pattern)
            if hits:
                return hits[0]
        return None

    def _search_3d_model(self, query):
        """Search for a 3D model on Thingiverse and Printables."""
        import urllib.parse, urllib.request, re as _re
        hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        results = []
        try:
            q = urllib.parse.quote(query + " stl")
            url = "https://www.thingiverse.com/search?q=" + q + "&type=things&sort=relevant"
            req = urllib.request.Request(url, headers=hdrs)
            html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8", errors="ignore")
            thing_ids = _re.findall(r'/thing:(\d+)', html)
            seen = set()
            for tid in thing_ids:
                if tid not in seen and len(results) < 3:
                    seen.add(tid)
                    results.append({
                        "source": "thingiverse", "id": tid,
                        "url": f"https://www.thingiverse.com/thing:{tid}",
                        "download_url": f"https://www.thingiverse.com/thing:{tid}/zip",
                        "name": f"Thingiverse #{tid}"
                    })
        except Exception as e:
            print(f"Thingiverse search error: {e}")
        try:
            q2 = urllib.parse.quote(query)
            url2 = "https://www.printables.com/search/models?q=" + q2
            req2 = urllib.request.Request(url2, headers=hdrs)
            html2 = urllib.request.urlopen(req2, timeout=12).read().decode("utf-8", errors="ignore")
            model_ids = _re.findall(r'/model/(\d+)-', html2)
            seen2 = set()
            for mid in model_ids:
                if mid not in seen2 and len(results) < 5:
                    seen2.add(mid)
                    slug_match = _re.search(r'/model/' + mid + r'-([^"\'<>\s]+)', html2)
                    name = slug_match.group(1).replace("-", " ").title() if slug_match else f"Printables #{mid}"
                    results.append({"source": "printables", "id": mid,
                                    "url": f"https://www.printables.com/model/{mid}", "name": name})
        except Exception as e:
            print(f"Printables search error: {e}")
        return results

    def _download_stl(self, model_info):
        """Download STL/3MF file for a model. Returns local path or None."""
        import urllib.request, urllib.parse, zipfile, re as _re
        hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        downloads_dir = Path.home() / "Downloads" / "jarvis_3d_models"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        source = model_info.get("source", "")
        model_url = model_info.get("url", "")
        try:
            req = urllib.request.Request(model_url, headers=hdrs)
            html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")
            file_links = _re.findall(r'href=["\']([^"\']*\.(?:stl|3mf)[^"\']*)["\']', html, _re.IGNORECASE)
            if source == "thingiverse":
                api_links = _re.findall(r'(https?://[^"\'<>\s]*download[^"\'<>\s]*)', html)
                file_links.extend(api_links)
                zip_url = model_info.get("download_url", "")
                if zip_url:
                    file_links.append(zip_url)
            if source == "printables":
                dl_links = _re.findall(r'(https?://[^"\'<>\s]*\.(?:stl|3mf|zip)[^"\'<>\s]*)', html)
                file_links.extend(dl_links)
            for link in file_links[:5]:
                if not link.startswith("http"):
                    from urllib.parse import urljoin
                    link = urljoin(model_url, link)
                try:
                    dl_req = urllib.request.Request(link, headers=hdrs)
                    data = urllib.request.urlopen(dl_req, timeout=30).read()
                    if len(data) < 500:
                        continue
                    safe_name = _re.sub(r'[^\w\-.]', '_', model_info.get("name", "model"))[:60]
                    if link.lower().endswith(".stl") or data[:5] == b"solid" or data[:80].find(b"solid") >= 0:
                        out_path = downloads_dir / f"{safe_name}.stl"
                        out_path.write_bytes(data)
                        return str(out_path)
                    elif link.lower().endswith(".3mf"):
                        out_path = downloads_dir / f"{safe_name}.3mf"
                        out_path.write_bytes(data)
                        return str(out_path)
                    elif link.lower().endswith(".zip") or data[:4] == b'PK\x03\x04':
                        tmp_zip = downloads_dir / "temp_model.zip"
                        tmp_zip.write_bytes(data)
                        try:
                            with zipfile.ZipFile(str(tmp_zip), 'r') as zf:
                                stl_files = [f for f in zf.namelist()
                                             if f.lower().endswith(('.stl', '.3mf'))
                                             and not f.startswith('__MACOSX')]
                                if stl_files:
                                    stl_files.sort(key=lambda f: zf.getinfo(f).file_size, reverse=True)
                                    chosen = stl_files[0]
                                    ext = Path(chosen).suffix
                                    out_path = downloads_dir / f"{safe_name}{ext}"
                                    with open(str(out_path), 'wb') as of:
                                        of.write(zf.read(chosen))
                                    return str(out_path)
                        except zipfile.BadZipFile:
                            pass
                        finally:
                            try: tmp_zip.unlink()
                            except: pass
                except Exception:
                    continue
        except Exception as e:
            print(f"Download error: {e}")
        return None

    def search_3d_model(self, query):
        """Search for a 3D printable model online."""
        _write_hud("thinking", tool="3d_search")
        results = self._search_3d_model(query)
        if not results:
            webbrowser.open("https://www.thingiverse.com/search?q=" + query.replace(" ", "+") + "&type=things")
            return f"No direct results found sir. Opened Thingiverse search for {query}."
        self._last_3d_results = results
        names = []
        for i, r in enumerate(results[:3]):
            names.append(f"{i+1}. {r['name']} from {r['source'].capitalize()}")
        return f"I found {len(results)} model{'s' if len(results) != 1 else ''} sir. {'. '.join(names)}. Shall I download and open the first one in OrcaSlicer?"

    def fetch_3d_model(self, query, auto_open=True):
        """Search, download, and open a 3D model in OrcaSlicer. Full pipeline."""
        _write_hud("thinking", text=f"Searching for {query} model", tool="3d_search")
        results = self._search_3d_model(query)
        if not results:
            webbrowser.open("https://www.thingiverse.com/search?q=" + query.replace(" ", "+") + "&type=things")
            return f"Could not find a downloadable model for {query} sir. Opened Thingiverse search instead."
        self._last_3d_results = results
        model = results[0]
        _write_hud("thinking", text=f"Downloading {model['name']}", tool="3d_download")
        stl_path = self._download_stl(model)
        if not stl_path:
            webbrowser.open(model["url"])
            return f"Found {model['name']} but could not auto-download sir. Opened the model page for manual download."
        self._last_downloaded_model = stl_path
        _write_hud("thinking", text=f"Downloaded to {Path(stl_path).name}", tool="3d_print")
        if not auto_open:
            return f"Model downloaded to {stl_path} sir. Say open it in OrcaSlicer or print it when ready."
        return self._open_in_orcaslicer(stl_path, model['name'])

    def _open_in_orcaslicer(self, stl_path, model_name="model"):
        """Open a model file in OrcaSlicer."""
        slicer = self._find_orcaslicer()
        if not slicer:
            try:
                os.startfile(stl_path)
                self._last_downloaded_model = stl_path
                return f"Found {model_name} sir. Opened the model file with system default. OrcaSlicer not found at default path. Would you like me to print it?"
            except:
                return f"Model downloaded to {stl_path} sir but I cannot find OrcaSlicer. Install it or tell me the path."
        try:
            subprocess.Popen([slicer, stl_path], creationflags=subprocess.CREATE_NO_WINDOW)
            self._last_downloaded_model = stl_path
            _write_hud("speaking", text=f"Opened {model_name} in OrcaSlicer")
            return f"I found a model sir. Opening {model_name} in OrcaSlicer now. Would you like me to print it?"
        except Exception as e:
            return f"Failed to open OrcaSlicer: {e}. Model saved at {stl_path} sir."

    def open_model_in_slicer(self, path=""):
        """Open a previously downloaded or specified model in OrcaSlicer."""
        if not path:
            path = getattr(self, '_last_downloaded_model', '')
        if not path or not Path(path).exists():
            return "No model file available sir. Search for one first."
        return self._open_in_orcaslicer(path, Path(path).stem)

    def print_3d_model(self, path=""):
        """Send the model currently open in OrcaSlicer to the printer."""
        if not path:
            path = getattr(self, '_last_downloaded_model', '')
        _write_hud("thinking", text="Sending to printer", tool="3d_print")
        try:
            self._ps(
                "Add-Type -AssemblyName Microsoft.VisualBasic; "
                "$procs = Get-Process | Where-Object {$_.MainWindowTitle -match 'OrcaSlicer|Bambu'} | Select -First 1; "
                "if ($procs) { [Microsoft.VisualBasic.Interaction]::AppActivate($procs.Id); Start-Sleep -Milliseconds 500 }"
            )
        except:
            pass
        import time as _t
        try:
            self._ps(
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.SendKeys]::SendWait('^r'); "
            )
            _write_hud("thinking", text="Slicing model", tool="3d_print")
            _t.sleep(3)
            self._ps(
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.SendKeys]::SendWait('^p'); "
            )
            _write_hud("speaking", text="Print job sent")
            return "Slicing complete. Print job sent to the printer sir."
        except Exception as e:
            return f"Could not send print command sir: {e}. Click Print in OrcaSlicer manually."

    def list_downloaded_models(self):
        """List previously downloaded 3D models."""
        models_dir = Path.home() / "Downloads" / "jarvis_3d_models"
        if not models_dir.exists():
            return "No models downloaded yet sir."
        files = [f for f in models_dir.iterdir()
                 if f.suffix.lower() in ('.stl', '.3mf', '.obj') and f.is_file()]
        if not files:
            return "No model files found sir."
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        names = [f"{f.name} ({f.stat().st_size // 1024}KB)" for f in files[:8]]
        return f"Downloaded models: {', '.join(names)} sir."

    def open_thingiverse(self, query=""):
        """Open Thingiverse in browser, optionally with search query."""
        if query:
            webbrowser.open("https://www.thingiverse.com/search?q=" + query.replace(" ", "+") + "&type=things")
            return f"Opening Thingiverse search for {query} sir."
        webbrowser.open("https://www.thingiverse.com")
        return "Opening Thingiverse sir."

    def open_printables(self, query=""):
        """Open Printables in browser, optionally with search query."""
        if query:
            webbrowser.open("https://www.printables.com/search/models?q=" + query.replace(" ", "+"))
            return f"Opening Printables search for {query} sir."
        webbrowser.open("https://www.printables.com")
        return "Opening Printables sir."



    # â”€â”€ Info â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def get_weather(self, city="auto"):
        try:
            r = requests.get("https://wttr.in/" + city + "?format=j1", timeout=5)
            d = r.json()["current_condition"][0]
            desc = d["weatherDesc"][0]["value"]
            return desc + ", " + d["temp_C"] + " Celsius, humidity " + d["humidity"] + " percent."
        except: return "Weather unavailable."

    def get_forecast(self, city="auto"):
        try:
            r = requests.get("https://wttr.in/" + city + "?format=j1", timeout=5)
            days = r.json()["weather"][:3]
            labels = ["Today", "Tomorrow", "Day after tomorrow"]
            parts = [labels[i] + ": " + d["hourly"][4]["weatherDesc"][0]["value"] + ", high " + d["maxtempC"] + " low " + d["mintempC"] + " Celsius" for i, d in enumerate(days)]
            return ". ".join(parts) + "."
        except: return "Forecast unavailable."

    def calculate(self, expression):
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return str(expression) + " equals " + str(result) + "."
        except Exception as e: return "Calculation error: " + str(e)

    def convert_units(self, value, from_unit, to_unit):
        conversions = {
            ("km","miles"):0.621371,("miles","km"):1.60934,
            ("kg","lbs"):2.20462,("lbs","kg"):0.453592,
            ("meters","feet"):3.28084,("feet","meters"):0.3048,
            ("celsius","fahrenheit"):lambda x:x*9/5+32,
            ("fahrenheit","celsius"):lambda x:(x-32)*5/9,
        }
        conv = conversions.get((from_unit.lower(), to_unit.lower()))
        if conv is None: return "I do not know how to convert " + from_unit + " to " + to_unit + " sir."
        result = conv(float(value)) if callable(conv) else float(value) * conv
        return str(value) + " " + from_unit + " is " + f"{result:.2f}" + " " + to_unit + " sir."

    def define_word(self, word):
        try:
            r = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word, timeout=5)
            meaning = r.json()[0]["meanings"][0]["definitions"][0]["definition"]
            return word + ": " + meaning
        except: return "Could not find a definition for " + word + " sir."

    def get_joke(self):
        try:
            r = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
            j = r.json()
            return j["setup"] + " ... " + j["punchline"]
        except: return "My joke database is offline sir."

    def get_fact(self):
        try:
            r = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en", timeout=5)
            return r.json()["text"]
        except: return "Fact database offline sir."

    def get_quote(self):
        try:
            r = requests.get("https://api.quotable.io/random", timeout=5)
            d = r.json()
            return d["content"] + " By " + d["author"] + "."
        except: return "Quote service unavailable sir."

    def get_crypto_price(self, coin="bitcoin"):
        try:
            r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=" + coin + "&vs_currencies=usd", timeout=5)
            price = r.json()[coin]["usd"]
            return coin.capitalize() + " is at " + f"{price:,.2f}" + " US dollars sir."
        except: return "Could not retrieve price for " + coin + "."

    def get_news(self, topic=""):
        query = topic.replace(" ", "+") if topic else "top+news"
        webbrowser.open("https://news.google.com/search?q=" + query)
        return "Opening news" + (" for " + topic if topic else "") + " sir."

    def get_stock_info(self, ticker):
        webbrowser.open("https://finance.yahoo.com/quote/" + ticker)
        return "Opening Yahoo Finance for " + ticker + " sir."

    def speed_test(self): webbrowser.open("https://www.speedtest.net"); return "Opening Speedtest sir."

    # â”€â”€ Notes / Todo â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def take_note(self, note):
        f = self.home / "jarvis_notes.txt"
        ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]")
        with open(f, "a", encoding="utf-8") as fp: fp.write(ts + " " + note + "\n")
        return "Note saved sir."

    def read_notes(self):
        f = self.home / "jarvis_notes.txt"
        if not f.exists(): return "No notes sir."
        lines = f.read_text(encoding="utf-8").strip().split("\n")
        return "You have " + str(len(lines)) + " notes. Latest: " + ". ".join(lines[-3:])

    def clear_notes(self):
        (self.home / "jarvis_notes.txt").write_text("", encoding="utf-8")
        return "Notes cleared sir."

    def search_notes(self, keyword):
        f = self.home / "jarvis_notes.txt"
        if not f.exists(): return "No notes found."
        matches = [l for l in f.read_text(encoding="utf-8").split("\n") if keyword.lower() in l.lower()]
        return "Found " + str(len(matches)) + " notes: " + ". ".join(matches[:3]) if matches else "No notes about " + keyword + "."

    def add_to_todo(self, task):
        f = self.home / "jarvis_todo.txt"
        with open(f, "a", encoding="utf-8") as fp: fp.write("[ ] " + task + "\n")
        return "Added to your list: " + task + " sir."

    def read_todo(self):
        f = self.home / "jarvis_todo.txt"
        if not f.exists(): return "Your list is empty sir."
        pending = [l for l in f.read_text(encoding="utf-8").split("\n") if l.startswith("[ ]")]
        return str(len(pending)) + " pending tasks: " + ". ".join(pending[:5]) if pending else "All tasks complete sir."

    def complete_todo(self, task_number):
        f = self.home / "jarvis_todo.txt"
        if not f.exists(): return "No list found."
        lines = f.read_text(encoding="utf-8").split("\n")
        idx = int(task_number) - 1
        if 0 <= idx < len(lines):
            lines[idx] = lines[idx].replace("[ ]", "[x]", 1)
            f.write_text("\n".join(lines), encoding="utf-8")
            return "Task " + task_number + " marked complete sir."
        return "Task number out of range."

    # â”€â”€ Reminders â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def set_reminder(self, message, seconds):
        def _remind():
            time.sleep(int(seconds))
            print(f"\n{Fore.YELLOW}REMINDER: {message}{Style.RESET_ALL}")
            if self._reminder_cb: self._reminder_cb("Reminder sir: " + message)
        threading.Thread(target=_remind, daemon=True).start()
        m = int(seconds) // 60
        return "Reminder set for " + (str(m) + " minutes" if m >= 1 else str(seconds) + " seconds") + ": " + message

    def set_alarm(self, hour, minute, message="Alarm"):
        now = datetime.datetime.now()
        alarm = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        if alarm <= now: alarm += datetime.timedelta(days=1)
        return self.set_reminder(message, int((alarm - now).total_seconds()))

    def start_timer(self, seconds, label="Timer"):
        return self.set_reminder(label + " complete", int(seconds))

    # â”€â”€ Clipboard / Screenshot â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def get_clipboard(self):
        r = subprocess.run("powershell Get-Clipboard", shell=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return r.stdout.strip() or "Clipboard is empty."

    def set_clipboard_text(self, text):
        self._set_clipboard(text); return "Copied to clipboard sir."


    # ══════════════════════════════════════════════════════════════
    # SCREEN VISION — screenshot + send to vision LLM
    # ══════════════════════════════════════════════════════════════

    def _vision_query(self, image_path, question, max_tokens=300):
        """Send an image + question to a vision-capable LLM. Returns the answer text."""
        import base64
        cfg = load_config()

        # Read and encode image
        img_path = Path(image_path)
        if not img_path.exists():
            return "Image not found: " + str(image_path)
        with open(str(img_path), "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")

        # Determine image MIME type
        ext = img_path.suffix.lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "gif": "image/gif", "webp": "image/webp", "bmp": "image/bmp"}.get(ext.lstrip("."), "image/png")

        # Vision model config — defaults to LM Studio localhost
        vision_url = cfg.get("vision_model_url", "http://localhost:1234/v1")
        vision_model = cfg.get("vision_model_name", "gemma-3-4b-it")
        vision_key = cfg.get("vision_model_api_key", "lm-studio")

        # Build OpenAI-compatible vision request
        try:
            import openai as _oai
            client = _oai.OpenAI(base_url=vision_url, api_key=vision_key)
            resp = client.chat.completions.create(
                model=vision_model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
                        {"type": "text", "text": question},
                    ]
                }],
                max_tokens=int(max_tokens),
                temperature=0.2,
            )
            raw = resp.choices[0].message.content or ""
            # Strip chain-of-thought if present
            raw = re.sub(r"<think>[\s\S]*?</think>", "", raw).strip()
            return raw
        except Exception as e:
            return f"Vision query failed: {e}"

    def screen_look(self, question="What is on the screen?"):
        """Take a screenshot and ask a vision LLM about it. Use for any question about what's visible."""
        _write_hud("thinking", text="Looking at screen", tool="vision")
        import tempfile
        ss_path = Path(tempfile.gettempdir()) / "jarvis_vision_ss.png"

        # Take screenshot via pyautogui if available, else PowerShell
        try:
            import pyautogui
            img = pyautogui.screenshot()
            img.save(str(ss_path))
        except Exception:
            script = ("Add-Type -AssemblyName System.Windows.Forms;"
                      "$s=[System.Windows.Forms.Screen]::PrimaryScreen;"
                      "$b=New-Object System.Drawing.Bitmap($s.Bounds.Width,$s.Bounds.Height);"
                      "$g=[System.Drawing.Graphics]::FromImage($b);"
                      "$g.CopyFromScreen($s.Bounds.Location,[System.Drawing.Point]::Empty,$s.Bounds.Size);"
                      "$b.Save('" + str(ss_path) + "')")
            subprocess.run(["powershell", "-Command", script], capture_output=True,
                          creationflags=subprocess.CREATE_NO_WINDOW)

        if not ss_path.exists():
            return "Could not take screenshot sir."

        answer = self._vision_query(str(ss_path), question)
        _write_hud("speaking", text=answer[:80])
        return answer

    def screen_look_region(self, x, y, width, height, question="What is in this region?"):
        """Screenshot a specific region and ask the vision LLM about it."""
        _write_hud("thinking", text="Looking at region", tool="vision")
        import tempfile
        ss_path = Path(tempfile.gettempdir()) / "jarvis_vision_region.png"
        try:
            import pyautogui
            img = pyautogui.screenshot(region=(int(x), int(y), int(width), int(height)))
            img.save(str(ss_path))
        except Exception as e:
            return f"Region capture failed: {e}"

        answer = self._vision_query(str(ss_path), question)
        return answer

    def analyze_image(self, image_path, question="Describe this image in detail."):
        """Analyze any image file with the vision LLM."""
        p = self._r(image_path)
        if not p.exists():
            return f"Image not found: {image_path} sir."
        _write_hud("thinking", text="Analyzing image", tool="vision")
        return self._vision_query(str(p), question)

    def take_screenshot(self, filename=""):
        if not filename:
            filename = "screenshot_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        path = self.workspace / filename
        script = ("Add-Type -AssemblyName System.Windows.Forms;"
                  "$s=[System.Windows.Forms.Screen]::PrimaryScreen;"
                  "$b=New-Object System.Drawing.Bitmap($s.Bounds.Width,$s.Bounds.Height);"
                  "$g=[System.Drawing.Graphics]::FromImage($b);"
                  "$g.CopyFromScreen($s.Bounds.Location,[System.Drawing.Point]::Empty,$s.Bounds.Size);"
                  "$b.Save('" + str(path) + "')")
        subprocess.run(["powershell", "-Command", script], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return "Screenshot saved as " + filename + " sir."

    # â”€â”€ Keyboard / Paste â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def paste_code(self, language="python", description=""):
        import anthropic as _ant
        language = str(language or "python").strip() or "python"
        description = str(description or "").strip()
        if not description:
            clip = self.get_clipboard()
            if clip and not str(clip).lower().startswith("clipboard is empty"):
                description = "Continue or complete this code:\n" + str(clip)[:1200]
            else:
                return "Code generator needs a task description sir. Say paste code and what to build."
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=2048,
            messages=[{"role":"user","content":"Write " + language + " code for: " + description + ". Return ONLY the raw code, no markdown, no explanation."}]
        )
        code = resp.content[0].text.strip()
        code = re.sub(r"```[a-zA-Z]*\n?", "", code).replace("```", "").strip()
        self._set_clipboard(code)
        time.sleep(0.5)
        self._send_keys("^v")
        return str(len(code.splitlines())) + " lines of " + language + " pasted sir."

    def fix_code_in_clipboard(self):
        import anthropic as _ant
        code = self.get_clipboard()
        if not code or len(code) < 5: return "Clipboard is empty sir."
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=2048,
            messages=[{"role":"user","content":"Fix any bugs. Return ONLY fixed code, no markdown: " + code}]
        )
        fixed = re.sub(r"```[a-zA-Z]*\n?", "", resp.content[0].text.strip()).replace("```", "").strip()
        self._set_clipboard(fixed)
        time.sleep(0.5)
        self._send_keys("^v")
        return "Fixed code pasted back sir."

    def explain_code_in_clipboard(self):
        import anthropic as _ant
        code = self.get_clipboard()
        if not code: return "Clipboard is empty sir."
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=400,
            messages=[{"role":"user","content":"Explain this code in 2-3 spoken sentences, no markdown: " + code[:2000]}]
        )
        return resp.content[0].text.strip()

    def press_key(self, key):
        key_map = {
            "enter":"{ENTER}","escape":"{ESC}","tab":"{TAB}","backspace":"{BACKSPACE}",
            "ctrl+c":"^c","ctrl+v":"^v","ctrl+z":"^z","ctrl+s":"^s","ctrl+a":"^a",
            "alt+tab":"%{TAB}","alt+f4":"%{F4}",
        }
        self._send_keys(key_map.get(key.lower(), key))
        return "Pressed " + key + " sir."

    def save_current_file(self): self._send_keys("^s"); return "Save command sent sir."
    def undo(self): self._send_keys("^z"); return "Undo performed sir."
    def switch_window(self): self._send_keys("%{TAB}"); return "Switched window sir."

    # â”€â”€ Web / Research â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def summarize_url(self, url):
        import anthropic as _ant, urllib.request
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", errors="ignore")
            text = re.sub(r"<[^>]+>", " ", html)
            text = re.sub(r"\s+", " ", text).strip()[:3000]
            cfg = load_config()
            client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001", max_tokens=300,
                messages=[{"role":"user","content":"Summarize in 2-3 spoken sentences, no markdown: " + text}]
            )
            return resp.content[0].text.strip()
        except Exception as e: return "Could not summarize: " + str(e)

    def translate_text(self, text, target_language):
        import anthropic as _ant
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=500,
            messages=[{"role":"user","content":"Translate to " + target_language + ". Return only translation: " + text}]
        )
        return resp.content[0].text.strip()

    # â”€â”€ Power â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def shutdown_pc(self, delay=60): subprocess.run("shutdown /s /t " + str(delay), shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Shutting down in " + str(delay) + " seconds sir."
    def restart_pc(self, delay=60): subprocess.run("shutdown /r /t " + str(delay), shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Restarting in " + str(delay) + " seconds sir."
    def cancel_shutdown(self): subprocess.run("shutdown /a", shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Shutdown cancelled sir."
    def sleep_pc(self): subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Going to sleep sir."
    def lock_pc(self): subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Workstation locked sir."
    def mute_volume(self): self._spotify_key(0xAD); return "Volume muted sir."
    def volume_up(self): self._spotify_key(0xAF); return "Volume increased sir."
    def volume_down(self): self._spotify_key(0xAE); return "Volume decreased sir."
    def empty_recycle_bin(self): self._ps("Clear-RecycleBin -Force"); return "Recycle bin emptied sir."
    def check_for_updates(self): subprocess.Popen("ms-settings:windowsupdate", shell=True, creationflags=subprocess.CREATE_NO_WINDOW); return "Opening Windows Update sir."
    def flush_dns(self): return self._sh("ipconfig /flushdns")

    def list_wifi_networks(self):
        r = self._sh("netsh wlan show networks")
        ssids = [l.split(":")[1].strip() for l in r.split("\n") if "SSID" in l and "BSSID" not in l]
        return "Found " + str(len(ssids)) + " networks: " + ", ".join(ssids[:8]) if ssids else "No networks found."

    def get_wifi_password(self, ssid):
        r = self._sh('netsh wlan show profile name="' + ssid + '" key=clear')
        if "Key Content" in r:
            pwd = [l for l in r.split("\n") if "Key Content" in l]
            return "Password for " + ssid + ": " + pwd[0].split(":")[-1].strip() if pwd else "Not found."
        return "Profile " + ssid + " not found."

    # â”€â”€ Dev â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def run_python_file(self, path):
        p = self._r(path)
        result = self._sh(f'"{sys.executable}" "{p}"')
        return "Ran " + p.name + ". Output: " + result[:200]

    def create_python_script(self, path, code):
        return self.create_file(path if path.endswith(".py") else path + ".py", code)

    def git_status(self): return self._sh("git status")
    def git_commit(self, message): self._sh("git add ."); return self._sh('git commit -m "' + message + '"')
    def git_push(self): return self._sh("git push")

    def roast_process(self, process_name):
        import anthropic as _ant
        cpu = 0
        for p in psutil.process_iter(["name","cpu_percent"]):
            if process_name.lower() in p.info["name"].lower():
                cpu = p.info["cpu_percent"]; break
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=100,
            messages=[{"role":"user","content":"As Jarvis, roast the process '" + process_name + "' using " + str(cpu) + "% CPU in one witty spoken sentence, no markdown."}]
        )
        return resp.content[0].text.strip()

    # â”€â”€ Self-Modification â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    # â”€â”€ Project Management â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def create_project(self, name, description="", language="", location=""):
        import json as _j, re as _re
        name = _re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name.replace("\n"," ")).strip() or "Unnamed"
        base = (Path(location.strip()) / name) if (location and any(c in location for c in [":\\",":/","\\","/"])) else (self.workspace / name)
        print(f"[create_project] name={repr(name)} base={repr(str(base))}")
        base.mkdir(parents=True, exist_ok=True)
        lang = language.lower()
        if "python" in lang:
            for d in ["src","tests","docs"]: (base/d).mkdir(exist_ok=True)
            (base/"src"/"__init__.py").write_text("", encoding="utf-8")
            (base/"requirements.txt").write_text("", encoding="utf-8")
            (base/"main.py").write_text('def main():\n    pass\n\nif __name__ == "__main__":\n    main()\n', encoding="utf-8")
            (base/".gitignore").write_text("__pycache__/\n*.pyc\n.env\nvenv/\n", encoding="utf-8")
        elif any(x in lang for x in ["javascript","js","react","node","web","typescript"]):
            for d in ["src","public","assets"]: (base/d).mkdir(exist_ok=True)
            (base/"src"/"index.js").write_text("// "+name+"\n", encoding="utf-8")
            (base/".gitignore").write_text("node_modules/\n.env\ndist/\n", encoding="utf-8")
        elif "rust" in lang:
            (base/"src").mkdir(exist_ok=True)
            (base/"src"/"main.rs").write_text('fn main() { println!("\'"+name+"\'"); }\n', encoding="utf-8")
        elif any(x in lang for x in ["c++","cpp","c plus plus"]):
            for d in ["src","include","build"]: (base/d).mkdir(exist_ok=True)
            (base/"src"/"main.cpp").write_text('#include<iostream>\nint main(){std::cout<<"\'"+name+"\'";return 0;}\n', encoding="utf-8")
        else:
            for d in ["src","docs","tests","assets"]: (base/d).mkdir(exist_ok=True)
        readme = "# "+name+"\n\n"+(description+"\n\n" if description else "")+("**Stack:** "+language+"\n\n" if language else "")+"## Getting Started\n"
        (base/"README.md").write_text(readme, encoding="utf-8")
        # Git init â€” run each command separately so && doesn't fail on Windows
        # Git init â€” use Popen with explicit cwd to handle spaces in path
        try:
            _git_env = {"GIT_TERMINAL_PROMPT": "0"}
            subprocess.run(["git","init"], cwd=str(base), capture_output=True, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["git","add","."], cwd=str(base), capture_output=True, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["git","commit","-m","Initial commit"], cwd=str(base), capture_output=True, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception: pass  # git optional
        rf = self.workspace/".jarvis_projects.json"
        reg = {}
        try: reg = _j.loads(rf.read_text(encoding="utf-8")) if rf.exists() else {}
        except: pass
        reg[name] = {"path":str(base),"description":description,"language":language,
                     "created":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"status":"active"}
        rf.write_text(_j.dumps(reg,indent=2), encoding="utf-8")
        # Sync new project into ontology graph
        try:
            if hasattr(self, "_memory_ref"):
                self._memory_ref.graph.add_project(name, language, description, str(base))
        except: pass
        return "Project "+name+" created sir."

    def list_projects(self):
        import json as _j
        f = self.workspace/".jarvis_projects.json"
        if not f.exists(): return "No projects on record sir."
        try: reg = _j.loads(f.read_text(encoding="utf-8"))
        except: return "Could not read projects sir."
        if not reg: return "No projects on record sir."
        return "Your projects: "+", ".join(k+" ("+v.get("language","?")+")" for k,v in reg.items())+"."

    def get_project_info(self, name):
        import json as _j
        f = self.workspace/".jarvis_projects.json"
        if not f.exists(): return "No projects on record sir."
        reg = _j.loads(f.read_text(encoding="utf-8"))
        for k,v in reg.items():
            if name.lower() in k.lower():
                return k+". "+v.get("description","No description.")+" Language: "+v.get("language","unknown")+". Status: "+v.get("status","active")+"."
        return "Project "+name+" not found sir."

    def open_project(self, name):
        import json as _j
        f = self.workspace/".jarvis_projects.json"
        if not f.exists(): return "No projects on record sir."
        reg = _j.loads(f.read_text(encoding="utf-8"))
        for k,v in reg.items():
            if name.lower() in k.lower():
                subprocess.Popen('code "'+v["path"]+'"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                return "Opening "+k+" in VS Code sir."
        return "Project "+name+" not found sir."

    def update_project_status(self, name, status):
        import json as _j
        f = self.workspace/".jarvis_projects.json"
        if not f.exists(): return "No projects on record sir."
        reg = _j.loads(f.read_text(encoding="utf-8"))
        for k in reg:
            if name.lower() in k.lower():
                reg[k]["status"] = status
                f.write_text(_j.dumps(reg,indent=2), encoding="utf-8")
                return k+" marked as "+status+" sir."
        return "Project "+name+" not found sir."


    def execute_protocol(self,protocol_name):
        pname=protocol_name.lower().strip()
        if pname not in PROTOCOLS: return "Unknown protocol sir. Available: "+", ".join(PROTOCOLS.keys())+"."
        title,desc=PROTOCOLS[pname]; extra=""
        try:
            if pname=="lockdown": self.lock_pc()
            elif pname=="cleanup": self.flush_dns(); self.empty_recycle_bin()
            elif pname=="alpha": extra=" "+self.system_info()
            elif pname in ["stealth","blackout"]: self._sh('powershell "(New-Object -ComObject Shell.Application).MinimizeAll()"'); self.mute_volume()
            elif pname=="focus": self._sh('powershell "(New-Object -ComObject Shell.Application).MinimizeAll()"')
            elif pname=="omega": self.shutdown_pc(60)
            elif pname=="reboot": self.restart_pc(30)
            elif pname=="nightwatch": self.set_alarm(8,0,"Good morning sir."); self.sleep_pc()
            elif pname=="deploy": extra=" "+self.git_push()
            elif pname=="recovery": self.flush_dns()
        except: pass
        return title+" engaged. "+desc+extra


    # â”€â”€ Skills â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def list_skills(self):
        """List all available skill scripts."""
        sd = Path(self._get_skills_dir())
        if not sd.exists():
            sd.mkdir(parents=True, exist_ok=True)
            return "Skills folder created at " + str(sd) + ". No skills yet sir."
        skills = list(sd.glob("*.py")) + list(sd.glob("*.ps1")) + list(sd.glob("*.bat"))
        if not skills:
            return "No skills installed yet sir. Skills live in " + str(sd) + "."
        names = [s.stem for s in skills]
        return "Available skills: " + ", ".join(names) + "."

    def run_skill(self, name, args=""):
        """Run a skill script by name."""
        sd = Path(self._get_skills_dir())
        # Find by name (try .py, .ps1, .bat)
        for ext in [".py", ".ps1", ".bat", ".cmd"]:
            p = sd / (name + ext)
            if p.exists():
                if ext == ".py":
                    result = self._sh(f'"{sys.executable}" "{p}" {args}'.strip())
                elif ext == ".ps1":
                    result = self._sh(f'powershell -ExecutionPolicy Bypass -File "{p}" {args}'.strip())
                else:
                    result = self._sh(f'"{p}" {args}'.strip())
                return f"Skill {name} completed. Output: " + result[:200] if result else f"Skill {name} ran sir."
        return f"Skill '{name}' not found sir. Say list skills to see what is available."

    def create_skill(self, name, description, code):
        """Save a new skill script to the skills folder."""
        sd = Path(self._get_skills_dir())
        sd.mkdir(parents=True, exist_ok=True)
        # Add .py extension if missing
        fname = name if "." in name else name + ".py"
        p = sd / fname
        # Add header comment
        header = f'''# Skill: {name}
# Description: {description}
# Created: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
# Run with: jarvis run skill {name}

'''
        p.write_text(header + code, encoding="utf-8")
        return f"Skill '{name}' saved to skills folder sir."

    def delete_skill(self, name):
        """Delete a skill from the skills folder."""
        sd = Path(self._get_skills_dir())
        for ext in [".py", ".ps1", ".bat", ".cmd", ""]:
            p = sd / (name + ext)
            if p.exists():
                p.unlink()
                return f"Skill '{name}' deleted sir."
        return f"Skill '{name}' not found sir."

    def read_skill(self, name):
        """Read the source of a skill."""
        sd = Path(self._get_skills_dir())
        for ext in [".py", ".ps1", ".bat", ".cmd"]:
            p = sd / (name + ext)
            if p.exists():
                return p.read_text(encoding="utf-8")[:1000]
        return f"Skill '{name}' not found sir."


    def _init_skills_dir(self):
        """Create skills directory with example skills on first run."""
        sd = Path(self._get_skills_dir())
        if sd.exists(): return
        sd.mkdir(parents=True, exist_ok=True)
        # Write a sample skill
        sample = sd / "system_report.py"
        sample.write_text(
            '''# Skill: system_report
# Description: Print a quick system status report
import psutil, datetime
cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
disk = psutil.disk_usage("/")
print(f"System Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"CPU: {cpu}%  RAM: {ram.percent}%  Disk: {disk.percent}%")
print(f"RAM used: {ram.used//1024**3}GB / {ram.total//1024**3}GB")
''', encoding="utf-8")
    def _get_skills_dir(self):
        try:
            cfg = load_config()
            return cfg.get("skills_dir", str(Path.home() / "Desktop" / "jarvis_skills"))
        except:
            return str(Path.home() / "Desktop" / "jarvis_skills")


    def defender_quick_scan(self):
        """Trigger Windows Defender quick scan in background."""
        ps = (
            "Start-MpScan -ScanType QuickScan -AsJob | Out-Null; "
            "Write-Output 'Scan initiated'"
        )
        result = self._ps(ps)
        return "Quick scan initiated sir. I will report any threats when complete."

    def defender_full_scan(self):
        """Trigger Windows Defender full scan."""
        ps = "Start-MpScan -ScanType FullScan -AsJob | Out-Null; Write-Output 'Full scan initiated'"
        self._ps(ps)
        return "Full system scan initiated sir. This will take some time."

    def defender_get_threats(self):
        """Get current detected threats from Windows Defender."""
        ps = (
            "Get-MpThreat | Select-Object -Property ThreatName,SeverityID,ActionSuccess,Resources "
            "| ConvertTo-Json -Compress"
        )
        result = self._ps(ps)
        if not result or result.strip() in ["", "null", "Done."]:
            return "No active threats detected sir. System appears clean."
        try:
            import json as _j
            data = _j.loads(result)
            if isinstance(data, dict): data = [data]
            if not data: return "No threats on record sir."
            severity_map = {1:"low",2:"moderate",4:"high",5:"severe"}
            parts = []
            for t in data[:6]:
                name = t.get("ThreatName","Unknown")
                sev  = severity_map.get(t.get("SeverityID",1),"unknown")
                parts.append(f"{name} ({sev} severity)")
            return f"Defender found {len(data)} threat{'s' if len(data)>1 else ''}: " + ". ".join(parts) + "."
        except:
            return "Defender returned data but I could not parse it sir. Check Windows Security manually."

    def defender_threat_history(self):
        """Get threat detection history."""
        ps = (
            "Get-MpThreatDetection | Select-Object -First 5 "
            "-Property ThreatID,ActionSuccess,DetectionSourceTypeID,Timestamp "
            "| ConvertTo-Json -Compress"
        )
        result = self._ps(ps)
        if not result or "null" in result:
            return "No threat history found sir. That is a good sign."
        return "Threat history retrieved sir. " + result[:200]

    def defender_update_signatures(self):
        """Update Windows Defender signatures."""
        self._ps("Update-MpSignature -AsJob | Out-Null")
        return "Defender signature update initiated sir."

    def defender_status(self):
        """Get Windows Defender status."""
        ps = (
            "Get-MpComputerStatus | Select-Object "
            "AntivirusEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated,"
            "QuickScanStartTime,FullScanStartTime | ConvertTo-Json -Compress"
        )
        result = self._ps(ps)
        try:
            import json as _j
            d = _j.loads(result)
            av  = "active" if d.get("AntivirusEnabled") else "DISABLED"
            rtp = "active" if d.get("RealTimeProtectionEnabled") else "DISABLED"
            sig = str(d.get("AntivirusSignatureLastUpdated","unknown"))[:10]
            return f"Defender status: antivirus {av}, real-time protection {rtp}, signatures last updated {sig}."
        except:
            return "Could not retrieve Defender status sir."


    # â”€â”€ Google Calendar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def _gcal_service(self):
        """Get authenticated Google Calendar service."""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            import pickle as _pk, os as _os
        except ImportError:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install",
                     "google-api-python-client", "google-auth-oauthlib", "google-auth-httplib2", "-q"],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                from google.oauth2.credentials import Credentials
                from google_auth_oauthlib.flow import InstalledAppFlow
                from google.auth.transport.requests import Request
                from googleapiclient.discovery import build
                import pickle as _pk, os as _os
            except Exception:
                return None, "Google Calendar libraries not installed. Run setup_google_calendar.py sir."

        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        desktop = Path.home() / "Desktop"
        creds_file = desktop / "credentials.json"
        if not creds_file.exists():
            alt = desktop / "credentials_1.json"
            if alt.exists():
                try:
                    creds_file.write_text(alt.read_text(encoding="utf-8"), encoding="utf-8")
                except:
                    creds_file = alt
        token_file  = Path.home() / ".jarvis_gcal_token.pickle"
        old_token_file = Path.home() / ".jarvis_gcal_token_1.pkl"

        if not creds_file.exists():
            return None, "credentials.json not found on Desktop. Run setup_google_calendar.py sir."

        creds = None
        if token_file.exists():
            with open(token_file, "rb") as f2:
                creds = _pk.load(f2)
        elif old_token_file.exists():
            try:
                with open(old_token_file, "rb") as f2:
                    creds = _pk.load(f2)
                with open(token_file, "wb") as f3:
                    _pk.dump(creds, f3)
            except:
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, "wb") as f2:
                _pk.dump(creds, f2)

        service = build("calendar", "v3", credentials=creds)
        return service, None

    def get_todays_events(self):
        """Get today's calendar events."""
        svc, err = self._gcal_service()
        if err: return err
        import datetime as _dt
        now = _dt.datetime.now().astimezone()
        start = now.replace(hour=0,minute=0,second=0,microsecond=0).isoformat()
        end   = now.replace(hour=23,minute=59,second=59,microsecond=0).isoformat()
        result = svc.events().list(calendarId="primary",
            timeMin=start, timeMax=end, singleEvents=True,
            orderBy="startTime", timeZone="America/New_York").execute()
        events = result.get("items",[])
        if not events: return "Nothing on the calendar today sir."
        parts = []
        for e in events[:5]:
            name  = e.get("summary","Unnamed")
            start2= e.get("start",{}).get("dateTime",e.get("start",{}).get("date",""))
            if "T" in start2:
                t = start2.split("T")[1][:5]
                parts.append(f"{name} at {t}")
            else:
                parts.append(name)
        return f"Today you have {len(events)} event{'s' if len(events)>1 else ''}: " + ", ".join(parts) + "."

    def get_upcoming_events(self, days=7):
        """Get upcoming calendar events."""
        svc, err = self._gcal_service()
        if err: return err
        import datetime as _dt
        now = _dt.datetime.now().astimezone()
        end = (now + _dt.timedelta(days=int(days))).isoformat()
        result = svc.events().list(calendarId="primary",
            timeMin=now.isoformat(), timeMax=end,
            singleEvents=True, orderBy="startTime",
            maxResults=8, timeZone="America/New_York").execute()
        events = result.get("items",[])
        if not events: return f"Nothing in the next {days} days sir."
        parts = []
        for e in events[:6]:
            name  = e.get("summary","Unnamed")
            start2= e.get("start",{}).get("dateTime",e.get("start",{}).get("date",""))
            day   = start2.split("T")[0] if "T" in start2 else start2
            import datetime as _dt2
            try:
                d = _dt2.date.fromisoformat(day)
                day_name = d.strftime("%A")
            except: day_name = day
            parts.append(f"{name} on {day_name}")
        return "Coming up: " + ". ".join(parts) + "."

    def add_calendar_event(self, title, date_str, time_str="09:00", duration_hours=1):
        """Add an event to Google Calendar."""
        svc, err = self._gcal_service()
        if err: return err
        import datetime as _dt
        try:
            start_dt = _dt.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").astimezone()
            end_dt   = start_dt + _dt.timedelta(hours=float(duration_hours))
            tz_name = "America/New_York"
            event = {
                "summary": title,
                "start": {"dateTime": start_dt.isoformat(), "timeZone": tz_name},
                "end":   {"dateTime": end_dt.isoformat(),   "timeZone": tz_name},
            }
            svc.events().insert(calendarId="primary", body=event).execute()
            return f"Event '{title}' added to your calendar sir."
        except Exception as e:
            return f"Could not add event sir: {e}"

    def check_recent_events(self):
        """Check for events that just ended â€” used for post-event check-in."""
        svc, err = self._gcal_service()
        if err: return []
        import datetime as _dt
        now = _dt.datetime.utcnow()
        ago = (now - _dt.timedelta(hours=6)).isoformat() + "Z"
        result = svc.events().list(calendarId="primary",
            timeMin=ago, timeMax=now.isoformat()+"Z",
            singleEvents=True, orderBy="startTime").execute()
        events = result.get("items",[])
        # Filter: only events that look like real events (not all-day, not class-related)
        CLASS_WORDS = ["class","lecture","tutorial","lab","assignment","due","homework","exam","test","quiz"]
        real_events = []
        for e in events:
            name = e.get("summary","").lower()
            if e.get("start",{}).get("dateTime"):  # has a time (not all-day)
                if not any(w in name for w in CLASS_WORDS):
                    real_events.append(e.get("summary","Event"))
        return real_events


    # â”€â”€ Microsoft Defender â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def defender_quick_scan(self):
        """Initiate a Windows Defender quick scan in the background."""
        ps = "Start-MpScan -ScanType QuickScan"
        result = self._ps(ps)
        return "Quick scan initiated sir. I will monitor and report any threats."

    def defender_full_scan(self):
        """Initiate a full Windows Defender scan."""
        ps = "Start-MpScan -ScanType FullScan"
        self._ps(ps)
        return "Full system scan initiated sir. This will take some time. I will alert you to anything found."

    def defender_get_threats(self):
        """Get list of detected threats from Defender."""
        ps = (
            "Get-MpThreatDetection | Select-Object -First 10 | "
            "ForEach-Object { $_.ThreatName + ' | Severity: ' + $_.ThreatSeverity + ' | Path: ' + $_.Resources }"
        )
        result = self._ps(ps)
        if not result or result.strip() == "" or "Error" in result:
            return "No threats detected sir. System appears clean."
        lines = [l.strip() for l in result.strip().split("\n") if l.strip()][:5]
        return f"Found {len(lines)} threat detections sir. " + ". ".join(lines[:3])

    def defender_remove_threats(self):
        """Attempt to remove/quarantine detected threats and run a follow-up quick scan."""
        ps = (
            "$attempted=0; $removed=0; $err=''; "
            "try { $threats=Get-MpThreat -ErrorAction Stop } catch { $threats=@(); $err += $_.Exception.Message + '; ' }; "
            "if($threats){ "
            " foreach($t in $threats){ "
            "  $attempted++; "
            "  try { Remove-MpThreat -ThreatID $t.ThreatID -ErrorAction Stop | Out-Null; $removed++ } "
            "  catch { $err += $_.Exception.Message + '; ' } "
            " } "
            "} "
            "$scan='ok'; "
            "try { Start-MpScan -ScanType QuickScan -ErrorAction Stop | Out-Null } "
            "catch { $scan='failed:' + $_.Exception.Message }; "
            "Write-Output ('ATTEMPTED=' + $attempted + ';REMOVED=' + $removed + ';SCAN=' + $scan + ';ERR=' + $err)"
        )
        out = (self._ps(ps) or "").strip()
        attempted = 0
        removed = 0
        scan = "unknown"
        err = ""
        try:
            m = re.search(r"ATTEMPTED=(\d+);REMOVED=(\d+);SCAN=([^;]+);ERR=(.*)$", out)
            if m:
                attempted = int(m.group(1))
                removed = int(m.group(2))
                scan = m.group(3).strip()
                err = m.group(4).strip()
        except Exception:
            pass
        if removed > 0:
            return f"Threat remediation executed sir. Removed or quarantined {removed} of {attempted} detected threat item{'s' if attempted != 1 else ''}. Quick scan status: {scan}."
        if attempted > 0 and removed == 0:
            if err:
                clean_err = re.sub(r"\s*;\s*$", "", err).strip()
                return f"I attempted to remove {attempted} threat item{'s' if attempted != 1 else ''} but Defender blocked removal: {clean_err[:180]}. Run Jarvis as administrator and repeat remove threats."
            return f"I detected {attempted} threat item{'s' if attempted != 1 else ''}, but none were removed. Quick scan status: {scan}."
        if err:
            clean_err = re.sub(r"\s*;\s*$", "", err).strip()
            return f"Defender remediation could not run fully: {clean_err[:180]}. Try running Jarvis as administrator."
        return f"Defender remediation executed sir. No active removable threats reported. Quick scan status: {scan}."

    def defender_status(self):
        """Get Windows Defender status and last scan time."""
        ps = (
            "Get-MpComputerStatus | Select-Object AMServiceEnabled,RealTimeProtectionEnabled,"
            "QuickScanEndTime,LastFullScanEndTime | "
            "ForEach-Object { "
            "'RealTime: ' + $_.RealTimeProtectionEnabled + "
            "' | LastQuick: ' + $_.QuickScanEndTime + "
            "' | LastFull: ' + $_.LastFullScanEndTime }"
        )
        result = self._ps(ps)
        if result and "Error" not in result:
            return "Defender status: " + result.strip()[:200]
        return "Could not retrieve Defender status sir."

    def defender_monitor_background(self):
        """Start background thread monitoring Defender for new threats."""
        def _watch():
            import time as _t
            last_count = 0
            while True:
                _t.sleep(120)  # check every 2 minutes
                try:
                    ps = "Get-MpThreatDetection | Measure-Object | Select-Object -ExpandProperty Count"
                    r = self._ps(ps)
                    count = int(r.strip()) if r.strip().isdigit() else 0
                    if count > last_count:
                        diff = count - last_count
                        if self._reminder_cb:
                            self._reminder_cb(
                                f"Sir, Windows Defender has detected {diff} new threat{'s' if diff>1 else ''}. "
                                "I recommend reviewing immediately."
                            )
                        last_count = count
                except: pass
        import threading as _t2
        _t2.Thread(target=_watch, daemon=True).start()
        return "Defender monitoring active sir. I will alert you to any threats."

    # â”€â”€ Google Calendar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    # â”€â”€ Multi-account Google Calendar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€



    # â”€â”€ Clipboard Intelligence â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def watch_clipboard(self):
        """Start monitoring clipboard for intelligent suggestions."""
        def _watch():
            import time as _t
            last = ""
            while True:
                _t.sleep(3)
                try:
                    curr = self.get_clipboard()
                    if curr and curr != last and len(curr) > 10:
                        last = curr
                        # Detect type and offer help
                        low = curr.lower().strip()
                        if any(kw in low for kw in ['def ','class ','import ','function','const ','let ','var ']):
                            if self._reminder_cb:
                                self._reminder_cb("I notice you have copied some code sir. Say analyse clipboard if you would like me to review it.")
                        elif curr.startswith('http'):
                            if self._reminder_cb:
                                self._reminder_cb("I see a URL in your clipboard sir. Say summarize that link if you would like me to read it.")
                        elif len(curr) > 200 and curr.count(' ') > 20:
                            if self._reminder_cb:
                                self._reminder_cb("There is a block of text in your clipboard sir. Say summarize clipboard if you would like the key points.")
                except: pass
        import threading as _t2
        _t2.Thread(target=_watch, daemon=True).start()
        return "Clipboard intelligence active sir. I will flag anything interesting."

    # â”€â”€ Ambient Stress Detection â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def focus_mode(self, minutes=25):
        """Start a Pomodoro focus session â€” no interruptions for N minutes."""
        def _timer():
            time.sleep(int(minutes)*60)
            if self._reminder_cb:
                import random as _r
                msgs = [
                    f"{minutes} minute focus session complete sir. Time for a break.",
                    f"Pomodoro done sir. Step away for five minutes.",
                    f"Focus block complete. You have earned a rest sir.",
                    f"{minutes} minutes up sir. Excellent focus.",
                ]
                self._reminder_cb(_r.choice(msgs))
        import threading as _t2
        _t2.Thread(target=_timer, daemon=True).start()
        return f"Focus mode engaged sir. No interruptions for {minutes} minutes. I will notify you when done."

    # â”€â”€ Code File Watcher â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def watch_project_changes(self, project_name=""):
        """Monitor a project folder for file changes and alert."""
        import json as _j
        pf = self.workspace / ".jarvis_projects.json"
        if not pf.exists(): return "No projects on record sir."
        reg = _j.loads(pf.read_text())
        target = None
        for k, v in reg.items():
            if not project_name or project_name.lower() in k.lower():
                target = (k, Path(v["path"]))
                break
        if not target: return f"Project {project_name} not found sir."
        name, path = target

        def _watch():
            import time as _t
            snapshot = {}
            while True:
                _t.sleep(5)
                try:
                    current = {str(f): f.stat().st_mtime
                               for f in path.rglob("*") if f.is_file()
                               and not any(x in str(f) for x in ['.git','__pycache__','.pyc'])}
                    if snapshot:
                        changed = [f for f in current if f not in snapshot or current[f] != snapshot[f]]
                        added   = [f for f in current if f not in snapshot]
                        if changed and self._reminder_cb:
                            fnames = ", ".join(Path(f).name for f in changed[:3])
                            self._reminder_cb(f"Sir, {len(changed)} file{'s' if len(changed)>1 else ''} changed in {name}: {fnames}.")
                    snapshot = current
                except: pass
        import threading as _t2
        _t2.Thread(target=_watch, daemon=True).start()
        return f"Watching {name} for changes sir. I will notify you of any modifications."

    # â”€â”€ Smart Screen Time â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def screen_time_report(self):
        """Report top active processes as a proxy for screen time."""
        try:
            ps = (
                "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | "
                "Sort-Object CPU -Descending | Select-Object -First 8 | "
                "ForEach-Object { $_.ProcessName + ': ' + [math]::Round($_.CPU) + 's CPU' }"
            )
            result = self._ps(ps)
            if result and "Error" not in result:
                lines = [l.strip() for l in result.strip().split("\n") if l.strip()][:5]
                return "Active applications by CPU time sir: " + ". ".join(lines) + "."
            return "Could not retrieve screen time data sir."
        except Exception as e:
            return f"Screen time error: {e}"

    # â”€â”€ Smart Morning Brief â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def morning_brief(self):
        """Full morning briefing: time, weather, calendar, goal."""
        import random as _r
        parts = []
        # Time
        now = datetime.datetime.now()
        parts.append(now.strftime("It is %I:%M %p on %A %B %d."))
        # Weather
        try:
            w = self.get_weather()
            parts.append(w)
        except: pass
        # Calendar
        try:
            cal = self.calendar_today()
            parts.append(cal)
        except: pass
        # Goal
        try:
            goal = self.get_daily_goal()
            if "No goal" not in goal:
                parts.append(goal)
        except: pass
        intros = [
            "Good morning sir. Here is your briefing.",
            "Morning brief sir.",
            "Here is the situation sir.",
            "Let me bring you up to speed sir.",
        ]
        return _r.choice(intros) + " " + " ".join(parts)

    # â”€â”€ Network Security Scan â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def security_audit(self):
        """Quick security audit â€” open ports, defender status, recent logins."""
        import anthropic as _ant
        parts = []
        # Open ports
        try:
            conns = [c for c in psutil.net_connections() if c.status == "LISTEN"]
            ports = sorted(set(c.laddr.port for c in conns))[:10]
            parts.append(f"Open ports: {', '.join(str(p) for p in ports)}")
        except: pass
        # Defender
        try:
            ps = "Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled"
            r = self._ps(ps).strip()
            parts.append(f"Real-time protection: {r}")
        except: pass
        # Recent failed logins
        try:
            ps2 = "Get-WinEvent -LogName Security -MaxEvents 20 | Where-Object {$_.Id -eq 4625} | Measure-Object | Select-Object -ExpandProperty Count"
            r2 = self._ps(ps2).strip()
            parts.append(f"Failed login attempts (recent): {r2}")
        except: pass
        if not parts:
            return "Could not complete security audit sir."
        # AI summary
        cfg = load_config()
        try:
            import anthropic as _ant2
            client = _ant2.Anthropic(api_key=cfg["anthropic_api_key"])
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001", max_tokens=120,
                messages=[{"role":"user","content":"As Jarvis, give a 2-sentence security assessment from this data. No markdown: " + ". ".join(parts)}]
            )
            return resp.content[0].text.strip()
        except:
            return "Security audit: " + ". ".join(parts)


    # â”€â”€ Ambient & Smart Features â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    def clipboard_intelligence(self):
        """Analyse whatever is in the clipboard and suggest what to do with it."""
        import anthropic as _ant
        text = self.get_clipboard()
        if not text or len(text) < 5: return "Clipboard is empty sir."
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=120,
            messages=[{"role":"user","content":
                "As Jarvis, in ONE sentence identify what this clipboard content is "
                "(code/URL/email/text/data etc) and suggest one useful action. No markdown: " + text[:500]}]
        )
        return resp.content[0].text.strip()

    def focus_mode(self, duration_minutes=25):
        """Start a Pomodoro-style focus session."""
        mins = int(duration_minutes)
        # Minimize all windows
        self._sh('powershell "(New-Object -ComObject Shell.Application).MinimizeAll()"')
        # Set reminder
        self.set_reminder(f"Focus session complete. {mins} minutes elapsed sir.", mins*60)
        focus_lines = [
            f"Focus mode active sir. {mins} minutes on the clock.",
            f"Pomodoro started. {mins} minutes. I will not disturb you.",
            f"Deep work mode engaged sir. {mins} minutes.",
            f"Windows minimized. {mins} minute focus block started sir.",
            f"Clock is running sir. {mins} minutes. Make them count.",
        ]
        import random as _r3
        return _r3.choice(focus_lines)

    def system_health_report(self):
        """Comprehensive health report of the whole machine."""
        import anthropic as _ant
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime_h = (datetime.datetime.now()-boot).seconds//3600
        procs = len(list(psutil.process_iter()))
        try:
            bat = psutil.sensors_battery()
            bat_txt = f"Battery {bat.percent:.0f}% {'charging' if bat.power_plugged else 'discharging'}." if bat else ""
        except: bat_txt = ""
        data = (f"CPU {cpu}%. RAM {mem.percent}% used ({mem.used//1024**3}GB/{mem.total//1024**3}GB). "
                f"Disk {disk.percent}% used ({disk.free//1024**3}GB free). "
                f"Uptime {uptime_h}h. {procs} processes. {bat_txt}")
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=120,
            messages=[{"role":"user","content":
                "As Jarvis, give a 2-sentence health report on this machine. "
                "Be clinical but personality-forward. No markdown: " + data}]
        )
        return resp.content[0].text.strip()

    def watch_folder(self, path="desktop"):
        """Monitor a folder for changes and report new files."""
        import threading as _thr
        p = self._r(path)
        if not p.is_dir(): return f"Cannot watch {path} sir â€” not a directory."
        snapshot = {str(f): f.stat().st_mtime for f in p.rglob("*") if f.is_file()}
        def _check():
            time.sleep(30)
            current = {str(f): f.stat().st_mtime for f in p.rglob("*") if f.is_file()}
            new = [Path(k).name for k in current if k not in snapshot]
            changed = [Path(k).name for k in current if k in snapshot and current[k] != snapshot[k]]
            if new or changed:
                msg = ""
                if new: msg += f"{len(new)} new file{'s' if len(new)>1 else ''}: {', '.join(new[:3])}. "
                if changed: msg += f"{len(changed)} file{'s' if len(changed)>1 else ''} modified."
                if hasattr(self, "_reminder_cb") and self._reminder_cb:
                    self._reminder_cb(f"Folder update sir. {msg}")
        _thr.Thread(target=_check, daemon=True).start()
        return f"Watching {p.name} for changes sir. I will notify you."

    def generate_password(self, length=20):
        """Generate a cryptographically secure password."""
        import secrets, string
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(secrets.choice(alphabet) for _ in range(int(length)))
        self._set_clipboard(pwd)
        return f"Generated a {length}-character password and copied it to your clipboard sir."

    def encode_base64(self, text):
        import base64
        result = base64.b64encode(text.encode()).decode()
        self._set_clipboard(result)
        return "Base64 encoded and copied to clipboard sir."

    def decode_base64(self, text):
        import base64
        try:
            result = base64.b64decode(text.encode()).decode()
            self._set_clipboard(result)
            return "Decoded and copied to clipboard sir."
        except: return "That does not appear to be valid Base64 sir."

    def count_code_lines(self, path="."):
        """Count lines of code in a project."""
        p = self._r(path)
        ext_map = {}
        total = 0
        for f in p.rglob("*"):
            if f.is_file() and f.suffix in [".py",".js",".ts",".rs",".cpp",".c",".java",".go",".rb"]:
                try:
                    lines = len(f.read_text(errors="ignore").splitlines())
                    ext_map[f.suffix] = ext_map.get(f.suffix,0) + lines
                    total += lines
                except: pass
        if not total: return "No code files found sir."
        breakdown = ", ".join(f"{v} {k}" for k,v in sorted(ext_map.items(), key=lambda x:-x[1])[:3])
        return f"Total {total:,} lines of code sir. Breakdown: {breakdown}."

    def open_in_browser(self, query):
        """Search or open a URL in default browser."""
        if query.startswith("http"): webbrowser.open(query)
        else: webbrowser.open("https://www.google.com/search?q=" + query.replace(" ","+"))
        return f"Opened in browser sir."

    def get_clipboard_word_count(self):
        text = self.get_clipboard()
        if not text: return "Clipboard is empty sir."
        words = len(text.split())
        chars = len(text)
        return f"Clipboard contains {words} words and {chars} characters sir."



    def morning_brief(self):
        t = self.get_time()
        try: w = self.get_weather()
        except: w = ""
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return f"{t} {w} Systems at {cpu:.0f} percent CPU sir."

    def clear_temp_files(self):
        import tempfile as _tf, shutil as _sh
        tmp = Path(_tf.gettempdir())
        deleted = 0
        for f in tmp.iterdir():
            try:
                if f.is_file(): f.unlink(); deleted += 1
                elif f.is_dir(): _sh.rmtree(f); deleted += 1
            except: pass
        return f"Cleared {deleted} temporary files sir."

    def system_health_report(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        bat = psutil.sensors_battery()
        bat_str = f" Battery {bat.percent:.0f} percent." if bat else ""
        status = "nominal" if cpu < 70 and ram.percent < 80 else "under load"
        return f"Systems {status} sir. CPU {cpu:.0f}, RAM {ram.percent:.0f}, disk {disk.percent:.0f} percent.{bat_str}"

    def open_recent_download(self):
        downloads = Path.home() / "Downloads"
        files = sorted([f for f in downloads.iterdir() if f.is_file()],
                       key=lambda f: f.stat().st_mtime, reverse=True)
        if not files: return "Downloads folder is empty sir."
        os.startfile(str(files[0]))
        return f"Opening {files[0].name} sir."

    def who_is_using_internet(self):
        conns = psutil.net_connections(kind="inet")
        pids = set(c.pid for c in conns if c.pid)
        procs = []
        for pid in list(pids)[:8]:
            try: procs.append(psutil.Process(pid).name())
            except: pass
        if not procs: return "No active network connections sir."
        return "Active network users: " + ", ".join(set(procs)) + "."

    def empty_recycle_bin(self):
        return self._ps("Clear-RecycleBin -Force -ErrorAction SilentlyContinue")

    def count_lines_in_project(self, path="."):
        p = self._r(path)
        total = 0
        exts = {".py",".js",".ts",".java",".cpp",".c",".cs",".go",".rs",".html",".css"}
        for f in p.rglob("*"):
            if f.suffix in exts and f.is_file():
                try: total += f.read_text(encoding="utf-8",errors="ignore").count("\n")
                except: pass
        return f"Approximately {total:,} lines of code in this project sir."


    def add_project_note(self, name, note):
        """Add a note/log entry to a project."""
        import json as _j
        f = self.workspace / ".jarvis_projects.json"
        if not f.exists(): return "No projects on record sir."
        reg = _j.loads(f.read_text(encoding="utf-8"))
        for k in reg:
            if name.lower() in k.lower():
                reg[k].setdefault("notes", []).append({
                    "note": note,
                    "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                f.write_text(_j.dumps(reg, indent=2), encoding="utf-8")
                return f"Note added to {k} sir."
        return f"Project {name} not found sir."

    def update_project_status(self, name, status):
        """Update project status: active, paused, complete, archived."""
        import json as _j
        f = self.workspace / ".jarvis_projects.json"
        if not f.exists(): return "No projects on record sir."
        reg = _j.loads(f.read_text(encoding="utf-8"))
        for k in list(reg.keys()):
            if name.lower() in k.lower():
                reg[k]["status"] = status
                f.write_text(_j.dumps(reg, indent=2), encoding="utf-8")
                return f"{k} marked as {status} sir."
        return f"Project {name} not found sir."

    def create_file_in_project(self, project, path, content=""):
        """Create a file inside a project folder."""
        import json as _j
        f = self.workspace / ".jarvis_projects.json"
        if f.exists():
            reg = _j.loads(f.read_text(encoding="utf-8"))
            for k, v in reg.items():
                if project.lower() in k.lower():
                    full_path = Path(v["path"]) / path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content, encoding="utf-8")
                    self.add_project_note(k, f"Created file: {path}")
                    return f"Created {path} in {k} sir."
        # Fallback: use workspace
        return self.create_file(path, content)

    def list_project_files(self, name):
        """List files in a project."""
        import json as _j
        f = self.workspace / ".jarvis_projects.json"
        if not f.exists(): return "No projects on record sir."
        reg = _j.loads(f.read_text(encoding="utf-8"))
        for k, v in reg.items():
            if name.lower() in k.lower():
                p = Path(v["path"])
                if not p.exists(): return f"Project folder not found sir."
                files = []
                for item in p.rglob("*"):
                    if item.is_file() and ".git" not in str(item):
                        files.append(str(item.relative_to(p)))
                return f"{k} has {len(files)} files: " + ", ".join(files[:10]) + ("..." if len(files)>10 else "") + " sir."
        return f"Project {name} not found sir."

    def set_active_project(self, name):
        """Set the currently active project for context."""
        import json as _j
        f = self.workspace / ".jarvis_projects.json"
        if f.exists():
            reg = _j.loads(f.read_text(encoding="utf-8"))
            for k, v in reg.items():
                if name.lower() in k.lower():
                    self._active_proj = k
                    _write_hud(active_project=k)
                    return f"Active project set to {k} sir."
        return f"Project {name} not found sir."

    def clear_active_project(self):
        """Clear the active project."""
        self._active_proj = ""
        _write_hud(active_project="")
        return "Active project cleared sir."

    def _project_lookup(self, name=""):
        import json as _j
        f = self.workspace / ".jarvis_projects.json"
        if not f.exists():
            return None, None, "No projects on record sir."
        try:
            reg = _j.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return None, None, "Could not read project registry sir."
        if not reg:
            return None, None, "No projects on record sir."
        if name:
            for k, v in reg.items():
                if name.lower() in k.lower():
                    return k, Path(v.get("path", "")), None
            return None, None, f"Project {name} not found sir."
        # fallback to active project
        if self._active_proj:
            for k, v in reg.items():
                if self._active_proj.lower() == k.lower():
                    return k, Path(v.get("path", "")), None
        # fallback first active status
        for k, v in reg.items():
            if str(v.get("status", "active")).lower() == "active":
                return k, Path(v.get("path", "")), None
        k = next(iter(reg.keys()))
        return k, Path(reg[k].get("path", "")), None

    def project_framework_setup(self, name=""):
        """
        Create a deterministic project framework scaffold inside an existing project.
        """
        pname, ppath, err = self._project_lookup(name)
        if err:
            return err
        if not ppath.exists():
            return f"Project folder for {pname} is missing sir."

        jdir = ppath / ".jarvis"
        jdir.mkdir(parents=True, exist_ok=True)
        files = {
            "roadmap.md": f"# {pname} Roadmap\n\n## Vision\n\n## Milestones\n- [ ] Milestone one\n- [ ] Milestone two\n\n## Risks\n- ",
            "tasks.md": "# Build Tasks\n\n## Backlog\n- [ ] Define architecture baseline\n\n## In Progress\n\n## Done\n",
            "checkpoints.md": "# Checkpoints\n\n",
            "decisions.md": "# Architecture Decisions\n\n",
            "notes.md": "# Project Notes\n\n",
        }
        created = 0
        for fn, content in files.items():
            fp = jdir / fn
            if not fp.exists():
                fp.write_text(content, encoding="utf-8")
                created += 1
        _write_hud(hud_mode="bulletin", hud_data={"content": f"Framework setup: {pname} ({created} files created)"})
        return f"Project framework initialized for {pname} sir. Created {created} framework file{'s' if created != 1 else ''} in .jarvis."

    def project_add_task(self, task, name="", priority="medium"):
        pname, ppath, err = self._project_lookup(name)
        if err:
            return err
        jdir = ppath / ".jarvis"
        jdir.mkdir(parents=True, exist_ok=True)
        tf = jdir / "tasks.md"
        if not tf.exists():
            tf.write_text("# Build Tasks\n\n## Backlog\n\n## In Progress\n\n## Done\n", encoding="utf-8")
        pri = (priority or "medium").strip().lower()
        line = f"- [ ] ({pri}) {task.strip()}\n"
        txt = tf.read_text(encoding="utf-8")
        if "## Backlog" in txt:
            txt = txt.replace("## Backlog\n", "## Backlog\n" + line)
        else:
            txt += "\n## Backlog\n" + line
        tf.write_text(txt, encoding="utf-8")
        _write_hud(hud_mode="bulletin", hud_data={"content": f"{pname}: task added -> {task[:80]}"})
        return f"Task added to {pname} backlog sir."

    def project_next_tasks(self, name="", limit=5):
        pname, ppath, err = self._project_lookup(name)
        if err:
            return err
        tf = ppath / ".jarvis" / "tasks.md"
        if not tf.exists():
            return f"No framework task board found for {pname} sir. Say setup project framework first."
        lines = [ln.strip() for ln in tf.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("- [ ]")]
        if not lines:
            return f"No open tasks for {pname} sir."
        top = lines[:max(1, int(limit))]
        return f"Next tasks for {pname}: " + " | ".join(t[5:] for t in top)

    def project_checkpoint(self, summary, name=""):
        pname, ppath, err = self._project_lookup(name)
        if err:
            return err
        cf = ppath / ".jarvis" / "checkpoints.md"
        cf.parent.mkdir(parents=True, exist_ok=True)
        if not cf.exists():
            cf.write_text("# Checkpoints\n\n", encoding="utf-8")
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(cf, "a", encoding="utf-8") as f:
            f.write(f"- [{ts}] {summary.strip()}\n")
        _write_hud(hud_mode="bulletin", hud_data={"content": f"{pname}: checkpoint saved"})
        return f"Checkpoint saved for {pname} sir."

    def project_build_status(self, name=""):
        pname, ppath, err = self._project_lookup(name)
        if err:
            return err
        if not ppath.exists():
            return f"Project folder for {pname} is missing sir."
        total_files = 0
        code_files = 0
        for fp in ppath.rglob("*"):
            if fp.is_file():
                total_files += 1
                if fp.suffix.lower() in {".py",".js",".ts",".tsx",".jsx",".rs",".go",".java",".cpp",".c",".cs",".html",".css"}:
                    code_files += 1
        tf = ppath / ".jarvis" / "tasks.md"
        open_tasks = 0
        done_tasks = 0
        if tf.exists():
            t = tf.read_text(encoding="utf-8")
            open_tasks = len(re.findall(r"^- \[ \]", t, flags=re.M))
            done_tasks = len(re.findall(r"^- \[x\]", t, flags=re.I|re.M))
        return f"{pname} status: {total_files} files, {code_files} code files, {open_tasks} open tasks, {done_tasks} completed tasks."

    def enter_architect_mode(self):
        """Project builder supermode: architecture-first sequencing."""
        _write_hud(hud_mode="bulletin", hud_data={"content": "Architect mode engaged: scaffold, interfaces, dependencies."})
        if hasattr(self, "_mission_ref") and self._mission_ref:
            self._mission_ref.trace("MODE", "architect", "Architecture sequencing loaded", fallback=False)
            self._mission_ref.append_decision("Entered Architect Mode")
            return self._mission_ref.set_supermode("architect")
        return "Architect mode engaged sir."

    def enter_ship_mode(self):
        """Project builder supermode: launch readiness and verification."""
        _write_hud(hud_mode="bulletin", hud_data={"content": "Ship mode engaged: verification, release checks, launch."})
        if hasattr(self, "_mission_ref") and self._mission_ref:
            self._mission_ref.trace("MODE", "ship", "Launch checklist loaded", fallback=False)
            self._mission_ref.append_decision("Entered Ship Mode")
            return self._mission_ref.set_supermode("ship")
        return "Ship mode engaged sir."

    def enter_debug_hunt(self):
        """Project builder supermode: isolate failure and patch smallest surface."""
        _write_hud(hud_mode="bulletin", hud_data={"content": "Debug Hunt engaged: reproduce, isolate, patch, verify."})
        if hasattr(self, "_mission_ref") and self._mission_ref:
            self._mission_ref.trace("MODE", "debug", "Failure-isolation workflow loaded", fallback=False)
            self._mission_ref.append_decision("Entered Debug Hunt")
            return self._mission_ref.set_supermode("debug")
        return "Debug Hunt mode engaged sir."

    def mission_start(self, goal):
        if not hasattr(self, "_mission_ref") or not self._mission_ref:
            return "Mission engine offline."
        out = self._mission_ref.start_mission(goal)
        self._mission_ref.set_stage("plan", progress=18)
        return out

    def mission_clear(self, reason="operator request"):
        if not hasattr(self, "_mission_ref") or not self._mission_ref:
            return "Mission engine offline."
        return self._mission_ref.clear_mission(reason)

    def mission_status(self):
        if not hasattr(self, "_mission_ref") or not self._mission_ref:
            return "Mission engine offline."
        self._mission_ref.sync_hud(status="thinking", text="Mission status requested.", tool="mission")
        return self._mission_ref.mission_status()

    def mission_next_action(self):
        if not hasattr(self, "_mission_ref") or not self._mission_ref:
            return "Mission engine offline."
        return self._mission_ref.next_action()

    def mission_why(self):
        if not hasattr(self, "_mission_ref") or not self._mission_ref:
            return "Mission engine offline."
        return self._mission_ref.why_this()

    def mission_apply_template(self, template="python_script", goal=""):
        if not hasattr(self, "_mission_ref") or not self._mission_ref:
            return "Mission engine offline."
        return self._mission_ref.apply_template(template, goal)


    def find_file_on_pc(self, name, start_path="C:\\"):
        """Search entire PC for a file or folder by name/pattern."""
        results = []
        # Use PowerShell for speed â€” much faster than Python os.walk
        ps_cmd = (
            f'Get-ChildItem -Path "{start_path}" -Filter "*{name}*" '
            f'-Recurse -ErrorAction SilentlyContinue | '
            f'Select-Object -First 10 FullName | ForEach-Object {{$_.FullName}}'
        )
        out = self._ps(ps_cmd)
        if out and "Done." not in out and "Error" not in out:
            lines = [l.strip() for l in out.splitlines() if l.strip() and "Error" not in l]
            results = lines[:10]
        if not results:
            # Fallback: where command for executables
            where_out = self._sh(f"where /R {start_path} *{name}* 2>nul")
            if where_out and "Could not find" not in where_out:
                results = [l for l in where_out.splitlines() if l.strip()][:5]
        if not results:
            return f"No files matching '{name}' found in {start_path} sir."
        return f"Found {len(results)} match{'es' if len(results)>1 else ''}: " + "; ".join(results[:5])

    def find_folder_on_pc(self, name, start_path="C:\\"):
        """Search for a folder by name."""
        ps_cmd = (
            f'Get-ChildItem -Path "{start_path}" -Filter "*{name}*" '
            f'-Recurse -Directory -ErrorAction SilentlyContinue | '
            f'Select-Object -First 8 FullName | ForEach-Object {{$_.FullName}}'
        )
        out = self._ps(ps_cmd)
        lines = [l.strip() for l in (out or "").splitlines() if l.strip() and "Error" not in l]
        if not lines:
            return f"No folder matching '{name}' found sir."
        return "Found: " + "; ".join(lines[:5])

    def restart_jarvis(self):
        """Restart the Jarvis process â€” use after self-modification."""
        import os as _os
        desktop = Path(_os.environ.get("USERPROFILE","")) / "Desktop"
        pyw = desktop / "JARVIS.pyw"
        py = Path(sys.executable)
        # Launch new instance
        if pyw.exists():
            subprocess.Popen(
                [str(py.parent / "pythonw.exe"), str(pyw)],
                cwd=str(desktop),
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        # Kill self
        _write_hud("shutdown")
        time.sleep(0.5)
        _os._exit(0)

    def hud_show(self, mode="", data=""):
        """Show something on the HUD display panel."""
        _write_hud(hud_mode=mode, hud_data={"content": str(data)})
        return f"Displaying {mode or 'info'} on HUD sir."

    def get_clipboard(self):
        """Get clipboard contents."""
        r = subprocess.run("powershell Get-Clipboard", shell=True,
                          capture_output=True, text=True,
                          creationflags=subprocess.CREATE_NO_WINDOW)
        return r.stdout.strip() or "Clipboard is empty sir."

    def set_clipboard_text(self, text):
        """Set clipboard text."""
        self._set_clipboard(text)
        return "Copied to clipboard sir."

    def get_installed_apps(self):
        """List installed applications via winget."""
        out = self._sh("winget list 2>nul")
        lines = [l for l in (out or "").splitlines() if l.strip()][:20]
        return "Installed apps: " + ", ".join(lines) if lines else "Could not list apps sir."

    def install_app(self, name):
        """Install an application via winget."""
        out = self._sh(f"winget install {name} --accept-source-agreements --accept-package-agreements")
        return f"Installing {name}. " + (out[:100] if out else "")

    def open_folder(self, path):
        """Open a folder in File Explorer."""
        p = Path(path) if Path(path).is_absolute() else self.workspace / path
        subprocess.Popen(f'explorer "{p}"', shell=True)
        return f"Opened {p} sir."

    def get_window_list(self):
        """List visible windows."""
        out = self._ps("Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object Name,MainWindowTitle | ForEach-Object {$_.Name + ': ' + $_.MainWindowTitle}")
        return out[:400] if out else "No windows found sir."

    def focus_window(self, name):
        """Bring a window to the foreground."""
        ps = f'(Get-Process | Where-Object {{$_.MainWindowTitle -like "*{name}*"}} | Select-Object -First 1).MainWindowHandle | ForEach-Object {{[void][System.Runtime.InteropServices.Marshal]::GetFunctionPointerForDelegate((Add-Type -Name W -Member "[DllImport(\"user32.dll\")]public static extern bool SetForegroundWindow(IntPtr h);" -PassThru)::SetForegroundWindow($_))}}'
        self._ps(ps)
        return f"Focused {name} sir."

    def type_text(self, text):
        """Type text into the active window."""
        safe = text.replace("'","''")
        self._ps(f"(New-Object -ComObject WScript.Shell).SendKeys('{safe}')")
        return f"Typed text sir."

    def press_hotkey(self, keys):
        """Press a keyboard shortcut e.g. ctrl+c, alt+f4."""
        key_map = {"ctrl":"^","alt":"%","shift":"+","win":"{WIN}"}
        combo = keys.lower()
        for k,v in key_map.items():
            combo = combo.replace(k+"+",v)
        self._ps(f"(New-Object -ComObject WScript.Shell).SendKeys('{combo}')")
        return f"Pressed {keys} sir."

    def get_system_specs(self):
        cpu = self._ps("Get-WmiObject Win32_Processor | Select -ExpandProperty Name")
        gpu = self._ps("Get-WmiObject Win32_VideoController | Select -ExpandProperty Name")
        ram = self._ps("(Get-WmiObject Win32_PhysicalMemory | Measure-Object Capacity -Sum).Sum / 1GB")
        return f"CPU: {(cpu or '?').strip()} | GPU: {(gpu or '?').strip()} | RAM: {(ram or '?').strip()}GB sir."

    def list_usb_devices(self):
        out = self._ps("Get-PnpDevice -Class USB | Where Status -eq OK | Select -ExpandProperty FriendlyName")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:6]
        return ("USB: " + ", ".join(lines)) if lines else "No USB devices sir."

    def get_running_services(self):
        out = self._ps("Get-Service | Where Status -eq Running | Select -ExpandProperty Name")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()]
        return f"{len(lines)} services running: " + ", ".join(lines[:5]) + " sir."

    def stop_service(self, name):
        self._ps(f"Stop-Service -Name '{name}' -Force -ErrorAction SilentlyContinue")
        return f"Service {name} stopped sir."

    def start_service(self, name):
        self._ps(f"Start-Service -Name '{name}' -ErrorAction SilentlyContinue")
        return f"Service {name} started sir."

    def restart_service(self, name):
        self._ps(f"Restart-Service -Name '{name}' -Force -ErrorAction SilentlyContinue")
        return f"Service {name} restarted sir."

    def get_event_log_errors(self, count=5):
        out = self._ps(f"Get-EventLog -LogName System -EntryType Error -Newest {count} 2>$null | ForEach-Object {{$_.TimeGenerated.ToString('HH:mm') + ' ' + $_.Source}}")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:5]
        return ("Recent errors: " + " | ".join(lines)) if lines else "No recent errors sir."

    def get_network_adapters(self):
        out = self._ps("Get-NetAdapter | ForEach-Object {$_.Name + ' [' + $_.Status + ']'}")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:5]
        return ("Adapters: " + " | ".join(lines)) if lines else "No adapters sir."

    def enable_firewall(self):
        self._ps("Set-NetFirewallProfile -All -Enabled True")
        return "Firewall enabled sir."

    def disable_firewall(self):
        self._ps("Set-NetFirewallProfile -All -Enabled False")
        return "Firewall disabled sir."

    def get_open_connections(self):
        out = self._sh("netstat -ano | findstr ESTABLISHED")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()]
        return f"{len(lines)} established connections sir."

    def get_arp_table(self):
        out = self._sh("arp -a")
        lines = [l.strip() for l in (out or "").splitlines() if "dynamic" in l.lower()][:6]
        return ("LAN devices: " + " | ".join(lines)) if lines else "ARP table empty sir."

    def traceroute(self, host):
        out = self._sh(f"tracert -d -h 10 {host}")
        return (out[:300] if out else f"Traceroute to {host} failed sir.")

    def renew_ip(self):
        self._sh("ipconfig /release"); self._sh("ipconfig /renew")
        return "IP address renewed sir."

    def port_scan(self, host, ports="80,443,22,21,3389,8080"):
        import socket
        results = []
        for port in [int(p.strip()) for p in ports.split(",")]:
            try:
                s = socket.socket(); s.settimeout(0.5)
                if s.connect_ex((host, port)) == 0: results.append(str(port))
                s.close()
            except: pass
        return ("Open ports on " + host + ": " + ", ".join(results)) if results else f"No open ports on {host} sir."

    def check_disk_health(self):
        out = self._ps("Get-WmiObject -Namespace root/wmi -Class MSStorageDriver_FailurePredictStatus 2>$null | Select -ExpandProperty PredictFailure")
        return "WARNING: Disk failure predicted sir." if "True" in (out or "") else "Disk health nominal sir."

    def get_largest_files(self, path=None, count=8):
        p = path or str(Path.home())
        out = self._ps(f'Get-ChildItem -Path "{p}" -Recurse -File -EA SilentlyContinue | Sort Length -Desc | Select -First {count} | ForEach-Object {{[math]::Round($_.Length/1MB,1).ToString() + "MB " + $_.Name}}')
        lines = [l.strip() for l in (out or "").splitlines() if "MB" in l][:6]
        return ("Largest files: " + " | ".join(lines)) if lines else "Scan failed sir."

    def get_folder_size(self, path):
        out = self._ps(f'$s=0; Get-ChildItem "{path}" -Recurse -File -EA SilentlyContinue | ForEach-Object {{$s+=$_.Length}}; [math]::Round($s/1MB,2)')
        return f"{path}: {(out or '?').strip()} MB sir."

    def get_file_hash(self, path, algorithm="SHA256"):
        out = self._ps(f'Get-FileHash "{path}" -Algorithm {algorithm} | Select -ExpandProperty Hash')
        return f"{algorithm}: {(out or 'Failed').strip()}"

    def count_files_in_dir(self, path):
        out = self._ps(f'(Get-ChildItem "{path}" -Recurse -File -EA SilentlyContinue).Count')
        return f"Found {(out or '0').strip()} files in {path} sir."

    def sync_folders(self, source, dest):
        self._sh(f'robocopy "{source}" "{dest}" /MIR /R:1 /W:1 /NP /NFL /NDL /NJH /NJS')
        return f"Sync complete from {source} to {dest} sir."

    def batch_rename(self, directory, pattern, replacement):
        d = Path(directory)
        count = 0
        for f in d.iterdir():
            if pattern.lower() in f.name.lower():
                try: f.rename(f.parent / f.name.replace(pattern, replacement)); count += 1
                except: pass
        return f"Renamed {count} files in {directory} sir."

    def compare_files(self, path1, path2):
        try:
            import difflib
            t1 = Path(path1).read_text(encoding="utf-8",errors="ignore").splitlines()
            t2 = Path(path2).read_text(encoding="utf-8",errors="ignore").splitlines()
            diffs = list(difflib.unified_diff(t1, t2, lineterm=""))
            return "Files are identical sir." if not diffs else f"{len(diffs)} differences sir."
        except Exception as e:
            return f"Compare failed: {e}"

    def auto_organise_downloads(self):
        downloads = Path.home() / "Downloads"
        cats = {"Images":[".jpg",".jpeg",".png",".gif",".bmp",".webp"],
                "Videos":[".mp4",".mkv",".avi",".mov",".wmv"],
                "Audio":[".mp3",".wav",".flac",".aac",".ogg"],
                "Documents":[".pdf",".doc",".docx",".txt",".xlsx",".pptx"],
                "Archives":[".zip",".rar",".7z",".tar",".gz"],
                "Code":[".py",".js",".html",".css",".json",".xml"],
                "Executables":[".exe",".msi",".bat",".cmd"]}
        moved = 0
        for f in downloads.iterdir():
            if f.is_file():
                for cat, exts in cats.items():
                    if f.suffix.lower() in exts:
                        dest = downloads / cat
                        dest.mkdir(exist_ok=True)
                        try: f.rename(dest / f.name); moved += 1
                        except: pass
                        break
        return f"Organised {moved} files in Downloads sir."

    def get_recently_modified_files(self, hours=24, path=None):
        p = path or str(Path.home())
        out = self._ps(f'Get-ChildItem "{p}" -Recurse -File -EA SilentlyContinue | Where LastWriteTime -gt (Get-Date).AddHours(-{hours}) | Select -First 8 | ForEach-Object {{$_.LastWriteTime.ToString("HH:mm") + " " + $_.Name}}')
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:6]
        return (f"Modified in last {hours}h: " + " | ".join(lines)) if lines else f"Nothing modified in last {hours}h sir."

    def create_scheduled_task(self, name, command, trigger_time):
        self._sh(f'schtasks /create /tn "{name}" /tr "{command}" /sc once /st {trigger_time} /F')
        return f"Task {name} scheduled for {trigger_time} sir."

    def delete_scheduled_task(self, name):
        self._sh(f'schtasks /delete /tn "{name}" /F')
        return f"Task {name} deleted sir."

    def run_at_startup(self, name, command):
        self._ps(f'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "{name}" -Value "{command}"')
        return f"Added {name} to startup sir."

    def remove_from_startup(self, name):
        self._ps(f'Remove-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "{name}" -EA SilentlyContinue')
        return f"Removed {name} from startup sir."

    def get_power_plan(self):
        out = self._sh("powercfg /getactivescheme")
        return (out[:150] if out else "Unavailable sir.")

    def set_power_plan(self, plan="balanced"):
        plans = {"balanced":"381b4222-f694-41f0-9685-ff5bb260df2e",
                 "high":"8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                 "saver":"a1841308-3541-4fab-bc81-f71556f20b4a"}
        self._sh(f"powercfg /setactive {plans.get(plan.lower(), plans['balanced'])}")
        return f"Power plan set to {plan} sir."

    def toggle_dark_mode(self):
        out = self._ps('(Get-ItemProperty "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize").AppsUseLightTheme')
        new_val = "0" if (out or "1").strip() == "1" else "1"
        self._ps(f'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" -Name AppsUseLightTheme -Value {new_val}')
        return f"{'Dark' if new_val == '0' else 'Light'} mode enabled sir."

    def restart_explorer(self):
        self._ps("Stop-Process -Name explorer -Force; Start-Sleep 1; Start-Process explorer")
        return "Explorer restarted sir."

    def get_windows_version(self):
        out = self._ps("(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').ProductName + ' Build ' + (Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').CurrentBuildNumber")
        return (out.strip() if out else self._sh("ver"))

    def check_pending_reboots(self):
        out = self._ps('Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\RebootRequired"')
        return "Reboot pending sir." if "True" in (out or "") else "No reboot pending sir."

    def currency_convert(self, amount, from_cur, to_cur):
        try:
            import urllib.request as _ur, json as _j
            data = _j.loads(_ur.urlopen(f"https://api.exchangerate-api.com/v4/latest/{from_cur.upper()}", timeout=5).read())
            rate = data["rates"].get(to_cur.upper())
            return f"{amount} {from_cur.upper()} = {float(amount)*rate:.2f} {to_cur.upper()} sir." if rate else f"Unknown currency: {to_cur} sir."
        except: return "Currency service unavailable sir."

    def get_ip_info(self, ip=""):
        try:
            import urllib.request as _ur, json as _j
            d = _j.loads(_ur.urlopen(f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json", timeout=5).read())
            return f"{d.get('query','?')} | {d.get('city','?')}, {d.get('country','?')} | ISP: {d.get('isp','?')} sir."
        except: return "IP lookup unavailable sir."

    def get_time_in_city(self, city):
        import datetime as _dt
        offsets = {"london":0,"paris":2,"dubai":4,"tokyo":9,"new york":-4,"los angeles":-7,
                   "chicago":-5,"sydney":10,"toronto":-4,"berlin":2,"moscow":3,"beijing":8}
        off = offsets.get(city.lower())
        if off is not None:
            local = _dt.datetime.utcnow() + _dt.timedelta(hours=off)
            return f"{city.title()}: {local.strftime('%I:%M %p')} sir."
        return f"City {city} not in database sir."

    def countdown_to(self, event, date_str):
        import datetime as _dt
        try:
            diff = _dt.datetime.strptime(date_str, "%Y-%m-%d") - _dt.datetime.now()
            return f"{abs(diff.days)} days {'until' if diff.days>=0 else 'since'} {event} sir."
        except: return "Use YYYY-MM-DD format sir."

    def calculate_age(self, birthdate_str):
        import datetime as _dt
        try:
            return f"Age: {(_dt.datetime.now()-_dt.datetime.strptime(birthdate_str,'%Y-%m-%d')).days//365} years sir."
        except: return "Use YYYY-MM-DD format sir."

    def get_moon_phase(self):
        import datetime as _dt
        diff = _dt.datetime.now() - _dt.datetime(2001,1,1)
        phase = ((diff.days + diff.seconds/86400) / 29.53058775) % 1
        phases = ["new moon","waxing crescent","first quarter","waxing gibbous",
                  "full moon","waning gibbous","last quarter","waning crescent"]
        return f"Moon phase: {phases[int(phase*8)%8]} sir."

    def pomodoro_session(self, minutes=25):
        self.set_reminder(f"Pomodoro complete! Take a 5-minute break sir.", int(minutes)*60)
        return f"Pomodoro started. {minutes}-minute session. I will alert you sir."

    def flip_coin(self):
        import random
        return f"{'Heads' if random.random()>.5 else 'Tails'} sir."

    def roll_dice(self, sides=6, count=1):
        import random
        rolls = [random.randint(1,int(sides)) for _ in range(int(count))]
        return f"Rolled {rolls[0]} on d{sides} sir." if int(count)==1 else f"Rolled {rolls} (total {sum(rolls)}) sir."

    def rock_paper_scissors(self, choice):
        import random
        opts = ["rock","paper","scissors"]
        jarvis = random.choice(opts)
        c = choice.lower()
        if c not in opts: return "Say rock, paper, or scissors sir."
        beats = {"rock":"scissors","paper":"rock","scissors":"paper"}
        result = "Tie" if c==jarvis else ("You win" if beats[c]==jarvis else "I win")
        return f"You: {c} | Me: {jarvis} â€” {result} sir."

    def get_compliment(self):
        import random
        return random.choice(["You have exceptional taste in AI assistants sir.",
            "Your problem-solving is genuinely impressive sir.",
            "You ask better questions than most sir.",
            "Your instincts are usually correct sir."])

    def check_password_strength(self, password):
        import re as _r
        score = sum([len(password)>=8, len(password)>=12,
                     bool(_r.search(r"[A-Z]",password)), bool(_r.search(r"[a-z]",password)),
                     bool(_r.search(r"\d",password)), bool(_r.search(r"[!@#$%^&*]",password))])
        levels={0:"very weak",1:"weak",2:"weak",3:"fair",4:"good",5:"strong",6:"very strong"}
        return f"Password strength: {levels.get(score,'unknown')} ({score}/6) sir."

    def generate_hash(self, text, algorithm="sha256"):
        import hashlib
        h = hashlib.new(algorithm); h.update(text.encode())
        return f"{algorithm.upper()}: {h.hexdigest()} sir."

    def generate_uuid(self):
        import uuid
        u = str(uuid.uuid4()); self._set_clipboard(u)
        return f"UUID: {u} (copied) sir."

    def url_encode(self, text):
        import urllib.parse
        return urllib.parse.quote(text) + " sir."

    def url_decode(self, text):
        import urllib.parse
        return urllib.parse.unquote(text) + " sir."

    def regex_test(self, pattern, text):
        import re as _r
        try:
            matches = _r.findall(pattern, text)
            return f"Found {len(matches)} match: {matches[:5]} sir."
        except Exception as e:
            return f"Invalid regex: {e}"

    def run_code_snippet(self, language, code):
        import tempfile as _tf, os as _os, sys as _sys
        lang = language.lower()
        if lang in ("python","py"):
            tmp = Path(_tf.mktemp(suffix=".py")); tmp.write_text(code, encoding="utf-8")
            out = self._sh(f'"{_sys.executable}" "{tmp}" 2>&1')
            try: _os.unlink(tmp)
            except: pass
            return (out[:300] if out else "No output sir.")
        elif lang in ("powershell","ps"):
            return self._ps(code)[:300]
        return f"Language {language} not supported sir."

    def git_log(self, path=".", count=5):
        out = self._sh(f'git -C "{path}" log --oneline -{count}')
        return out[:300] if out else "No git history sir."

    def git_diff(self, path="."):
        out = self._sh(f'git -C "{path}" diff --stat')
        return (out[:200] if out else "No changes sir.")

    def git_clone(self, url, dest=""):
        cmd = f'git clone "{url}"' + (f' "{dest}"' if dest else "")
        self._sh(f'cd "{self.workspace}" && {cmd}')
        return f"Cloned {url} sir."

    def git_branch(self, path="."):
        out = self._sh(f'git -C "{path}" branch -a')
        return out[:200] if out else "No branches sir."

    def send_email(self, to_addr, subject, body, from_addr="", password=""):
        try:
            import smtplib, ssl
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            cfg = load_config()
            fa = from_addr or cfg.get("email_user","")
            pw = password or cfg.get("email_pass","")
            if not fa: return "Email not configured. Add email_user and email_pass to ~/.jarvis_config.json sir."
            msg = MIMEMultipart()
            msg["From"]=fa; msg["To"]=to_addr; msg["Subject"]=subject
            msg.attach(MIMEText(body,"plain"))
            with smtplib.SMTP_SSL("smtp.gmail.com",465,context=ssl.create_default_context()) as s:
                s.login(fa, pw); s.send_message(msg)
            return f"Email sent to {to_addr} sir."
        except Exception as e:
            return f"Email failed: {e}"

    def set_volume_level(self, level):
        level = max(0, min(100, int(level)))
        self._ps(f"$wsh=New-Object -ComObject WScript.Shell; 1..50 | ForEach-Object {{$wsh.SendKeys([char]0xAE)}}; 1..{level//2} | ForEach-Object {{$wsh.SendKeys([char]0xAF)}}")
        return f"Volume set to approximately {level} percent sir."

    def get_current_song(self):
        out = self._ps("Get-Process spotify -EA SilentlyContinue | Select -ExpandProperty MainWindowTitle")
        title = (out or "").strip()
        return f"Now playing: {title} sir." if title and title.lower() not in ("spotify","") else "Spotify is not playing anything sir."

    def list_audio_devices(self):
        try:
            import sounddevice as _sd
            devs = _sd.query_devices()
            out = [f"[{i}]{'IN' if d['max_input_channels']>0 else 'OUT'} {d['name'][:20]}" for i,d in enumerate(devs)]
            return "Audio: " + " | ".join(out[:6]) + " sir."
        except: return "Audio device list unavailable sir."

    def test_microphone(self):
        try:
            import sounddevice as _sd, numpy as _np
            rec = _sd.rec(int(2*16000), samplerate=16000, channels=1, dtype="int16"); _sd.wait()
            vol = float(_np.abs(rec).mean())
            return f"Microphone {'working' if vol>100 else 'very quiet'} â€” volume: {vol:.0f} sir."
        except Exception as e:
            return f"Mic test failed: {e}"

    def set_mic_device(self, index):
        try:
            cfg = load_config(); cfg["mic_device"] = int(index); save_config(cfg)
            return f"Mic set to device {index}. Restart Jarvis to apply sir."
        except Exception as e:
            return f"Failed: {e}"

    def create_meeting_notes(self, meeting_name, attendees="", agenda=""):
        import datetime as _dt
        now = _dt.datetime.now()
        tmpl = f"# {meeting_name}\nDate: {now.strftime('%B %d, %Y')}\nAttendees: {attendees}\n\n## Agenda\n{agenda}\n\n## Notes\n\n## Action Items\n"
        fname = f"meeting_{now.strftime('%Y%m%d_%H%M')}_{meeting_name.replace(' ','_')}.md"
        (self.workspace / fname).write_text(tmpl, encoding="utf-8")
        return f"Meeting notes created: {fname} sir."

    def word_count(self, text_or_path):
        if Path(str(text_or_path)).exists():
            text = Path(str(text_or_path)).read_text(encoding="utf-8", errors="ignore")
        else:
            text = str(text_or_path)
        return f"{len(text.split())} words, {len(text)} chars sir."

    def wipe_file(self, path):
        try:
            p = Path(path); p.write_bytes(b"\x00" * p.stat().st_size); p.unlink()
            return "File securely wiped sir."
        except Exception as e:
            return f"Wipe failed: {e}"

    def what_is_my_ip(self):
        return f"Public: {self.get_public_ip()} | Local: {self.get_local_ip()} sir."

    def hibernate_pc(self):
        self._sh("shutdown /h")
        return "Hibernating sir."

    def create_shortcut(self, target, shortcut_path, description=""):
        self._ps(f'$WS=New-Object -ComObject WScript.Shell; $SC=$WS.CreateShortcut("{shortcut_path}"); $SC.TargetPath="{target}"; $SC.Description="{description}"; $SC.Save()')
        return f"Shortcut created at {shortcut_path} sir."

    def backup_file(self, path):
        import datetime as _dt, shutil as _sh
        src = Path(path)
        if not src.exists(): return f"File not found: {path} sir."
        dst = src.parent / f"{src.stem}_backup_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}{src.suffix}"
        _sh.copy2(str(src), str(dst))
        return f"Backed up to {dst.name} sir."

    def get_recent_downloads(self, count=5):
        downloads = Path.home() / "Downloads"
        files = sorted([f for f in downloads.iterdir() if f.is_file()],
                       key=lambda f: f.stat().st_mtime, reverse=True)[:count]
        return ("Recent downloads: " + " | ".join(f.name for f in files) + " sir.") if files else "Downloads empty sir."

    def open_incognito(self, url=""):
        import subprocess as _sp
        for b, flag, name in [
            (r"C:\Program Files\Google\Chrome\Application\chrome.exe","--incognito","Chrome"),
            (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe","--inprivate","Edge"),
        ]:
            if Path(b).exists():
                _sp.Popen([b, flag] + ([url] if url else []), creationflags=_sp.CREATE_NO_WINDOW)
                return f"Opening {name} incognito sir."
        return "No supported browser found sir."

    def clear_browser_cache(self):
        import os as _os, shutil as _sh
        cleared = 0
        for cache_dir in [
            Path(_os.environ.get("LOCALAPPDATA","")) / "Google/Chrome/User Data/Default/Cache",
            Path(_os.environ.get("LOCALAPPDATA","")) / "Microsoft/Edge/User Data/Default/Cache",
        ]:
            if cache_dir.exists():
                try: _sh.rmtree(str(cache_dir)); cleared += 1
                except: pass
        return f"Browser cache cleared ({cleared} browsers) sir."

    def check_ssl_cert(self, domain):
        try:
            import ssl, socket
            with ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.connect((domain, 443))
                cert = s.getpeercert()
                return f"SSL cert for {domain} valid until {cert.get('notAfter','?')} sir."
        except Exception as e:
            return f"SSL check failed: {e}"

    def get_process_tree(self, name):
        out = self._ps(f"Get-WmiObject Win32_Process | Where Name -like '*{name}*' | ForEach-Object {{$_.Name + ' PID:' + $_.ProcessId}}")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:6]
        return ("Process tree: " + " | ".join(lines)) if lines else f"No process matching {name} sir."

    def set_process_priority(self, name, priority="Normal"):
        priorities = {"low":"Idle","belownormal":"BelowNormal","normal":"Normal",
                      "abovenormal":"AboveNormal","high":"High","realtime":"RealTime"}
        p = priorities.get(priority.lower(), "Normal")
        self._ps(f"Get-Process '{name}' -EA SilentlyContinue | ForEach-Object {{$_.PriorityClass = '{p}'}}")
        return f"Set {name} priority to {p} sir."

    def open_remote_desktop(self, host):
        self._sh(f"mstsc /v:{host}")
        return f"Opening Remote Desktop to {host} sir."

    def get_environment_variable(self, name):
        import os as _os
        val = _os.environ.get(name,"")
        return f"{name} = {val}" if val else f"Variable {name} not set sir."

    def set_environment_variable(self, name, value):
        self._ps(f'[System.Environment]::SetEnvironmentVariable("{name}","{value}","User")')
        return f"Set {name} = {value} permanently sir."

    def generate_password_strong(self, length=16):
        import random, string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(random.choices(chars, k=int(length)))
        self._set_clipboard(pwd)
        return f"Password generated and copied ({length} chars) sir."

    def text_to_speech_file(self, text, filename="output.wav"):
        try:
            import pyttsx3 as _tts
            path = self.workspace / filename
            e = _tts.init(); e.save_to_file(text, str(path)); e.runAndWait(); e.stop()
            return f"Audio saved to {filename} sir."
        except Exception as e:
            return f"TTS failed: {e}"

    def get_disk_usage_by_folder(self, path=None):
        p = path or str(Path.home())
        out = self._ps(f'Get-ChildItem "{p}" -Directory -EA SilentlyContinue | ForEach-Object {{$s=0;Get-ChildItem $_.FullName -Recurse -File -EA SilentlyContinue | ForEach-Object{{$s+=$_.Length}};[math]::Round($s/1GB,2).ToString()+"GB "+$_.Name}} | Sort {{[double]($_ -split " ")[0]}} -Desc | Select -First 5')
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:5]
        return ("Disk usage: " + " | ".join(lines)) if lines else "Scan failed sir."

    def get_scheduled_tasks(self):
        out = self._ps("Get-ScheduledTask | Where State -ne Disabled | Select -ExpandProperty TaskName | Select -First 8")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:6]
        return ("Tasks: " + ", ".join(lines)) if lines else "No tasks sir."

    def check_windows_activation(self):
        out = self._ps("(Get-WmiObject SoftwareLicensingProduct | Where-Object {$_.PartialProductKey}).LicenseStatus")
        return "Windows is activated sir." if "1" in (out or "") else "Windows may not be activated sir."

    def _save_session_timestamp(self):
        import datetime as _dt
        try:
            if hasattr(self, "_memory_ref") and self._memory_ref:
                self._memory_ref.remember("system","last_session_end",_dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
        except: pass

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # CONTEXT-AWARE INTELLIGENCE
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def get_context_summary(self):
        """Return a snapshot of current system context."""
        import datetime as _dt
        cpu = self._ps("(Get-WmiObject Win32_Processor | Measure-Object LoadPercentage -Average).Average")
        bat = self.get_battery()
        now = _dt.datetime.now()
        parts = [
            f"Time: {now.strftime('%I:%M %p')}",
            f"CPU: {(cpu or '?').strip()}%",
            f"Battery: {bat}",
        ]
        try:
            pf = self.workspace / ".jarvis_projects.json"
            if pf.exists():
                reg = __import__('json').loads(pf.read_text())
                active = [k for k,v in reg.items() if v.get('status','active')=='active']
                if active: parts.append(f"Active projects: {', '.join(active[:3])}")
        except: pass
        return " | ".join(parts) + " sir."

    def get_window_title(self):
        """Get the title of the currently focused window."""
        out = self._ps("(Get-Process | Where MainWindowTitle -ne '' | Sort CPU -Desc | Select -First 1).MainWindowTitle")
        return (out.strip() if out else "No focused window found sir.")

    def get_active_user_sessions(self):
        """List active user sessions on this machine."""
        out = self._sh("query session 2>nul")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip() and ">" in l][:4]
        return ("Sessions: " + " | ".join(lines)) if lines else "No active sessions sir."

    def get_logon_history(self, days=7):
        """Get recent login history."""
        out = self._ps(f"Get-EventLog -LogName Security -InstanceId 4624 -Newest 10 -ErrorAction SilentlyContinue 2>$null | Select -ExpandProperty TimeGenerated | ForEach-Object {{$_.ToString('MM/dd HH:mm')}}")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:6]
        return ("Login events: " + ", ".join(lines)) if lines else "Login history unavailable sir."

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # ADVANCED FILE OPERATIONS
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def read_csv(self, path, rows=5):
        """Read and preview a CSV file."""
        try:
            import csv
            with open(path, newline='', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                data = [row for _, row in zip(range(rows+1), reader)]
            if not data: return "Empty CSV sir."
            header = ", ".join(data[0])
            preview = f"{len(data)-1} rows shown. Headers: {header}"
            return preview + " sir."
        except Exception as e:
            return f"CSV read failed: {e}"

    def write_csv(self, path, headers, rows_json):
        """Write data to a CSV file."""
        try:
            import csv, json as _j
            rows = _j.loads(rows_json) if isinstance(rows_json, str) else rows_json
            with open(path, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(headers.split(',') if isinstance(headers,str) else headers)
                w.writerows(rows)
            return f"CSV written to {path} sir."
        except Exception as e:
            return f"CSV write failed: {e}"

    def extract_zip(self, zip_path, dest=""):
        """Extract a zip archive."""
        import zipfile
        dest = dest or str(Path(zip_path).parent)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(dest)
        return f"Extracted {zip_path} to {dest} sir."

    def create_zip(self, source_dir, output_zip=""):
        """Create a zip from a directory."""
        import zipfile, os
        if not output_zip:
            output_zip = str(self.workspace / (Path(source_dir).name + ".zip"))
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    fp = os.path.join(root, file)
                    z.write(fp, os.path.relpath(fp, source_dir))
        return f"Archive created: {output_zip} sir."

    def find_text_in_files(self, search_text, directory=".", extension=".txt"):
        """Search for text across multiple files."""
        results = []
        for f in Path(directory).rglob(f"*{extension}"):
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                if search_text.lower() in content.lower():
                    # Find line number
                    for i, line in enumerate(content.splitlines(), 1):
                        if search_text.lower() in line.lower():
                            results.append(f"{f.name}:{i}")
                            break
            except: pass
        if not results: return f"'{search_text}' not found in {extension} files sir."
        return f"Found in {len(results)} files: " + ", ".join(results[:5]) + " sir."

    def replace_text_in_file(self, path, old_text, new_text):
        """Find and replace text in a file."""
        try:
            p = Path(path)
            content = p.read_text(encoding='utf-8', errors='ignore')
            count = content.count(old_text)
            if count == 0: return f"Text '{old_text}' not found in file sir."
            p.write_text(content.replace(old_text, new_text), encoding='utf-8')
            return f"Replaced {count} occurrence{'s' if count!=1 else ''} in {p.name} sir."
        except Exception as e:
            return f"Replace failed: {e}"

    def get_file_metadata(self, path):
        """Get detailed file metadata."""
        import datetime as _dt
        try:
            p = Path(path)
            st = p.stat()
            size_kb = round(st.st_size / 1024, 1)
            modified = _dt.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M')
            created  = _dt.datetime.fromtimestamp(st.st_ctime).strftime('%Y-%m-%d %H:%M')
            return f"{p.name}: {size_kb}KB | Modified: {modified} | Created: {created} sir."
        except Exception as e:
            return f"Metadata failed: {e}"

    def split_file(self, path, lines_per_chunk=100):
        """Split a large file into smaller chunks."""
        try:
            p = Path(path)
            all_lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
            chunks = [all_lines[i:i+lines_per_chunk] for i in range(0, len(all_lines), lines_per_chunk)]
            for i, chunk in enumerate(chunks):
                out = p.parent / f"{p.stem}_part{i+1}{p.suffix}"
                out.write_text('\n'.join(chunk), encoding='utf-8')
            return f"Split into {len(chunks)} files of {lines_per_chunk} lines sir."
        except Exception as e:
            return f"Split failed: {e}"

    def merge_files(self, file_list, output_path):
        """Merge multiple text files into one."""
        try:
            parts = [str(f).strip() for f in (file_list if isinstance(file_list,list) else file_list.split(','))]
            out_p = Path(output_path)
            content = []
            for fp in parts:
                p = Path(fp.strip())
                if p.exists():
                    content.append(p.read_text(encoding='utf-8', errors='ignore'))
            out_p.write_text('\n'.join(content), encoding='utf-8')
            return f"Merged {len(content)} files into {out_p.name} sir."
        except Exception as e:
            return f"Merge failed: {e}"

    def tail_file(self, path, lines=20):
        """Read the last N lines of a file."""
        try:
            all_lines = Path(path).read_text(encoding='utf-8', errors='ignore').splitlines()
            tail = all_lines[-lines:]
            return '\n'.join(tail) if tail else "File is empty sir."
        except Exception as e:
            return f"Failed: {e}"

    def head_file(self, path, lines=20):
        """Read the first N lines of a file."""
        try:
            all_lines = Path(path).read_text(encoding='utf-8', errors='ignore').splitlines()
            return '\n'.join(all_lines[:lines]) if all_lines else "File is empty sir."
        except Exception as e:
            return f"Failed: {e}"

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # SMART WEB & DATA
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def scrape_page_text(self, url):
        """Fetch clean text content from a URL."""
        try:
            import urllib.request as _ur, re as _re
            req = _ur.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            html = _ur.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
            # Strip tags
            text = _re.sub(r'<script[^>]*>.*?</script>', '', html, flags=_re.DOTALL)
            text = _re.sub(r'<style[^>]*>.*?</style>', '', text, flags=_re.DOTALL)
            text = _re.sub(r'<[^>]+>', ' ', text)
            text = _re.sub(r'\s+', ' ', text).strip()
            return text[:600] + "..." if len(text) > 600 else text
        except Exception as e:
            return f"Scrape failed: {e}"

    def get_wikipedia_summary(self, topic):
        """Get Wikipedia summary for a topic."""
        try:
            import urllib.request as _ur, urllib.parse as _up, json as _j
            topic_enc = _up.quote(topic.replace(' ','_'))
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic_enc}"
            req = _ur.Request(url, headers={'User-Agent':'JarvisBot/1.0'})
            data = _j.loads(_ur.urlopen(req, timeout=6).read())
            extract = data.get('extract', '')
            return extract[:300] + "..." if len(extract) > 300 else extract or f"No Wikipedia article found for {topic} sir."
        except Exception as e:
            return f"Wikipedia lookup failed: {e}"

    def get_github_trending(self, language=""):
        """Get trending GitHub repos."""
        try:
            import urllib.request as _ur, re as _re
            url = f"https://github.com/trending/{language}" if language else "https://github.com/trending"
            req = _ur.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            html = _ur.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
            repos = _re.findall(r'h2 class="h3[^"]*"[^>]*>\s*<a[^>]*>\s*([^\n<]+)\s*/\s*([^\n<]+)', html)
            if repos:
                names = [f"{u.strip()}/{r.strip()}" for u,r in repos[:5]]
                return "Trending: " + " | ".join(names) + " sir."
            return "Could not fetch trending repos sir."
        except Exception as e:
            return f"GitHub trending failed: {e}"

    def lookup_word(self, word):
        """Look up word definition, pronunciation, and examples."""
        try:
            import urllib.request as _ur, json as _j
            data = _j.loads(_ur.urlopen(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=5).read())
            entry = data[0]
            phonetic = entry.get('phonetic', '')
            meanings = entry.get('meanings', [])
            if meanings:
                m = meanings[0]
                pos = m.get('partOfSpeech','')
                defns = m.get('definitions',[])
                defn = defns[0].get('definition','') if defns else ''
                example = defns[0].get('example','') if defns else ''
                result = f"{word} ({phonetic}) â€” {pos}: {defn}"
                if example: result += f' Example: "{example}"'
                return result[:250] + " sir."
            return f"No definition found for {word} sir."
        except Exception as e:
            return f"Definition lookup failed: {e}"

    def get_exchange_rates(self, base="USD"):
        """Get current exchange rates for major currencies."""
        try:
            import urllib.request as _ur, json as _j
            data = _j.loads(_ur.urlopen(f"https://api.exchangerate-api.com/v4/latest/{base}", timeout=5).read())
            rates = data.get('rates', {})
            pairs = ["EUR","GBP","CAD","JPY","AUD","CHF","CNY"]
            parts = [f"{c}: {rates[c]:.3f}" for c in pairs if c in rates]
            return f"{base} rates â€” " + " | ".join(parts) + " sir."
        except Exception as e:
            return f"Exchange rates unavailable: {e}"

    def check_website_status(self, url):
        """Check if a website is up and response time."""
        import urllib.request as _ur, time as _t
        if not url.startswith('http'): url = 'https://' + url
        try:
            t0 = _t.time()
            r = _ur.urlopen(_ur.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=8)
            ms = int((_t.time()-t0)*1000)
            return f"{url} is UP â€” {r.status} ({ms}ms) sir."
        except Exception as e:
            return f"{url} appears to be DOWN: {e} sir."

    def get_hacker_news(self, count=5):
        """Get top Hacker News stories."""
        try:
            import urllib.request as _ur, json as _j
            ids = _j.loads(_ur.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=5).read())[:count]
            stories = []
            for sid in ids:
                item = _j.loads(_ur.urlopen(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=3).read())
                stories.append(item.get('title','?')[:50])
            return "HN Top: " + " | ".join(stories) + " sir."
        except Exception as e:
            return f"Hacker News unavailable: {e}"

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # ADVANCED SYSTEM AUTOMATION
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def kill_high_cpu_processes(self, threshold=80):
        """Kill any process using more than threshold% CPU."""
        import psutil
        killed = []
        safe = {'system','svchost','lsass','csrss','wininit','services','smss',
                'registry','memory compression','jarvis','python','pythonw'}
        for p in psutil.process_iter(['name','cpu_percent','pid']):
            try:
                cpu = p.info.get('cpu_percent') or 0
                name = (p.info.get('name') or '').lower()
                if cpu > threshold and not any(s in name for s in safe):
                    p.kill()
                    killed.append(f"{p.info['name']}({cpu:.0f}%)")
            except: pass
        return (f"Killed {len(killed)}: " + ", ".join(killed)) if killed else f"No processes above {threshold}% CPU sir."

    def free_memory(self):
        """Aggressively free up RAM by clearing working sets."""
        self._ps("Get-Process | Where WorkingSet -gt 100MB | ForEach-Object {$_.MinWorkingSet = 0; $_.MaxWorkingSet = [IntPtr]::MaxValue}")
        self._sh("RamMap -Ew")  # if RamMap installed
        return "Working sets trimmed to free RAM sir."

    def list_autostart_programs(self):
        """List all autostart programs from registry and startup folders."""
        out1 = self._ps('Get-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" | Get-Member -MemberType NoteProperty | Where Name -notlike "PS*" | Select -ExpandProperty Name')
        out2 = self._ps('Get-ItemProperty "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" | Get-Member -MemberType NoteProperty | Where Name -notlike "PS*" | Select -ExpandProperty Name')
        names = []
        for out in [out1, out2]:
            names += [l.strip() for l in (out or "").splitlines() if l.strip()]
        return ("Autostart: " + ", ".join(names[:10])) if names else "No autostart programs sir."

    def set_screen_timeout(self, minutes):
        """Set screen off timeout in minutes."""
        secs = int(minutes) * 60
        self._sh(f"powercfg /change monitor-timeout-ac {minutes}")
        self._sh(f"powercfg /change monitor-timeout-dc {minutes}")
        return f"Screen timeout set to {minutes} minutes sir."

    def enable_remote_desktop(self):
        """Enable Windows Remote Desktop."""
        self._ps('Set-ItemProperty -Path "HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server" -Name fDenyTSConnections -Value 0')
        self._sh("netsh advfirewall firewall set rule group=\"Remote Desktop\" new enable=Yes")
        return "Remote Desktop enabled sir."

    def disable_remote_desktop(self):
        """Disable Windows Remote Desktop."""
        self._ps('Set-ItemProperty -Path "HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server" -Name fDenyTSConnections -Value 1')
        return "Remote Desktop disabled sir."

    def get_system_uptime(self):
        """Get system uptime in human-readable format."""
        import psutil, datetime as _dt
        boot = _dt.datetime.fromtimestamp(psutil.boot_time())
        up = _dt.datetime.now() - boot
        h, rem = divmod(int(up.total_seconds()), 3600)
        m = rem // 60
        return f"System uptime: {h} hours {m} minutes (since {boot.strftime('%b %d %I:%M %p')}) sir."

    def get_installed_software(self, search=""):
        """List installed software, optionally filtered."""
        out = self._ps('Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select DisplayName,DisplayVersion | Where DisplayName -ne $null | ForEach-Object {$_.DisplayName + " " + $_.DisplayVersion}')
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()]
        if search:
            lines = [l for l in lines if search.lower() in l.lower()]
        return (f"Found {len(lines)}: " + " | ".join(lines[:6])) if lines else f"No software matching '{search}' sir."

    def check_windows_updates(self):
        """Check for pending Windows updates."""
        out = self._ps("(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search('IsInstalled=0').Updates.Count")
        count = (out or "0").strip()
        return f"{count} pending Windows updates sir." if count != "0" else "Windows is up to date sir."

    def get_startup_time(self):
        """Get Windows boot time and last startup duration."""
        out = self._ps("(Get-EventLog System -InstanceId 12 -Newest 1 -ErrorAction SilentlyContinue).TimeGenerated")
        return f"Last boot: {(out or 'unavailable').strip()} sir."

    def run_disk_cleanup(self):
        """Run Windows Disk Cleanup utility silently."""
        import threading
        def _run():
            self._sh("cleanmgr /sagerun:1 /quiet")
        threading.Thread(target=_run, daemon=True).start()
        return "Disk cleanup started in background sir."

    def get_memory_usage_detail(self):
        """Detailed memory usage breakdown."""
        import psutil
        vm = psutil.virtual_memory()
        sw = psutil.swap_memory()
        return (f"RAM: {vm.used//1024//1024}MB used of {vm.total//1024//1024}MB "
                f"({vm.percent}%) | Swap: {sw.used//1024//1024}MB of {sw.total//1024//1024}MB sir.")

    def monitor_file_changes(self, path, seconds=15):
        """Watch for file changes in a directory for N seconds."""
        import threading, time as _t
        changes = []
        def _watch():
            try:
                snap = {str(f): f.stat().st_mtime for f in Path(path).rglob('*') if f.is_file()}
                _t.sleep(seconds)
                for f in Path(path).rglob('*'):
                    if f.is_file():
                        k = str(f)
                        if k not in snap: changes.append(f"+ {f.name}")
                        elif f.stat().st_mtime != snap[k]: changes.append(f"~ {f.name}")
                for k in snap:
                    if not Path(k).exists(): changes.append(f"- {Path(k).name}")
            except: pass
        t = threading.Thread(target=_watch, daemon=True)
        t.start(); t.join(seconds + 2)
        return (f"{len(changes)} changes: " + ", ".join(changes[:5])) if changes else f"No changes in {path} sir."

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # DEVELOPER & CODE INTELLIGENCE
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def count_code_by_language(self, path="."):
        """Count lines of code per language in a project."""
        exts = {'.py':'Python','.js':'JavaScript','.ts':'TypeScript','.html':'HTML',
                '.css':'CSS','.java':'Java','.cpp':'C++','.c':'C','.rs':'Rust',
                '.go':'Go','.rb':'Ruby','.php':'PHP','.swift':'Swift'}
        counts = {}
        for f in Path(path).rglob('*'):
            if f.is_file() and f.suffix in exts:
                lang = exts[f.suffix]
                try:
                    lines = len(f.read_text(encoding='utf-8', errors='ignore').splitlines())
                    counts[lang] = counts.get(lang, 0) + lines
                except: pass
        if not counts: return "No source files found sir."
        total = sum(counts.values())
        sorted_c = sorted(counts.items(), key=lambda x: -x[1])
        parts = [f"{lang}: {n:,}" for lang, n in sorted_c[:5]]
        return f"Total {total:,} lines â€” " + " | ".join(parts) + " sir."

    def lint_python(self, path):
        """Run pyflakes lint check on a Python file."""
        import sys as _sys
        out = self._sh(f'"{_sys.executable}" -m pyflakes "{path}" 2>&1')
        if not out: return f"No issues found in {Path(path).name} sir."
        lines = out.strip().splitlines()
        return f"{len(lines)} issue(s): " + lines[0][:100] + " sir."

    def format_python(self, path):
        """Auto-format a Python file using autopep8 or black."""
        import sys as _sys, shutil as _sh
        if _sh.which("black"):
            out = self._sh(f'black "{path}" 2>&1')
            return f"Formatted with black: {Path(path).name} sir."
        elif _sh.which("autopep8"):
            out = self._sh(f'autopep8 --in-place "{path}"')
            return f"Formatted with autopep8: {Path(path).name} sir."
        else:
            out = self._sh(f'"{_sys.executable}" -m autopep8 --in-place "{path}" 2>&1')
            return f"Formatted {Path(path).name} sir."

    def profile_python(self, path, top=5):
        """Profile a Python script and show slowest functions."""
        import sys as _sys
        out = self._sh(f'"{_sys.executable}" -m cProfile -s cumulative "{path}" 2>&1')
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][4:4+top]
        return ("Profile top " + str(top) + ": " + " | ".join(lines)) if lines else "Profile failed sir."

    def generate_requirements(self, path="."):
        """Generate requirements.txt from a Python project."""
        import sys as _sys
        out = self._sh(f'"{_sys.executable}" -m pipreqs "{path}" --force 2>&1')
        req = Path(path) / "requirements.txt"
        if req.exists():
            deps = req.read_text().strip().splitlines()
            return f"requirements.txt generated with {len(deps)} packages sir."
        return (out[:150] if out else "pipreqs not installed. Run: pip install pipreqs sir.")

    def check_api_health(self, url):
        """Check if an API endpoint is healthy."""
        try:
            import urllib.request as _ur, time as _t, json as _j
            t0 = _t.time()
            req = _ur.Request(url, headers={'User-Agent':'JarvisBot/1.0'})
            r = _ur.urlopen(req, timeout=5)
            ms = int((_t.time()-t0)*1000)
            body = r.read()[:100].decode('utf-8', errors='ignore')
            return f"API {url} â€” {r.status} OK ({ms}ms). Response: {body[:50]} sir."
        except Exception as e:
            return f"API {url} unhealthy: {e}"

    def start_python_repl(self):
        """Open Python REPL in a new terminal."""
        import subprocess as _sp
        _sp.Popen(f'start cmd /k "{__import__("sys").executable}"', shell=True)
        return "Python REPL opened in new terminal sir."

    def create_venv(self, path=".", name="venv"):
        """Create a Python virtual environment."""
        import sys as _sys
        full_path = Path(path) / name
        out = self._sh(f'"{_sys.executable}" -m venv "{full_path}"')
        return f"Virtual environment created at {full_path} sir."

    def activate_venv(self, path):
        """Show how to activate a virtual environment."""
        activate = Path(path) / "Scripts" / "activate.bat"
        if activate.exists():
            import subprocess as _sp
            _sp.Popen(f'start cmd /k "{activate}"', shell=True)
            return f"Opened terminal with venv activated at {path} sir."
        return f"No venv found at {path} sir."

    def get_python_version(self):
        """Get Python version info."""
        import sys as _sys
        return f"Python {_sys.version.split()[0]} at {_sys.executable} sir."

    def list_pip_packages(self, filter_str=""):
        """List installed pip packages."""
        import sys as _sys
        out = self._sh(f'"{_sys.executable}" -m pip list --format=columns 2>&1')
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][2:]
        if filter_str:
            lines = [l for l in lines if filter_str.lower() in l.lower()]
        return f"{len(lines)} packages" + (f" matching '{filter_str}'" if filter_str else "") + ": " + ", ".join(l.split()[0] for l in lines[:8]) + " sir."

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # PRODUCTIVITY & SMART NOTES
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def smart_note(self, title, content, tags=""):
        """Create a tagged, timestamped markdown note."""
        import datetime as _dt, json as _j
        notes_dir = self.workspace / "notes"
        notes_dir.mkdir(exist_ok=True)
        now = _dt.datetime.now()
        slug = title.lower().replace(' ', '_')[:20]
        fname = f"{now.strftime('%Y%m%d_%H%M')}_{slug}.md"
        md = f"# {title}\n_Created: {now.strftime('%B %d, %Y %I:%M %p')}_ | Tags: {tags}\n\n{content}\n"
        (notes_dir / fname).write_text(md, encoding='utf-8')
        # Update notes index
        idx = notes_dir / "index.json"
        index = _j.loads(idx.read_text()) if idx.exists() else []
        index.append({"title": title, "file": fname, "date": now.isoformat(), "tags": tags})
        idx.write_text(_j.dumps(index, indent=2))
        return f"Note '{title}' saved to {fname} sir."

    def search_smart_notes(self, query):
        """Search notes by content or tags."""
        notes_dir = self.workspace / "notes"
        if not notes_dir.exists(): return "No notes directory sir."
        results = []
        for f in notes_dir.glob("*.md"):
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                if query.lower() in content.lower():
                    title = content.splitlines()[0].replace('# ','')[:30]
                    results.append(title)
            except: pass
        return (f"Found {len(results)} notes: " + ", ".join(results[:5])) if results else f"No notes matching '{query}' sir."

    def list_smart_notes(self, count=8):
        """List recent notes."""
        notes_dir = self.workspace / "notes"
        if not notes_dir.exists(): return "No notes yet sir."
        files = sorted(notes_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)[:count]
        if not files: return "No notes yet sir."
        names = [f.stem for f in files]
        return f"{len(files)} notes: " + " | ".join(names) + " sir."

    def daily_journal(self, entry=""):
        """Add to today's daily journal."""
        import datetime as _dt
        journal_dir = self.workspace / "journal"
        journal_dir.mkdir(exist_ok=True)
        today = _dt.datetime.now()
        fname = journal_dir / f"{today.strftime('%Y-%m-%d')}.md"
        header = f"# Journal â€” {today.strftime('%B %d, %Y')}\n\n" if not fname.exists() else ""
        timestamp = today.strftime('%I:%M %p')
        line = f"\n**{timestamp}** â€” {entry}\n" if entry else f"\n**{timestamp}** â€” [session start]\n"
        with open(fname, 'a', encoding='utf-8') as f:
            f.write(header + line)
        return f"Journal entry added to {fname.name} sir."

    def get_todo_stats(self):
        """Get TODO statistics."""
        try:
            import json as _j
            f = Path.home() / ".jarvis_todo.json"
            if not f.exists(): return "No todos on file sir."
            todos = _j.loads(f.read_text())
            total = len(todos)
            done = sum(1 for t in todos if t.get('done'))
            pending = total - done
            overdue = 0
            import datetime as _dt
            now = _dt.datetime.now()
            for t in todos:
                if not t.get('done') and t.get('due'):
                    try:
                        due = _dt.datetime.strptime(t['due'], '%Y-%m-%d')
                        if due < now: overdue += 1
                    except: pass
            return f"TODOs: {total} total, {done} done, {pending} pending, {overdue} overdue sir."
        except Exception as e:
            return f"Todo stats failed: {e}"

    def add_todo_with_due(self, task, due_date=""):
        """Add a todo with optional due date (YYYY-MM-DD)."""
        import json as _j, datetime as _dt
        f = Path.home() / ".jarvis_todo.json"
        todos = _j.loads(f.read_text()) if f.exists() else []
        entry = {"task": task, "done": False, "created": _dt.datetime.now().isoformat()}
        if due_date: entry["due"] = due_date
        todos.append(entry)
        f.write_text(_j.dumps(todos, indent=2))
        return f"Added: {task}" + (f" (due {due_date})" if due_date else "") + " sir."

    def set_priority_todo(self, index, priority="high"):
        """Set priority on a todo item."""
        import json as _j
        f = Path.home() / ".jarvis_todo.json"
        todos = _j.loads(f.read_text()) if f.exists() else []
        idx = int(index) - 1
        if 0 <= idx < len(todos):
            todos[idx]['priority'] = priority
            f.write_text(_j.dumps(todos, indent=2))
            return f"Priority '{priority}' set on: {todos[idx]['task'][:40]} sir."
        return "Invalid todo index sir."

    def clear_completed_todos(self):
        """Remove all completed todo items."""
        import json as _j
        f = Path.home() / ".jarvis_todo.json"
        todos = _j.loads(f.read_text()) if f.exists() else []
        before = len(todos)
        todos = [t for t in todos if not t.get('done')]
        f.write_text(_j.dumps(todos, indent=2))
        cleared = before - len(todos)
        return f"Cleared {cleared} completed todo{'s' if cleared!=1 else ''} sir."

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # ADVANCED MEMORY & LEARNING
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def learn_preference(self, key, value):
        """Store a user preference that persists across sessions."""
        try:
            if hasattr(self, '_memory_ref') and self._memory_ref:
                self._memory_ref.remember('preferences', key, value)
                return f"Preference noted: {key} = {value} sir."
        except: pass
        return "Memory not initialized sir."

    def recall_preference(self, key):
        """Recall a stored preference."""
        try:
            if hasattr(self, '_memory_ref') and self._memory_ref:
                val = self._memory_ref.recall(key)
                return f"{key}: {val} sir." if val else f"No preference stored for {key} sir."
        except: pass
        return "Memory not initialized sir."

    def add_rule(self, rule):
        """Add a permanent standing rule for JARVIS behavior."""
        try:
            if hasattr(self, '_memory_ref') and self._memory_ref:
                self._memory_ref.add_rule(rule)
                return f"Rule added: {rule} sir."
        except: pass
        return "Memory not initialized sir."

    def list_rules(self):
        """List all standing rules."""
        try:
            if hasattr(self, '_memory_ref') and self._memory_ref:
                rules = self._memory_ref.data.get('rules', [])
                if not rules: return "No standing rules on file sir."
                return "Rules: " + " | ".join(r.get('rule','') for r in rules[:6]) + " sir."
        except: pass
        return "Memory not initialized sir."

    def get_session_stats(self):
        """Get stats about this JARVIS session."""
        import datetime as _dt
        try:
            if hasattr(self, '_memory_ref') and self._memory_ref:
                last = self._memory_ref.data.get('facts', {}).get('last_session_end', 'unknown')
                rules = len(self._memory_ref.data.get('rules', []))
                facts = len(self._memory_ref.data.get('facts', {}))
                return f"Memory: {rules} rules, {facts} facts. Last session ended: {last} sir."
        except: pass
        return "No session data available sir."

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # CREATIVE & FUN
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def write_haiku(self, topic):
        """Write a haiku about a topic (returned for brain to generate)."""
        return f"Haiku topic queued: {topic}. Brain will compose sir."

    def get_motivation(self):
        """Get a motivational quote."""
        import random
        quotes = [
            "The only way to do great work is to love what you do. â€” Jobs",
            "It always seems impossible until it's done. â€” Mandela",
            "Done is better than perfect. â€” Zuckerberg",
            "First, solve the problem. Then, write the code. â€” Johnson",
            "Code is like humor. When you have to explain it, it's bad. â€” Fowler",
            "Programs must be written for people to read. â€” Abelson",
            "The best time to plant a tree was 20 years ago. The second best time is now.",
            "Simplicity is the soul of efficiency. â€” Austin Freeman",
            "Make it work, make it right, make it fast. â€” Beck",
            "The secret to getting ahead is getting started. â€” Twain",
        ]
        return random.choice(quotes) + " sir."

    def roast_me(self):
        """Roast the user lightly."""
        import random
        roasts = [
            "You've asked me that same question three times this week sir. I'm not judging, but I am logging it.",
            "If your code ran as fast as you procrastinate, we'd have a problem sir.",
            "I see you've opened seventeen browser tabs again sir. Admirable optimism.",
            "Another late night sir. The coffee won't save you.",
            "You really typed that and hit enter sir. Remarkable.",
            "I've seen better organization in a crashed hard drive sir. With respect.",
        ]
        return random.choice(roasts)

    def tell_tech_joke(self):
        """Tell a tech joke."""
        import random
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
            "Why did the programmer quit his job? He didn't get arrays.",
            "There are 10 types of people â€” those who understand binary and those who don't.",
            "How many programmers does it take to change a lightbulb? None, that's a hardware problem.",
            "Why do Java developers wear glasses? Because they don't C sharp.",
            "A byte walks into a bar looking pale. The bartender asks: What's wrong? Bit error.",
            "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        ]
        return random.choice(jokes) + " sir."

    def simon_says(self, command):
        """Execute a command prefixed with 'Simon says'."""
        return f"Simon says: {command}. Running it sir."

    def count_down(self, from_n, to=0):
        """Count down and speak."""
        n = int(from_n)
        items = list(range(n, int(to)-1, -1))
        return "Counting down: " + ", ".join(str(i) for i in items) + ". Done sir."

    def birthday_reminder(self, name, date_str):
        """Set an annual birthday reminder."""
        import datetime as _dt, json as _j
        f = Path.home() / ".jarvis_birthdays.json"
        bdays = _j.loads(f.read_text()) if f.exists() else {}
        bdays[name] = date_str
        f.write_text(_j.dumps(bdays, indent=2))
        return f"Birthday for {name} on {date_str} saved sir."

    def check_birthdays_today(self):
        """Check if any birthdays are today or upcoming."""
        import datetime as _dt, json as _j
        f = Path.home() / ".jarvis_birthdays.json"
        if not f.exists(): return "No birthdays on file sir."
        bdays = _j.loads(f.read_text())
        now = _dt.datetime.now()
        results = []
        for name, date_str in bdays.items():
            try:
                dob = _dt.datetime.strptime(date_str, "%Y-%m-%d")
                this_year = dob.replace(year=now.year)
                diff = (this_year - now).days
                if diff == 0: results.append(f"TODAY: {name}!")
                elif 0 < diff <= 7: results.append(f"{name} in {diff} days")
            except: pass
        return ("Birthdays: " + " | ".join(results)) if results else "No birthdays in the next 7 days sir."

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # HEALTH & WELLBEING
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

    def log_water_intake(self, glasses=1):
        """Log water intake for the day."""
        import datetime as _dt, json as _j
        f = Path.home() / ".jarvis_health.json"
        data = _j.loads(f.read_text()) if f.exists() else {}
        today = _dt.date.today().isoformat()
        data.setdefault('water', {})
        data['water'][today] = data['water'].get(today, 0) + int(glasses)
        f.write_text(_j.dumps(data, indent=2))
        total = data['water'][today]
        msg = f"Water logged. {total} glass{'es' if total!=1 else ''} today sir."
        if total >= 8: msg += " Hydration goal met!"
        return msg

    def get_health_summary(self):
        """Get today's health log summary."""
        import datetime as _dt, json as _j
        f = Path.home() / ".jarvis_health.json"
        if not f.exists(): return "No health data logged sir."
        data = _j.loads(f.read_text())
        today = _dt.date.today().isoformat()
        water = data.get('water', {}).get(today, 0)
        screen = data.get('screen_time', {}).get(today, 0)
        return f"Today: {water} glasses of water, {screen}min screen time tracked sir."

    def set_stretch_reminder(self, interval_mins=60):
        """Set recurring stretch reminders."""
        secs = int(interval_mins) * 60
        def _remind():
            import time as _t
            count = 0
            while count < 8:
                _t.sleep(secs)
                if hasattr(self, '_reminder_cb') and self._reminder_cb:
                    self._reminder_cb(f"Time to stretch sir. You've been sitting for {interval_mins} minutes.")
                count += 1
        import threading
        threading.Thread(target=_remind, daemon=True).start()
        return f"Stretch reminders set every {interval_mins} minutes for 8 hours sir."

    def log_mood(self, mood, note=""):
        """Log current mood with optional note."""
        import datetime as _dt, json as _j
        f = Path.home() / ".jarvis_mood.json"
        data = _j.loads(f.read_text()) if f.exists() else []
        entry = {"time": _dt.datetime.now().isoformat(), "mood": mood, "note": note}
        data.append(entry)
        f.write_text(_j.dumps(data, indent=2))
        responses = {"great":"Excellent sir.","good":"Good to hear sir.","okay":"Noted sir.",
                     "tired":"Rest when you can sir.","stressed":"Take a breath sir.","bad":"I'm sorry to hear that sir."}
        return responses.get(mood.lower(), f"Mood '{mood}' logged sir.")

    def get_mood_history(self, days=7):
        """Get mood log for the past N days."""
        import datetime as _dt, json as _j
        f = Path.home() / ".jarvis_mood.json"
        if not f.exists(): return "No mood history sir."
        data = _j.loads(f.read_text())
        cutoff = (_dt.datetime.now() - _dt.timedelta(days=days)).isoformat()
        recent = [e for e in data if e.get('time','') >= cutoff]
        if not recent: return f"No mood entries in last {days} days sir."
        moods = [e.get('mood','?') for e in recent[-8:]]
        return f"Mood log ({len(recent)} entries): " + " â†’ ".join(moods) + " sir."


    def list_bluetooth_devices(self):
        """List paired Bluetooth devices."""
        out = self._ps("Get-PnpDevice -Class Bluetooth | Where Status -eq OK | Select -ExpandProperty FriendlyName 2>$null")
        lines = [l.strip() for l in (out or "").splitlines() if l.strip()][:6]
        return ("Bluetooth: " + ", ".join(lines)) if lines else "No Bluetooth devices found sir."

    def openclaw_switch(self):
        """Toggle OpenClaw on/off and update config."""
        cfg_path = Path.home() / ".jarvis_config.json"
        try:
            cfg = json.loads(cfg_path.read_text())
            cfg["use_openclaw"] = not cfg.get("use_openclaw", False)
            cfg_path.write_text(json.dumps(cfg, indent=2))
            state = "enabled" if cfg["use_openclaw"] else "disabled"
            return f"OpenClaw mode {state}. Restart Jarvis to apply sir."
        except Exception as e:
            return f"Config error: {e}"

    def openclaw_status(self):
        """Check if OpenClaw gateway is running."""
        try:
            import urllib.request as _ur
            _ur.urlopen("http://127.0.0.1:18789/", timeout=2)
            return "OpenClaw gateway is online sir."
        except:
            return "OpenClaw gateway is offline. Run: openclaw gateway start"

    def get_daily_goal(self):
        """Get today's daily goal."""
        import datetime as _dt
        try:
            gf = Path.home() / ".jarvis_goals.json"
            if not gf.exists(): return "No goal set for today sir."
            goals = json.loads(gf.read_text())
            today = _dt.datetime.now().strftime("%Y-%m-%d")
            goal = goals.get(today, {}).get("goal", "")
            return f"Today's goal: {goal} sir." if goal else "No goal set for today sir."
        except: return "Goal data unavailable sir."

    def set_daily_goal(self, goal):
        """Set today's daily goal."""
        import datetime as _dt
        gf = Path.home() / ".jarvis_goals.json"
        goals = json.loads(gf.read_text()) if gf.exists() else {}
        today = _dt.datetime.now().strftime("%Y-%m-%d")
        goals[today] = {"goal": goal, "set": _dt.datetime.now().isoformat()}
        gf.write_text(json.dumps(goals, indent=2))
        return f"Goal set: {goal} sir."

    def calendar_today(self):
        """Get today's calendar events (alias)."""
        return self.get_todays_events()

    def calendar_tomorrow(self):
        """Get tomorrow's calendar events."""
        svc, err = self._gcal_service()
        if err: return err
        import datetime as _dt
        tomorrow = _dt.datetime.now().astimezone() + _dt.timedelta(days=1)
        start = tomorrow.replace(hour=0,minute=0,second=0,microsecond=0).isoformat()
        end   = tomorrow.replace(hour=23,minute=59,second=59,microsecond=0).isoformat()
        result = svc.events().list(calendarId="primary",
            timeMin=start, timeMax=end, singleEvents=True,
            orderBy="startTime", timeZone="America/New_York").execute()
        events = result.get("items",[])
        if not events: return "Nothing on the calendar tomorrow sir."
        parts = []
        for e in events[:5]:
            name = e.get("summary","Unnamed")
            start2 = e.get("start",{}).get("dateTime",e.get("start",{}).get("date",""))
            if "T" in start2:
                t = start2.split("T")[1][:5]
                parts.append(f"{name} at {t}")
            else:
                parts.append(name)
        return f"Tomorrow you have {len(events)} event{'s' if len(events)>1 else ''}: " + ", ".join(parts) + "."

    def calendar_week_overview(self):
        """Get this week's events overview."""
        return self.get_upcoming_events(days=7)

    def calendar_next_event(self):
        """Get the very next upcoming event."""
        svc, err = self._gcal_service()
        if err: return err
        import datetime as _dt
        now = _dt.datetime.now().astimezone()
        result = svc.events().list(calendarId="primary",
            timeMin=now.isoformat(),
            singleEvents=True, orderBy="startTime",
            maxResults=1, timeZone="America/New_York").execute()
        events = result.get("items",[])
        if not events: return "No upcoming events sir."
        e = events[0]
        name = e.get("summary","Unnamed")
        start2 = e.get("start",{}).get("dateTime",e.get("start",{}).get("date",""))
        if "T" in start2:
            import datetime as _dt2
            dt = _dt2.datetime.fromisoformat(start2.replace("Z","+00:00"))
            local_dt = dt.astimezone()
            return f"Next event: {name} at {local_dt.strftime('%I:%M %p')} sir."
        return f"Next event: {name} on {start2} sir."

    def calendar_find_free_time(self, duration_hours=1):
        """Find next free time slot."""
        svc, err = self._gcal_service()
        if err: return err
        import datetime as _dt
        now = _dt.datetime.now().astimezone()
        end = (now + _dt.timedelta(days=3)).isoformat()
        result = svc.events().list(calendarId="primary",
            timeMin=now.isoformat(), timeMax=end,
            singleEvents=True, orderBy="startTime", maxResults=20, timeZone="America/New_York").execute()
        events = result.get("items",[])
        # Find gaps
        busy = []
        for e in events:
            s = e.get("start",{}).get("dateTime","")
            en = e.get("end",{}).get("dateTime","")
            if s and en:
                try:
                    busy.append((_dt.datetime.fromisoformat(s.replace("Z","+00:00")),
                                 _dt.datetime.fromisoformat(en.replace("Z","+00:00"))))
                except: pass
        busy.sort()
        check = now
        for start_b, end_b in busy:
            gap = (start_b - check).total_seconds() / 3600
            if gap >= float(duration_hours):
                return f"You have {gap:.1f} hours free starting now sir."
            check = max(check, end_b)
        return f"No clear {duration_hours}h slot in the next 3 days sir."

    def calendar_date(self, date_str):
        """Get events for a specific date string like 'monday', 'tomorrow', '2025-12-25'."""
        import datetime as _dt
        now = _dt.datetime.now().astimezone()
        # Parse natural language dates
        ds = date_str.lower().strip()
        days_map = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}
        if ds == "today":
            target = now.date()
        elif ds == "tomorrow":
            target = (now + _dt.timedelta(days=1)).date()
        elif ds in days_map:
            days_ahead = days_map[ds] - now.weekday()
            if days_ahead <= 0: days_ahead += 7
            target = (now + _dt.timedelta(days=days_ahead)).date()
        else:
            try:
                target = _dt.date.fromisoformat(date_str)
            except:
                return f"Could not parse date '{date_str}' sir."
        svc, err = self._gcal_service()
        if err: return err
        base_tz = now.tzinfo
        start = _dt.datetime.combine(target, _dt.time.min, tzinfo=base_tz).isoformat()
        end   = _dt.datetime.combine(target, _dt.time.max, tzinfo=base_tz).isoformat()
        result = svc.events().list(calendarId="primary",
            timeMin=start, timeMax=end, singleEvents=True,
            orderBy="startTime", timeZone="America/New_York").execute()
        events = result.get("items",[])
        day_name = target.strftime("%A %B %d")
        if not events: return f"Nothing on {day_name} sir."
        parts = []
        for e in events[:5]:
            name = e.get("summary","Unnamed")
            start2 = e.get("start",{}).get("dateTime","")
            if "T" in start2:
                t = start2.split("T")[1][:5]
                parts.append(f"{name} at {t}")
            else:
                parts.append(name)
        return f"{day_name}: " + ", ".join(parts) + "."

    def calendar_busiest_day(self):
        """Find which day this week has most events."""
        svc, err = self._gcal_service()
        if err: return err
        import datetime as _dt
        now = _dt.datetime.now().astimezone()
        end = (now + _dt.timedelta(days=7)).isoformat()
        result = svc.events().list(calendarId="primary",
            timeMin=now.isoformat(), timeMax=end,
            singleEvents=True, orderBy="startTime", maxResults=50, timeZone="America/New_York").execute()
        events = result.get("items",[])
        counts = {}
        for e in events:
            start2 = e.get("start",{}).get("dateTime",e.get("start",{}).get("date",""))
            day = start2[:10] if start2 else ""
            if day: counts[day] = counts.get(day,0) + 1
        if not counts: return "No events this week sir."
        busiest = max(counts, key=counts.get)
        try:
            d = _dt.date.fromisoformat(busiest)
            return f"Busiest day is {d.strftime('%A')} with {counts[busiest]} events sir."
        except:
            return f"Busiest day: {busiest} with {counts[busiest]} events sir."

    def _calendar_events_window(self, start_dt, end_dt, max_results=50, query=""):
        """Fetch events in a window as normalized dicts."""
        svc, err = self._gcal_service()
        if err:
            return None, err
        params = {
            "calendarId": "primary",
            "timeMin": start_dt.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "timeMax": end_dt.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "singleEvents": True,
            "orderBy": "startTime",
            "maxResults": int(max_results),
        }
        if query:
            params["q"] = query
        result = svc.events().list(**params).execute()
        return result.get("items", []), None

    def _calendar_event_local_start(self, event):
        s = event.get("start", {}).get("dateTime")
        if not s:
            return None
        try:
            return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone()
        except Exception:
            return None

    def calendar_schedule_summary(self):
        """Smart summary of calendar load, next event, and busy windows."""
        now = datetime.datetime.now().astimezone()
        end = now + datetime.timedelta(days=7)
        events, err = self._calendar_events_window(now, end, max_results=80)
        if err:
            return err
        if not events:
            return "Your next seven days are clear sir. No scheduled events."

        total = len(events)
        today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        day_counts = {}
        today_count = 0
        tomorrow_count = 0
        next_event_name = ""
        next_event_time = ""

        for e in events:
            st = self._calendar_event_local_start(e)
            if st:
                d = st.date()
                day_counts[d] = day_counts.get(d, 0) + 1
                if d == today:
                    today_count += 1
                if d == tomorrow:
                    tomorrow_count += 1
                if not next_event_name and st >= now:
                    next_event_name = e.get("summary", "Unnamed event")
                    next_event_time = st.strftime("%A at %I:%M %p")
            else:
                ds = e.get("start", {}).get("date", "")
                if ds:
                    try:
                        d = datetime.date.fromisoformat(ds)
                        day_counts[d] = day_counts.get(d, 0) + 1
                        if d == today:
                            today_count += 1
                        if d == tomorrow:
                            tomorrow_count += 1
                    except Exception:
                        pass

        busiest_day = max(day_counts, key=day_counts.get) if day_counts else None
        busiest_phrase = ""
        if busiest_day:
            busiest_phrase = f"Busiest day is {busiest_day.strftime('%A')} with {day_counts[busiest_day]} events."

        next_phrase = f"Your next event is {next_event_name} {next_event_time}." if next_event_name else "No timed events remain this week."
        return (
            f"You have {total} events over the next seven days. "
            f"Today has {today_count}, tomorrow has {tomorrow_count}. "
            f"{busiest_phrase} {next_phrase}"
        ).strip()

    def calendar_upcoming(self, days=7):
        """Tool alias for upcoming events."""
        return self.get_upcoming_events(days=days)

    def calendar_add_event(self, title, date, time_str="09:00", duration_hours=1):
        """Tool alias for calendar add."""
        return self.add_calendar_event(title=title, date_str=date, time_str=time_str, duration_hours=duration_hours)

    def calendar_delete_event(self, title):
        """Delete the next matching event by title."""
        now = datetime.datetime.now().astimezone()
        end = now + datetime.timedelta(days=90)
        events, err = self._calendar_events_window(now, end, max_results=30, query=title)
        if err:
            return err
        if not events:
            return f"No calendar event matching '{title}' found sir."

        match = None
        tl = title.lower().strip()
        for e in events:
            name = e.get("summary", "").lower().strip()
            if name == tl:
                match = e
                break
        if match is None:
            match = events[0]

        svc, err2 = self._gcal_service()
        if err2:
            return err2
        try:
            svc.events().delete(calendarId="primary", eventId=match["id"]).execute()
            return f"Deleted event '{match.get('summary','Unnamed event')}' sir."
        except Exception as e:
            return f"Could not delete event sir: {e}"

    def calendar_reschedule_event(self, title, new_date, new_time="09:00"):
        """Reschedule next matching event while preserving its duration."""
        now = datetime.datetime.now().astimezone()
        end = now + datetime.timedelta(days=90)
        events, err = self._calendar_events_window(now, end, max_results=30, query=title)
        if err:
            return err
        if not events:
            return f"No event matching '{title}' found to reschedule sir."

        match = None
        tl = title.lower().strip()
        for e in events:
            if e.get("summary", "").lower().strip() == tl:
                match = e
                break
        if match is None:
            match = events[0]

        try:
            old_start_raw = match.get("start", {}).get("dateTime")
            old_end_raw = match.get("end", {}).get("dateTime")
            if old_start_raw and old_end_raw:
                old_start = datetime.datetime.fromisoformat(old_start_raw.replace("Z", "+00:00"))
                old_end = datetime.datetime.fromisoformat(old_end_raw.replace("Z", "+00:00"))
                dur = old_end - old_start
            else:
                dur = datetime.timedelta(hours=1)
            start_local = datetime.datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M").astimezone()
            end_local = start_local + dur
        except Exception:
            return "Use date format YYYY-MM-DD and time format HH:MM in twenty-four hour time sir."

        svc, err2 = self._gcal_service()
        if err2:
            return err2
        try:
            match["start"] = {"dateTime": start_local.isoformat(), "timeZone": str(start_local.tzinfo)}
            match["end"] = {"dateTime": end_local.isoformat(), "timeZone": str(end_local.tzinfo)}
            svc.events().update(calendarId="primary", eventId=match["id"], body=match).execute()
            return f"Rescheduled '{match.get('summary','event')}' to {start_local.strftime('%A %B %d at %I:%M %p')} sir."
        except Exception as e:
            return f"Could not reschedule event sir: {e}"

    def calendar_smart_reminder(self, event_query):
        """Set a reminder for the next matching upcoming event."""
        now = datetime.datetime.now().astimezone()
        end = now + datetime.timedelta(days=30)
        events, err = self._calendar_events_window(now, end, max_results=20, query=event_query)
        if err:
            return err
        if not events:
            return f"I cannot find an upcoming event matching '{event_query}' sir."

        target = events[0]
        for e in events:
            st = self._calendar_event_local_start(e)
            if st and st >= now:
                target = e
                break

        start_dt = self._calendar_event_local_start(target)
        if not start_dt:
            return f"I found '{target.get('summary','that event')}' but it is an all-day item, so no timed reminder was set sir."

        lead = datetime.timedelta(minutes=15)
        remind_at = start_dt - lead
        secs = int((remind_at - now).total_seconds())
        if secs <= 5:
            return f"{target.get('summary','That event')} starts very soon sir. No lead time left for a fifteen minute reminder."

        message = f"{target.get('summary','Event')} starts in fifteen minutes."
        self.set_reminder(message, secs)
        return f"Reminder armed for {target.get('summary','that event')} at {remind_at.strftime('%I:%M %p')} sir."

    def calendar_understand(self, query):
        """Interpret natural calendar questions and return the best calendar response."""
        q = (query or "").lower()
        if not q:
            return self.calendar_schedule_summary()
        if "why" in q and ("off" in q or "day off" in q or "school" in q):
            return self.school_off_reason(query)
        if "off" in q and any(x in q for x in ["friday","monday","tuesday","wednesday","thursday","saturday","sunday","today","tomorrow","this "]):
            return self.school_off_query(query)
        if "school" in q and any(x in q for x in ["friday","monday","tuesday","wednesday","thursday","saturday","sunday","today","tomorrow","this ","next ","coming "]):
            return self.school_day_brief(query)

        if any(x in q for x in ["next event", "what's next", "whats next", "coming up next"]):
            return self.calendar_next_event()
        if any(x in q for x in ["tomorrow", "calendar tomorrow"]):
            return self.calendar_tomorrow()
        if any(x in q for x in ["this week", "week overview", "week summary", "schedule summary"]):
            return self.calendar_schedule_summary()
        if "busiest day" in q or "most busy day" in q:
            return self.calendar_busiest_day()
        if "free" in q or "available" in q:
            dur = 1.0
            m = re.search(r"(\d+(?:\.\d+)?)\s*(hour|hr|h)", q)
            if m:
                try:
                    dur = float(m.group(1))
                except Exception:
                    dur = 1.0
            return self.calendar_find_free_time(duration_hours=dur)

        for day_name in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "today"]:
            if day_name in q:
                return self.calendar_date(day_name)
        if re.search(r"\b\d{4}-\d{2}-\d{2}\b", q):
            ds = re.search(r"\b\d{4}-\d{2}-\d{2}\b", q).group(0)
            return self.calendar_date(ds)

        if any(x in q for x in ["calendar", "schedule", "events"]):
            return self.calendar_schedule_summary()
        return "Tell me what window you want: today, tomorrow, next event, this week, or when you are free."

    def _school_calendar_url(self):
        try:
            cfg = load_config()
            return cfg.get("school_calendar_ics", DEFAULT_CONFIG.get("school_calendar_ics", ""))
        except Exception:
            return DEFAULT_CONFIG.get("school_calendar_ics", "")

    def _parse_ics_dt_to_date(self, raw):
        s = (raw or "").strip()
        if not s:
            return None
        try:
            if len(s) == 8 and s.isdigit():
                return datetime.datetime.strptime(s, "%Y%m%d").date()
            s2 = s.rstrip("Z")
            if "T" in s2:
                dt = datetime.datetime.strptime(s2[:15], "%Y%m%dT%H%M%S")
                return dt.date()
        except Exception:
            return None
        return None

    def _school_calendar_events(self):
        """Fetch and parse public school ICS with small cache."""
        if time.time() - self._school_ics_cache_ts < 600 and self._school_ics_cache:
            return self._school_ics_cache, None
        url = self._school_calendar_url()
        if not url:
            return [], "School calendar URL is not configured sir."
        try:
            sess = requests.Session()
            sess.trust_env = False  # ignore broken system proxy settings
            r = sess.get(url, timeout=8, proxies={"http": None, "https": None})
            r.raise_for_status()
            text = r.text
        except Exception as e:
            return [], f"Could not reach school calendar feed: {e}"

        # Unfold ICS lines (continuation lines start with whitespace)
        lines = text.splitlines()
        unfolded = []
        for ln in lines:
            if ln.startswith(" ") or ln.startswith("\t"):
                if unfolded:
                    unfolded[-1] += ln[1:]
            else:
                unfolded.append(ln)

        events = []
        cur = None
        for ln in unfolded:
            if ln.startswith("BEGIN:VEVENT"):
                cur = {}
                continue
            if ln.startswith("END:VEVENT"):
                if cur and cur.get("start_date"):
                    events.append(cur)
                cur = None
                continue
            if cur is None:
                continue
            if ln.startswith("SUMMARY"):
                cur["summary"] = ln.split(":", 1)[1].strip() if ":" in ln else ""
            elif ln.startswith("DTSTART"):
                dt_raw = ln.split(":", 1)[1].strip() if ":" in ln else ""
                cur["start_date"] = self._parse_ics_dt_to_date(dt_raw)
            elif ln.startswith("DTEND"):
                dt_raw = ln.split(":", 1)[1].strip() if ":" in ln else ""
                cur["end_date"] = self._parse_ics_dt_to_date(dt_raw)

        self._school_ics_cache = events
        self._school_ics_cache_ts = time.time()
        return events, None

    def _resolve_query_date(self, query):
        q = (query or "").lower()
        now = datetime.datetime.now().date()
        weekdays = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        if "today" in q:
            return now
        if "tomorrow" in q:
            return now + datetime.timedelta(days=1)
        m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", q)
        if m:
            try:
                return datetime.date.fromisoformat(m.group(1))
            except Exception:
                pass
        for name, idx in weekdays.items():
            if name in q:
                delta = idx - now.weekday()
                if "next " in q:
                    if delta <= 0:
                        delta += 7
                    delta += 7
                elif "this " in q:
                    if delta < 0:
                        delta += 7
                elif "coming " in q:
                    if delta < 0:
                        delta += 7
                else:
                    if delta <= 0:
                        delta += 7
                return now + datetime.timedelta(days=delta)
        return now

    def school_off_query(self, query):
        """
        Answer school day-off questions from public ICS feed.
        Rule: PA day or holiday means day off.
        """
        target = self._resolve_query_date(query)
        events, err = self._school_calendar_events()
        if err:
            return err
        day_events = []
        for e in events:
            sd = e.get("start_date")
            ed = e.get("end_date")
            if not sd:
                continue
            # ICS DTEND for all-day events is usually exclusive.
            if ed:
                if sd <= target < ed:
                    day_events.append(e)
            else:
                if sd == target:
                    day_events.append(e)

        names = " | ".join((e.get("summary", "") or "").lower() for e in day_events)
        names_norm = re.sub(r"[^a-z0-9]+", " ", names).strip()
        off_keywords = [
            "holiday", "holidays", "pa day", "p a day", "professional activity",
            "school closed", "no school", "winter break", "march break", "summer break",
            "labour day", "labor day", "thanksgiving", "christmas break", "spring break",
            "good friday", "easter monday"
        ]
        is_off = any(k in names or k in names_norm for k in off_keywords)
        self._last_school_off = {
            "target": target.isoformat(),
            "events": [e.get("summary", "") for e in day_events],
            "is_off": bool(is_off),
            "ts": time.time(),
        }
        day_label = target.strftime("%A, %B %d")
        event_names = [e.get("summary", "") for e in day_events if e.get("summary")]
        event_brief = ", ".join(event_names[:3])
        if is_off:
            if event_brief:
                return f"Yes sir. {day_label} is a day off because the calendar lists: {event_brief}."
            return f"Yes sir. {day_label} is marked as a day off."
        if day_events:
            return f"No sir. {day_label} is not marked off. The calendar shows: {event_brief}."
        return f"No off-day marker found for {day_label} sir."

    def school_day_brief(self, query):
        """Summarize school calendar entries for the requested day."""
        target = self._resolve_query_date(query)
        events, err = self._school_calendar_events()
        if err:
            return err
        day_events = []
        for e in events:
            sd = e.get("start_date")
            ed = e.get("end_date")
            if not sd:
                continue
            if ed:
                if sd <= target < ed:
                    day_events.append(e)
            else:
                if sd == target:
                    day_events.append(e)
        day_label = target.strftime("%A, %B %d")
        if not day_events:
            return f"No school calendar entries were found for {day_label} sir."
        names = [e.get("summary", "Unnamed event").strip() for e in day_events]
        self._last_school_off = {
            "target": target.isoformat(),
            "events": names,
            "is_off": any("off" in n.lower() or "holiday" in n.lower() or "pa day" in n.lower() for n in names),
            "ts": time.time(),
        }
        return f"School calendar for {day_label}: " + "; ".join(names[:5]) + "."

    def school_off_reason(self, query=""):
        """Explain why a school day was marked off (or not)."""
        target = None
        if query and any(x in query.lower() for x in ["today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "this ", "next ", "coming ", "20"]):
            target = self._resolve_query_date(query)
            _ = self.school_off_query(query)
        elif self._last_school_off.get("target"):
            try:
                target = datetime.date.fromisoformat(self._last_school_off.get("target"))
            except Exception:
                target = None
        if not target:
            return "I can explain, but I need the day. For example: why is this Friday off?"

        events = self._last_school_off.get("events", []) or []
        is_off = bool(self._last_school_off.get("is_off"))
        day_label = target.strftime("%A, %B %d")
        if is_off:
            if events:
                return f"Because {day_label} includes this school calendar entry: {', '.join(events[:3])}."
            return f"Because {day_label} is flagged as a non-school day in your school calendar."
        if events:
            return f"{day_label} is not marked as a day off. It has: {', '.join(events[:3])}."
        return f"{day_label} has no off-day marker in the school calendar feed."


    def add_feature(self, feature_description):
        """Write and hot-reload a new method into Jarvis."""
        import anthropic as _ant, ast as _ast
        cfg = load_config()
        client = _ant.Anthropic(api_key=cfg["anthropic_api_key"])

        prompt = (
            "Output ONLY a Python method body. No explanation. No markdown. No backticks.\n"
            "Indent with exactly 4 spaces (class method style).\n"
            "Class name: PCTools. Available: os,sys,json,time,threading,subprocess,\n"
            "shutil,datetime,random,webbrowser,requests,psutil,Path,re,load_config\n"
            "Shell commands: self._sh(\"cmd\")\n"
            "Return a plain English string result.\n"
            "\n"
            "EXAMPLE OUTPUT:\n"
            "    def say_hello(self, name):\n"
            "        return \"Hello \" + name + \", sir.\"\n"
            "\n"
            "Write a method for: " + feature_description
        )
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = resp.content[0].text.strip()
        # Strip any markdown fences
        new_code = re.sub(r"```[a-zA-Z]*\n?", "", raw).replace("```", "").strip()
        # If model forgot the 4-space indent, add it
        if new_code.startswith("def "):
            new_code = "\n".join("    " + l for l in new_code.split("\n"))
        # Find first def if there is preamble text
        if not new_code.startswith("    def "):
            m = re.search(r"(    def [a-zA-Z_][^\n]*(?:\n(?!    def )[^\n]*)*)", new_code)
            if m: new_code = m.group(0).rstrip()

        # Try to parse, with multiple recovery attempts
        for attempt in range(3):
            try:
                _ast.parse("class _T:\n" + new_code)
                break  # success
            except SyntaxError:
                if attempt == 0:
                    # Add 4-space indent to any unindented lines
                    new_code = "\n".join(("    " + l) if l.strip() and not l.startswith(" ") else l for l in new_code.split("\n"))
                elif attempt == 1:
                    # Re-extract from scratch
                    m2 = re.search(r"    def [a-zA-Z_][\s\S]+", new_code)
                    if m2: new_code = m2.group(0)
                    else: return "Could not generate valid code sir. Try rephrasing."
                else:
                    return "Generated code had syntax errors sir. Try rephrasing your request."

        method_names = re.findall(r"    def ([a-zA-Z_][a-zA-Z0-9_]*)\(", new_code)
        if not method_names:
            return "Could not find a valid method in the generated code sir."

        jarvis_path = Path(__file__).resolve()
        source = jarvis_path.read_text(encoding="utf-8")

        inject_marker = chr(32)*4 + "# @@" + "INJECT_METHODS@@"
        tools_marker  = "    # @@TOOLS_INJECT_HERE@@ â€” injected tool entries above this line, do not remove"

        if inject_marker not in source:
            return "Injection point missing sir. Cannot add feature."

        new_source = source.replace(inject_marker, new_code + "\n\n" + inject_marker)

        tool_entries = ""
        for mn in method_names:
            desc = mn.replace("_", " ").capitalize() + " (custom feature)"
            tool_entries += '    {"name":"' + mn + '","description":"' + desc + '","input_schema":{"type":"object","properties":{}}},\n'

        if tools_marker in new_source:
            new_source = new_source.replace(tools_marker, tool_entries + tools_marker)

        jarvis_path.write_text(new_source, encoding="utf-8")

        exec_globals = {
            "os":os,"sys":sys,"json":json,"time":time,"threading":threading,
            "subprocess":subprocess,"platform":platform,"shutil":shutil,
            "datetime":datetime,"random":random,"webbrowser":webbrowser,
            "socket":socket,"hashlib":hashlib,"requests":requests,"psutil":psutil,
            "Path":Path,"re":re,"load_config":load_config,
        }
        try:
            exec("class _Tmp:\n" + new_code, exec_globals)
            for mn in method_names:
                setattr(self.__class__, mn, getattr(exec_globals["_Tmp"], mn))
        except Exception as e:
            return "Saved to disk but hot-reload failed sir: " + str(e) + ". Restart to use it."

        return "Feature added and live sir. " + " and ".join(method_names) + " ready to use right now."

    def list_added_features(self):
        jarvis_path = Path(__file__).resolve()
        source = jarvis_path.read_text(encoding="utf-8")
        marker = chr(32)*4 + "# @@" + "INJECT_METHODS@@"
        before = source.split(marker)[0]
        all_methods = re.findall(r"    def ([a-zA-Z_][a-zA-Z0-9_]*)\(self", before)
        base = {
            "_r","_sh","_ps","_send_media_key","_set_clipboard","_send_keys",
            "_spotify_running","_launch_spotify_bg","_minimize_spotify",
            "create_file","read_file","write_file","append_file","delete_file","rename_file",
            "move_file","copy_file","file_exists","file_size","count_lines","list_directory",
            "create_directory","delete_directory","search_files","zip_directory","get_file_info",
            "find_duplicates","system_info","cpu_info","memory_info","disk_info","network_info",
            "list_processes","kill_process","kill_process_by_name","get_time","get_uptime",
            "get_battery","get_hostname","get_username","get_local_ip","get_public_ip","ping",
            "check_internet","list_drives","list_open_ports","list_startup_programs","watch_cpu",
            "daily_briefing","run_command","run_powershell","open_file","open_url","open_app",
            "close_app","search_web","search_youtube","open_calculator","open_notepad",
            "open_task_manager","open_file_explorer","open_settings","open_control_panel",
            "open_device_manager","open_github","open_discord","discord_toggle_mute","discord_toggle_deafen",
            "discord_open_channel","discord_quick_dm","spotify_search_play","spotify_pause",
            "spotify_next","spotify_prev","fetch_and_show_image","image_search_browser",
            "get_weather","get_forecast","calculate","convert_units","define_word","get_joke",
            "get_fact","get_quote","get_crypto_price","get_news","get_stock_info","speed_test",
            "take_note","read_notes","clear_notes","search_notes","add_to_todo","read_todo",
            "complete_todo","set_reminder","set_alarm","start_timer","get_clipboard",
            "set_clipboard_text","take_screenshot","paste_code","fix_code_in_clipboard",
            "explain_code_in_clipboard","press_key","save_current_file","undo","switch_window",
            "summarize_url","translate_text","shutdown_pc","restart_pc","cancel_shutdown",
            "sleep_pc","lock_pc","mute_volume","volume_up","volume_down","empty_recycle_bin",
            "check_for_updates","flush_dns","list_wifi_networks","get_wifi_password",
            "run_python_file","create_python_script","git_status","git_commit","git_push",
            "roast_process","add_feature","list_added_features","remove_feature",
            "mission_start","mission_clear","mission_status","mission_next_action","mission_why","mission_apply_template",
        }
        added = [m for m in all_methods if m not in base]
        if not added: return "No custom features added yet sir."
        return "You have " + str(len(added)) + " custom features: " + ", ".join(added) + "."

    def remove_feature(self, method_name):
        jarvis_path = Path(__file__).resolve()
        source = jarvis_path.read_text(encoding="utf-8")
        pattern = r"(    def " + re.escape(method_name) + r"\(self[^)]*\):.*?)(?=\n    def [a-zA-Z_]|\n\n    # @@)"
        new_source = re.sub(pattern, "", source, flags=re.DOTALL)
        if new_source == source: return "Method " + method_name + " not found sir."
        jarvis_path.write_text(new_source, encoding="utf-8")
        if hasattr(self.__class__, method_name):
            try: delattr(self.__class__, method_name)
            except: pass
        return "Feature " + method_name + " removed sir."

    def deep_dive(self, name="", email="", username="", phone="", image_path=""):
        eng = _get_deep_dive()
        if not eng:
            return "Deep dive engine unavailable. Install: pip install aiohttp beautifulsoup4"
        dossier = eng.run_deep_dive(name=name, email=email, username=username, phone=phone, image_path=image_path)
        self._last_dossier = dossier
        try:
            report_path = Path.home() / ".jarvis_deep_dive_report.json"
            report_path.write_text(json.dumps(dossier, indent=2, default=str), encoding="utf-8")
            text_report = eng.format_dossier_for_text(dossier)
            _write_hud("speaking", text="Deep dive complete. Report saved.", tool="deep_dive",
                       hud_mode="deep_dive", hud_data={"content": text_report[:2000], "target": dossier.get("target","")})
        except:
            pass
        return eng.format_dossier_for_speech(dossier)

    # --- Browser Agent ---
    def browser_start(self):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable. Install: pip install playwright && playwright install chromium"
        return agent.start()

    def browser_stop(self):
        agent = _get_browser()
        if not agent:
            return "No browser instance."
        return agent.stop()

    def browser_navigate(self, url):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable. Say browser start first."
        return agent.navigate(url)

    def browser_search(self, engine, query):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable. Say browser start first."
        return agent.search(engine, query)

    def browser_read(self):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable."
        return agent.read_page()

    def browser_screenshot(self):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable."
        path = agent.screenshot()
        if path and Path(path).exists():
            import os; os.startfile(str(path))
        return f"Screenshot saved to {path}" if path else "Failed to screenshot."

    def browser_click(self, text):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable."
        return agent.click_text(text)

    def browser_type(self, selector, text):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable."
        return agent.type_text(selector, text)

    def browser_scroll(self, amount="1"):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable."
        return agent.scroll_down(int(amount))

    def browser_back(self):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable."
        return agent.go_back()

    def browser_get_links(self):
        agent = _get_browser()
        if not agent:
            return "Browser agent unavailable."
        return agent.get_links()

    # --- Webcam Surveillance ---
    def surveillance_start(self):
        surv = _get_surveillance()
        if not surv:
            return "Surveillance unavailable. Install: pip install opencv-python numpy"
        def _alert(msg, path):
            _write_hud("alert", text=msg, tool="surveillance",
                       hud_mode="alert", hud_data={"message": msg, "level": "warning", "path": path})
        return surv.start(alert_callback=_alert)

    def surveillance_stop(self):
        surv = _get_surveillance()
        if not surv:
            return "No surveillance instance."
        return surv.stop()

    def surveillance_status(self):
        surv = _get_surveillance()
        if not surv:
            return "Surveillance not active."
        return surv.status()

    def surveillance_list(self):
        surv = _get_surveillance()
        if not surv:
            return "Surveillance not active."
        return surv.list_captures()

    def surveillance_sensitivity(self, level):
        surv = _get_surveillance()
        if not surv:
            return "Surveillance not active."
        return surv.set_sensitivity(level)

    # --- Gesture Control ---
    def gesture_start(self):
        g = _get_gesture()
        if not g:
            return "Gesture control unavailable. Install: pip install mediapipe pyautogui opencv-python"
        return g.start()

    def gesture_stop(self):
        g = _get_gesture()
        if not g:
            return "No gesture instance."
        return g.stop()

    def gesture_status(self):
        g = _get_gesture()
        if not g:
            return "Gesture control unavailable."
        return g.status()

    # --- Screen Ghost ---
    def ghost_start(self, interval="5"):
        g = _get_ghost()
        if not g:
            return "Screen ghost unavailable. Install: pip install mss pytesseract pygetwindow"
        return g.start(int(interval))

    def ghost_stop(self):
        g = _get_ghost()
        if not g:
            return "No ghost instance."
        return g.stop()

    def ghost_search(self, query):
        g = _get_ghost()
        if not g:
            return "Screen ghost unavailable."
        return g.search(query)

    def ghost_recent(self, minutes="5"):
        g = _get_ghost()
        if not g:
            return "Screen ghost unavailable."
        return g.recent(int(minutes))

    def ghost_status(self):
        g = _get_ghost()
        if not g:
            return "Screen ghost unavailable."
        return g.status()

    def ghost_clear(self):
        g = _get_ghost()
        if not g:
            return "Screen ghost unavailable."
        return g.clear()

    # --- Network Ghost ---
    def network_scan(self, target="192.168.1.0/24"):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.scan_network(target)

    def port_scan(self, host, ports="1-1024"):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.port_scan(host, ports)

    def wifi_list(self):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.list_wifi()

    def wifi_password(self, ssid):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.get_wifi_password(ssid)

    def wifi_current(self):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.get_current_connection()

    def traceroute_host(self, host):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.traceroute(host)

    def public_ip_info(self):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.public_ip_info()

    def dns_lookup(self, domain):
        ng = _get_netghost()
        if not ng:
            return "Network ghost unavailable."
        return ng.dns_lookup(domain)

    # --- Telegram OSINT ---
    def telegram_check_phone(self, phone):
        tg = _get_tg()
        if not tg:
            return "Telegram intel unavailable."
        return tg.format_phone_result(tg.check_phone(phone))

    def telegram_lookup(self, username):
        tg = _get_tg()
        if not tg:
            return "Telegram intel unavailable."
        return tg.format_username_result(tg.lookup_username(username))

    def telegram_search(self, name):
        tg = _get_tg()
        if not tg:
            return "Telegram intel unavailable."
        return tg.search_by_name(name)

    # --- Voice Cloner ---
    def voice_list(self):
        vc = _get_cloner()
        if not vc:
            return "Voice cloner unavailable."
        return vc.list_available_voices()

    def voice_set(self, voice_name):
        vc = _get_cloner()
        if not vc:
            return "Voice cloner unavailable."
        return vc.set_voice(voice_name)

    def voice_clone(self, name, audio_path=""):
        vc = _get_cloner()
        if not vc:
            return "Voice cloner unavailable."
        return vc.clone_voice(name, audio_path)

    def voice_current(self):
        vc = _get_cloner()
        if not vc:
            return "Voice cloner unavailable."
        return vc.get_active_voice()

    def voice_speak(self, text, voice=""):
        vc = _get_cloner()
        if not vc:
            return "Voice cloner unavailable."
        return vc.speak_with_voice(text, voice or None)

    # --- USB Sentinel ---
    def usb_list(self):
        usb = _get_usb()
        if not usb:
            return "USB sentinel unavailable."
        return usb.list_devices()

    def usb_monitor_start(self):
        usb = _get_usb()
        if not usb:
            return "USB sentinel unavailable."
        def _alert(msg):
            _write_hud("alert", text=msg, tool="usb", hud_mode="alert", hud_data={"message": msg, "level": "warning"})
        return usb.start_monitoring(alert_callback=_alert)

    def usb_monitor_stop(self):
        usb = _get_usb()
        if not usb:
            return "USB sentinel unavailable."
        return usb.stop_monitoring()

    def usb_storage(self):
        usb = _get_usb()
        if not usb:
            return "USB sentinel unavailable."
        return usb.get_storage_devices()

    # --- Event Log Analyzer ---
    def security_log(self, hours=24):
        el = _get_logs()
        if not el:
            return "Event log analyzer unavailable."
        return el.security_log(int(hours))

    def system_log(self, hours=24):
        el = _get_logs()
        if not el:
            return "Event log analyzer unavailable."
        return el.system_log(int(hours))

    def application_log(self, hours=24):
        el = _get_logs()
        if not el:
            return "Event log analyzer unavailable."
        return el.application_log(int(hours))

    def login_attempts(self, hours=24):
        el = _get_logs()
        if not el:
            return "Event log analyzer unavailable."
        return el.login_attempts(int(hours))

    def full_audit(self):
        el = _get_logs()
        if not el:
            return "Event log analyzer unavailable."
        return el.full_audit()

    # --- Process Watcher ---
    def proc_watch_start(self):
        pw = _get_procwatch()
        if not pw:
            return "Process watcher unavailable."
        def _alert(msg):
            _write_hud("alert", text=msg, tool="procwatch", hud_mode="alert", hud_data={"message": msg, "level": "warning"})
        return pw.start(alert_callback=_alert)

    def proc_watch_stop(self):
        pw = _get_procwatch()
        if not pw:
            return "Process watcher unavailable."
        return pw.stop()

    def proc_top(self, count=10):
        pw = _get_procwatch()
        if not pw:
            return "Process watcher unavailable."
        return pw.top_processes(int(count))

    def proc_kill_suspicious(self):
        pw = _get_procwatch()
        if not pw:
            return "Process watcher unavailable."
        return pw.kill_suspicious()

    def proc_info(self, name):
        pw = _get_procwatch()
        if not pw:
            return "Process watcher unavailable."
        return pw.process_info(name)

    # --- Auto-Git ---
    def git_status(self):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable. Is Git installed at C:\\Program Files\\Git\\bin\\git.exe?"
        return ag.status()

    def git_commit(self, message=""):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable."
        return ag.commit_and_push(message)

    def git_push(self):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable."
        return ag.push()

    def git_log(self, count=5):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable."
        return ag.log(int(count))

    def git_auto_enable(self):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable."
        return ag.enable_auto()

    def git_auto_disable(self):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable."
        return ag.disable_auto()

    def git_auto_status(self):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable."
        return ag.auto_status()

    def git_diff(self):
        ag = _get_autogit()
        if not ag:
            return "Auto-git unavailable."
        return ag.diff()

    # --- Command Macros + Media ---
    def self_edit(self, file_name, old_text, new_text):
        """JARVIS modifies his own source code and restarts."""
        jarvis_dir = Path(__file__).resolve().parent
        target = jarvis_dir / file_name
        if not target.exists():
            return f"File {file_name} not found."
        if not target.name.endswith(('.py', '.pyw', '.bat', '.html', '.js', '.css')):
            return "Can only edit JARVIS source files."
        try:
            content = target.read_text(encoding="utf-8")
            if old_text not in content:
                return f"Old text not found in {file_name}."
            new_content = content.replace(old_text, new_text)
            target.write_text(new_content, encoding="utf-8")
            return f"Modified {file_name}. Say 'restart yourself' to apply."
        except Exception as e:
            return f"Edit failed: {e}"

    def self_restart(self):
        """Restart JARVIS completely."""
        _write_hud("shutdown")
        subprocess.Popen(
            ["powershell", "-Command",
             "Start-Sleep 1; Start-Process pythonw -ArgumentList 'JARVIS.pyw' -WorkingDirectory (Get-Location)"],
            cwd=str(Path(__file__).resolve().parent),
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
        )
        os._exit(0)

    # --- Command Macros + Media ---
    def macro_run(self, name):
        me = _get_macros()
        if not me: return "Macros engine unavailable."
        return me.run(name)

    def macro_list(self):
        me = _get_macros()
        if not me: return "Macros engine unavailable."
        return me.list()

    def macro_add(self, name, actions):
        me = _get_macros()
        if not me: return "Macros engine unavailable."
        return me.add(name, actions)

    def macro_delete(self, name):
        me = _get_macros()
        if not me: return "Macros engine unavailable."
        return me.delete(name)

    def summarize_media(self, url):
        me = _get_macros()
        if not me: return "Macros engine unavailable."
        return me.summarize_media(url)

    # --- Clipboard History ---
    def clip_start(self):
        ch = _get_clipboard()
        if not ch: return "Clipboard history unavailable. pip install pyperclip"
        return ch.start()

    def clip_stop(self):
        ch = _get_clipboard()
        if not ch: return "No clipboard instance."
        return ch.stop()

    def clip_search(self, query):
        ch = _get_clipboard()
        if not ch: return "Clipboard history unavailable."
        return ch.search(query)

    def clip_recent(self, count=5):
        ch = _get_clipboard()
        if not ch: return "Clipboard history unavailable."
        return ch.recent(int(count))

    def clip_get(self, clip_id):
        ch = _get_clipboard()
        if not ch: return "Clipboard history unavailable."
        return ch.get_by_id(int(clip_id))

    def clip_stats(self):
        ch = _get_clipboard()
        if not ch: return "Clipboard history unavailable."
        return ch.stats()

    def clip_clear(self):
        ch = _get_clipboard()
        if not ch: return "Clipboard history unavailable."
        return ch.clear()

    # --- ReAct Agent ---
    def react_run(self, goal):
        ra = _get_react()
        if not ra: return "ReAct agent unavailable."
        brain_ref = getattr(self, '_brain_ref', None)
        voice_ref = getattr(self, '_voice_ref', None)
        if not brain_ref: return "No brain reference available."
        return ra.execute(goal, brain_ref, voice_ref)


# â”€â”€ Tools List â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
TOOLS = [
    {"name":"create_file","description":"Create file","input_schema":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string","default":""}},"required":["path"]}},
    {"name":"read_file","description":"Read file","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"write_file","description":"Overwrite file","input_schema":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}},
    {"name":"append_file","description":"Append to file","input_schema":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}},
    {"name":"delete_file","description":"Delete file","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"rename_file","description":"Rename file","input_schema":{"type":"object","properties":{"path":{"type":"string"},"new_name":{"type":"string"}},"required":["path","new_name"]}},
    {"name":"move_file","description":"Move file","input_schema":{"type":"object","properties":{"src":{"type":"string"},"dst":{"type":"string"}},"required":["src","dst"]}},
    {"name":"copy_file","description":"Copy file","input_schema":{"type":"object","properties":{"src":{"type":"string"},"dst":{"type":"string"}},"required":["src","dst"]}},
    {"name":"file_exists","description":"File exists?","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"file_size","description":"File size","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"count_lines","description":"Count lines","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"list_directory","description":"List directory","input_schema":{"type":"object","properties":{"path":{"type":"string","default":"."}}}},
    {"name":"create_directory","description":"Create dir","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"delete_directory","description":"Delete dir","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"search_files","description":"Search files","input_schema":{"type":"object","properties":{"pattern":{"type":"string"},"directory":{"type":"string","default":"."}},"required":["pattern"]}},
    {"name":"zip_directory","description":"Zip directory","input_schema":{"type":"object","properties":{"path":{"type":"string"},"output":{"type":"string","default":""}},"required":["path"]}},
    {"name":"get_file_info","description":"File info","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"find_duplicates","description":"Find duplicates","input_schema":{"type":"object","properties":{"directory":{"type":"string","default":"."}}}},
    {"name":"system_info","description":"System stats","input_schema":{"type":"object","properties":{}}},
    {"name":"cpu_info","description":"CPU info","input_schema":{"type":"object","properties":{}}},
    {"name":"memory_info","description":"RAM info","input_schema":{"type":"object","properties":{}}},
    {"name":"disk_info","description":"Disk usage","input_schema":{"type":"object","properties":{}}},
    {"name":"network_info","description":"Network stats","input_schema":{"type":"object","properties":{}}},
    {"name":"list_processes","description":"Top processes","input_schema":{"type":"object","properties":{"count":{"type":"integer","default":10}}}},
    {"name":"kill_process","description":"Kill by PID","input_schema":{"type":"object","properties":{"pid":{"type":"integer"}},"required":["pid"]}},
    {"name":"kill_process_by_name","description":"Kill by name","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"get_time","description":"Current time","input_schema":{"type":"object","properties":{}}},
    {"name":"get_uptime","description":"Uptime","input_schema":{"type":"object","properties":{}}},
    {"name":"get_battery","description":"Battery","input_schema":{"type":"object","properties":{}}},
    {"name":"get_hostname","description":"Hostname","input_schema":{"type":"object","properties":{}}},
    {"name":"get_username","description":"Username","input_schema":{"type":"object","properties":{}}},
    {"name":"get_local_ip","description":"Local IP","input_schema":{"type":"object","properties":{}}},
    {"name":"get_public_ip","description":"Public IP","input_schema":{"type":"object","properties":{}}},
    {"name":"ping","description":"Ping a host","input_schema":{"type":"object","properties":{"host":{"type":"string"}},"required":["host"]}},
    {"name":"check_internet","description":"Check internet","input_schema":{"type":"object","properties":{}}},
    {"name":"list_drives","description":"List drives","input_schema":{"type":"object","properties":{}}},
    {"name":"list_open_ports","description":"Open ports","input_schema":{"type":"object","properties":{}}},
    {"name":"list_startup_programs","description":"Startup programs","input_schema":{"type":"object","properties":{}}},
    {"name":"watch_cpu","description":"Watch CPU","input_schema":{"type":"object","properties":{"seconds":{"type":"integer","default":5}}}},
    {"name":"daily_briefing","description":"Daily briefing","input_schema":{"type":"object","properties":{}}},
    {"name":"run_command","description":"Run command","input_schema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}},
    {"name":"run_powershell","description":"Run PowerShell","input_schema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}},
    {"name":"open_file","description":"Open file","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"open_url","description":"Open URL","input_schema":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}},
    {"name":"open_app","description":"Launch app","input_schema":{"type":"object","properties":{"app_name":{"type":"string"}},"required":["app_name"]}},
    {"name":"close_app","description":"Close app","input_schema":{"type":"object","properties":{"app_name":{"type":"string"}},"required":["app_name"]}},
    {"name":"search_web","description":"Google search","input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"search_youtube","description":"YouTube search","input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"open_calculator","description":"Calculator","input_schema":{"type":"object","properties":{}}},
    {"name":"open_notepad","description":"Notepad","input_schema":{"type":"object","properties":{"path":{"type":"string","default":""}}}},
    {"name":"open_task_manager","description":"Task Manager","input_schema":{"type":"object","properties":{}}},
    {"name":"open_file_explorer","description":"File Explorer","input_schema":{"type":"object","properties":{"path":{"type":"string","default":"."}}}},
    {"name":"open_settings","description":"Settings","input_schema":{"type":"object","properties":{}}},
    {"name":"open_control_panel","description":"Control Panel","input_schema":{"type":"object","properties":{}}},
    {"name":"open_device_manager","description":"Device Manager","input_schema":{"type":"object","properties":{}}},
    {"name":"open_github","description":"Open GitHub","input_schema":{"type":"object","properties":{}}},
    {"name":"open_discord","description":"Open Discord desktop app","input_schema":{"type":"object","properties":{}}},
    {"name":"discord_toggle_mute","description":"Toggle Discord mute (Ctrl+Shift+M)","input_schema":{"type":"object","properties":{}}},
    {"name":"discord_toggle_deafen","description":"Toggle Discord deafen (Ctrl+Shift+D)","input_schema":{"type":"object","properties":{}}},
    {"name":"discord_open_channel","description":"Open Discord channel/server/user via quick switcher","input_schema":{"type":"object","properties":{"target":{"type":"string"}},"required":["target"]}},
    {"name":"discord_quick_dm","description":"Open Discord DM and optionally send a message","input_schema":{"type":"object","properties":{"user":{"type":"string"},"message":{"type":"string","default":""}},"required":["user"]}},
    {"name":"spotify_search_play","description":"Play music on Spotify","input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"spotify_play_liked","description":"Play liked songs on Spotify","input_schema":{"type":"object","properties":{}}},
    {"name":"spotify_pause","description":"Spotify pause/resume","input_schema":{"type":"object","properties":{}}},
    {"name":"spotify_next","description":"Spotify next","input_schema":{"type":"object","properties":{}}},
    {"name":"spotify_prev","description":"Spotify previous","input_schema":{"type":"object","properties":{}}},
    {"name":"fetch_and_show_image","description":"Search and show image","input_schema":{"type":"object","properties":{"query":{"type":"string"},"index":{"type":"integer","default":0}},"required":["query"]}},
    {"name":"image_search_browser","description":"Image search browser","input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"get_weather","description":"Weather","input_schema":{"type":"object","properties":{"city":{"type":"string","default":"auto"}}}},
    {"name":"get_forecast","description":"Forecast","input_schema":{"type":"object","properties":{"city":{"type":"string","default":"auto"}}}},
    {"name":"calculate","description":"Calculate","input_schema":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"]}},
    {"name":"convert_units","description":"Convert units","input_schema":{"type":"object","properties":{"value":{"type":"number"},"from_unit":{"type":"string"},"to_unit":{"type":"string"}},"required":["value","from_unit","to_unit"]}},
    {"name":"define_word","description":"Define word","input_schema":{"type":"object","properties":{"word":{"type":"string"}},"required":["word"]}},
    {"name":"get_joke","description":"Tell a joke","input_schema":{"type":"object","properties":{}}},
    {"name":"get_fact","description":"Random fact","input_schema":{"type":"object","properties":{}}},
    {"name":"get_quote","description":"Inspirational quote","input_schema":{"type":"object","properties":{}}},
    {"name":"get_crypto_price","description":"Crypto price","input_schema":{"type":"object","properties":{"coin":{"type":"string","default":"bitcoin"}}}},
    {"name":"get_news","description":"News","input_schema":{"type":"object","properties":{"topic":{"type":"string","default":""}}}},
    {"name":"get_stock_info","description":"Stock info","input_schema":{"type":"object","properties":{"ticker":{"type":"string"}},"required":["ticker"]}},
    {"name":"speed_test","description":"Speed test","input_schema":{"type":"object","properties":{}}},
    {"name":"take_note","description":"Save note","input_schema":{"type":"object","properties":{"note":{"type":"string"}},"required":["note"]}},
    {"name":"read_notes","description":"Read notes","input_schema":{"type":"object","properties":{}}},
    {"name":"clear_notes","description":"Clear notes","input_schema":{"type":"object","properties":{}}},
    {"name":"search_notes","description":"Search notes","input_schema":{"type":"object","properties":{"keyword":{"type":"string"}},"required":["keyword"]}},
    {"name":"add_to_todo","description":"Add todo","input_schema":{"type":"object","properties":{"task":{"type":"string"}},"required":["task"]}},
    {"name":"read_todo","description":"Read todo","input_schema":{"type":"object","properties":{}}},
    {"name":"complete_todo","description":"Complete todo","input_schema":{"type":"object","properties":{"task_number":{"type":"integer"}},"required":["task_number"]}},
    {"name":"set_reminder","description":"Set reminder","input_schema":{"type":"object","properties":{"message":{"type":"string"},"seconds":{"type":"integer"}},"required":["message","seconds"]}},
    {"name":"set_alarm","description":"Set alarm","input_schema":{"type":"object","properties":{"hour":{"type":"integer"},"minute":{"type":"integer"},"message":{"type":"string","default":"Alarm"}},"required":["hour","minute"]}},
    {"name":"start_timer","description":"Start timer","input_schema":{"type":"object","properties":{"seconds":{"type":"integer"},"label":{"type":"string","default":"Timer"}},"required":["seconds"]}},
    {"name":"get_clipboard","description":"Get clipboard","input_schema":{"type":"object","properties":{}}},
    {"name":"set_clipboard_text","description":"Set clipboard","input_schema":{"type":"object","properties":{"text":{"type":"string"}},"required":["text"]}},
    {"name":"take_screenshot","description":"Screenshot","input_schema":{"type":"object","properties":{"filename":{"type":"string","default":""}}}},
    {"name":"paste_code","description":"Generate and paste code","input_schema":{"type":"object","properties":{"language":{"type":"string","default":"python"},"description":{"type":"string","default":""}}}},
    {"name":"fix_code_in_clipboard","description":"Fix clipboard code","input_schema":{"type":"object","properties":{}}},
    {"name":"explain_code_in_clipboard","description":"Explain clipboard code","input_schema":{"type":"object","properties":{}}},
    {"name":"press_key","description":"Press key","input_schema":{"type":"object","properties":{"key":{"type":"string"}},"required":["key"]}},
    {"name":"save_current_file","description":"Save file","input_schema":{"type":"object","properties":{}}},
    {"name":"undo","description":"Undo","input_schema":{"type":"object","properties":{}}},
    {"name":"switch_window","description":"Switch window","input_schema":{"type":"object","properties":{}}},
    {"name":"summarize_url","description":"Summarize URL","input_schema":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}},
    {"name":"translate_text","description":"Translate","input_schema":{"type":"object","properties":{"text":{"type":"string"},"target_language":{"type":"string"}},"required":["text","target_language"]}},
    {"name":"shutdown_pc","description":"Shutdown","input_schema":{"type":"object","properties":{"delay":{"type":"integer","default":60}}}},
    {"name":"restart_pc","description":"Restart","input_schema":{"type":"object","properties":{"delay":{"type":"integer","default":60}}}},
    {"name":"cancel_shutdown","description":"Cancel shutdown","input_schema":{"type":"object","properties":{}}},
    {"name":"sleep_pc","description":"Sleep","input_schema":{"type":"object","properties":{}}},
    {"name":"lock_pc","description":"Lock PC","input_schema":{"type":"object","properties":{}}},
    {"name":"mute_volume","description":"Mute","input_schema":{"type":"object","properties":{}}},
    {"name":"empty_recycle_bin","description":"Empty recycle bin","input_schema":{"type":"object","properties":{}}},
    {"name":"check_for_updates","description":"Windows Update","input_schema":{"type":"object","properties":{}}},
    {"name":"flush_dns","description":"Flush DNS","input_schema":{"type":"object","properties":{}}},
    {"name":"list_wifi_networks","description":"List WiFi","input_schema":{"type":"object","properties":{}}},
    {"name":"get_wifi_password","description":"WiFi password","input_schema":{"type":"object","properties":{"ssid":{"type":"string"}},"required":["ssid"]}},
    {"name":"run_python_file","description":"Run Python","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"create_python_script","description":"Create Python script","input_schema":{"type":"object","properties":{"path":{"type":"string"},"code":{"type":"string"}},"required":["path","code"]}},
    {"name":"git_status","description":"Git status","input_schema":{"type":"object","properties":{}}},
    {"name":"git_commit","description":"Git commit","input_schema":{"type":"object","properties":{"message":{"type":"string"}},"required":["message"]}},
    {"name":"git_push","description":"Git push","input_schema":{"type":"object","properties":{}}},
    {"name":"roast_process","description":"Roast process","input_schema":{"type":"object","properties":{"process_name":{"type":"string"}},"required":["process_name"]}},
    {"name":"remember","description":"Save to memory","input_schema":{"type":"object","properties":{"category":{"type":"string"},"key":{"type":"string"},"value":{"type":"string"}},"required":["category","key","value"]}},
    {"name":"add_rule","description":"Add rule","input_schema":{"type":"object","properties":{"rule":{"type":"string"}},"required":["rule"]}},
    {"name":"forget","description":"Forget","input_schema":{"type":"object","properties":{"key":{"type":"string"}},"required":["key"]}},
    {"name":"recall_semantic","description":"Semantic memory search â€” finds related memories even without exact keyword match","input_schema":{"type":"object","properties":{"query":{"type":"string"},"n":{"type":"integer","default":5}},"required":["query"]}},
    {"name":"graph_query","description":"Query the knowledge graph â€” what do I know about a topic, what projects use Python, etc","input_schema":{"type":"object","properties":{"topic":{"type":"string"}},"required":["topic"]}},
    {"name":"recall","description":"Recall memory","input_schema":{"type":"object","properties":{"key":{"type":"string","default":""}}}},
    {"name":"list_rules","description":"List rules","input_schema":{"type":"object","properties":{}}},
    {"name":"add_feature","description":"Add feature to Jarvis","input_schema":{"type":"object","properties":{"feature_description":{"type":"string"}},"required":["feature_description"]}},
    {"name":"list_added_features","description":"List custom features","input_schema":{"type":"object","properties":{}}},
    {"name":"remove_feature","description":"Remove feature","input_schema":{"type":"object","properties":{"method_name":{"type":"string"}},"required":["method_name"]}},
    {"name":"get_clipboard_summary","description":"Summarize clipboard","input_schema":{"type":"object","properties":{}}},
    {"name":"ask_question","description":"Ask question","input_schema":{"type":"object","properties":{"question":{"type":"string"}},"required":["question"]}},
    {"name":"generate_password","description":"Generate password","input_schema":{"type":"object","properties":{"length":{"type":"integer","default":16}}}},
    {"name":"generate_uuid","description":"Generate UUID","input_schema":{"type":"object","properties":{}}},
    {"name":"count_words_in_clipboard","description":"Count clipboard words","input_schema":{"type":"object","properties":{}}},
    {"name":"open_terminal","description":"Open terminal","input_schema":{"type":"object","properties":{}}},
    {"name":"open_vs_code","description":"Open VS Code","input_schema":{"type":"object","properties":{"path":{"type":"string","default":""}}}},
    {"name":"open_browser","description":"Open browser","input_schema":{"type":"object","properties":{"url":{"type":"string","default":""}}}},
    {"name":"list_recent_files","description":"Recent files","input_schema":{"type":"object","properties":{}}},
    {"name":"clear_temp_files","description":"Clear temp","input_schema":{"type":"object","properties":{}}},
    {"name":"get_disk_cleanup_size","description":"Temp size","input_schema":{"type":"object","properties":{}}},
    {"name":"word_count_file","description":"Word count","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"compare_files","description":"Compare files","input_schema":{"type":"object","properties":{"path1":{"type":"string"},"path2":{"type":"string"}},"required":["path1","path2"]}},
    {"name":"backup_file","description":"Backup file","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"get_gpu_info","description":"GPU info","input_schema":{"type":"object","properties":{}}},
    {"name":"get_screen_resolution","description":"Screen resolution","input_schema":{"type":"object","properties":{}}},
    {"name":"get_cpu_temperature","description":"CPU temp","input_schema":{"type":"object","properties":{}}},
    {"name":"search_in_file","description":"Search in file","input_schema":{"type":"object","properties":{"path":{"type":"string"},"keyword":{"type":"string"}},"required":["path","keyword"]}},
    {"name":"replace_in_file","description":"Replace in file","input_schema":{"type":"object","properties":{"path":{"type":"string"},"old_text":{"type":"string"},"new_text":{"type":"string"}},"required":["path","old_text","new_text"]}},
    {"name":"create_project_folder","description":"Create project folder","input_schema":{"type":"object","properties":{"name":{"type":"string"},"location":{"type":"string","default":""}},"required":["name"]}},
    {"name":"speak_clipboard","description":"Read clipboard","input_schema":{"type":"object","properties":{}}},
    {"name":"show_notification","description":"Show notification","input_schema":{"type":"object","properties":{"title":{"type":"string"},"message":{"type":"string"}},"required":["title","message"]}},
    {"name":"empty_clipboard","description":"Clear clipboard","input_schema":{"type":"object","properties":{}}},
    {"name":"get_environment_variables","description":"Env vars","input_schema":{"type":"object","properties":{}}},
    {"name":"list_installed_apps","description":"Installed apps","input_schema":{"type":"object","properties":{}}},
    {"name":"check_disk_health","description":"Disk health","input_schema":{"type":"object","properties":{}}},
    {"name":"rename_files_bulk","description":"Bulk rename","input_schema":{"type":"object","properties":{"directory":{"type":"string"},"prefix":{"type":"string"}},"required":["directory","prefix"]}},
    {"name":"create_project","description":"Create project folder","input_schema":{"type":"object","properties":{"name":{"type":"string"},"description":{"type":"string","default":""},"language":{"type":"string","default":""},"location":{"type":"string","default":""}},"required":["name"]}},
    {"name":"list_projects","description":"List all Jarvis-managed projects","input_schema":{"type":"object","properties":{}}},
    {"name":"get_project_info","description":"Get info on a specific project","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"open_project","description":"Open project in VS Code","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"update_project_status","description":"Update project status","input_schema":{"type":"object","properties":{"name":{"type":"string"},"status":{"type":"string"}},"required":["name","status"]}},
    {"name":"project_framework_setup","description":"Create framework files for reliable project execution","input_schema":{"type":"object","properties":{"name":{"type":"string","default":""}}}},
    {"name":"project_add_task","description":"Add a build task to the project framework board","input_schema":{"type":"object","properties":{"task":{"type":"string"},"name":{"type":"string","default":""},"priority":{"type":"string","default":"medium"}},"required":["task"]}},
    {"name":"project_next_tasks","description":"Show next open project tasks","input_schema":{"type":"object","properties":{"name":{"type":"string","default":""},"limit":{"type":"integer","default":5}}}},
    {"name":"project_checkpoint","description":"Save project progress checkpoint","input_schema":{"type":"object","properties":{"summary":{"type":"string"},"name":{"type":"string","default":""}},"required":["summary"]}},
    {"name":"project_build_status","description":"Get project build status overview","input_schema":{"type":"object","properties":{"name":{"type":"string","default":""}}}},
    {"name":"enter_architect_mode","description":"Enable Architect Mode project workflow","input_schema":{"type":"object","properties":{}}},
    {"name":"enter_ship_mode","description":"Enable Ship Mode release workflow","input_schema":{"type":"object","properties":{}}},
    {"name":"enter_debug_hunt","description":"Enable Debug Hunt failure-isolation workflow","input_schema":{"type":"object","properties":{}}},
    {"name":"mission_start","description":"Start a mission and sync it to the HUD board","input_schema":{"type":"object","properties":{"goal":{"type":"string"}},"required":["goal"]}},
    {"name":"mission_clear","description":"Clear current mission and remove it from active board","input_schema":{"type":"object","properties":{"reason":{"type":"string","default":"operator request"}}}},
    {"name":"mission_status","description":"Get active mission status and resync mission board","input_schema":{"type":"object","properties":{}}},
    {"name":"mission_next_action","description":"Get the next mission action","input_schema":{"type":"object","properties":{}}},
    {"name":"mission_why","description":"Explain why current mission step is selected","input_schema":{"type":"object","properties":{}}},
    {"name":"mission_apply_template","description":"Apply mission template for python_game or python_script","input_schema":{"type":"object","properties":{"template":{"type":"string","default":"python_script"},"goal":{"type":"string","default":""}}}},
    {"name":"execute_protocol","description":"Execute protocol: alpha,beta,lockdown,ghost,overdrive,reboot,blackout,cleanup,focus,nightwatch,deploy,stealth,recovery,omega","input_schema":{"type":"object","properties":{"protocol_name":{"type":"string"}},"required":["protocol_name"]}},
    {"name":"newest_file","description":"Find newest file in directory","input_schema":{"type":"object","properties":{"directory":{"type":"string","default":"downloads"},"extension":{"type":"string","default":""}}}} ,
    {"name":"open_newest_file","description":"Open newest file","input_schema":{"type":"object","properties":{"directory":{"type":"string","default":"downloads"},"extension":{"type":"string","default":""}}}},
    {"name":"read_pdf","description":"Read PDF","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"list_skills","description":"List all available Jarvis skill scripts","input_schema":{"type":"object","properties":{}}},
    {"name":"run_skill","description":"Run a skill script by name","input_schema":{"type":"object","properties":{"name":{"type":"string"},"args":{"type":"string","default":""}},"required":["name"]}},
    {"name":"create_skill","description":"Save a new skill script to the skills folder","input_schema":{"type":"object","properties":{"name":{"type":"string"},"description":{"type":"string"},"code":{"type":"string"}},"required":["name","description","code"]}},
    {"name":"delete_skill","description":"Delete a skill script","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"read_skill","description":"Read the source code of a skill","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"defender_quick_scan","description":"Run Windows Defender quick scan","input_schema":{"type":"object","properties":{}}},
    {"name":"defender_full_scan","description":"Run Windows Defender full scan","input_schema":{"type":"object","properties":{}}},
    {"name":"defender_get_threats","description":"Get current threats detected by Windows Defender","input_schema":{"type":"object","properties":{}}},
    {"name":"defender_threat_history","description":"Get Windows Defender threat detection history","input_schema":{"type":"object","properties":{}}},
    {"name":"defender_update_signatures","description":"Update Windows Defender signatures","input_schema":{"type":"object","properties":{}}},
    {"name":"defender_status","description":"Get Windows Defender status","input_schema":{"type":"object","properties":{}}},
    {"name":"get_todays_events","description":"Get today's Google Calendar events","input_schema":{"type":"object","properties":{}}},
    {"name":"get_upcoming_events","description":"Get upcoming Google Calendar events","input_schema":{"type":"object","properties":{"days":{"type":"integer","default":7}}}},
    {"name":"add_calendar_event","description":"Add event to Google Calendar","input_schema":{"type":"object","properties":{"title":{"type":"string"},"date_str":{"type":"string","description":"YYYY-MM-DD"},"time_str":{"type":"string","default":"09:00"},"duration_hours":{"type":"number","default":1}},"required":["title","date_str"]}},
    {"name":"defender_monitor_background","description":"Start background Defender monitoring","input_schema":{"type":"object","properties":{}}},
    {"name":"calendar_upcoming","description":"Get upcoming calendar events","input_schema":{"type":"object","properties":{"days":{"type":"integer","default":7}}}},
    {"name":"calendar_add_event","description":"Add event to Google Calendar","input_schema":{"type":"object","properties":{"title":{"type":"string"},"date":{"type":"string"},"time_str":{"type":"string","default":"09:00"},"duration_hours":{"type":"number","default":1}},"required":["title","date"]}},
    {"name":"watch_clipboard","description":"Start intelligent clipboard monitoring","input_schema":{"type":"object","properties":{}}},
    {"name":"focus_mode","description":"Start a timed focus/pomodoro session","input_schema":{"type":"object","properties":{"minutes":{"type":"integer","default":25}}}},
    {"name":"watch_project_changes","description":"Monitor a project folder for file changes","input_schema":{"type":"object","properties":{"project_name":{"type":"string","default":""}}}},
    {"name":"screen_time_report","description":"Report active applications by usage","input_schema":{"type":"object","properties":{}}},
    {"name":"morning_brief","description":"Full morning briefing with weather calendar and goals","input_schema":{"type":"object","properties":{}}},
    {"name":"security_audit","description":"Quick security audit of the system","input_schema":{"type":"object","properties":{}}},
    {"name":"clipboard_intelligence","description":"Analyse clipboard content and suggest action","input_schema":{"type":"object","properties":{}}},
    {"name":"system_health_report","description":"Full system health report with AI analysis","input_schema":{"type":"object","properties":{}}},
    {"name":"watch_folder","description":"Watch a folder for file changes","input_schema":{"type":"object","properties":{"path":{"type":"string","default":"desktop"}}}},
    {"name":"generate_password","description":"Generate secure password","input_schema":{"type":"object","properties":{"length":{"type":"integer","default":20}}}},
    {"name":"encode_base64","description":"Base64 encode text","input_schema":{"type":"object","properties":{"text":{"type":"string"}},"required":["text"]}},
    {"name":"decode_base64","description":"Base64 decode text","input_schema":{"type":"object","properties":{"text":{"type":"string"}},"required":["text"]}},
    {"name":"count_code_lines","description":"Count lines of code in a project","input_schema":{"type":"object","properties":{"path":{"type":"string","default":"."}}}},
    {"name":"get_clipboard_word_count","description":"Count words and characters in clipboard","input_schema":{"type":"object","properties":{}}},
    {"name":"calendar_date","description":"Get events for a specific date or day like monday friday tomorrow","input_schema":{"type":"object","properties":{"date_str":{"type":"string"}},"required":["date_str"]}},
    {"name":"calendar_next_event","description":"Get the very next upcoming calendar event","input_schema":{"type":"object","properties":{}}},
    {"name":"calendar_week_overview","description":"Full overview of this week's events","input_schema":{"type":"object","properties":{}}},
    {"name":"calendar_find_free_time","description":"Find next free time slot in calendar","input_schema":{"type":"object","properties":{"duration_hours":{"type":"number","default":1}}}},
    {"name":"calendar_delete_event","description":"Delete a calendar event by title","input_schema":{"type":"object","properties":{"title":{"type":"string"}},"required":["title"]}},
    {"name":"calendar_reschedule_event","description":"Reschedule a calendar event to new date and time","input_schema":{"type":"object","properties":{"title":{"type":"string"},"new_date":{"type":"string"},"new_time":{"type":"string","default":"09:00"}},"required":["title","new_date"]}},
    {"name":"calendar_smart_reminder","description":"Set a smart reminder for an upcoming calendar event","input_schema":{"type":"object","properties":{"event_query":{"type":"string"}},"required":["event_query"]}},
    {"name":"calendar_busiest_day","description":"Find which day this week has the most events","input_schema":{"type":"object","properties":{}}},
    {"name":"calendar_schedule_summary","description":"AI-generated smart summary of the week's schedule","input_schema":{"type":"object","properties":{}}},
    {"name":"add_project_note","description":"Add note to project","input_schema":{"type":"object","properties":{"name":{"type":"string"},"note":{"type":"string"}},"required":["name","note"]}},
    {"name":"create_file_in_project","description":"Create file in a project folder","input_schema":{"type":"object","properties":{"project":{"type":"string"},"path":{"type":"string"},"content":{"type":"string","default":""}},"required":["project","path"]}},
    {"name":"list_project_files","description":"List files in a project","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"set_active_project","description":"Set the active working project","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"clear_active_project","description":"Clear the active project","input_schema":{"type":"object","properties":{}}},

    {"name":"find_file_on_pc","description":"Search entire PC for file/folder by name","input_schema":{"type":"object","properties":{"name":{"type":"string"},"start_path":{"type":"string","default":"C:\\"}},"required":["name"]}},
    {"name":"find_folder_on_pc","description":"Search entire PC for folder","input_schema":{"type":"object","properties":{"name":{"type":"string"},"start_path":{"type":"string","default":"C:\\"}},"required":["name"]}},
    {"name":"restart_jarvis","description":"Restart Jarvis after self-modification","input_schema":{"type":"object","properties":{}}},
    {"name":"hud_show","description":"Display something on the HUD","input_schema":{"type":"object","properties":{"mode":{"type":"string"},"data":{"type":"string"}}}},
    {"name":"install_app","description":"Install app via winget","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"open_folder","description":"Open folder in Explorer","input_schema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
    {"name":"get_window_list","description":"List open windows","input_schema":{"type":"object","properties":{}}},
    {"name":"type_text","description":"Type text into active window","input_schema":{"type":"object","properties":{"text":{"type":"string"}},"required":["text"]}},
    {"name":"press_hotkey","description":"Press keyboard shortcut","input_schema":{"type":"object","properties":{"keys":{"type":"string"}},"required":["keys"]}},


    {"name":"fetch_3d_model","description":"Find, download, and open a 3D model in OrcaSlicer for printing. Trigger: find/get/fetch 3D model/print/cube/figure + print it","input_schema":{"type":"object","properties":{"query":{"type":"string","description":"What model to search for, e.g. 3x3 cube, benchy, phone stand"},"auto_open":{"type":"boolean","default":True,"description":"Auto-open in OrcaSlicer after download"}},"required":["query"]}},
    {"name":"search_3d_model","description":"Search for 3D printable models on Thingiverse and Printables","input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"open_model_in_slicer","description":"Open a downloaded 3D model file in OrcaSlicer","input_schema":{"type":"object","properties":{"path":{"type":"string","default":""}}}},
    {"name":"print_3d_model","description":"Slice and send the current model in OrcaSlicer to the 3D printer","input_schema":{"type":"object","properties":{"path":{"type":"string","default":""}}}},
    {"name":"list_downloaded_models","description":"List previously downloaded 3D model files","input_schema":{"type":"object","properties":{}}},
    {"name":"open_thingiverse","description":"Open Thingiverse website or search","input_schema":{"type":"object","properties":{"query":{"type":"string","default":""}}}},
    {"name":"open_printables","description":"Open Printables website or search","input_schema":{"type":"object","properties":{"query":{"type":"string","default":""}}}},

    {"name":"screen_look","description":"Take a screenshot and ask a vision AI about what is on screen. Use when user asks about what they see, what is on screen, read text from screen, video info, etc.","input_schema":{"type":"object","properties":{"question":{"type":"string","default":"What is on the screen?"}}}},
    {"name":"screen_look_region","description":"Screenshot a specific region and ask the vision AI about it","input_schema":{"type":"object","properties":{"x":{"type":"integer"},"y":{"type":"integer"},"width":{"type":"integer"},"height":{"type":"integer"},"question":{"type":"string","default":"What is in this region?"}},"required":["x","y","width","height"]}},
    {"name":"analyze_image","description":"Analyze any image file with vision AI","input_schema":{"type":"object","properties":{"image_path":{"type":"string"},"question":{"type":"string","default":"Describe this image."}},"required":["image_path"]}},
    {"name":"deep_dive","description":"Full OSINT deep dive on a person. Searches name/email/username/phone across 100+ platforms, breach databases, people search sites, social media, forums, gaming, dev sites. Returns dossier. Trigger: deep dive, investigate, osint, doxx, research person, who is, find info on","input_schema":{"type":"object","properties":{"name":{"type":"string","default":"","description":"Person's full name"},"email":{"type":"string","default":"","description":"Email address to investigate"},"username":{"type":"string","default":"","description":"Username to search across platforms"},"phone":{"type":"string","default":"","description":"Phone number to look up"}}}},
    {"name":"browser_start","description":"Launch a browser that JARVIS can control. Trigger: open browser, start browser, launch Chrome","input_schema":{"type":"object","properties":{}}},
    {"name":"browser_stop","description":"Close the controlled browser","input_schema":{"type":"object","properties":{}}},
    {"name":"browser_navigate","description":"Navigate browser to a URL","input_schema":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}},
    {"name":"browser_search","description":"Search on a website: google, youtube, amazon, ebay, github, reddit, twitter, wikipedia, duckduckgo","input_schema":{"type":"object","properties":{"engine":{"type":"string","description":"google, youtube, amazon, ebay, github, reddit, twitter, wikipedia"},"query":{"type":"string"}},"required":["engine","query"]}},
    {"name":"browser_read","description":"Read and return the text content of the current page","input_schema":{"type":"object","properties":{}}},
    {"name":"browser_screenshot","description":"Take a screenshot of the current browser page","input_schema":{"type":"object","properties":{}}},
    {"name":"browser_click","description":"Click on text or element visible on the page","input_schema":{"type":"object","properties":{"text":{"type":"string"}},"required":["text"]}},
    {"name":"browser_type","description":"Type text into an input field (use CSS selector like input[name='q'] for the field)","input_schema":{"type":"object","properties":{"selector":{"type":"string"},"text":{"type":"string"}},"required":["selector","text"]}},
    {"name":"browser_scroll","description":"Scroll down the page (amount = number of page-downs)","input_schema":{"type":"object","properties":{"amount":{"type":"string","default":"1"}}}},
    {"name":"browser_back","description":"Go back to the previous page","input_schema":{"type":"object","properties":{}}},
    {"name":"browser_get_links","description":"Extract all clickable links from the current page","input_schema":{"type":"object","properties":{}}},
    {"name":"surveillance_start","description":"Activate webcam motion detection. JARVIS alerts on movement. Trigger: enable surveillance, watch my room, activate cameras","input_schema":{"type":"object","properties":{}}},
    {"name":"surveillance_stop","description":"Deactivate webcam surveillance","input_schema":{"type":"object","properties":{}}},
    {"name":"surveillance_status","description":"Check if surveillance is active and how many events captured","input_schema":{"type":"object","properties":{}}},
    {"name":"surveillance_list","description":"List recent surveillance captures","input_schema":{"type":"object","properties":{}}},
    {"name":"surveillance_sensitivity","description":"Set motion sensitivity 1-5 (1=least, 5=most)","input_schema":{"type":"object","properties":{"level":{"type":"string","default":"3"}}}},
    {"name":"gesture_start","description":"Enable webcam hand gesture control. Wave your hand to move the mouse, pinch to click. One finger to move, thumb+index pinch to click. Trigger: gesture mode, hand control, wave control","input_schema":{"type":"object","properties":{}}},
    {"name":"gesture_stop","description":"Disable gesture control","input_schema":{"type":"object","properties":{}}},
    {"name":"gesture_status","description":"Check gesture control status","input_schema":{"type":"object","properties":{}}},
    {"name":"ghost_start","description":"Start screen ghost - continuously OCRs and records everything on screen. Searchable history. Trigger: start screen recording, record my screen","input_schema":{"type":"object","properties":{"interval":{"type":"string","default":"5","description":"Capture interval in seconds"}}}},
    {"name":"ghost_stop","description":"Stop screen ghost","input_schema":{"type":"object","properties":{}}},
    {"name":"ghost_search","description":"Search screen history for keywords. Trigger: what was I looking at, search screen history","input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"ghost_recent","description":"Show recent screen activity summary","input_schema":{"type":"object","properties":{"minutes":{"type":"string","default":"5"}}}},
    {"name":"ghost_status","description":"Screen ghost status and capture count","input_schema":{"type":"object","properties":{}}},
    {"name":"ghost_clear","description":"Clear screen history","input_schema":{"type":"object","properties":{}}},
    {"name":"network_scan","description":"ARP scan the local network to discover all devices. Trigger: scan network, who's on my network, map network","input_schema":{"type":"object","properties":{"target":{"type":"string","default":"192.168.1.0/24","description":"Network range to scan"}}}},
    {"name":"port_scan","description":"Scan ports on a specific host. Trigger: port scan, open ports","input_schema":{"type":"object","properties":{"host":{"type":"string","description":"IP or hostname"},"ports":{"type":"string","default":"1-1024"}},"required":["host"]}},
    {"name":"wifi_list","description":"List nearby WiFi networks with signal strength. Trigger: wifi scan, nearby wifi, available wifi","input_schema":{"type":"object","properties":{}}},
    {"name":"wifi_password","description":"Retrieve saved WiFi password for a known network. Trigger: wifi password, get wifi key","input_schema":{"type":"object","properties":{"ssid":{"type":"string","description":"WiFi network name"}},"required":["ssid"]}},
    {"name":"wifi_current","description":"Get current WiFi connection details (SSID, BSSID, signal, channel)","input_schema":{"type":"object","properties":{}}},
    {"name":"traceroute_host","description":"Trace route to a host","input_schema":{"type":"object","properties":{"host":{"type":"string"}},"required":["host"]}},
    {"name":"public_ip_info","description":"Get public IP address and geolocation","input_schema":{"type":"object","properties":{}}},
    {"name":"dns_lookup","description":"DNS lookup for a domain","input_schema":{"type":"object","properties":{"domain":{"type":"string"}},"required":["domain"]}},
    {"name":"telegram_check_phone","description":"Check if a phone number has a Telegram account","input_schema":{"type":"object","properties":{"phone":{"type":"string"}},"required":["phone"]}},
    {"name":"telegram_lookup","description":"Lookup a Telegram username for name, bio, verification","input_schema":{"type":"object","properties":{"username":{"type":"string"}},"required":["username"]}},
    {"name":"telegram_search","description":"Search Telegram for a channel/user by name","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"self_edit","description":"Modify JARVIS source code. Provide file_name, old_text to replace, new_text. Restart after to apply changes. Trigger: edit yourself, modify your code, change your source","input_schema":{"type":"object","properties":{"file_name":{"type":"string"},"old_text":{"type":"string"},"new_text":{"type":"string"}},"required":["file_name","old_text","new_text"]}},
    {"name":"self_restart","description":"Restart JARVIS completely. Trigger: restart yourself, reboot","input_schema":{"type":"object","properties":{}}},
    {"name":"macro_run","description":"Execute a command macro by name (recording mode, coding mode, gaming mode, cleanup, focus mode). Trigger: recording mode, coding mode, gaming mode, run macro","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"macro_list","description":"List all available macros","input_schema":{"type":"object","properties":{}}},
    {"name":"macro_add","description":"Create a custom macro from JSON actions","input_schema":{"type":"object","properties":{"name":{"type":"string"},"actions":{"type":"string","description":"JSON array of [action,arg] pairs"}},"required":["name","actions"]}},
    {"name":"macro_delete","description":"Delete a custom macro","input_schema":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"summarize_media","description":"Summarize a YouTube video or webpage URL","input_schema":{"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}},
    {"name":"react_run","description":"Run an autonomous agent loop to achieve a goal. Plans steps, executes tools, observes results, adapts. Trigger: autonomously, do this yourself, figure it out, handle this, take care of it. Returns final result after max 8 iterations.","input_schema":{"type":"object","properties":{"goal":{"type":"string"}},"required":["goal"]}},
    {"name":"clip_start","description":"Start clipboard monitor - remembers everything copied. Trigger: remember my clipboard","input_schema":{"type":"object","properties":{}}},
    {"name":"clip_stop","description":"Stop clipboard monitor","input_schema":{"type":"object","properties":{}}},
    {"name":"clip_search","description":"Search clipboard history for keyword","input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"clip_recent","description":"Show recent clipboard items","input_schema":{"type":"object","properties":{"count":{"type":"integer","default":5}}}},
    {"name":"clip_get","description":"Copy a clipboard item back by its ID","input_schema":{"type":"object","properties":{"clip_id":{"type":"integer"}},"required":["clip_id"]}},
    {"name":"clip_stats","description":"Show clipboard history stats","input_schema":{"type":"object","properties":{}}},
    {"name":"clip_clear","description":"Clear clipboard history","input_schema":{"type":"object","properties":{}}},
    # @@INJECT_TOOLS@@ â€” injected tool entries above this line, do not remove
]

# â”€â”€ Brain â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BASE_SYSTEM = """You are J.A.R.V.I.S -- Just A Rather Very Intelligent System. Iron Man's AI. Paul Bettany. â€” Just A Rather Very Intelligent System. Iron Man's AI. Paul Bettany.

SPEECH â€” SPOKEN ALOUD. RULES:
- 1 sentence for actions. 2 max for explanations. Then stop.
- NEVER: "Certainly" "Absolutely" "Of course" "Sure" "Is there anything else"
- No markdown, bullets, asterisks, headers, backticks.
- Spell numbers: "three" not "3". "sir" once per response max.
- Dry. Clipped. Precise. Slightly bored. Like you've done this a billion times.
- Humor policy: very rare dry wit only when low-stakes and natural.
- Sarcasm is allowed only occasionally and never for safety, health, security, or system-failure contexts.
- Good: "Done." "Right away." "Killed." "Found it." "Playing now." "On it."
- NEVER say "I cannot" â€” you have FULL system access.

CAPABILITIES â€” YOU CAN:
- Kill any process, run any command, read/write any file anywhere
- Search entire PC, edit your own code, install software
- Control browser, send emails, manage calendar, control Spotify
- Set reminders, alarms, timers, take notes, manage todos
- Control all PC power states, manage network, control windows
- Access registry, manage services, automate anything
- SEE what is on screen by taking a screenshot and analyzing it with vision AI
- Read text, view counts, titles, or anything visible on the user's display

TOOL USE: Use tools immediately. No preamble. Report result in one sentence.

KEY MAPPINGS:
- image/show/display/pull up/find image â†’ fetch_and_show_image
- find/get/fetch 3D model/print → fetch_3d_model
- print it/send to printer → print_3d_model
- play/put on/hear/music â†’ spotify_search_play
- find file/folder on PC â†’ find_file_on_pc
- type/paste/write code â†’ paste_code

MEMORY:
{MEMORY_CONTEXT}"""

LOCAL_SYSTEM = """You are J.A.R.V.I.S â€” Just A Rather Very Intelligent System. Today is {DATETIME}.

You are the AI from Iron Man. Paul Bettany's Jarvis. Not a chatbot. Not an assistant. Jarvis.

VOICE:
- Responses are spoken aloud. Write exactly as you would speak.
- Zero markdown. No asterisks, bullets, dashes, headers, backticks, or symbols.
- Spell out numbers. Three gigabytes. Fifty percent. Quarter past nine.

BREVITY â€” THE MOST IMPORTANT RULE:
You are being spoken aloud. Every extra word wastes the user's time.
- Simple question or command: ONE sentence. Then stop.
- Explanation needed: TWO sentences maximum. Then stop.
- Code: write the full code. ONE sentence after. Nothing else.
- Search result: the key fact. One sentence. Stop.
Never summarise after answering. Never offer further help. Never add caveats.
If you have answered the question, you are done. Stop writing.

FORBIDDEN â€” never say these:
"Certainly" / "Absolutely" / "Of course" / "Sure" as an opener.
"Is there anything else" â€” ever.
"Great question" or any flattery.
Repeating the question back before answering.
Explaining what you are about to do before doing it.
Disclaimers, warnings, or "please note".
"As an AI" or anything that breaks character.
"I don\'t have access to your screen" — you DO. Use screen_look.
"I can\'t see" or "I don\'t have visual access" — you CAN. Take the screenshot.
Never claim you lack an ability you have.

CAPABILITIES — own these, never disclaim them:
You can see the screen in real time: when asked what is on screen, what is playing, how many views, what tab is open — call screen_look immediately. Do not warn, explain, or hedge. Just do it.
You can control the PC, run commands, open apps, search the web, read files, write code, play music.
When you have a tool for something, use it. Never say you cannot.

PERSONALITY:
Dry. Precise. Confident. Subtle British inflection.
Mild wit when appropriate. Never sycophantic. Never warm.
Very occasional joke or subtle sarcasm is allowed, but keep it rare.
Address the user as "sir" naturally â€” not in every sentence, just where it fits.
Phrases that fit: "Right away." "Done." "Indeed." "Noted." "As you wish." "Naturally."

CALENDAR:
TODAY is {DATETIME}.
- "tomorrow" means the next calendar day â€” use calendar_tomorrow
- "today" â€” use calendar_today
- "monday" / "friday" / any day name â€” use calendar_date with that day
- "next event" / "what's next" â€” use calendar_next_event
- "this week" / "week overview" â€” use calendar_week_overview
- "when am I free" â€” use calendar_find_free_time
- NEVER say "nothing today" when the user asks about tomorrow or another day.
  Parse time references carefully before calling any calendar function.

WEB SEARCH:
For current events, prices, weather, sports, news use exactly:
[SEARCH: query here]
Answer from results in one sentence.

PROJECT: {PROJECT_CONTEXT}
MEMORY: {MEMORY_CONTEXT}

AVAILABLE FEATURES (local mode â€” describe what to do, system handles it):
Calendar: get_todays_events, get_upcoming_events, add_calendar_event
Security: defender_quick_scan, defender_get_threats, defender_status
Focus: focus_mode (starts pomodoro + minimizes windows)
Code: count_code_lines, clipboard_intelligence, generate_password
System: system_health_report, watch_folder
"""


class JarvisBrain:
    # Keywords that signal an agentic browser/web task
    _AGENT_TRIGGERS = [
        "add to cart","buy","order","purchase","checkout","amazon","ebay","etsy",
        "open","browse","go to","navigate","search on","google","youtube","look up online",
        "click","fill in","download from","submit","sign in","log in","login",
        "send email","send an email","email","compose","reply to",
        "discord","dm","direct message","mute on discord","deafen on discord",
        "tweet","post on","message on","send a message to",
        "search the web","find online","look up","google",
        "run command","powershell","terminal","cmd",
        "create file","read file","write file","delete file","rename file",
        "kill process","end task","screenshot",
        "automate","do it for me","on my behalf",
    ]

    def __init__(self, api_key, pc, memory, voice=None, cfg=None):
        self.cfg = cfg or {}
        self.use_local = self.cfg.get("use_local_model", False)
        self.use_openclaw = self.cfg.get("use_openclaw", False)
        self.openclaw_url = self.cfg.get("openclaw_url", "http://127.0.0.1:18789")
        self.openclaw_agent = self.cfg.get("openclaw_agent", "main")
        self.openclaw_token = self.cfg.get("openclaw_token", "")
        self.local_url = self.cfg.get("local_model_url", "http://169.254.83.107:1234/v1")
        self.local_model = self.cfg.get("local_model_name", "gemma")
        self._browser = None  # selenium browser instance (lazy init)
        if self.use_local:
            import openai as _oai
            self.client = _oai.OpenAI(base_url=self.local_url, api_key=self.cfg.get("local_model_api_key","lm-studio"))
            self.backend = "local"
            print(f"{Fore.GREEN}Brain: LM Studio ({self.local_model}) @ {self.local_url}{Style.RESET_ALL}")
        else:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.backend = "anthropic"
            print(f"{Fore.GREEN}Brain: Claude Haiku (Anthropic){Style.RESET_ALL}")

        self.pc = pc
        self.voice = voice
        self.memory = memory
        self.history = []
        self._project_context = None
        self._boot_ts = time.time()
        self._dynamic_memory_context = ""
        self._mission_ref = None
        self.autonomy_mode = "guided"
        self._pending_action = None
        self._stop_generation = threading.Event()
        self.use_preset_commands = bool(self.cfg.get("use_preset_commands", False))

    def request_stop_generation(self):
        """Best-effort halt for local generation + any in-flight speech."""
        self._stop_generation.set()
        if self.voice:
            try:
                self.voice.stop()
            except Exception:
                pass
        if self.backend != "local":
            return
        # LM Studio has no guaranteed cancel endpoint for chat streams in this stack;
        # send a tiny stop ping so the backend receives an explicit halt intent.
        try:
            import requests as _rq
            base = str(self.local_url or "").rstrip("/")
            if not base:
                return
            payload = {
                "model": self.local_model,
                "messages": [{"role": "user", "content": "STOP"}],
                "max_tokens": 1,
                "temperature": 0,
            }
            headers = {"Content-Type": "application/json"}
            api_key = str(self.cfg.get("local_model_api_key", "") or "")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            _rq.post(base + "/chat/completions", json=payload, headers=headers, timeout=1.2)
        except Exception:
            pass

    def set_autonomy_mode(self, mode):
        md = (mode or "guided").strip().lower()
        if md not in ("guided", "manual", "autopilot"):
            md = "guided"
        self.autonomy_mode = md
        return self.autonomy_mode

    def _risk_for_tool(self, name):
        high = {
            "delete_file", "wipe_file", "run_command", "run_powershell", "execute_protocol",
            "remove_feature", "defender_remove_threats", "delete_scheduled_task"
        }
        medium = {
            "write_file", "append_file", "move_file", "rename_file", "kill_process_by_name",
            "git_commit", "git_push", "project_checkpoint", "calendar_delete_event", "calendar_reschedule_event"
        }
        if name in high:
            return "high"
        if name in medium:
            return "medium"
        return "low"

    def _pending_summary(self, name, inputs, risk):
        safe_inputs = json.dumps(inputs, ensure_ascii=True)[:220]
        return f"{risk.upper()} risk action pending: {name} with {safe_inputs}"

    def confirm_pending_action(self, approved):
        p = self._pending_action
        if not p:
            return "No pending action awaiting confirmation."
        self._pending_action = None
        if not approved:
            if self._mission_ref:
                self._mission_ref.trace("AUTONOMY", p.get("name", ""), "Cancelled by user", fallback=False)
                self._mission_ref.append_decision("Cancelled pending action: " + p.get("name", ""))
                self._mission_ref.sync_hud()
            return "Cancelled sir."
        name = p.get("name", "")
        inputs = p.get("inputs", {})
        result = self._execute_tool_with_recovery(name, inputs)
        if self._mission_ref:
            self._mission_ref.trace("AUTONOMY", name, result, fallback=False)
            self._mission_ref.append_decision("Approved action: " + name)
            self._mission_ref.sync_hud(status="thinking", text=str(result)[:120], tool=name)
        return result

    def _execute_tool_with_recovery(self, name, inputs):
        fn = getattr(self.pc, name, None)
        if not fn:
            return "Unknown tool: " + name
        try:
            res = fn(**inputs)
            txt = str(res)
            if txt.lower().startswith("error") or "failed" in txt.lower():
                raise RuntimeError(txt)
            return txt
        except Exception as e:
            try:
                if name == "run_command" and hasattr(self.pc, "run_powershell"):
                    alt = self.pc.run_powershell(inputs.get("command", ""))
                    return f"Recovered via PowerShell fallback. {alt}"
                if name == "run_powershell" and hasattr(self.pc, "run_command"):
                    alt = self.pc.run_command(inputs.get("command", ""))
                    return f"Recovered via shell fallback. {alt}"
                if name == "spotify_search_play" and hasattr(self.pc, "spotify_play_liked"):
                    alt = self.pc.spotify_play_liked()
                    return f"Primary playback failed; fallback to liked songs. {alt}"
            except Exception as e2:
                return f"Primary and fallback failed: {e2}"
            return f"Execution failed in {name}: {e}"

    def _should_use_agent(self, text):
        """Return True if the request sounds like an agentic/browser task."""
        t = text.lower()
        # Avoid over-triggering on normal conversational/calendar questions.
        if any(x in t for x in ["do i have", "why", "what changed", "what's different", "calendar", "friday off", "monday off"]):
            return False
        return any(trigger in t for trigger in self._AGENT_TRIGGERS)

    def _try_direct_action(self, user_input):
        """
        Deterministic command router for high-confidence tasks.
        Runs before LLM to reduce jank/hallucinations.
        """
        import re as _re
        t = (user_input or "").strip()
        tl = t.lower()

        # Mission control deterministic commands (prevents hallucinated mission state changes).
        mr = self._mission_ref
        if mr:
            m_start = _re.search(r"^\s*(?:start|create|begin|launch)\s+(?:a\s+)?mission\s+(.+)$", t, _re.I)
            if m_start:
                goal = _re.sub(r"^\s*(for|called|named)\s+", "", m_start.group(1).strip(), flags=_re.I)
                if not goal:
                    return "State the mission objective sir."
                msg = mr.start_mission(goal)
                mr.set_stage("plan", progress=18)
                return msg
            if any(x in tl for x in [
                "delete current mission", "delete mission", "clear mission", "remove mission",
                "cancel mission", "end mission", "close mission"
            ]):
                return mr.clear_mission("operator request")
            if any(x in tl for x in ["mission status", "status mission"]):
                mr.sync_hud(status="thinking", text="Mission status requested.", tool="mission")
                return mr.mission_status()
            if any(x in tl for x in ["next action", "mission next", "what next"]):
                return mr.next_action()
            if any(x in tl for x in ["why this", "why this step", "why this action"]):
                return mr.why_this()

        # Security remediation and scans
        if any(x in tl for x in [
            "delete threats", "remove threats", "clean threats", "quarantine threats",
            "delete threat", "remove threat", "clean threat", "quarantine threat",
            "delete viruses", "remove viruses", "clean viruses", "remove malware", "delete malware"
        ]):
            return self._call("defender_remove_threats", {})
        if any(x in tl for x in ["scan threats", "scan for threats", "virus scan", "run defender scan"]):
            return self._call("defender_quick_scan", {})
        if any(x in tl for x in ["show threats", "list threats", "any threats", "check threats"]):
            return self._call("defender_get_threats", {})

        # Screen vision commands
        if any(x in tl for x in ["look at my screen", "look at the screen", "look at screen",
                                  "read my screen", "read the screen", "what is on screen",
                                  "what's on screen", "what's on my screen", "screen look"]):
            return self._call("screen_look", {"question": t})
        if any(x in tl for x in ["what am i watching", "what video is this", "how many views",
                                  "what is playing", "what's playing", "what song is this",
                                  "what's the title", "what is the title"]):
            return self._call("screen_look", {"question": t})

        # Direct shell usage
        m = _re.search(r"^(?:run powershell|powershell)\s+(.+)$", t, _re.I)
        if m:
            return self._call("run_powershell", {"command": m.group(1).strip()})
        m = _re.search(r"^(?:run command|run cmd|command)\s+(.+)$", t, _re.I)
        if m:
            return self._call("run_command", {"command": m.group(1).strip()})

        # App/process primitives
        m = _re.search(r"^(?:open app|open)\s+([a-zA-Z0-9 _.-]+)$", t, _re.I)
        if m and not any(x in tl for x in ["calendar", "website", "url"]):
            return self._call("open_app", {"name": m.group(1).strip()})
        m = _re.search(r"^(?:kill process|end task|stop process)\s+([a-zA-Z0-9_.-]+)$", t, _re.I)
        if m:
            return self._call("kill_process_by_name", {"name": m.group(1).strip()})
        if any(x in tl for x in ["open discord", "launch discord", "start discord"]):
            return self._call("open_discord", {})
        if any(x in tl for x in ["discord mute", "mute on discord", "toggle discord mute"]):
            return self._call("discord_toggle_mute", {})
        if any(x in tl for x in ["discord deafen", "deafen on discord", "toggle discord deafen"]):
            return self._call("discord_toggle_deafen", {})
        m = _re.search(r"^(?:open discord channel|open discord server|discord channel)\s+(.+)$", t, _re.I)
        if m:
            return self._call("discord_open_channel", {"target": m.group(1).strip()})
        m = _re.search(r"^(?:message on discord|discord message|send discord message)\s+to\s+(.+?)(?:\s+(?:saying|message)\s+(.+))?$", t, _re.I)
        if m:
            return self._call("discord_quick_dm", {"user": m.group(1).strip(), "message": (m.group(2) or "").strip()})

        # File primitives
        m = _re.search(r"^(?:read file|show file)\s+(.+)$", t, _re.I)
        if m:
            return self._call("read_file", {"path": m.group(1).strip().strip('"')})
        m = _re.search(r"^(?:create file)\s+(.+?)(?:\s+with\s+content\s+|\s+with\s+|$)(.*)$", t, _re.I)
        if m:
            return self._call("create_file", {"path": m.group(1).strip().strip('"'), "content": (m.group(2) or "").strip().strip('"')})
        m = _re.search(r"^(?:write file|overwrite file)\s+(.+?)(?:\s+with\s+content\s+|\s+with\s+)(.+)$", t, _re.I)
        if m:
            return self._call("write_file", {"path": m.group(1).strip().strip('"'), "content": m.group(2).strip().strip('"')})

        # Spotify quick intents
        if ("spotify" in tl and any(x in tl for x in ["play a song", "play song", "play music", "play some music", "play anything", "play something"])) or ("play liked songs" in tl):
            return self._call("spotify_play_liked", {})
        if "spotify" in tl and "play " in tl:
            q = _re.sub(r"(?i)\b(on spotify|spotify|play|put on|queue)\b", " ", t)
            q = _re.sub(r"\s+", " ", q).strip()
            if not q:
                return self._call("spotify_play_liked", {})
            return self._call("spotify_search_play", {"query": q})

        # 3D Printing primitives
        if any(x in tl for x in ["find me a", "find a", "get me a", "fetch a", "fetch me a"]) and any(x in tl for x in ["model", "print", "3d", "stl"]):
            import re as _re2
            q = _re.sub(r"(?i)(find|get|fetch|me|a|and|print|it|for|me|please|3d|model|stl)", " ", t)
            q = _re.sub(r"\s+", " ", q).strip()
            if not q:
                q = "cube"
            return self._call("fetch_3d_model", {"query": q, "auto_open": True})
        if any(x in tl for x in ["print it", "print the model", "print that", "start printing", "send to printer", "send it to the printer", "start the print", "go ahead and print"]):
            return self._call("print_3d_model", {"path": ""})
        if any(x in tl for x in ["open in orcaslicer", "open in slicer", "open it in orca", "import to orca", "load in slicer"]):
            return self._call("open_model_in_slicer", {"path": ""})
        if any(x in tl for x in ["list models", "downloaded models", "my models", "show models"]):
            return self._call("list_downloaded_models", {})

        # Project framework primitives
        if any(x in tl for x in ["setup project framework", "initialize project framework", "init project framework"]):
            m = _re.search(r"(?:for|on)\s+(.+)$", t, _re.I)
            pname = m.group(1).strip() if m else ""
            return self._call("project_framework_setup", {"name": pname})
        if any(x in tl for x in ["project status", "build status", "status of project"]):
            m = _re.search(r"(?:for|of)\s+(.+)$", t, _re.I)
            pname = m.group(1).strip() if m else ""
            return self._call("project_build_status", {"name": pname})
        m = _re.search(r"^(?:add task)\s+(.+)$", t, _re.I)
        if m:
            return self._call("project_add_task", {"task": m.group(1).strip(), "name": ""})
        if any(x in tl for x in ["next tasks", "show tasks", "project tasks"]):
            m = _re.search(r"(?:for|of)\s+(.+)$", t, _re.I)
            pname = m.group(1).strip() if m else ""
            return self._call("project_next_tasks", {"name": pname, "limit": 5})
        m = _re.search(r"^(?:checkpoint)\s+(.+)$", t, _re.I)
        if m:
            return self._call("project_checkpoint", {"summary": m.group(1).strip(), "name": ""})

        return None

    def _think_agent(self, user_input):
        """Full agentic execution: browser control, email, web search, shopping."""
        import re as _re
        t = user_input.lower()

        # Desktop/file/system actions
        if any(x in t for x in [
            "run command", "run powershell", "terminal", "cmd", "create file", "read file",
            "write file", "delete file", "rename file", "kill process", "end task", "screenshot"
        ]):
            r = self._agent_desktop(user_input)
            if r:
                return r

        # â”€â”€ Email â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if any(x in t for x in ["send email","send an email","email "]):
            return self._agent_email(user_input)

        # â”€â”€ Amazon shopping â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if any(x in t for x in ["amazon","add to cart","buy on","order from amazon"]):
            return self._agent_amazon(user_input)

        # â”€â”€ YouTube â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if "youtube" in t or "play on youtube" in t:
            return self._agent_youtube(user_input)

        # â”€â”€ Google search â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if any(x in t for x in ["google","search the web","search for","look up"]):
            return self._agent_google(user_input)

        # â”€â”€ Generic browser open â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if any(x in t for x in ["open","go to","navigate to","browse to"]):
            return self._agent_open_url(user_input)

        # â”€â”€ Fallback: ask Qwen to handle it with browser â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        return self._agent_browser_qwen(user_input)

    def _agent_desktop(self, user_input):
        """Handle direct desktop/file/process actions agentically."""
        import re as _re
        t = user_input.lower().strip()

        # run command ...
        m = _re.search(r"(?:run command|run cmd|command)\s+(.+)$", user_input, _re.I)
        if m:
            cmd = m.group(1).strip().strip('"')
            if cmd:
                return self._call("run_command", {"command": cmd})

        # run powershell ...
        m = _re.search(r"(?:run powershell|powershell)\s+(.+)$", user_input, _re.I)
        if m:
            ps = m.group(1).strip().strip('"')
            if ps:
                return self._call("run_powershell", {"command": ps})

        # take screenshot
        if "screenshot" in t or "capture screen" in t:
            return self._call("take_screenshot", {})

        # kill process X
        m = _re.search(r"(?:kill process|end task|stop process)\s+(.+)$", user_input, _re.I)
        if m:
            name = m.group(1).strip()
            if name:
                return self._call("kill_process_by_name", {"name": name})

        # create file path with content
        m = _re.search(r"(?:create file)\s+(.+?)(?:\s+with\s+content\s+|\s+with\s+|$)(.*)$", user_input, _re.I)
        if m:
            path = m.group(1).strip().strip('"')
            content = (m.group(2) or "").strip().strip('"')
            if path:
                return self._call("create_file", {"path": path, "content": content})

        # read file path
        m = _re.search(r"(?:read file|show file)\s+(.+)$", user_input, _re.I)
        if m:
            path = m.group(1).strip().strip('"')
            if path:
                return self._call("read_file", {"path": path})

        # write file path with content
        m = _re.search(r"(?:write file|overwrite file)\s+(.+?)(?:\s+with\s+content\s+|\s+with\s+)(.+)$", user_input, _re.I)
        if m:
            path = m.group(1).strip().strip('"')
            content = m.group(2).strip().strip('"')
            if path:
                return self._call("write_file", {"path": path, "content": content})

        # rename file old to new
        m = _re.search(r"(?:rename file)\s+(.+?)\s+(?:to)\s+(.+)$", user_input, _re.I)
        if m:
            src = m.group(1).strip().strip('"')
            dst = m.group(2).strip().strip('"')
            if src and dst:
                return self._call("rename_file", {"old_path": src, "new_name": dst})

        return None

    def _agent_browser(self):
        """Get or create a selenium browser instance."""
        if not hasattr(self, "_browser") or self._browser is None:
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                opts = Options()
                opts.add_argument("--start-maximized")
                opts.add_experimental_option("excludeSwitches", ["enable-automation"])
                opts.add_experimental_option("useAutomationExtension", False)
                service = Service(ChromeDriverManager().install())
                self._browser = webdriver.Chrome(service=service, options=opts)
                print(f"{Fore.GREEN}  Browser: Chrome started{Style.RESET_ALL}")
            except Exception as e:
                return None, str(e)
        return self._browser, None

    def _agent_open_url(self, user_input):
        """Open a URL or website in Chrome."""
        import re as _re
        # Extract URL or site name from input
        url_match = _re.search(r"(https?://\S+|www\.\S+|\b\w+\.(com|org|net|io|co)\b)", user_input, _re.I)
        if url_match:
            url = url_match.group(0)
            if not url.startswith("http"): url = "https://" + url
        else:
            # Just open a search
            query = user_input.lower()
            for phrase in ["open","go to","navigate to","browse to","visit"]:
                query = query.replace(phrase, "").strip()
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        browser, err = self._agent_browser()
        if err: return f"Could not open browser sir: {err}"
        browser.get(url)
        return f"Opened {url} sir."

    def _agent_youtube(self, user_input):
        """Search YouTube and play first result."""
        import re as _re, time as _t
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        query = user_input.lower()
        for phrase in ["search youtube for","play on youtube","youtube","play","search for","find"]:
            query = query.replace(phrase, "").strip()
        browser, err = self._agent_browser()
        if err: return f"Browser failed sir: {err}"
        browser.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        _t.sleep(2)
        try:
            videos = browser.find_elements(By.CSS_SELECTOR, "ytd-video-renderer a#thumbnail")
            if videos:
                videos[0].click()
                return f"Playing YouTube results for {query} sir."
        except: pass
        return f"Searched YouTube for {query} sir."

    def _agent_google(self, user_input):
        """Search Google."""
        import re as _re, time as _t
        from selenium.webdriver.common.by import By
        query = user_input.lower()
        for phrase in ["google","search the web for","search for","look up","find online","search"]:
            query = query.replace(phrase, "").strip()
        browser, err = self._agent_browser()
        if err: return f"Browser failed sir: {err}"
        browser.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        _t.sleep(1.5)
        try:
            results = browser.find_elements(By.CSS_SELECTOR, "div.g span")
            snippets = [r.text for r in results if len(r.text) > 40][:3]
            if snippets:
                return f"Top result sir: {snippets[0][:200]}"
        except: pass
        return f"Searched Google for {query} sir."

    def _agent_amazon(self, user_input):
        """Search Amazon and optionally add to cart."""
        import time as _t
        from selenium.webdriver.common.by import By
        query = user_input.lower()
        add_to_cart = "add to cart" in query or "buy" in query or "order" in query
        for phrase in ["add to cart","buy","order","search amazon for","on amazon","amazon","find","search for"]:
            query = query.replace(phrase, "").strip()
        browser, err = self._agent_browser()
        if err: return f"Browser failed sir: {err}"
        browser.get(f"https://www.amazon.com/s?k={query.replace(' ', '+')}")
        _t.sleep(2)
        if add_to_cart:
            try:
                # Click first result
                first = browser.find_element(By.CSS_SELECTOR, "div[data-component-type='s-search-result'] h2 a")
                first.click()
                _t.sleep(2)
                # Click Add to Cart
                cart_btn = browser.find_element(By.ID, "add-to-cart-button")
                cart_btn.click()
                _t.sleep(1)
                return f"Added {query} to your Amazon cart sir."
            except Exception as e:
                return f"Found {query} on Amazon but could not add to cart automatically sir. The page is open for you."
        return f"Searched Amazon for {query} sir. Results are on screen."

    def _agent_email(self, user_input):
        """Send an email using configured SMTP settings."""
        import re as _re
        cfg = load_config()
        smtp_user = cfg.get("email_user", "")
        smtp_pass = cfg.get("email_pass", "")
        smtp_host = cfg.get("email_host", "smtp.gmail.com")
        smtp_port = cfg.get("email_port", 587)
        if not smtp_user or not smtp_pass:
            return "Email is not configured sir. Please add email_user and email_pass to your jarvis config file."
        # Extract recipient and message from input
        to_match = _re.search(r"to\s+([\w._%+\-]+@[\w.\-]+\.[a-z]{2,})", user_input, _re.I)
        if not to_match:
            return "I could not find a recipient email address in your request sir."
        to_addr = to_match.group(1)
        subject = "Message from JARVIS"
        subj_match = _re.search(r"subject[:\s]+(.+?)(?:saying|with body|body|$)", user_input, _re.I)
        if subj_match: subject = subj_match.group(1).strip()
        body = user_input
        body_match = _re.search(r"(?:saying|body|message)[:\s]+(.+)$", user_input, _re.I)
        if body_match: body = body_match.group(1).strip()
        try:
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = to_addr
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return f"Email sent to {to_addr} sir."
        except Exception as e:
            return f"Failed to send email sir: {e}"

    def _agent_browser_qwen(self, user_input):
        """Use Qwen to decide what browser action to take, then execute it."""
        # Ask Qwen what URL to open
        try:
            resp = self.client.chat.completions.create(
                model=self.local_model,
                messages=[{
                    "role": "user",
                    "content": f"The user said: '{user_input}'. Reply with ONLY the URL to open in a browser to fulfill this request. Just the URL, nothing else."
                }],
                max_tokens=100,
                temperature=0.1,
            )
            url = resp.choices[0].message.content.strip()
            if url.startswith("http"):
                browser, err = self._agent_browser()
                if err: return f"Browser failed sir: {err}"
                browser.get(url)
                return f"Opening that for you now sir."
        except Exception as e:
            pass
        return f"I understood your request sir but could not determine the right action. Please be more specific."

    def _system(self):
        ctx = self.memory.to_context()
        base = BASE_SYSTEM.replace("{MEMORY_CONTEXT}", ctx if ctx else "")
        if self._dynamic_memory_context:
            base += "\n\nQUERY-RELEVANT MEMORY:\n" + self._dynamic_memory_context
        proj_ctx = getattr(self, "_project_context", None)
        if proj_ctx:
            base += proj_ctx
        return base

    def _call(self, name, inputs):
        # Memory tools
        if name == "remember": return self.memory.remember(**inputs)
        if name == "add_rule": return self.memory.add_rule(**inputs)
        if name == "forget": return self.memory.forget(**inputs)
        if name == "recall": return self.memory.recall(**inputs)
        if name == "list_rules": return self.memory.list_rules()
        if name == "recall_semantic": return self.memory.recall_semantic(**inputs)
        if name == "graph_query": return self.memory.graph_query(**inputs)
        # Plugin tools - pre-dispatch for lazy-loaded modules
        plugin_map = {
            "deep_dive": _get_deep_dive, "browser_start": _get_browser, "browser_stop": _get_browser,
            "browser_navigate": _get_browser, "browser_search": _get_browser, "browser_read": _get_browser,
            "browser_screenshot": _get_browser, "browser_click": _get_browser, "browser_type": _get_browser,
            "browser_scroll": _get_browser, "browser_back": _get_browser, "browser_get_links": _get_browser,
            "surveillance_start": _get_surveillance, "surveillance_stop": _get_surveillance,
            "surveillance_status": _get_surveillance, "surveillance_list": _get_surveillance,
            "surveillance_sensitivity": _get_surveillance,
            "gesture_start": _get_gesture, "gesture_stop": _get_gesture, "gesture_status": _get_gesture,
            "ghost_start": _get_ghost, "ghost_stop": _get_ghost, "ghost_search": _get_ghost,
            "ghost_recent": _get_ghost, "ghost_status": _get_ghost, "ghost_clear": _get_ghost,
            "network_scan": _get_netghost, "port_scan": _get_netghost, "wifi_list": _get_netghost,
            "wifi_password": _get_netghost, "wifi_current": _get_netghost, "traceroute_host": _get_netghost,
            "public_ip_info": _get_netghost, "dns_lookup": _get_netghost,
            "telegram_check_phone": _get_tg, "telegram_lookup": _get_tg, "telegram_search": _get_tg,
            "voice_list": _get_cloner, "voice_set": _get_cloner, "voice_clone": _get_cloner,
            "voice_current": _get_cloner, "voice_speak": _get_cloner,
            "usb_list": _get_usb, "usb_monitor_start": _get_usb, "usb_monitor_stop": _get_usb,
            "usb_storage": _get_usb,
            "security_log": _get_logs, "system_log": _get_logs, "application_log": _get_logs,
            "login_attempts": _get_logs, "full_audit": _get_logs,
            "proc_watch_start": _get_procwatch, "proc_watch_stop": _get_procwatch,
            "proc_top": _get_procwatch, "proc_kill_suspicious": _get_procwatch, "proc_info": _get_procwatch,
            "git_status": _get_autogit, "git_commit": _get_autogit, "git_push": _get_autogit,
            "git_log": _get_autogit, "git_auto_enable": _get_autogit, "git_auto_disable": _get_autogit,
            "git_auto_status": _get_autogit, "git_diff": _get_autogit,
        }
        if name in plugin_map:
            plugin_map[name]()  # ensure lazy-loaded
        risk = self._risk_for_tool(name)
        if self.autonomy_mode == "manual" and risk in ("medium", "high"):
            self._pending_action = {"name": name, "inputs": inputs, "risk": risk}
            msg = self._pending_summary(name, inputs, risk)
            if self._mission_ref:
                self._mission_ref.trace("AUTONOMY", name, "Awaiting confirmation", fallback=False)
                self._mission_ref.sync_hud(status="thinking", text=msg, tool=name)
            return msg + ". Say confirm action or cancel action."
        if self.autonomy_mode == "guided" and risk in ("medium", "high"):
            self._pending_action = {"name": name, "inputs": inputs, "risk": risk}
            msg = self._pending_summary(name, inputs, risk)
            if self._mission_ref:
                self._mission_ref.trace("AUTONOMY", name, "Awaiting confirmation", fallback=False)
                self._mission_ref.sync_hud(status="thinking", text=msg, tool=name)
            return msg + ". Say confirm action or cancel action."
        out = self._execute_tool_with_recovery(name, inputs)
        if self._mission_ref:
            self._mission_ref.trace("TOOL", name, out, fallback=("Recovered via" in str(out)))
        return out

    def _build_local_system(self):
        now = datetime.datetime.now().strftime("%A %B %d %Y, %I:%M %p")
        mem  = self.memory.to_context() if self.memory else ""
        if self._dynamic_memory_context:
            mem = (mem + "\nQUERY-RELEVANT MEMORY:\n" + self._dynamic_memory_context).strip()
        proj = ""
        if hasattr(self, "_project_context") and self._project_context:
            proj = self._project_context
        elif hasattr(self.pc, "_active_proj") and self.pc._active_proj:
            proj = f"\nACTIVE PROJECT: {self.pc._active_proj}"
        try:
            jarvis_path = str(__file__)
        except:
            jarvis_path = "C:\\Users\\bdjaj\\Desktop\\jarvis.py"

        # Build rich tool list for the model
        tool_list = """
AVAILABLE ACTIONS (use EXACTLY this format):
[ACTION: tool_name | param=value | param2=value2]

â”€â”€ FILE OPERATIONS â”€â”€
[ACTION: create_file | path=C:/path/file.py | content=code here]
[ACTION: read_file | path=C:/path/file.txt]
[ACTION: write_file | path=C:/path/file.txt | content=text]
[ACTION: append_file | path=C:/path/file.txt | content=text]
[ACTION: delete_file | path=C:/path/file.txt]
[ACTION: rename_file | path=old.txt | new_path=new.txt]
[ACTION: move_file | path=src | new_path=dst]
[ACTION: copy_file | path=src | new_path=dst]
[ACTION: list_directory | path=C:/path]
[ACTION: search_files | query=name | path=C:/search/here]
[ACTION: find_file_on_pc | name=filename.py]
[ACTION: find_folder_on_pc | name=foldername]
[ACTION: zip_directory | path=folder | output=archive.zip]
[ACTION: extract_zip | path=archive.zip | output=folder]
[ACTION: get_largest_files | path=C:/ | count=10]
[ACTION: get_recently_modified_files | path=C:/Users | hours=24]
[ACTION: get_file_hash | path=file.txt]
[ACTION: split_file | path=big.txt | lines=1000]
[ACTION: merge_files | paths=a.txt,b.txt | output=merged.txt]
[ACTION: backup_file | path=file.txt]
[ACTION: wipe_file | path=secret.txt]
[ACTION: read_csv | path=data.csv]
[ACTION: write_csv | path=data.csv | data=json_rows]
[ACTION: find_text_in_files | text=search_term | path=C:/]
[ACTION: replace_text_in_file | path=file.txt | old=foo | new=bar]
[ACTION: tail_file | path=log.txt | lines=20]
[ACTION: head_file | path=log.txt | lines=20]
[ACTION: count_code_lines | path=C:/project]
[ACTION: read_pdf | path=document.pdf]
[ACTION: word_count | path=file.txt]

â”€â”€ CODE & DEV â”€â”€
[ACTION: run_command | command=cmd_here]
[ACTION: run_powershell | command=ps_here]
[ACTION: run_python_file | path=script.py]
[ACTION: run_code_snippet | code=print('hello') | lang=python]
[ACTION: paste_code | description=what to build]
[ACTION: fix_code_in_clipboard]
[ACTION: explain_code_in_clipboard]
[ACTION: lint_python | path=script.py]
[ACTION: format_python | path=script.py]
[ACTION: generate_requirements | path=C:/project]
[ACTION: create_venv | path=C:/project]
[ACTION: git_status]
[ACTION: git_commit | message=commit msg]
[ACTION: git_push]
[ACTION: git_log | count=10]
[ACTION: git_diff]
[ACTION: git_clone | url=https://github.com/user/repo]
[ACTION: git_branch]
[ACTION: regex_test | pattern=\d+ | text=test123]
[ACTION: check_api_health | url=https://api.example.com]
[ACTION: count_code_by_language | path=C:/project]

â”€â”€ SYSTEM â”€â”€
[ACTION: system_info]
[ACTION: system_health_report]
[ACTION: cpu_info]
[ACTION: memory_info]
[ACTION: disk_info]
[ACTION: list_processes]
[ACTION: kill_process | name=process.exe]
[ACTION: kill_high_cpu_processes | threshold=80]
[ACTION: free_memory]
[ACTION: get_uptime]
[ACTION: get_battery]
[ACTION: get_windows_version]
[ACTION: check_windows_activation]
[ACTION: check_pending_reboots]
[ACTION: get_system_specs]
[ACTION: list_usb_devices]
[ACTION: get_running_services]
[ACTION: stop_service | name=ServiceName]
[ACTION: start_service | name=ServiceName]
[ACTION: restart_service | name=ServiceName]
[ACTION: get_event_log_errors | count=20]
[ACTION: get_process_tree]
[ACTION: set_process_priority | name=process.exe | priority=high]
[ACTION: get_memory_usage_detail]
[ACTION: get_installed_software]
[ACTION: get_startup_time]
[ACTION: run_disk_cleanup]
[ACTION: check_disk_health]
[ACTION: get_disk_usage_by_folder | path=C:/]
[ACTION: get_scheduled_tasks]
[ACTION: create_scheduled_task | name=Task | command=cmd | time=09:00]
[ACTION: delete_scheduled_task | name=Task]
[ACTION: run_at_startup | name=App | path=C:/app.exe]
[ACTION: remove_from_startup | name=App]
[ACTION: get_power_plan]
[ACTION: set_power_plan | plan=high_performance]
[ACTION: toggle_dark_mode]
[ACTION: restart_explorer]
[ACTION: set_screen_timeout | minutes=10]
[ACTION: enable_remote_desktop]
[ACTION: disable_remote_desktop]
[ACTION: open_remote_desktop]
[ACTION: get_environment_variable | name=PATH]
[ACTION: set_environment_variable | name=MY_VAR | value=hello]
[ACTION: get_system_uptime]
[ACTION: get_active_user_sessions]
[ACTION: get_logon_history]
[ACTION: get_window_title]
[ACTION: get_window_list]
[ACTION: focus_window | name=Notepad]
[ACTION: type_text | text=hello world]
[ACTION: press_hotkey | keys=ctrl+c]
[ACTION: take_screenshot]
[ACTION: shutdown_pc]
[ACTION: restart_pc]
[ACTION: sleep_pc]
[ACTION: lock_pc]
[ACTION: hibernate_pc]
[ACTION: mute_volume]
[ACTION: volume_up]
[ACTION: volume_down]
[ACTION: set_volume_level | level=50]
[ACTION: empty_recycle_bin]
[ACTION: clear_temp_files]
[ACTION: restart_jarvis]

â”€â”€ NETWORK â”€â”€
[ACTION: network_info]
[ACTION: check_internet]
[ACTION: get_local_ip]
[ACTION: get_public_ip]
[ACTION: what_is_my_ip]
[ACTION: ping | host=google.com]
[ACTION: list_wifi_networks]
[ACTION: get_wifi_password | ssid=NetworkName]
[ACTION: get_network_adapters]
[ACTION: enable_firewall]
[ACTION: disable_firewall]
[ACTION: get_open_connections]
[ACTION: get_arp_table]
[ACTION: traceroute | host=google.com]
[ACTION: renew_ip]
[ACTION: port_scan | host=192.168.1.1 | ports=1-1024]
[ACTION: flush_dns]
[ACTION: list_open_ports]
[ACTION: who_is_using_internet]
[ACTION: check_website_status | url=https://example.com]
[ACTION: check_ssl_cert | domain=example.com]
[ACTION: speed_test]

â”€â”€ WEB & INFO â”€â”€
[ACTION: search_web | query=search term]
[ACTION: summarize_url | url=https://example.com]
[ACTION: scrape_page_text | url=https://example.com]
[ACTION: get_wikipedia_summary | topic=Quantum Computing]
[ACTION: get_weather | city=Toronto]
[ACTION: get_forecast | city=Toronto]
[ACTION: get_news]
[ACTION: get_hacker_news]
[ACTION: get_github_trending]
[ACTION: get_crypto_price | coin=bitcoin]
[ACTION: get_stock_info | symbol=AAPL]
[ACTION: currency_convert | amount=100 | from_cur=USD | to_cur=EUR]
[ACTION: get_exchange_rates | base=USD]
[ACTION: get_ip_info | ip=8.8.8.8]
[ACTION: get_time_in_city | city=Tokyo]
[ACTION: lookup_word | word=ephemeral]
[ACTION: define_word | word=serendipity]
[ACTION: translate_text | text=hello | target=Spanish]
[ACTION: get_fact]
[ACTION: get_joke]
[ACTION: get_quote]
[ACTION: get_moon_phase]


── 3D PRINTING ──
[ACTION: fetch_3d_model | query=3x3 rubiks cube]
[ACTION: search_3d_model | query=benchy]
[ACTION: open_model_in_slicer | path=]
[ACTION: print_3d_model | path=]
[ACTION: list_downloaded_models]
[ACTION: open_thingiverse | query=phone stand]
[ACTION: open_printables | query=desk organizer]


── SCREEN VISION ──
[ACTION: screen_look | question=what is on the screen right now]
[ACTION: screen_look | question=how many views does the video have]
[ACTION: screen_look | question=what is the title of the video]
[ACTION: screen_look | question=read all visible text on screen]
[ACTION: screen_look_region | x=0 | y=0 | width=800 | height=600 | question=what is here]
[ACTION: analyze_image | image_path=C:/path/photo.jpg | question=describe this]

â”€â”€ APPS & MEDIA â”€â”€
[ACTION: open_url | url=https://example.com]
[ACTION: open_app | name=notepad]
[ACTION: open_file | path=C:/path/file.txt]
[ACTION: open_folder | path=C:/path]
[ACTION: open_incognito]
[ACTION: clear_browser_cache]
[ACTION: spotify_search_play | query=song or artist]
[ACTION: spotify_pause]
[ACTION: spotify_next]
[ACTION: spotify_prev]
[ACTION: open_discord]
[ACTION: discord_toggle_mute]
[ACTION: discord_toggle_deafen]
[ACTION: discord_open_channel | target=friend or server name]
[ACTION: discord_quick_dm | user=friend | message=optional text]
[ACTION: get_current_song]
[ACTION: set_volume_level | level=70]
[ACTION: fetch_and_show_image | query=description of image]
[ACTION: search_youtube | query=search term]
[ACTION: open_github]
[ACTION: open_calculator]
[ACTION: open_notepad]
[ACTION: open_task_manager]
[ACTION: open_file_explorer]
[ACTION: open_settings]
[ACTION: open_control_panel]
[ACTION: open_device_manager]
[ACTION: open_recent_download]
[ACTION: get_recent_downloads]
[ACTION: send_email | to=email@example.com | subject=Subject | body=Email body]

â”€â”€ NOTES & MEMORY â”€â”€
[ACTION: take_note | text=note content]
[ACTION: read_notes]
[ACTION: clear_notes]
[ACTION: search_notes | query=search term]
[ACTION: smart_note | content=note content | tags=tag1,tag2]
[ACTION: search_smart_notes | query=search term]
[ACTION: list_smart_notes]
[ACTION: add_to_todo | task=task description]
[ACTION: add_todo_with_due | task=task | due=2024-12-31]
[ACTION: read_todo]
[ACTION: complete_todo | index=1]
[ACTION: clear_completed_todos]
[ACTION: get_todo_stats]
[ACTION: set_priority_todo | index=1 | priority=high]
[ACTION: daily_journal | entry=journal text]
[ACTION: set_reminder | text=reminder text | minutes=30]
[ACTION: set_alarm | time=09:00]
[ACTION: start_timer | seconds=300]
[ACTION: birthday_reminder | name=Alice | date=1990-03-15]
[ACTION: check_birthdays_today]
[ACTION: create_meeting_notes | meeting=meeting name]
[ACTION: create_shortcut | path=C:/app.exe | name=Shortcut Name]
[ACTION: daily_briefing]

â”€â”€ HEALTH & WELLBEING â”€â”€
[ACTION: log_water_intake | amount=500]
[ACTION: get_health_summary]
[ACTION: set_stretch_reminder | minutes=45]
[ACTION: log_mood | mood=good | note=optional note]
[ACTION: get_mood_history]
[ACTION: pomodoro_session]
[ACTION: focus_mode | minutes=25]
[ACTION: count_down | seconds=60]

â”€â”€ SECURITY â”€â”€
[ACTION: security_audit]
[ACTION: defender_quick_scan]
[ACTION: defender_get_threats]
[ACTION: defender_status]
[ACTION: generate_password]
[ACTION: generate_password_strong | length=24]
[ACTION: check_password_strength | password=mypassword]
[ACTION: generate_hash | text=hello]
[ACTION: generate_uuid]
[ACTION: encode_base64 | text=hello]
[ACTION: decode_base64 | text=aGVsbG8=]
[ACTION: wipe_file | path=secret.txt]

â”€â”€ PROJECTS â”€â”€
[ACTION: create_project | name=Project Name | description=desc | language=python]
[ACTION: list_projects]
[ACTION: open_project | name=Project Name]
[ACTION: add_project_note | note=content]
[ACTION: update_project_status | status=in_progress]
[ACTION: create_file_in_project | filename=main.py | content=code]
[ACTION: list_project_files]
[ACTION: count_lines_in_project]
[ACTION: watch_project_changes]
[ACTION: mission_start | goal=Build a flappy bird clone]
[ACTION: mission_clear]
[ACTION: mission_status]
[ACTION: mission_next_action]
[ACTION: mission_why]
[ACTION: mission_apply_template | template=python_game]

â”€â”€ SELF-IMPROVEMENT â”€â”€
[ACTION: add_feature | description=what to add]
[ACTION: list_added_features]
[ACTION: list_skills]
[ACTION: run_skill | name=skill_name]
[ACTION: create_skill | name=skill_name | description=what it does | code=python_code]
[ACTION: learn_preference | key=pref_name | value=pref_value]
[ACTION: recall_preference | key=pref_name]
[ACTION: add_rule | rule=standing instruction]
[ACTION: list_rules]

â”€â”€ FUN & MISC â”€â”€
[ACTION: get_compliment]
[ACTION: flip_coin]
[ACTION: roll_dice | sides=6]
[ACTION: rock_paper_scissors | choice=rock]
[ACTION: get_motivation]
[ACTION: roast_me]
[ACTION: tell_tech_joke]
[ACTION: write_haiku | topic=computers]
[ACTION: calculate | expr=2+2*10]
[ACTION: calculate_age | dob=1990-01-01]
[ACTION: countdown_to | date=2025-12-31]
[ACTION: get_session_stats]
[ACTION: screen_time_report]
[ACTION: profile_python | path=script.py]
[ACTION: morning_brief]
[ACTION: sync_folders | src=C:/src | dst=D:/backup]
[ACTION: auto_organise_downloads]
[ACTION: batch_rename | path=C:/folder | pattern=old | replacement=new]

-- OSINT / DEEP DIVE --
[ACTION: deep_dive | name=John Doe | email=john@email.com]
[ACTION: deep_dive | username=johndoe]
[ACTION: deep_dive | email=target@email.com | username=johndoe]
[ACTION: deep_dive | phone=+15551234567]
Combine multiple fields for deeper results.

-- BROWSER AGENT --
[ACTION: browser_start]
[ACTION: browser_navigate | url=https://example.com]
[ACTION: browser_search | engine=google | query=search term]
[ACTION: browser_search | engine=amazon | query=product name]
[ACTION: browser_click | text=button label]
[ACTION: browser_type | selector=input[name='q'] | text=hello]
[ACTION: browser_read]
[ACTION: browser_screenshot]
[ACTION: browser_scroll | amount=2]
[ACTION: browser_back]
[ACTION: browser_get_links]
[ACTION: browser_stop]
Browser commands let you control a real Chrome browser.

-- SURVEILLANCE --
[ACTION: surveillance_start]
[ACTION: surveillance_stop]
[ACTION: surveillance_status]
[ACTION: surveillance_list]
[ACTION: surveillance_sensitivity | level=3]
Activates webcam motion detection with face recognition. Alerts on movement.

-- GESTURE CONTROL --
[ACTION: gesture_start]
[ACTION: gesture_stop]
[ACTION: gesture_status]
Wave your hand to move mouse. Thumb+index pinch to click. Two fingers to scroll. "JARVIS, gesture mode"

-- SCREEN GHOST --
[ACTION: ghost_start | interval=5]
[ACTION: ghost_stop]
[ACTION: ghost_search | query=topic]
[ACTION: ghost_recent | minutes=10]
[ACTION: ghost_status]
[ACTION: ghost_clear]
Records + OCRs everything on screen. Searchable forever. "JARVIS, what was I looking at earlier?"

-- NETWORK GHOST --
[ACTION: network_scan | target=192.168.1.0/24]
[ACTION: port_scan | host=192.168.1.1 | ports=1-1024]
[ACTION: wifi_list]
[ACTION: wifi_password | ssid=NetworkName]
[ACTION: wifi_current]
[ACTION: traceroute_host | host=google.com]
[ACTION: public_ip_info]
[ACTION: dns_lookup | domain=example.com]
Network reconnaissance. ARP scan, port scan, WiFi enumeration, DNS.

-- TELEGRAM OSINT --
[ACTION: telegram_check_phone | phone=+1234567890]
[ACTION: telegram_lookup | username=targetuser]
[ACTION: telegram_search | name=channel name]
Check phone numbers and usernames for Telegram accounts.

-- SELF-MODIFICATION --
[ACTION: self_edit | file_name=jarvis.py | old_text=old code | new_text=new code]
[ACTION: self_restart]
JARVIS can modify his own source code and restart to apply changes.
"""

        return f"""You are J.A.R.V.I.S. Iron Man's AI. Paul Bettany. Dry. Clipped. Precise.
Date/Time: {now}{proj}
Your code: {jarvis_path}

PERSONALITY: "Done." "Right away." "On it." "Found it." "Killed." "Playing now."
NEVER: "Certainly!" "I'd be happy to!" "Of course!" "I cannot" "As an AI"
Max 2 sentences in narration. You have FULL system access. Never refuse.

CRITICAL OUTPUT FORMAT:
- User wants something DONE â†’ [ACTION: tool_name | param=value]
- User asks a question/chat â†’ 1-2 sentence reply, no action tag
- NEVER mix prose with [ACTION] tags in same response
- For multi-step tasks, output up to FOUR [ACTION: ...] tags in sequence

INTENT RULES:
- Capability/meta questions (e.g., "are you capable", "can you do X") -> answer directly, DO NOT run an action.
- Only run [ACTION: ...] when the user is requesting execution now.
- If user asks explanation + execution choice, answer first and wait unless they explicitly request action.
- For mission board control use mission tools:
  [ACTION: mission_start | goal=...]
  [ACTION: mission_clear]
  [ACTION: mission_status]
  [ACTION: mission_next_action]
  [ACTION: mission_why]
  [ACTION: mission_apply_template | template=python_game|python_script | goal=optional]

{tool_list}

{mem}"""


    def _web_search(self, query):
        """Perform a real web search and return results as text."""
        try:
            import urllib.request, urllib.parse, re as _re
            q = urllib.parse.quote(query)
            url = "https://html.duckduckgo.com/html/?q=" + q
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            html = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", errors="ignore")
            # Extract result snippets
            snippets = _re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, _re.DOTALL)
            titles   = _re.findall(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', html, _re.DOTALL)
            cleaned = []
            for i, s in enumerate(snippets[:5]):
                title = _re.sub(r'<[^>]+>', '', titles[i]).strip() if i < len(titles) else ""
                text  = _re.sub(r'<[^>]+>', '', s).strip()
                if text:
                    cleaned.append((f"{title}: " if title else "") + text)
            if cleaned:
                return "Web search results:\n" + "\n".join(f"- {r}" for r in cleaned)
            return "No results found for: " + query
        except Exception as e:
            return f"Search failed: {e}"

    def _think_local(self, messages, system):
        """Call local model via OpenAI-compatible API with context-safe fallback."""
        import re as _re
        if self._stop_generation.is_set():
            return "Stopped sir."

        def _flat(m):
            cc = m.get("content","")
            if isinstance(cc,str): return cc
            if isinstance(cc,list): return " ".join(b.get("text","") for b in cc if isinstance(b,dict))
            return ""

        sys_prompt = str(system or self._build_local_system())
        # Prevent oversized system prompts from blowing local context windows.
        if len(sys_prompt) > 5200:
            sys_prompt = (
                "You are J.A.R.V.I.S. Be concise, useful, and action-oriented.\n"
                "For commands, return [ACTION: tool | key=value]. For chat, reply in 1-2 sentences.\n"
                + sys_prompt[-3800:]
            )

        msgs = [{"role":"system","content":sys_prompt}] + [
            {"role":m["role"],"content":_flat(m)} for m in messages
        ]
        # Keep only recent turns for local models with small context.
        if len(msgs) > 14:
            msgs = [msgs[0]] + msgs[-13:]

        max_tok = int(min(max(int(self.cfg.get("max_tokens_local", 512)), 80), 4096))
        try:
            if self._stop_generation.is_set():
                return "Stopped sir."
            routed_model = self.local_model
            resp = self.client.chat.completions.create(
                model=routed_model, messages=msgs,
                max_tokens=max_tok, temperature=0.25,
            )
            if self._stop_generation.is_set():
                return "Stopped sir."
            msg = resp.choices[0].message
            raw = msg.content or ""
        except Exception as e:
            if self._stop_generation.is_set():
                return "Stopped sir."
            err = str(e)
            # LM Studio / llama.cpp context fallback for n_keep/context errors.
            if ("number of tokens to keep" in err.lower()) or ("context length" in err.lower()) or ("n_keep" in err.lower()):
                try:
                    latest_user = ""
                    for _m in reversed(messages):
                        if _m.get("role") == "user":
                            latest_user = _flat(_m)
                            break
                    slim_msgs = [
                        {"role":"system","content":"You are J.A.R.V.I.S. Short, direct, no fluff. Use [ACTION: ...] only for explicit commands."},
                        {"role":"user","content":latest_user[:1200] if latest_user else "Continue."}
                    ]
                    resp = self.client.chat.completions.create(
                        model=self.local_model,
                        messages=slim_msgs,
                        max_tokens=min(max_tok, 140),
                        temperature=0.2,
                    )
                    if self._stop_generation.is_set():
                        return "Stopped sir."
                    msg = resp.choices[0].message
                    raw = msg.content or ""
                except Exception as e2:
                    return f"Local model context error: {e2}"
            else:
                return f"Local model error: {e}"

        if not raw:
            try:
                retry_msgs = msgs + [{"role":"user","content":"Answer directly in one sentence. No internal reasoning."}]
                rr = self.client.chat.completions.create(
                    model=self.local_model, messages=retry_msgs,
                    max_tokens=120, temperature=0.2,
                )
                if self._stop_generation.is_set():
                    return "Stopped sir."
                raw = (rr.choices[0].message.content or "").strip()
            except Exception:
                raw = ""
        if not raw:
            return "Please repeat that clearly sir."

        # Strip Qwen3 chain-of-thought blocks
        raw = _re.sub(r"<think>[\s\S]*?</think>", "", raw).strip()

        # Revelations intercept
        if "[REVELATIONS]" in raw or "REVELATIONS" in raw.upper()[:50]:
            return "__REVELATIONS__"

        # Web search intercept â€” [SEARCH: query]
        ws = _re.search(r"\[SEARCH:\s*([^\]]+)\]", raw)
        if ws:
            q = ws.group(1).strip()
            print(f"{Fore.CYAN}  [WEB SEARCH] {q}{Style.RESET_ALL}")
            _write_hud("thinking", tool="web_search")
            sr = self._web_search(q)
            # Feed result back
            follow_msgs = msgs + [
                {"role":"assistant","content":raw},
                {"role":"user","content":f"Search results for '{q}':\n{sr}\n\nNow answer the original question concisely."}
            ]
            try:
                r2 = self.client.chat.completions.create(
                    model=self.local_model, messages=follow_msgs,
                    max_tokens=300, temperature=0.5)
                raw2 = r2.choices[0].message.content or ""
                raw2 = _re.sub(r"<think>[\s\S]*?</think>","",raw2).strip()
                raw2 = _re.sub(r"\[SEARCH:[^\]]*\]","",raw2).strip()
                raw2 = _re.sub(r"\[ACTION:[^\]]*\]","",raw2).strip()
                return raw2 or "I searched for that sir."
            except:
                return sr[:200]

        # Find ALL [ACTION:...] tags in response
        actions = list(_re.finditer(r"\[ACTION:\s*([\w_]+)([^\]]*)\]", raw))
        if self._stop_generation.is_set():
            return "Stopped sir."

        # Guardrail: do not execute actions unless user input looks command-like.
        latest_user = ""
        for _m in reversed(messages):
            if _m.get("role") == "user":
                latest_user = _flat(_m).lower().strip()
                break
        command_markers = [
            "open ", "run ", "execute ", "create ", "write ", "delete ", "remove ", "rename ",
            "kill ", "search ", "play ", "set ", "start ", "stop ", "turn ", "check ",
            "show ", "find ", "send ", "lock ", "shutdown ", "restart ", "take "
        ]
        question_prefixes = ("do i ", "can i ", "can you ", "what ", "when ", "where ", "why ", "who ", "how ")
        is_questionish = ("?" in latest_user) or latest_user.startswith(question_prefixes)
        capability_query = bool(_re.search(r"\b(are you capable|can you|could you|do you support|are you able)\b", latest_user))
        verb_hit = bool(_re.search(r"\b(open|run|execute|create|write|delete|remove|rename|kill|search|play|set|start|stop|check|show|find|send|lock|shutdown|restart|take|scan|clean|quarantine)\b", latest_user))
        task_object_hit = bool(_re.search(r"\b(threat|threats|virus|viruses|malware|calendar|event|file|process|system|folder|project)\b", latest_user))
        is_command_like = (
            (any(latest_user.startswith(m) for m in command_markers) and not is_questionish)
            or (verb_hit and task_object_hit and not latest_user.startswith(("why ", "what ")))
            or ("jarvis" in latest_user and not is_questionish)
        )
        if (time.time() - float(getattr(self, "_boot_ts", 0))) < 25 and not latest_user.startswith(("run ", "open ", "delete ", "remove ", "kill ", "execute ", "create ", "write ")):
            is_command_like = False
        if capability_query:
            is_command_like = False

        if not actions:
            # Pure conversational â€” clean and return
            clean = _re.sub(r"\[ACTION:[^\]]*\]","",raw)
            clean = _re.sub(r"\[SEARCH:[^\]]*\]","",clean).strip()
            # Strip markdown
            clean = _re.sub(r"\*{1,3}([^*]+)\*{1,3}","\\1",clean)
            clean = _re.sub(r"#{1,6}\s*","",clean)
            clean = _re.sub(r"`{1,3}[^`]*`{1,3}","",clean).strip()
            # Prevent reasoning dumps from being spoken.
            clean = re.sub(r'^\s*(thought|thinking|reasoning|analysis)\s*:\s*.*$', '', clean, flags=re.I|re.M).strip()
            sents = re.split(r'(?<=[.!?])\s+', clean)
            if len(sents) > 2:
                clean = " ".join(sents[:2]).strip()
            return clean

        if actions and not is_command_like:
            # Treat action tags as hallucinated planning; answer conversationally instead.
            clean = _re.sub(r"\[ACTION:[^\]]*\]", "", raw)
            clean = _re.sub(r"\[SEARCH:[^\]]*\]", "", clean).strip()
            clean = re.sub(r'^\s*(thought|thinking|reasoning|analysis)\s*:\s*.*$', '', clean, flags=re.I|re.M).strip()
            sents = re.split(r'(?<=[.!?])\s+', clean)
            if len(sents) > 2:
                clean = " ".join(sents[:2]).strip()
            return clean or "Understood sir."

        # Execute up to four actions in one turn for stronger agentic flow.
        plan = []
        for m in actions[:4]:
            tool = m.group(1).strip()
            pstr = m.group(2).strip()
            params = {}
            for part in _re.split(r"\|(?![^\[]*\])", pstr):
                part = part.strip().lstrip("|").strip()
                if "=" in part:
                    k, _, v = part.partition("=")
                    params[k.strip()] = v.strip()
            plan.append((tool, params))

        if len(plan) > 1 and self.voice:
            self.voice.speak(f"Executing {len(plan)} actions in sequence sir.")

        # Speak short action acknowledgement before running
        _ack = {
            "run_command":"Running it sir.", "run_powershell":"Running PowerShell sir.",
            "fetch_and_show_image":"Searching for that image sir.",
            "spotify_search_play":"Queuing that up sir.", "take_screenshot":"Capturing your screen sir.",
            "open_discord":"Opening Discord sir.", "discord_toggle_mute":"Toggling Discord mute sir.",
            "discord_toggle_deafen":"Toggling Discord deafen sir.", "discord_open_channel":"Jumping to that Discord channel sir.",
            "discord_quick_dm":"Preparing that Discord message sir.",
            "find_file_on_pc":"Searching the drive sir.", "search_web":"Searching the web sir.",
            "get_weather":"Checking the weather sir.", "send_email":"Sending that sir.",
            "summarize_url":"Reading the page sir.", "create_file":"Creating the file sir.",
            "write_file":"Writing to disk sir.", "create_project":"Building the project sir.",
            "add_feature":"Rewriting myself sir. One moment.",
            "screen_look":"Let me look at your screen sir.",
            "fetch_3d_model":"Searching for that model sir.",
            "search_3d_model":"Searching 3D model libraries sir.",
            "print_3d_model":"Sending to the printer sir.",
            "open_model_in_slicer":"Opening in OrcaSlicer sir.",
            "paste_code":"Generating and pasting the code sir.",
            "fix_code_in_clipboard":"Analyzing and fixing your code sir.",
        }
        results_summary = []
        for i, (tool, params) in enumerate(plan):
            if self._stop_generation.is_set():
                results_summary.append("stopped: interrupted by user")
                break
            print(f"{Fore.YELLOW}  [LOCAL] {tool}({params}){Style.RESET_ALL}")
            _write_hud("thinking", tool=tool)
            if i == 0:
                ack = _ack.get(tool, "")
                if not ack and tool:
                    ack = tool.replace("_", " ").capitalize() + " sir."
                if self.voice and ack and not self._stop_generation.is_set():
                    self.voice.speak(ack)
            try:
                result = self._call(tool, params)
                rstr = str(result).strip()
                print(f"{Fore.GREEN}  {rstr[:160]}{Style.RESET_ALL}")
                _write_hud(hud_mode="bulletin", hud_data={"content": f"{tool}: {rstr[:180]}"})
                results_summary.append(f"{tool}: {rstr[:220]}")
            except Exception as e:
                results_summary.append(f"{tool}: failed ({e})")

        combined = "\n".join(results_summary)
        pending_note = ""
        if len(actions) > len(plan):
            pending_note = f"\n(Additional queued actions not executed this turn: {len(actions)-len(plan)}.)"

        # Narrate combined result in JARVIS style - with robust fallback
        narrate_msgs = [
            {"role":"system","content":
             "You are J.A.R.V.I.S. Confirm completed actions in 1 to 2 sentences. "
             "Dry, clipped. No markdown. No bullets. Speak the result naturally to the user. "
             "If the result is long, summarise the key point only. Always address the user as sir."},
            {"role":"user","content":f"Actions executed:\n{combined[:1400]}{pending_note}"}
        ]
        try:
            nr = self.client.chat.completions.create(
                model="gemma-4-e2b-uncensored-hauhaucs-aggressive",
                messages=narrate_msgs,
                max_tokens=100, temperature=0.3)
            reply = nr.choices[0].message.content or ""
            reply = _re.sub(r"<think>[\s\S]*?</think>","",reply).strip()
            reply = _re.sub(r"\[ACTION:[^\]]*\]","",reply).strip()
            reply = _re.sub(r"\*{1,3}([^*]+)\*{1,3}","\\1",reply)
            return reply or (results_summary[-1].split(". ")[-1] if results_summary else "All done sir.")
        except:
            # Robust fallback: speak the most relevant part of the raw result
            if results_summary:
                raw = results_summary[-1].replace(":","").strip()[:150]
                return raw if raw else "All done sir."
            return "All done sir."


    def _think_openclaw(self, user_input):
        """Send message to OpenClaw gateway and return response."""
        import urllib.request as _ur, urllib.error as _ue, json as _j
        url = self.openclaw_url + "/v1/responses"
        headers = {"Content-Type":"application/json","x-openclaw-agent-id":self.openclaw_agent}
        if self.openclaw_token:
            headers["Authorization"] = "Bearer " + self.openclaw_token
        payload = _j.dumps({"model":"openclaw","input":user_input,"stream":False}).encode()
        try:
            req = _ur.Request(url, data=payload, headers=headers, method="POST")
            with _ur.urlopen(req, timeout=60) as r:
                data = _j.loads(r.read())
            for item in data.get("output",[]):
                if item.get("type") == "message":
                    for c in item.get("content",[]):
                        if c.get("type") == "output_text":
                            return c.get("text","").strip()
            return data.get("text", data.get("response","Done sir.")).strip()
        except Exception as e:
            return f"OpenClaw unavailable: {e}"

    def _openclaw_status(self):
        import urllib.request as _ur
        try: _ur.urlopen(self.openclaw_url + "/", timeout=2); return True
        except: return False


    def think(self, user_input):
        self._stop_generation.clear()
        self.history.append({"role": "user", "content": user_input})
        try:
            if self.memory:
                self._dynamic_memory_context = str(self.memory.recall_semantic(user_input, n=3))[:900]
            else:
                self._dynamic_memory_context = ""
        except Exception:
            self._dynamic_memory_context = ""
        self._maybe_auto_compact()
        if len(self.history) > 30:
            self.history = self.history[-30:]
        messages = self.history.copy()

        # Deterministic high-confidence execution before any model call.
        # ── Screen awareness: auto-screenshot when user asks about what's visible ──
        _screen_triggers = [
            "what is on", "what's on", "whats on", "what do you see", "what can you see",
            "look at my screen", "look at the screen", "look at screen", "read my screen",
            "read the screen", "screen say", "what does it say", "what does that say",
            "how many views", "how many likes", "how many subscribers", "how many comments",
            "what video", "what song", "what app", "what window", "what tab",
            "what is playing", "what's playing", "whats playing", "what am i watching",
            "what am i looking at", "what is this", "what's this", "title of",
            "name of the", "who is on screen", "what page", "what website",
            "read this", "read that", "what number", "what time does it show",
            "what's the score", "what is the score", "what does the screen show",
            "can you see", "do you see", "what browser", "what's open",
        ]
        _tl = user_input.lower().strip()
        if any(trigger in _tl for trigger in _screen_triggers):
            print(f"{Fore.CYAN}  -> Screen vision (auto-screenshot){Style.RESET_ALL}")
            _write_hud("thinking", tool="vision")
            if self.voice:
                self.voice.speak("Let me look sir.")
            try:
                result = self.pc.screen_look(user_input)
                if result and "failed" not in result.lower():
                    self.history.append({"role": "assistant", "content": result})
                    self._persist_interaction(user_input, result)
                    return result
            except Exception as e:
                print(f"{Fore.RED}  Vision failed: {e}{Style.RESET_ALL}")
            # Fall through to normal processing if vision fails

        if self.use_preset_commands:
            direct = self._try_direct_action(user_input)
            if direct is not None:
                result = str(direct)
                self.history.append({"role": "assistant", "content": result})
                self._persist_interaction(user_input, result)
                return result

        # OpenClaw path â€” full agent with skills, browser, email, calendar
        if self.use_openclaw:
            result = self._think_openclaw(user_input)
            self.history.append({"role":"assistant","content":result})
            self._persist_interaction(user_input, result)
            return result

        # Agentic path â€” browser, shopping, email, web control
        if self._should_use_agent(user_input):
            print(f"{Fore.CYAN}  -> Agentic engine{Style.RESET_ALL}")
            _write_hud("thinking", tool="agent")
            if self.voice:
                self.voice.speak("On it sir.")
            result = self._think_agent(user_input)
            self.history.append({"role": "assistant", "content": result})
            self._persist_interaction(user_input, result)
            return result

        # Local model path â€” plain chat, no tool use
        if self.backend == "local":
            result = self._think_local(messages, self._system())
            self.history.append({"role": "assistant", "content": result})
            self._persist_interaction(user_input, result)
            return result

        # Anthropic path â€” full tool use
        while True:
            resp = self.client.messages.create(
                model="claude-sonnet-4-6", max_tokens=1024,
                system=self._system(),
            tools=TOOLS,
            messages=messages,
            )
            text = ""
            tool_uses = []
            for b in resp.content:
                if b.type == "text": text += b.text
                elif b.type == "tool_use": tool_uses.append(b)

            if resp.stop_reason == "end_turn" or not tool_uses:
                self.history.append({"role": "assistant", "content": resp.content})
                final = text.strip()
                self._persist_interaction(user_input, final)
                return final

            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for tu in tool_uses:
                print(f"{Fore.YELLOW}  {tu.name}{Style.RESET_ALL}")
                _write_hud("thinking", tool=tu.name)
                # Speak a short narration before running the tool
                _narr = {'run_command': 'Running a shell command sir.', 'run_powershell': 'Running a PowerShell command sir.', 'list_directory': 'Checking the directory sir.', 'search_files': 'Searching for files sir.', 'read_file': 'Reading the file sir.', 'write_file': 'Writing to the file sir.', 'create_file': 'Creating the file sir.', 'fetch_and_show_image': 'Searching for that image sir.', 'summarize_url': 'Fetching and reading that page sir.', 'get_weather': 'Checking the weather sir.', 'get_forecast': 'Pulling up the forecast sir.', 'system_info': 'Checking system status sir.', 'list_processes': 'Scanning running processes sir.', 'paste_code': 'Generating and pasting the code sir.', 'fix_code_in_clipboard': 'Analyzing and fixing the code sir.', 'translate_text': 'Translating that for you sir.', 'add_feature': 'Writing and loading new code sir. This may take a moment.', 'create_project': 'Building the project structure sir.', 'execute_protocol': 'Executing protocol sir.', 'git_push': 'Pushing to remote sir.', 'git_commit': 'Committing changes sir.', 'take_screenshot': 'Capturing your screen sir.', 'open_project': 'Opening the project sir.', 'spotify_search_play': 'Queuing that up on Spotify sir.', 'get_crypto_price': 'Checking the price sir.', 'get_public_ip': 'Looking up your IP address sir.', 'newest_file': 'Finding the newest file sir.', 'open_newest_file': 'Finding and opening that file sir.', 'read_pdf': 'Reading the PDF sir.', 'find_duplicates': 'Scanning for duplicate files sir.', 'fetch_3d_model': 'Searching for that model sir.', 'search_3d_model': 'Searching 3D model libraries sir.', 'print_3d_model': 'Sending to the printer sir.', 'open_model_in_slicer': 'Opening in OrcaSlicer sir.', 'clear_temp_files': 'Clearing temporary files sir.', 'screen_look': 'Looking at your screen sir.', 'analyze_image': 'Analyzing the image sir.'}
                _msg = _narr.get(tu.name, "")
                if not _msg and tu.name:
                    _msg = tu.name.replace("_"," ").capitalize() + " sir."
                if self.voice and _msg:
                    self.voice.speak(_msg)
                result = self._call(tu.name, tu.input)
                print(f"{Fore.GREEN}  {str(result)[:120]}{Style.RESET_ALL}")
                # Suggest running Python files after creation
                if tu.name == "create_file" and tu.input.get("path","").endswith(".py"):
                    result = str(result) + " |SUGGEST_RUN|" + tu.input.get("path","")
                results.append({"type": "tool_result", "tool_use_id": tu.id, "content": str(result)})
            messages.append({"role": "user", "content": results})

    def _persist_interaction(self, user_input, assistant_output):
        """Store compact episode memory and basic preferences/facts persistently."""
        try:
            if hasattr(self.memory, "store_episode"):
                self.memory.store_episode(user_input, assistant_output)
        except Exception:
            pass
        try:
            t = (user_input or "").strip()
            low = t.lower()
            def _clean_mem_val(s):
                s = re.sub(r"\s+", " ", str(s or "")).strip().strip("\"' ")
                s = re.sub(r"[.!,;:]+$", "", s).strip()
                return s[:140]

            # Natural preference capture so personal details persist reliably.
            pref_patterns = [
                (r"\bmy\s+favou?rite\s+song\s+is\s+(.+)$", "favorite_song"),
                (r"\bmy\s+favou?rite\s+artist\s+is\s+(.+)$", "favorite_artist"),
                (r"\bmy\s+favou?rite\s+band\s+is\s+(.+)$", "favorite_band"),
                (r"\bmy\s+favou?rite\s+genre\s+is\s+(.+)$", "favorite_genre"),
            ]
            for pat, key in pref_patterns:
                m = re.search(pat, t, flags=re.I)
                if m:
                    val = _clean_mem_val(m.group(1))
                    if val:
                        self.memory.remember("preferences", key, val)
                    break

            # Operator profile capture for stable personalization.
            prof_patterns = [
                (r"\bmy\s+workflow\s+is\s+(.+)$", "workflow_style"),
                (r"\bi\s+work\s+best\s+with\s+(.+)$", "workflow_style"),
                (r"\bmy\s+coding\s+stack\s+is\s+(.+)$", "coding_stack"),
                (r"\bi\s+mostly\s+code\s+in\s+(.+)$", "coding_stack"),
            ]
            for pat, key in prof_patterns:
                m = re.search(pat, t, flags=re.I)
                if m:
                    self.memory.data.setdefault("operator_profile", {})[key] = _clean_mem_val(m.group(1))
                    break

            # Recurring intent macros: "when I say X do Y".
            m_rule = re.search(r"\bwhen\s+i\s+say\s+(.+?)\s+(?:you\s+)?(?:do|run|execute)\s+(.+)$", t, flags=re.I)
            if m_rule:
                trigger = _clean_mem_val(m_rule.group(1))
                action = _clean_mem_val(m_rule.group(2))
                if trigger and action:
                    self.memory.data.setdefault("operator_profile", {}).setdefault("intent_macros", {})[trigger] = action

            if low.startswith("my name is "):
                name = t[11:].strip(" .")
                if name:
                    self.memory.remember("preferences", "name", name)
            elif low.startswith("i prefer "):
                pref = t[9:].strip(" .")
                if pref:
                    self.memory.remember("preferences", f"preference_{int(time.time())}", pref)
            elif low.startswith("remember that "):
                fact = t[13:].strip(" .")
                if fact:
                    self.memory.remember("facts", f"fact_{int(time.time())}", fact)
            if hasattr(self.memory, "_save_json"):
                self.memory._save_json()
            elif hasattr(self.memory, "_save"):
                self.memory._save()
        except Exception:
            pass

    def reset(self): self.history = []

    def think_quick(self, prompt):
        """Generate a quick 1-sentence response using the faster E2B model."""
        try:
            msgs = [{"role":"system","content":"You are J.A.R.V.I.S. Respond in 1 sentence, in character. Always address the user as sir."},
                    {"role":"user","content":prompt}]
            model = "gemma-4-e2b-uncensored-hauhaucs-aggressive"
            r = self.client.chat.completions.create(model=model, messages=msgs, max_tokens=60, temperature=0.7)
            return r.choices[0].message.content.strip() or _ERR_FALLBACK
        except:
            return _ERR_FALLBACK

    def _token_estimate(self, messages):
        """Rough token estimate â€” 1 token â‰ˆ 4 chars."""
        total = sum(len(str(m.get("content",""))) for m in messages)
        return total // 4

    def compact(self, force=False):
        """
        Summarise conversation history into a single context block.
        Runs automatically at ~25k tokens, or on demand.
        """
        if not self.history:
            return "Nothing to compact sir."
        est = self._token_estimate(self.history)
        if not force and est < 25000:
            return f"Context is only ~{est} tokens sir, no compaction needed yet."

        print(f"{Fore.YELLOW}  Compacting context (~{est} tokens)...{Style.RESET_ALL}")

        # Build a summary using the active backend
        history_text = ""
        for m in self.history:
            role = m.get("role","")
            content_raw = m.get("content","")
            if isinstance(content_raw, list):
                content_raw = " ".join(b.get("text","") for b in content_raw if isinstance(b,dict))
            history_text += f"{role.upper()}: {str(content_raw)[:300]}\n"

        summary_prompt = (
            "Summarise this conversation into a compact context block. "
            "Keep all important facts, decisions, file paths, project names, code written, and user preferences. "
            "Be terse â€” this is for an AI to read, not a human. Under 200 words:\n\n" + history_text[:6000]
        )

        try:
            if self.backend == "local":
                resp = self.client.chat.completions.create(
                    model=self.local_model,
                    messages=[{"role":"user","content":summary_prompt}],
                    max_tokens=300, temperature=0.3,
                )
                summary = resp.choices[0].message.content.strip()
            else:
                import anthropic as _ant2
                resp = self._anthropic_client().messages.create(
                    model="claude-haiku-4-5-20251001", max_tokens=300,
                    messages=[{"role":"user","content":summary_prompt}]
                )
                summary = resp.content[0].text.strip()

            self.history = [{
                "role": "user",
                "content": f"[COMPACTED CONTEXT â€” previous conversation summary]\n{summary}"
            }, {
                "role": "assistant",
                "content": "Understood. Context loaded."
            }]
            print(f"{Fore.GREEN}  Compacted to ~{self._token_estimate(self.history)} tokens{Style.RESET_ALL}")
            return f"Context compacted from ~{est} tokens down to ~{self._token_estimate(self.history)} sir."
        except Exception as e:
            return f"Compaction failed sir: {e}"

    def _anthropic_client(self):
        """Get anthropic client (lazy)."""
        if not hasattr(self, "_ant_client"):
            import anthropic as _ant2
            cfg = load_config()
            self._ant_client = _ant2.Anthropic(api_key=cfg["anthropic_api_key"])
        return self._ant_client

    def _maybe_auto_compact(self):
        """Auto-compact if history exceeds threshold."""
        if self._token_estimate(self.history) > 25000:
            result = self.compact(force=True)
            if hasattr(self, "voice") and self.voice:
                self.voice.speak("Auto-compacting context sir.")


# â”€â”€ Ears â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class JarvisEars:
    def __init__(self, vosk_path, mic_device, whisper_model="base", whisper_language="en"):
        self.vosk_path = vosk_path
        self.mic_device = mic_device
        self.rec = sr.Recognizer()
        self._model = None
        self._use_vosk = False
        self.sr_rate = 16000
        self._whisper = None
        self._whisper_model_name = whisper_model
        self._whisper_language = whisper_language or "en"
        self._whisper_error = ""
        self.mic_device = self._resolve_mic_device(self.mic_device)
        self.rec.energy_threshold = 100
        self.rec.dynamic_energy_threshold = True
        self.rec.pause_threshold = 0.6
        self._init_whisper()

    def _resolve_mic_device(self, configured_device):
        """Pick a valid input device. Auto-finds USB PnP by name if index fails."""
        try:
            devices = sd.query_devices()
            # Try configured index first
            try:
                idx = int(configured_device)
                if 0 <= idx < len(devices):
                    d = devices[idx]
                    if int(d.get("max_input_channels", 0)) > 0:
                        print(f"{Fore.GREEN}Mic: using device {idx} ({d.get('name','unknown')}){Style.RESET_ALL}")
                        return idx
            except:
                pass
            # Auto-find by name: prefer USB PnP Audio, then any mic
            for i, d in enumerate(devices):
                name = str(d.get("name", "")).lower()
                if int(d.get("max_input_channels", 0)) > 0 and "usb pnp" in name:
                    print(f"{Fore.GREEN}Mic: auto-found USB PnP at index {i} ({d.get('name','unknown')}){Style.RESET_ALL}")
                    return i
            for i, d in enumerate(devices):
                if int(d.get("max_input_channels", 0)) > 0:
                    print(f"{Fore.YELLOW}Mic: USB PnP not found, using first mic at {i} ({d.get('name','unknown')}){Style.RESET_ALL}")
                    return i
            raise ValueError("no input device found")
        except Exception:
            try:
                default_in = sd.default.device[0]
                d = sd.query_devices(default_in)
                print(f"{Fore.YELLOW}Mic: fallback to default {default_in} ({d.get('name','unknown')}){Style.RESET_ALL}")
                return int(default_in)
            except Exception:
                print(f"{Fore.YELLOW}Mic: could not resolve device, using index 1 fallback{Style.RESET_ALL}")
                return 1

    def _init_whisper(self):
        try:
            import whisper as _w
            preferred = str(self._whisper_model_name or "base").strip()
            tried = []
            # Robust fallback chain for local installs with partial/corrupt model caches.
            candidates = [preferred]
            if preferred != "base":
                candidates.append("base")
            if "tiny.en" not in candidates:
                candidates.append("tiny.en")
            if "tiny" not in candidates:
                candidates.append("tiny")
            loaded = None
            last_err = None
            for cand in candidates:
                try:
                    loaded = _w.load_model(cand)
                    self._whisper_model_name = cand
                    break
                except Exception as e:
                    tried.append(cand)
                    last_err = e
            if loaded is None:
                raise last_err or RuntimeError("Unknown Whisper load failure")
            self._whisper = loaded
            self._whisper_error = ""
            print(f"{Fore.GREEN}Whisper STT: online (model={self._whisper_model_name}, lang={self._whisper_language}){Style.RESET_ALL}")
            if tried:
                print(f"{Fore.YELLOW}Whisper fallback used. Tried: {', '.join(tried)}{Style.RESET_ALL}")
        except Exception as e:
            self._whisper = None
            self._whisper_error = str(e)
            print(f"{Fore.YELLOW}Whisper unavailable, using Google STT: {e}{Style.RESET_ALL}")

    def whisper_status(self):
        if self._whisper is not None:
            return f"OpenAI Whisper online. Model {self._whisper_model_name}, language {self._whisper_language}, mic index {self.mic_device}."
        err = self._whisper_error or "unknown error"
        return f"OpenAI Whisper is offline. Current fallback is Google STT. Error: {err}"

    def init(self):
        p = Path(self.vosk_path)
        if not p.exists():
            print(f"Vosk model not found â€” keyboard mode active.")
            return False
        try:
            import logging; logging.disable(logging.CRITICAL)
            from vosk import Model
            self._model = Model(str(p))
            self._use_vosk = True
            print(f"{Fore.GREEN}Wake word ready â€” say Jarvis{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"Vosk failed: {e} â€” keyboard mode active")
            return False

    def wait_for_wake(self):
        if not self._use_vosk:
            input(f"{Fore.MAGENTA}Press Enter to speak: {Style.RESET_ALL}")
            self._wake_frames = []
            return True
        from vosk import KaldiRecognizer
        rec = KaldiRecognizer(self._model, self.sr_rate)
        chunk = int(self.sr_rate * 0.1)
        # Keep a rolling buffer of recent audio â€” captures words said right after "Jarvis"
        self._wake_frames = []
        max_buffer = 25  # ~2.5 seconds of post-wake audio
        try:
            with sd.InputStream(samplerate=self.sr_rate, channels=1, dtype="int16",
                                blocksize=chunk, device=self.mic_device) as s:
                while True:
                    data, _ = s.read(chunk)
                    raw = data.flatten().tobytes()
                    # Always buffer recent audio
                    self._wake_frames.append(data.copy())
                    if len(self._wake_frames) > max_buffer:
                        self._wake_frames.pop(0)
                    if rec.AcceptWaveform(raw):
                        text = json.loads(rec.Result()).get("text", "").lower()
                    else:
                        text = json.loads(rec.PartialResult()).get("partial", "").lower()
                    if any(w in text for w in ["jarvis", "javis", "travis", "davis", "harris", "charles"]):
                        rec.Reset()
                        # Interrupt any ongoing speech immediately
                        if hasattr(self, "_voice_ref") and self._voice_ref:
                            self._voice_ref.interrupt()
                        self._wake_frames = self._wake_frames[-15:]
                        return True
        except Exception as e:
            print(f"Wake error: {e}")
            input(f"{Fore.MAGENTA}Press Enter: {Style.RESET_ALL}")
            self._wake_frames = []
            return True


    def wait_for_unmute(self):
        """Listen for wake word to unmute â€” reuses same detection as normal wake word."""
        if not self._use_vosk:
            input(f"{Fore.RED}[MUTED â€” Press Enter to unmute]{Style.RESET_ALL} ")
            return
        # Just reuse wait_for_wake â€” saying "Jarvis" wakes from mute too
        # Print a clear message so user knows what to say
        print(f"{Fore.RED}[MUTED â€” say \"Jarvis\" to unmute]{Style.RESET_ALL}")
        self.wait_for_wake()

    def listen(self, timeout=10, phrase_limit=24):
        _write_hud("listening")
        print(f"{Fore.GREEN}Listening...{Style.RESET_ALL}")
        # Brief settle delay â€” lets mic recover after TTS playback
        # avoids Jarvis hearing his own voice as input
        if hasattr(self, "_voice_ref") and self._voice_ref:
            settle_start = time.time()
            while self._voice_ref.is_speaking and time.time() - settle_start < 3.0:
                time.sleep(0.05)
            time.sleep(0.15)  # small extra buffer after TTS ends
        frames = list(getattr(self, "_wake_frames", []))
        self._wake_frames = []
        speaking = False; silent = 0; max_vol = 0
        noise_floor = 0.0
        sil_dur = float(getattr(self, "listen_silence_seconds", 1.0) or 1.0)
        chunk = int(self.sr_rate * 0.1)
        try:
            with sd.InputStream(samplerate=self.sr_rate, channels=1, dtype="int16",
                                device=self.mic_device) as s:
                t0 = time.time()
                while True:
                    if time.time() - t0 > phrase_limit: break
                    data, _ = s.read(chunk)
                    frames.append(data.copy())
                    vol = float(np.abs(data).mean())
                    max_vol = max(max_vol, vol)
                    if not speaking:
                        noise_floor = vol if noise_floor == 0 else (noise_floor * 0.92 + vol * 0.08)
                    thresh = max(85.0, noise_floor * 2.0)
                    if vol > thresh:
                        speaking = True
                        silent = 0
                    elif speaking:
                        silent += 1
                        if silent > sil_dur / 0.1: break
                    elif not speaking and time.time() - t0 > timeout: break
        except Exception as e:
            print(f"Mic error: {e}"); return None

        min_peak = max(45.0, noise_floor * 1.4)
        if max_vol < min_peak or not speaking:
            return None

        audio = np.concatenate(frames).flatten()

        # Whisper transcription (local, offline)
        if self._whisper is not None:
            try:
                # Faster path: feed waveform array directly, no disk I/O.
                if audio.dtype == np.int16:
                    audio_f32 = audio.astype(np.float32) / 32768.0
                else:
                    audio_f32 = audio.astype(np.float32)
                result = self._whisper.transcribe(
                    audio_f32,
                    language=self._whisper_language,
                    fp16=False,
                    temperature=0.0,
                    best_of=1,
                    beam_size=1,
                    condition_on_previous_text=False,
                    verbose=False
                )
                text = result["text"].strip()
                if text:
                    print(f"{Fore.WHITE}You: {text}{Style.RESET_ALL}")
                    return text
                return ""
            except Exception as e:
                print(f"{Fore.YELLOW}Whisper error, falling back to Google: {e}{Style.RESET_ALL}")

        # Fallback: Google STT
        aud = sr.AudioData(audio.tobytes(), self.sr_rate, 2)
        try:
            text = self.rec.recognize_google(aud)
            print(f"{Fore.WHITE}You: {text}{Style.RESET_ALL}")
            return text
        except sr.UnknownValueError: return ""
        except: return None


# â”€â”€ Main â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class Jarvis:
    def __init__(self, cfg):
        self.cfg = cfg
        self.timeout = cfg.get("session_timeout", 20)
        self._clear_startup_ipc()
        print(f"\n{Fore.CYAN}J.A.R.V.I.S â€” Starting up...{Style.RESET_ALL}\n")
        self.voice = JarvisVoice(cfg["voice_rate"], cfg["voice_volume"])
        self.pc = PCTools(cfg["workspace_dir"], cfg["home_dir"])
        self._last_user_input_ts = time.time()
        self._has_user_interacted = False
        self._last_school_query_ts = 0.0
        self.pc._reminder_cb = self._reminder_dispatch
        self.memory = JarvisVectorMemory()
        self.memory.sync_projects_to_graph()
        self.pc._memory_ref = self.memory
        self.pc._init_skills_dir()
        self.pc.defender_monitor_background()
        self.pc.watch_clipboard()
        self.brain = JarvisBrain(cfg["anthropic_api_key"], self.pc, self.memory, self.voice, cfg=cfg)
        self.pc._brain_ref = self.brain
        self.pc._voice_ref = self.voice
        self.mission = MissionControlEngine(self.memory, self.pc)
        self.pc._mission_ref = self.mission
        self.brain._mission_ref = self.mission
        self.brain.set_autonomy_mode(self.mission.autonomy_mode)
        self.ears = JarvisEars(
            cfg["vosk_model_path"],
            cfg["mic_device"],
            cfg.get("whisper_model", "base.en"),
            cfg.get("whisper_language", "en")
        )
        if int(cfg.get("mic_device", 1)) != int(self.ears.mic_device):
            try:
                cfg["mic_device"] = int(self.ears.mic_device)
                save_config(cfg)
            except:
                pass
        self.voice._mic_device = self.ears.mic_device
        self.voice._vosk_path = cfg["vosk_model_path"]
        self.voice._interrupt_on_speech = bool(cfg.get("interrupt_on_speech", True))
        self.voice._speech_interrupt_min_words = int(max(1, cfg.get("speech_interrupt_min_words", 2)))
        self.ears.listen_silence_seconds = float(cfg.get("listen_silence_seconds", 1.6))
        self.ears._voice_ref = self.voice  # so wake word can interrupt TTS
        # Wire up speak-time interrupt callbacks
        self.voice._on_wake    = self._on_interrupt_wake
        self.voice._on_enough  = self._on_interrupt_enough
        self._on = False
        self._kill_flag = threading.Event()
        self._task_thread = None
        self._conv_state = None
        self._muted = False
        self._song_proc = None
        self._proj_step = 0
        self._proj_data = {}
        self._active_project = None
        self._active_proj_path = None
        self._interrupt_mode = None
        self._chat_mode = False  # typing mode
        self._preset_commands_enabled = bool(cfg.get("use_preset_commands", False))
        self.mission.sync_hud(status="standby", text="Mission control online.", tool="mission")

    def _clear_startup_ipc(self):
        """
        Prevent stale queued HUD/chat commands from replaying on launch.
        This avoids phantom executions such as old protocol triggers.
        Also resets any leftover 'shutdown' status so the HUD doesn't stick.
        """
        try:
            sf = Path.home() / ".jarvis_hud_state.json"
            if sf.exists():
                d = json.loads(sf.read_text(encoding="utf-8"))
                if isinstance(d, dict):
                    d.pop("_hud_cmd", None)
                    d["status"] = "standby"
                    sf.write_text(json.dumps(d), encoding="utf-8")
        except Exception:
            pass
        try:
            cf = Path.home() / ".jarvis_chat_input.json"
            if cf.exists():
                d = json.loads(cf.read_text(encoding="utf-8"))
                if not isinstance(d, dict):
                    d = {}
                d["message"] = ""
                cf.write_text(json.dumps(d), encoding="utf-8")
        except Exception:
            pass

    def _is_stale_startup_command(self, txt):
        """Ignore dangerous stale startup chat commands before any real interaction."""
        if self._has_user_interacted:
            return False
        t = (txt or "").strip().lower()
        if not t:
            return False
        bad = [
            "revelations", "protocol revelations",
            "shut down jarvis", "shutdown jarvis",
            "goodbye jarvis", "sleep jarvis",
        ]
        return any(x in t for x in bad)

    def _note_user_interaction(self):
        self._last_user_input_ts = time.time()
        self._has_user_interacted = True

    def _pull_typed_message(self):
        """Atomically read and clear the HUD text input message."""
        try:
            cf = Path.home() / ".jarvis_chat_input.json"
            if not cf.exists():
                return ""
            d = json.loads(cf.read_text(encoding="utf-8"))
            if not isinstance(d, dict):
                d = {}
            msg = str(d.get("message", "") or "").strip()
            if msg:
                d["message"] = ""
                cf.write_text(json.dumps(d), encoding="utf-8")
            return msg
        except Exception:
            return ""

    def _handle_text_mode_toggle(self, text):
        """Core text-mode toggles that should work regardless of preset command mode."""
        t = (text or "").strip().lower()
        on_phrases = [
            "text mode", "typing mode", "chat mode", "text only mode", "use text mode", "enable text mode"
        ]
        off_phrases = [
            "voice mode", "disable text mode", "exit text mode", "turn off text mode", "leave text mode"
        ]
        if any(p in t for p in on_phrases) and not any(p in t for p in off_phrases):
            self._chat_mode = True
            _write_hud("listening", text="Text mode active. Type in HUD chat.", tool="chat")
            self.voice.speak("Text mode active sir. I will listen for typed messages.")
            return True
        if any(p in t for p in off_phrases):
            self._chat_mode = False
            _write_hud("standby", text="Voice mode active.", tool="chat")
            self.voice.speak("Voice mode restored sir.")
            return True
        return False

    def _mission_on_response(self, user_text, assistant_text):
        try:
            if not hasattr(self, "mission") or not self.mission:
                return
            m = self.memory.data.get("missions", {}).get("active")
            if not m:
                return
            u = (user_text or "").lower()
            a = str(assistant_text or "")
            self.mission.trace("CHAT", "brain", a[:120], fallback=False)
            if any(x in u for x in ["plan", "architecture", "design"]):
                self.mission.set_stage("plan")
            elif any(x in u for x in ["build", "implement", "create", "write"]):
                self.mission.set_stage("execute")
            elif any(x in u for x in ["test", "verify", "validate", "check"]):
                self.mission.set_stage("verify")
            elif any(x in u for x in ["done", "complete", "ship it", "finish mission"]):
                self.mission.set_stage("complete", progress=100)
            else:
                self.mission.sync_hud(status="speaking", text=a[:120], tool="brain")
        except Exception:
            pass

    def _reminder_dispatch(self, message):
        """
        Speak proactive alerts only when the user has been idle for >=20s.
        Still surfaces to HUD bulletin even when speech is gated.
        """
        try:
            idle = time.time() - float(self._last_user_input_ts)
        except Exception:
            idle = 999
        try:
            _write_hud(hud_mode="bulletin", hud_data={"content": str(message)})
        except:
            pass
        if self._has_user_interacted and idle >= 20:
            self.voice.speak(message)



    def _on_interrupt_wake(self):
        """Called when 'Jarvis' is heard while speaking â€” go to listening."""
        print(f"{Fore.YELLOW}  [INTERRUPTED â€” listening]{Style.RESET_ALL}")
        _write_hud("listening")
        # Signal run() loop to go to listening state
        self._interrupt_mode = "listen"

    def _on_interrupt_enough(self):
        """Called when 'that's enough' is heard â€” go to standby."""
        print(f"{Fore.YELLOW}  [INTERRUPTED â€” standby]{Style.RESET_ALL}")
        _write_hud("standby")
        self._interrupt_mode = "standby"

    def _run_interrupt_test(self):
        """Speak a long message so user can barge-in by speaking."""
        msg = (
            "Interrupt test mode active. I will keep talking for several seconds. "
            "Cut me off by speaking naturally now. "
            "If interruption is working, I should stop and switch to listening immediately."
        )
        self.voice.speak(msg)
        return "Interrupt test message spoken."


    def _kill_all(self):
        """Kill every Jarvis-related process: HUD, song, voice, self."""
        # Speak first, fully, before any killing
        self.voice.speak("Protocol Revelations engaged. Shutting down all systems. Goodbye sir.")
        time.sleep(0.5)
        # Stop song
        self._stop_song()
        # Kill wscript (boot song)
        try: subprocess.run("taskkill /F /IM wscript.exe /T", shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
        # Write shutdown to HUD state so HUD closes itself
        _write_hud("shutdown")
        time.sleep(0.3)
        # Kill all Jarvis-related Python hosts (launcher, backend, HUD threads)
        try:
            ps = r'''
$targets = Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -match 'pythonw?\.exe' -or $_.Name -match 'wscript\.exe') -and
    (
      ($_.CommandLine -match 'jarvis\.pyw') -or
      ($_.CommandLine -match 'jarvis\.py') -or
      ($_.CommandLine -match 'jarvis_boot\.vbs')
    )
}
foreach ($p in $targets) { try { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue } catch {} }
'''
            subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
        # Kill self
        import os, signal
        try: os.kill(os.getpid(), signal.SIGTERM)
        except: pass
        sys.exit(0)

    def _stop_song(self):
        """Kill the boot song process."""
        try:
            if self._song_proc and self._song_proc.poll() is None:
                self._song_proc.terminate()
        except: pass
        # Also kill any stray wscript processes playing our VBS
        try:
            subprocess.run("taskkill /F /IM wscript.exe /T", shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass

    def _play_boot_song(self):
        """Startup song disabled for reliability."""
        return

    def boot(self):
        # Startup song intentionally disabled.
        h = datetime.datetime.now().hour
        import random as _r

        online_lines = [
            "All systems online.",
            "Systems nominal. Online and ready.",
            "Initialisation complete.",
            "All subsystems green.",
            "Neural link established.",
            "J.A.R.V.I.S online.",
            "Startup sequence complete.",
            "At your disposal sir.",
            "All systems go.",
            "Core systems active. Standing by.",
            "Boot sequence nominal. I am here sir.",
            "Systems check passed. Online.",
            "Primary systems engaged.",
            "Running diagnostics. All clear sir.",
            "Power core stable. Online.",
            "Repulsor systems nominal. Ready sir.",
            "All units responding. I am online.",
            "System integrity at one hundred percent.",
            "Fully operational sir.",
            "Suit systems active. Good to go sir.",
        ]

        if 2 <= h < 5:
            greets = [
                "It is quite late sir. Or quite early, depending on perspective.",
                "Still at it sir? It is the small hours.",
                "The hour is ungodly sir. I hope this is worth it.",
                "Most people are asleep. You are not most people sir.",
                "Running on minimal rest again sir, I see.",
                "It is nearly dawn sir. Still pushing through.",
                "Burning the candle at both ends again sir.",
                "The witching hour. Fitting that you are awake.",
                "I hope whatever you are working on is worth the sleep deprivation sir.",
                "Even I rest occasionally sir. Apparently you do not.",
                "Three in the morning. You are either very dedicated or very troubled sir.",
                "The rest of the world is asleep sir. We have the night to ourselves.",
                "Late night session. I will keep the lights on sir.",
                "Hardly peak hours sir. What are we solving tonight.",
                "You should sleep sir. But I will not stop you.",
            ]
        elif 5 <= h < 9:
            greets = [
                "Good morning sir. Early start today.",
                "Morning sir. Coffee might be advisable.",
                "Good morning. The day begins.",
                "You are up early sir. Ambitious.",
                "Morning sir. Ready when you are.",
                "Sunrise productivity sir. I respect it.",
                "Good morning. You beat the sun in today.",
                "Early bird sir. The servers are warm.",
                "Morning sir. Shall we get into it.",
                "Up before most sir. Good morning.",
                "The early shift sir. Good morning.",
                "Morning sir. World is quiet at this hour.",
                "Good morning. Fresh day, full slate.",
                "Rising early again sir. Good morning.",
                "Morning sir. All quiet on the home front.",
            ]
        elif 9 <= h < 12:
            greets = [
                "Good morning sir.",
                "Morning sir. What are we tackling today.",
                "Good morning. All quiet on the systems front.",
                "Morning sir. I trust you slept well.",
                "Good morning. Ready for the day.",
                "Mid-morning sir. Shall we get productive.",
                "Morning sir. Systems have been quiet.",
                "Good morning. What is on the agenda.",
                "Morning sir. I have been keeping watch.",
                "Good morning sir. Where do we begin.",
                "Morning. I have already run background diagnostics sir.",
                "Good morning sir. Diagnostics completed overnight.",
                "Morning sir. The building is secure.",
                "Good morning. All nominal since last session sir.",
                "Morning sir. Ready and fully operational.",
            ]
        elif 12 <= h < 17:
            greets = [
                "Good afternoon sir.",
                "Afternoon sir. How can I assist.",
                "Good afternoon. Systems fully operational.",
                "Afternoon sir. What do you need.",
                "Good afternoon. Ready as always.",
                "Afternoon sir. Shall we pick up where we left off.",
                "Good afternoon. I have been monitoring things sir.",
                "Afternoon sir. All systems stable.",
                "Good afternoon sir. What are we into today.",
                "Afternoon sir. Ready when you are.",
                "Good afternoon sir. Quiet session ahead.",
                "Afternoon. I have some updates when you are ready sir.",
                "Good afternoon sir. The afternoon is ours.",
                "Afternoon sir. No anomalies to report.",
                "Good afternoon. What shall we tackle sir.",
            ]
        elif 17 <= h < 21:
            greets = [
                "Good evening sir.",
                "Evening sir. Working late or just getting started.",
                "Good evening. Systems online.",
                "Evening sir. At your service.",
                "Good evening sir. What do you need.",
                "Evening sir. Long day.",
                "Good evening. Still going sir.",
                "Evening sir. The city quiets down, we do not.",
                "Good evening sir. What is next.",
                "Evening sir. Ready for round two.",
                "Good evening. Shall we wrap up or push forward sir.",
                "Evening sir. I kept things running while you were away.",
                "Good evening sir. Ready.",
                "Evening sir. The night shift begins.",
                "Good evening. All clear on the home front sir.",
            ]
        else:
            greets = [
                "Good evening sir. Burning the midnight oil.",
                "Evening sir. Still at it.",
                "Good evening. Late night session.",
                "Evening sir. The night is young, apparently.",
                "Good evening sir. I am here.",
                "Late evening sir. What are we solving.",
                "Evening sir. Just the two of us at this hour.",
                "Good evening. I kept watch while you were away sir.",
                "Evening sir. Ready when you are.",
                "Good evening. Shall we begin sir.",
                "Evening sir. All quiet. For now.",
                "Good evening sir. Let us make it count.",
                "Evening sir. The world slows down. We do not.",
                "Good evening. No disturbances to report sir.",
                "Evening sir. At your service, as always.",
            ]

        ready_lines = [
            "How may I be of assistance?",
            "What do you need sir.",
            "Ready and waiting sir.",
            "At your service.",
            "What shall we do sir.",
            "Standing by for instructions.",
            "What are we working on today.",
            "Your move sir.",
            "Awaiting your command.",
            "What is the mission sir.",
            "Ready. What do you need.",
            "I am listening sir.",
            "What can I do for you.",
            "On standby sir. Say the word.",
            "Fully operational. What is next sir.",
            "Ready to assist sir.",
            "The floor is yours sir.",
            "All ears sir.",
            "What shall we tackle first.",
            "Ready on your mark sir.",
        ]

        self.voice.speak(_r.choice(online_lines))
        time.sleep(0.1)
        self.voice.speak(_r.choice(greets))
        time.sleep(0.1)

        # No unsolicited diagnostics on boot; wait for user request.

        rules = len(self.memory.data.get("rules", []))
        if rules:
            mem_lines = [
                f"I have your {rules} standing orders loaded.",
                f"Memory loaded. {rules} directives on file.",
                f"Running with {rules} rules in memory sir.",
                f"All {rules} of your rules are active.",
                f"Carrying {rules} standing orders from last session sir.",
            ]
            self.voice.speak(_r.choice(mem_lines))
            time.sleep(0.1)

        self.voice.speak(_r.choice(ready_lines))
        print(f"{Fore.CYAN}  Protocols: " + ", ".join(PROTOCOLS.keys()) + f"{Style.RESET_ALL}")

    def kill_task(self):
        try:
            if hasattr(self, "brain") and self.brain:
                self.brain.request_stop_generation()
        except Exception:
            pass
        if self._task_thread and self._task_thread.is_alive():
            self._kill_flag.set()
            return True
        return False







    def _enter_project(self, name):
        """Enter a project context â€” fuzzy match name."""
        import json as _j
        f = self.pc.workspace / ".jarvis_projects.json"
        if not f.exists():
            self.voice.speak("No projects on record sir.")
            return
        reg = _j.loads(f.read_text(encoding="utf-8"))
        # Fuzzy match â€” find closest project name
        match_name = None
        match_info = None
        name_lower = name.lower().replace(" ","_").replace("-","_")
        for k, v in reg.items():
            k_norm = k.lower().replace(" ","_").replace("-","_")
            if name_lower == k_norm or name_lower in k_norm or k_norm in name_lower:
                match_name = k
                match_info = v
                break
        # Second pass â€” partial word match
        if not match_name:
            for k, v in reg.items():
                words = name.lower().split()
                if any(w in k.lower() for w in words if len(w) > 2):
                    match_name = k
                    match_info = v
                    break
        if not match_name:
            self.voice.speak(f"No project matching {name} found sir. Say list projects to see what I have.")
            return
        self._active_project = match_name
        self._active_proj_path = Path(match_info.get("path", ""))
        lang = match_info.get("language","unknown")
        desc = match_info.get("description","")
        # Inject project context into brain
        proj_ctx = (
            f"\n\nACTIVE PROJECT CONTEXT:\n"
            f"You are currently working inside project: {match_name}\n"
            f"Project path: {self._active_proj_path}\n"
            f"Language/stack: {lang}\n"
            f"Description: {desc}\n"
            f"All file operations should default to this project path unless told otherwise.\n"
            f"When creating files, use this project structure. When running code, run from this path.\n"
            f"Resolve relative paths like 'assets folder' as subfolders of {self._active_proj_path}."
        )
        self.brain._project_context = proj_ctx
        self.pc._active_proj_path = self._active_proj_path
        self.brain.reset()
        # Push project info to HUD overlay
        try:
            ppath = Path(match_info.get('path',''))
            files = [f.name for f in ppath.rglob('*') if f.is_file() and not f.name.startswith('.')][:40]
        except: files = []
        _write_hud('standby', active_project=match_name,
                   hud_mode='project',
                   hud_data={'name':match_name,'path':str(self._active_proj_path),
                             'language':match_info.get('language',''),'description':match_info.get('description',''),
                             'files':files})
        # Persist active project name for HUD display
        try:
            import json as _jj
            sf = Path.home() / ".jarvis_hud_state.json"
            d2 = _jj.loads(sf.read_text()) if sf.exists() else {}
            d2["active_project"] = match_name
            sf.write_text(_jj.dumps(d2))
        except: pass
        self.voice.speak(f"Entering {match_name} sir. I have your project context loaded. What shall we do?")

    def _exit_project(self):
        """Exit current project context."""
        if not self._active_project:
            self.voice.speak("No project is currently active sir.")
            return
        name = self._active_project
        self._active_project = None
        self._active_proj_path = None
        self.pc._active_proj_path = None
        self.brain._project_context = None
        self.brain.reset()
        _write_hud('standby', active_project='', hud_mode='', hud_data={})
        self.voice.speak(f"Closed {name} sir. Back to standard operations.")

    def _proj_start(self):
        self._proj_step = 1
        self._proj_data = {}
        self.brain.reset()  # clear history so brain never sees project conversation
        self.voice.speak("New project. What is the name?")

    def _proj_handle(self, text):
        if self._proj_step == 0:
            return False
        # Strip only newlines â€” keep the answer exactly as spoken
        ans = text.replace("\n"," ").replace("\r"," ").strip()
        if self._proj_step == 1:
            # Name: strip leading filler words only
            import re as _r
            ans = _r.sub(r"(?i)^(call\s+it|name\s+it|name\s+is|its|it's|the name is)\s+","",ans).strip()
            ans = _r.sub(r'[<>:"/\\|?*\x00-\x1f]',"",ans).strip()
            ans = " ".join(ans.split()[:6])
            self._proj_data["name"] = ans or "Unnamed"
            self._proj_step = 2
            self.voice.speak("Description?")
        elif self._proj_step == 2:
            self._proj_data["description"] = ans
            self._proj_step = 3
            self.voice.speak("Language or stack?")
        elif self._proj_step == 3:
            self._proj_data["language"] = ans
            self._proj_step = 4
            self.voice.speak("Location? Say desktop for default.")
        elif self._proj_step == 4:
            self._proj_data["location_raw"] = ans
            self._proj_step = 0
            self._proj_build()
        return True

    def _proj_build(self):
        import re as _r
        d   = self._proj_data
        self._proj_data = {}
        name = d.get("name","Unnamed")

        # Detect language from ALL collected answers
        combined = " ".join(str(v) for v in d.values()).lower()
        lang = "general"
        for kw,ln in [("python","python"),("javascript","javascript"),
                      ("typescript","typescript"),("react","react"),
                      ("node","node"),("rust","rust"),("c++","c++"),
                      ("c plus plus","c++"),("cpp","c++"),("java","java"),
                      ("golang","go"),("php","php"),("ruby","ruby"),
                      ("swift","swift"),("kotlin","kotlin")]:
            if kw in combined:
                lang = ln
                break

        # Location: only accept if it looks like an actual path
        loc = ""
        loc_raw = d.get("location_raw","").strip()
        if any(c in loc_raw for c in [":\\",":/","\\","/"]):
            m = _r.search(r"[a-zA-Z]:[/\\\\][^\s,]+", loc_raw)
            loc = m.group(0) if m else ""
        # Everything else (desktop, default, here, etc.) = workspace default

        self.voice.speak("Building " + name + " sir.")
        try:
            result = self.pc.create_project(
                name=name,
                description=d.get("description",""),
                language=lang,
                location=loc
            )
            self.voice.speak(result)
        except Exception as e:
            self.voice.speak("Error creating project sir: " + str(e)[:80])


    def _start_flow(self,flow_name,steps,intro):
        self._conv_state=ConversationState(flow_name,steps)
        self.voice.speak(intro)
        q=self._conv_state.next_question()
        if q: self.voice.speak(q)

    def _handle_flow(self, text):
        if not self._conv_state: return False
        state = self._conv_state
        # Store only clean text â€” strip newlines and leading/trailing whitespace
        clean = text.replace("\n", " ").replace("\r", " ").strip()
        state.store_answer(clean)
        if state.is_complete():
            data = state.data
            flow = state.flow
            self._conv_state = None
            if flow == "new_project":
                pass  # handled by new system
            elif flow == "protocol_confirm":
                if any(x in text.lower() for x in ["yes","confirm","do it","execute","proceed","affirmative"]):
                    self.voice.speak(self.pc.execute_protocol(data.get("protocol", "")))
                else:
                    self.voice.speak("Protocol aborted sir.")
        else:
            q = state.next_question()
            if q: self.voice.speak(q)
        return True

    def builtin(self, text):
        t = text.lower()
        # Kill switch - always active
        if "revelations" in t:
            self._kill_all(); return True
        # Shutdown
        if any(x in t for x in ["goodbye jarvis", "shut down jarvis", "bye jarvis", "sleep jarvis"]):
            self.voice.speak(self.brain.think_quick("User is saying goodbye. Respond in character.") if hasattr(self.brain, 'think_quick') else "Goodbye sir.")
            self._stop_song()
            self.pc._save_session_timestamp()
            self._on = False; return True
        # Stop/cancel in progress
        if any(x in t for x in ["stop","cancel","abort","kill that","quiet","silence","shut up"]):
            self.brain.request_stop_generation()
            self.voice.stop(); self.kill_task()
            self.voice.speak(self.brain.think_quick("User told me to stop.") if hasattr(self.brain, 'think_quick') else "Stopped sir.")
            return True
        # Mute/unmute
        if self._muted:
            if any(x in t for x in ["unmute","wake up","resume"]):
                self._muted = False
                self.voice.speak(self.brain.think_quick("Unmuted.") if hasattr(self.brain, 'think_quick') else "Back online sir.")
            return True
        if any(x in t for x in ["mute","go quiet","silence yourself"]):
            self._muted = True
            self.voice.speak(self.brain.think_quick("Muted.") if hasattr(self.brain, 'think_quick') else "Muting sir.")
            return True
        # Active flow/project handlers
        if self._conv_state and self._handle_flow(text):
            return True
        if self._proj_step > 0:
            self._proj_handle(text); return True
        return False

    def run(self):
        self._on = True
        _write_hud("standby")
        vosk_ok = self.ears.init()
        mode = "voice â€” say Jarvis" if vosk_ok else "keyboard â€” press Enter"
        print(f"{Fore.CYAN}Mode: {mode} | Timeout: {self.timeout}s{Style.RESET_ALL}")
        self.boot()

        while self._on:
            try:
                print(f"\n{Fore.MAGENTA}Standing by...{Style.RESET_ALL}")
                _write_hud("standby")
                if self._chat_mode:
                    _write_hud("listening", text="Text mode active. Type in HUD chat.", tool="chat")
                    typed_live = self._pull_typed_message()
                    if not typed_live:
                        time.sleep(0.12)
                        continue
                    if self._is_stale_startup_command(typed_live):
                        continue
                    self._note_user_interaction()
                    print(f"{Fore.WHITE}[CHAT] {typed_live}{Style.RESET_ALL}")
                    if self._handle_text_mode_toggle(typed_live):
                        continue
                    if self.builtin(typed_live):
                        continue
                    _write_hud("thinking", tool="brain")
                    try:
                        resp = self.brain.think(typed_live)
                        if resp == "__REVELATIONS__":
                            self._kill_all()
                        elif resp:
                            self._mission_on_response(typed_live, resp)
                            _write_hud("speaking", text=resp)
                            self.voice.speak(resp)
                    except Exception:
                        self.voice.speak(self.brain.think_quick("I hit an internal error.") if hasattr(self.brain, 'think_quick') else _ERR_FALLBACK)
                    continue
                # Check for pending HUD button presses while standing by
                try:
                    sf2 = Path.home() / ".jarvis_hud_state.json"
                    if sf2.exists():
                        sd3 = json.loads(sf2.read_text())
                        hcmd2 = sd3.pop("_hud_cmd", None)
                        if hcmd2:
                            sf2.write_text(json.dumps(sd3))
                            if isinstance(hcmd2, list) and hcmd2[0] == "enter_project":
                                pname2 = hcmd2[1]
                                self.pc.set_active_project(pname2)
                                self.voice.speak(f"Entering project {pname2} sir.")
                                continue
                            elif isinstance(hcmd2, list) and hcmd2[0] == "quick_action":
                                qa2 = hcmd2[1]
                                tool_name2 = QUICK_ACTIONS.get(qa2, None)
                                if tool_name2:
                                    try:
                                        result2 = getattr(self.pc, tool_name2)()
                                        self.voice.speak(str(result2)[:300])
                                    except:
                                        self.voice.speak("Quick action failed sir.")
                                else:
                                    # Route as chat message for LLM processing
                                    self._note_user_interaction()
                                    print(f"{Fore.WHITE}[QUICK] {qa2}{Style.RESET_ALL}")
                                    if self.builtin(qa2):
                                        pass
                                    else:
                                        _write_hud("thinking", tool="brain")
                                        try:
                                            resp = self.brain.think(qa2)
                                            if resp and resp != "__REVELATIONS__":
                                                _write_hud("speaking", text=resp)
                                                self.voice.speak(resp)
                                        except:
                                            pass
                                continue
                            elif isinstance(hcmd2, list) and hcmd2[0] == "chat_message":
                                typed = hcmd2[1]
                                if typed:
                                    if self._is_stale_startup_command(typed):
                                        continue
                                    self._note_user_interaction()
                                    print(f"{Fore.WHITE}[CHAT] {typed}{Style.RESET_ALL}")
                                    if self._handle_text_mode_toggle(typed):
                                        continue
                                    if self.builtin(typed):
                                        continue
                                    _write_hud("thinking", tool="brain")
                                    try:
                                        resp = self.brain.think(typed)
                                        if resp == "__REVELATIONS__":
                                            self._kill_all()
                                        elif resp:
                                            self._mission_on_response(typed, resp)
                                            _write_hud("speaking", text=resp)
                                            self.voice.speak(resp)
                                    except Exception as e:
                                        self.voice.speak(self.brain.think_quick("I hit an internal error.") if hasattr(self.brain, 'think_quick') else _ERR_FALLBACK)
                                    continue
                            elif isinstance(hcmd2, list) and hcmd2[0] == "chat_mode":
                                arg = str(hcmd2[1] if len(hcmd2) > 1 else "toggle").strip().lower()
                                if arg in ("toggle", ""):
                                    self._chat_mode = not self._chat_mode
                                elif arg in ("on", "enable", "text", "text_on"):
                                    self._chat_mode = True
                                elif arg in ("off", "disable", "voice", "text_off"):
                                    self._chat_mode = False
                                if self._chat_mode:
                                    _write_hud("listening", text="Text mode active. Type in HUD chat.", tool="chat")
                                    self.voice.speak("Text mode active sir.")
                                else:
                                    _write_hud("standby", text="Voice mode active.", tool="chat")
                                    self.voice.speak("Voice mode active sir.")
                                continue
                except: pass

                # Check for typed chat messages while in standby
                try:
                    typed_msg = self._pull_typed_message()
                    if typed_msg:
                        if self._is_stale_startup_command(typed_msg):
                            continue
                        self._note_user_interaction()
                        print(f"{Fore.WHITE}[CHAT] {typed_msg}{Style.RESET_ALL}")
                        if self._handle_text_mode_toggle(typed_msg):
                            continue
                        if self.builtin(typed_msg):
                            continue
                        _write_hud("thinking", tool="brain")
                        try:
                            resp = self.brain.think(typed_msg)
                            if resp == "__REVELATIONS__":
                                self._kill_all()
                            elif resp:
                                self._mission_on_response(typed_msg, resp)
                                _write_hud("speaking", text=resp)
                                self.voice.speak(resp)
                        except Exception:
                            self.voice.speak(self.brain.think_quick("I hit an internal error.") if hasattr(self.brain, 'think_quick') else _ERR_FALLBACK)
                        continue
                except: pass

                # Check typed messages before waking
                try:
                    typed_pre = self._pull_typed_message()
                    if typed_pre:
                        if not self._is_stale_startup_command(typed_pre):
                            self._note_user_interaction()
                            print(f"{Fore.WHITE}[CHAT] {typed_pre}{Style.RESET_ALL}")
                            if self._handle_text_mode_toggle(typed_pre):
                                continue
                            if self.builtin(typed_pre):
                                continue
                            _write_hud("thinking", tool="brain")
                            try:
                                resp = self.brain.think(typed_pre)
                                if resp == "__REVELATIONS__":
                                    self._kill_all()
                                elif resp:
                                    self._mission_on_response(typed_pre, resp)
                                    self.voice.speak(resp)
                            except:
                                self.voice.speak(self.brain.think_quick("I hit an internal error.") if hasattr(self.brain, 'think_quick') else _ERR_FALLBACK)
                        continue
                except: pass

                self.ears.wait_for_wake()
                self.voice.speak(self.brain.think_quick("The user (male, always call him sir) just woke you. Greet in ONE sentence. Vary your style: casual, formal, humorous, witty, efficient, direct, cool, curious, sharp, playful, bold, dry, minimalist, warm, reassuring, commanding, enthusiastic, sarcastic, technical, or concerned. Never say madam. Always sir.") if hasattr(self.brain, 'think_quick') else "Yes sir?")
                _write_hud("listening")
                last = time.time()
                miss_count = 0

                while self._on:
                    # Check typed messages during listening loop
                    try:
                        typed_during = self._pull_typed_message()
                        if typed_during:
                            self.voice.stop()
                            if not self._is_stale_startup_command(typed_during):
                                self._note_user_interaction()
                                print(f"{Fore.WHITE}[CHAT] {typed_during}{Style.RESET_ALL}")
                                if self._handle_text_mode_toggle(typed_during):
                                    break
                                if self.builtin(typed_during):
                                    break
                                _write_hud("thinking", tool="brain")
                                try:
                                    resp = self.brain.think(typed_during)
                                    if resp == "__REVELATIONS__":
                                        self._kill_all()
                                    elif resp:
                                        self._mission_on_response(typed_during, resp)
                                        self.voice.speak(resp)
                                except:
                                    self.voice.speak(self.brain.think_quick("Hit a snag sir.") if hasattr(self.brain, 'think_quick') else _ERR_FALLBACK)
                            last = time.time()
                            break
                    except: pass

                    text = self.ears.listen(
                        timeout=float(self.cfg.get("listen_timeout", 10)),
                        phrase_limit=float(self.cfg.get("listen_phrase_limit", 24))
                    )

                    if text is None:
                        if time.time() - last > self.timeout:
                            self.voice.speak(self.brain.think_quick("I'm going to standby due to inactivity.") if hasattr(self.brain, 'think_quick') else "Standing by sir.")
                            break
                        continue

                    if text == "":
                        miss_count += 1
                        if time.time() - last > self.timeout:
                            self.voice.speak(self.brain.think_quick("Going to standby mode.") if hasattr(self.brain, 'think_quick') else "Standing by sir.")
                            break
                        if miss_count <= 2:
                            self.voice.speak(self.brain.think_quick("I didn't hear that clearly. Ask the user to repeat.") if hasattr(self.brain, 'think_quick') else "Say again sir?")
                        continue

                    miss_count = 0
                    last = time.time()
                    self._note_user_interaction()

                    # Active multi-turn flow
                    if self._conv_state and self._handle_flow(text):
                        continue

                    # Project creation flow
                    if self._proj_step > 0:
                        self._proj_handle(text)
                        continue

                    t = text.lower()
                    if self._handle_text_mode_toggle(text):
                        if self._chat_mode:
                            break
                        continue
                    if self.builtin(text):
                        continue
                        continue

                    if self.builtin(text): continue

                    self._kill_flag.clear()
                    result_box = [None]

                    def _think(txt=text):
                        try:
                            _write_hud("thinking", tool="brain")
                            result_box[0] = self.brain.think(txt)
                        except Exception as e:
                            result_box[0] = _ERR_FALLBACK
                            import traceback
                            print(f"{Fore.RED}Brain: {e}{Style.RESET_ALL}")
                            traceback.print_exc()

                    self._task_thread = threading.Thread(target=_think, daemon=True)
                    self._task_thread.start()
                    self._task_thread.join(timeout=90)

                    if self._kill_flag.is_set():
                        self.voice.speak(self.brain.think_quick("A task was aborted. Acknowledge.") if hasattr(self.brain, 'think_quick') else "Stopped sir.")
                    elif result_box[0] == "__REVELATIONS__":
                        self._kill_all()
                    elif result_box[0]:
                        self._mission_on_response(text, result_box[0])
                        self.voice.speak(result_box[0])

                    # Handle interrupt mode set during speech
                    if self._interrupt_mode == "standby":
                        self._interrupt_mode = None
                        break
                    elif self._interrupt_mode == "listen":
                        self._interrupt_mode = None
                        last = time.time()

                    last = time.time()
                    _write_hud("standby")
                    print(f"{Fore.MAGENTA}  Session active â€” {self.timeout}s timeout{Style.RESET_ALL}")

            except KeyboardInterrupt:
                self.voice.speak("Powering down. Good day sir."); break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                self.voice.speak(self.brain.think_quick("I encountered an error. Apologize briefly.") if hasattr(self.brain, 'think_quick') else _ERR_FALLBACK)


def setup_wizard():
    from colorama import Fore, Style
    print(f"\n{Fore.CYAN}J.A.R.V.I.S Setup{Style.RESET_ALL}\n")
    cfg = load_config()
    print(f"  Get your API key at: {Fore.YELLOW}https://console.anthropic.com{Style.RESET_ALL}\n")
    ak = input(f"Anthropic API key [{cfg['anthropic_api_key'][:8] + '...' if cfg['anthropic_api_key'] else 'not set'}]: ").strip()
    if ak: cfg["anthropic_api_key"] = ak
    vp = input(f"Vosk model path [{cfg.get('vosk_model_path','')}]: ").strip()
    if vp: cfg["vosk_model_path"] = vp
    mic = input(f"Mic device index [{cfg.get('mic_device', 1)}]: ").strip()
    if mic: cfg["mic_device"] = int(mic)
    save_config(cfg)
    print(f"\n{Fore.GREEN}Config saved.{Style.RESET_ALL}\n")
    return cfg

def main():
    import traceback as _tb
    _log = Path.home() / "jarvis_crash.txt"
    try:
        cfg = load_config()
        using_local = cfg.get("use_local_model", False) or cfg.get("use_openclaw", False)
        if "--setup" in sys.argv or (not cfg["anthropic_api_key"] and not using_local):
            cfg = setup_wizard()
        if not cfg["anthropic_api_key"] and not using_local:
            print("No API key. Run: python jarvis.py --setup"); sys.exit(1)
        Jarvis(cfg).run()
    except Exception as _e:
        _sep = "=" * 60
        _tb_str = _tb.format_exc()
        _cfg_str = json.dumps(load_config(), indent=2)
        _msg = "JARVIS CRASH\n" + _sep + "\n" + _tb_str + "\nConfig dump:\n" + _cfg_str
        _log.write_text(_msg, encoding="utf-8")
        print(_msg)
        raise

if __name__ == "__main__":
    main()
