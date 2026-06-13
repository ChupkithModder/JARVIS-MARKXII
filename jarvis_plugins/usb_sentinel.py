"""
USB Sentinel for JARVIS.
Monitors for USB device connections/disconnections in real-time.
Alerts when unknown devices are plugged in.
"JARVIS, monitor USB" / "JARVIS, list USB devices"
"""
import threading
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

_USB_INSTANCE = None
_USB_LOCK = threading.Lock()


class USBSentinel:
    def __init__(self):
        self._running = False
        self._thread = None
        self._known_devices = set()
        self._alert_callback = None
        self._last_scan = []
        self._load_known()

    def _load_known(self):
        f = Path.home() / ".jarvis_usb_known.json"
        if f.exists():
            try:
                self._known_devices = set(json.loads(f.read_text()))
            except:
                pass

    def _save_known(self):
        f = Path.home() / ".jarvis_usb_known.json"
        f.write_text(json.dumps(list(self._known_devices)))

    def _get_usb_devices(self):
        """Get all currently connected USB devices using PowerShell."""
        try:
            r = subprocess.run([
                "powershell", "-Command",
                "Get-PnpDevice -PresentOnly | Where-Object {$_.Class -eq 'USB' -or $_.Class -eq 'HIDClass'} | "
                "Select-Object FriendlyName, InstanceId, Status | ConvertTo-Json"
            ], capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW)
            if r.returncode == 0 and r.stdout.strip():
                try:
                    devices = json.loads(r.stdout)
                    if isinstance(devices, dict):
                        devices = [devices]
                    return devices
                except:
                    pass
        except:
            pass
        return []

    def list_devices(self):
        """List all connected USB devices."""
        devices = self._get_usb_devices()
        if not devices:
            return "No USB devices detected or failed to query."

        lines = [f"Connected USB devices ({len(devices)}):"]
        for d in devices:
            name = d.get("FriendlyName", "Unknown")[:60]
            status = d.get("Status", "?")
            known = "known" if name in self._known_devices else "UNKNOWN"
            lines.append(f"  [{status}] {name} ({known})")
        return "\n".join(lines)

    def start_monitoring(self, alert_callback=None):
        if self._running:
            return "USB monitoring already active."

        self._alert_callback = alert_callback
        self._running = True
        self._last_scan = [d.get("FriendlyName", "") for d in self._get_usb_devices()]

        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        return "USB monitoring active. I will alert on new devices."

    def stop_monitoring(self):
        self._running = False
        return "USB monitoring stopped."

    def _monitor_loop(self):
        while self._running:
            try:
                current = self._get_usb_devices()
                current_names = [d.get("FriendlyName", "") for d in current]

                # Detect new devices
                for name in current_names:
                    if name and name not in self._last_scan:
                        if name not in self._known_devices:
                            ts = datetime.now().strftime("%H:%M:%S")
                            msg = f"NEW USB DEVICE: {name}"
                            self._known_devices.add(name)
                            self._save_known()
                            if self._alert_callback:
                                self._alert_callback(msg)

                # Detect removed devices
                for name in self._last_scan:
                    if name and name not in current_names:
                        ts = datetime.now().strftime("%H:%M:%S")
                        if self._alert_callback:
                            self._alert_callback(f"USB removed: {name}")

                self._last_scan = current_names
            except:
                pass
            time.sleep(2)

    def status(self):
        count = len(self._last_scan)
        state = "active" if self._running else "offline"
        return f"USB monitor {state}. {count} devices seen. {len(self._known_devices)} known."

    def get_storage_devices(self):
        """List removable storage devices (USB drives)."""
        try:
            r = subprocess.run([
                "powershell", "-Command",
                "Get-Volume | Where-Object {$_.DriveType -eq 'Removable'} | "
                "Select-Object DriveLetter, FileSystemLabel, SizeRemaining, Size | ConvertTo-Json"
            ], capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW)
            if r.returncode == 0 and r.stdout.strip():
                try:
                    devices = json.loads(r.stdout)
                    if isinstance(devices, dict):
                        devices = [devices]
                    lines = ["USB Storage Devices:"]
                    for d in devices:
                        letter = d.get("DriveLetter", "?")
                        label = d.get("FileSystemLabel", "No Label")
                        size = int(d.get("Size", 0)) // (1024**3) if d.get("Size") else 0
                        lines.append(f"  {letter}:\\ - {label} ({size}GB)")
                    return "\n".join(lines)
                except:
                    pass
        except:
            pass
        return "No USB storage devices found."


def get_usb_sentinel():
    global _USB_INSTANCE
    with _USB_LOCK:
        if _USB_INSTANCE is None:
            try:
                _USB_INSTANCE = USBSentinel()
            except:
                _USB_INSTANCE = False
    return _USB_INSTANCE if _USB_INSTANCE is not False else None
