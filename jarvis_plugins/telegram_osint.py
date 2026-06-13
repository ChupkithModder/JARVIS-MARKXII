"""
Telegram OSINT for JARVIS.
Resolve phone numbers to Telegram accounts.
"JARVIS, check if this number is on Telegram" / "lookup telegram user @username"
"""
import threading
import requests
import json
import re
from pathlib import Path

_TG_INSTANCE = None
_TG_LOCK = threading.Lock()


class TelegramIntel:
    def __init__(self):
        self._sessions = {}

    def _tg_request(self, method, data=None):
        """Make a request to Telegram's public API."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Origin": "https://web.telegram.org",
        }
        urls = {
            "search": "https://t.me/{query}",
            "resolve": "https://api.telegram.org/bot{token}/getUpdates",
            "user_info": "https://t.me/{username}",
        }
        try:
            r = requests.get(urls.get(method, urls["search"]).format(**data) if data else urls["search"],
                             headers=headers, timeout=8, allow_redirects=True)
            return r.status_code, r.text, r.url
        except Exception as e:
            return None, str(e), ""

    def check_phone(self, phone):
        """Check if a phone number has a Telegram account (via contact import method)."""
        cleaned = re.sub(r"[^\d+]", "", phone)
        if not cleaned.startswith("+"):
            cleaned = "+" + cleaned

        results = {
            "phone": cleaned,
            "telegram_found": False,
            "username": "",
            "name": "",
            "direct_link": "",
        }

        # Try public Telegram user search
        # Attempt 1: t.me/+phone number link
        try:
            r = requests.get(f"https://t.me/+{cleaned[1:]}", headers={
                "User-Agent": "Mozilla/5.0"
            }, timeout=5, allow_redirects=True)
            if r.status_code == 200 and "tgme_page_title" in r.text:
                results["telegram_found"] = True
                name_match = re.search(r'<meta property="og:title" content="([^"]+)"', r.text)
                if name_match:
                    results["name"] = name_match.group(1)
                results["direct_link"] = str(r.url)
        except:
            pass

        return results

    def lookup_username(self, username):
        """Lookup information about a Telegram username."""
        username = username.strip().lstrip("@")
        results = {
            "username": username,
            "exists": False,
            "name": "",
            "description": "",
            "direct_link": f"https://t.me/{username}",
        }

        try:
            r = requests.get(f"https://t.me/{username}", headers={
                "User-Agent": "Mozilla/5.0"
            }, timeout=5, allow_redirects=True)

            if r.status_code == 200:
                results["exists"] = True
                # Parse the meta tags
                name_match = re.search(r'<meta property="og:title" content="([^"]+)"', r.text)
                desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', r.text)

                if name_match:
                    results["name"] = name_match.group(1)
                if desc_match:
                    results["description"] = desc_match.group(1)
                else:
                    # Try alt description
                    alt_desc = re.search(r'<div class="tgme_page_description"[^>]*>(.*?)</div>', r.text, re.DOTALL)
                    if alt_desc:
                        results["description"] = re.sub(r'<[^>]+>', '', alt_desc.group(1)).strip()
            else:
                results["exists"] = False
        except:
            pass

        return results

    def search_by_name(self, name):
        """Search Telegram for users/groups by name."""
        try:
            r = requests.get(f"https://t.me/s/{name}", headers={
                "User-Agent": "Mozilla/5.0"
            }, timeout=5, allow_redirects=True)
            if r.status_code == 200:
                return f"Found Telegram channel/user: https://t.me/{name}"
            return f"No public Telegram entity found for: {name}"
        except:
            return f"Search failed for: {name}"

    def format_phone_result(self, result):
        if result.get("telegram_found"):
            name = result.get("name", "Unknown")
            return f"Phone {result['phone']} has Telegram: {name}"
        return f"Phone {result['phone']} not found on Telegram (public)."

    def format_username_result(self, result):
        if result.get("exists"):
            name = result.get("name", "Unknown")
            desc = result.get("description", "")[:100]
            parts = [f"@{result['username']} - {name}"]
            if desc:
                parts.append(f"Bio: {desc}")
            return " | ".join(parts)
        return f"@{result['username']} does not exist on Telegram."


def get_telegram_intel():
    global _TG_INSTANCE
    with _TG_LOCK:
        if _TG_INSTANCE is None:
            try:
                _TG_INSTANCE = TelegramIntel()
            except:
                _TG_INSTANCE = False
    return _TG_INSTANCE if _TG_INSTANCE is not False else None
