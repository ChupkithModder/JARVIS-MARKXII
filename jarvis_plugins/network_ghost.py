"""
Network Ghost for JARVIS.
Network scanning, port scanning, WiFi enumeration, deauth detection.
"JARVIS, scan my network" / "port scan 192.168.1.1" / "who's on my WiFi"
"""
import threading
import time
import subprocess
import socket
import json
import requests
from datetime import datetime
from pathlib import Path

_NETGHOST_INSTANCE = None
_NETGHOST_LOCK = threading.Lock()


class NetworkGhost:
    def __init__(self):
        self._scan_results = {}
        self._last_scan = ""

    def scan_network(self, target="192.168.1.0/24"):
        """ARP scan the local network to discover devices."""
        results = []
        try:
            import scapy.all as scapy
            arp_req = scapy.ARP(pdst=target)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            answered = scapy.srp(broadcast / arp_req, timeout=2, verbose=False)[0]
            for _, rcv in answered:
                hostname = "unknown"
                try:
                    hostname = socket.gethostbyaddr(rcv.psrc)[0]
                except:
                    pass
                results.append({
                    "ip": rcv.psrc,
                    "mac": rcv.hwsrc,
                    "hostname": hostname,
                    "vendor": self._mac_vendor_lookup(rcv.hwsrc)
                })
        except ImportError:
            # Fallback: use arp -a
            try:
                r = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=5,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                for line in r.stdout.split("\n"):
                    parts = line.strip().split()
                    if len(parts) >= 3 and "." in parts[0]:
                        ip = parts[0]
                        mac = parts[1].replace("-", ":")
                        hostname = "unknown"
                        try:
                            hostname = socket.gethostbyaddr(ip)[0]
                        except:
                            pass
                        results.append({"ip": ip, "mac": mac, "hostname": hostname, "vendor": ""})
            except:
                return "Network scan failed. Install scapy: pip install scapy"

        self._scan_results = {"time": datetime.now().strftime("%H:%M:%S"), "devices": results}
        self._last_scan = json.dumps(self._scan_results, indent=2)

        if not results:
            return "No devices found on the network."

        lines = [f"Found {len(results)} devices:"]
        for d in results:
            vendor = f" [{d['vendor']}]" if d.get('vendor') else ""
            lines.append(f"  {d['ip']} - {d.get('hostname','unknown')}{vendor}")
        return "\n".join(lines)

    def _mac_vendor_lookup(self, mac):
        try:
            oui = mac.replace(":", "").upper()[:6]
        except:
            return ""
        try:
            r = requests.get(f"https://api.macvendors.com/{oui}", timeout=3)
            if r.status_code == 200:
                return r.text.strip()
        except:
            pass
        return ""

    def port_scan(self, host, ports="1-1024"):
        """Scan common ports on a host."""
        try:
            import socket
            open_ports = []
            port_range = self._parse_ports(ports)
            for port in port_range:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex((host, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    open_ports.append(f"{port} ({service})")
                sock.close()

            if not open_ports:
                return f"No open ports found on {host}."
            return f"Open ports on {host}: {', '.join(open_ports)}"
        except Exception as e:
            return f"Port scan failed: {e}"

    def _parse_ports(self, ports_str):
        ports = []
        for part in ports_str.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(part))
        return ports[:200]  # cap at 200

    def list_wifi(self):
        """List nearby WiFi networks."""
        try:
            r = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=bssid"],
                capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if r.returncode != 0:
                return "WiFi scan failed. Are you on a laptop with WiFi?"

            networks = []
            current_ssid = ""
            current_auth = ""
            for line in r.stdout.split("\n"):
                line = line.strip()
                if line.startswith("SSID"):
                    current_ssid = line.split(":")[-1].strip()
                elif "Authentication" in line:
                    current_auth = line.split(":")[-1].strip()
                elif "Signal" in line:
                    signal = line.split(":")[-1].strip().rstrip("%")
                    if current_ssid:
                        networks.append(f"{current_ssid} ({signal}%) [{current_auth}]")

            if not networks:
                return "No WiFi networks found."
            return f"Nearby WiFi ({len(networks)}): " + " | ".join(networks[:15])
        except:
            return "WiFi scan failed."

    def get_wifi_password(self, ssid):
        """Retrieve saved WiFi password for a known network."""
        try:
            r = subprocess.run(
                ["netsh", "wlan", "show", "profile", f"name={ssid}", "key=clear"],
                capture_output=True, text=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in r.stdout.split("\n"):
                if "Key Content" in line:
                    return f"Password for {ssid}: {line.split(':')[-1].strip()}"
            return f"Could not retrieve password for {ssid}."
        except:
            return "Failed to get WiFi password."

    def get_current_connection(self):
        """Get current WiFi connection info."""
        try:
            r = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True, text=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            info = {}
            for line in r.stdout.split("\n"):
                line = line.strip()
                if "SSID" in line and "BSSID" not in line:
                    info["ssid"] = line.split(":")[-1].strip()
                elif "BSSID" in line:
                    info["bssid"] = line.split(":")[-1].strip()
                elif "Signal" in line:
                    info["signal"] = line.split(":")[-1].strip()
                elif "Channel" in line:
                    info["channel"] = line.split(":")[-1].strip()
                elif "Radio type" in line:
                    info["radio"] = line.split(":")[-1].strip()
            if info:
                return f"Connected to {info.get('ssid','?')} ({info.get('bssid','?')}) - Signal: {info.get('signal','?')} - Channel: {info.get('channel','?')}"
            return "Not connected to WiFi."
        except:
            return "Could not get WiFi info."

    def traceroute(self, host):
        """Trace route to a host."""
        try:
            r = subprocess.run(
                ["tracert", "-d", "-h", "10", host],
                capture_output=True, text=True, timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return r.stdout[-1000:] or "Traceroute returned empty."
        except:
            return "Traceroute failed."

    def public_ip_info(self):
        """Get public IP and geolocation info."""
        try:
            import requests as _rq
            ip = _rq.get("https://api.ipify.org", timeout=5).text
            geo = _rq.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            return f"Public IP: {ip} | {geo.get('city','?')}, {geo.get('country','?')} | ISP: {geo.get('isp','?')}"
        except:
            return "Could not determine public IP info."

    def dns_lookup(self, domain):
        """Perform DNS lookups."""
        try:
            import socket
            ip = socket.gethostbyname(domain)
            return f"{domain} resolves to {ip}"
        except:
            return f"Could not resolve {domain}."


def get_netghost():
    global _NETGHOST_INSTANCE
    with _NETGHOST_LOCK:
        if _NETGHOST_INSTANCE is None:
            try:
                _NETGHOST_INSTANCE = NetworkGhost()
            except:
                _NETGHOST_INSTANCE = False
    return _NETGHOST_INSTANCE if _NETGHOST_INSTANCE is not False else None
