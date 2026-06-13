import asyncio
import json
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

import aiohttp
import requests
from bs4 import BeautifulSoup


class DeepDiveEngine:
    def __init__(self):
        self.session = None
        self.results = {}
        self._proxy = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        ]
        self._ua_idx = 0

    def _ua(self):
        self._ua_idx = (self._ua_idx + 1) % len(self.user_agents)
        return self.user_agents[self._ua_idx]

    def _headers(self):
        return {"User-Agent": self._ua(), "Accept-Language": "en-US,en;q=0.9"}

    # --- Username search ---
    def search_username(self, username):
        import concurrent.futures
        from concurrent.futures import ThreadPoolExecutor
        
        sites = {
            # Social Media
            "GitHub": f"https://github.com/{quote_plus(username)}",
            "Twitter/X": f"https://x.com/{quote_plus(username)}",
            "Instagram": f"https://www.instagram.com/{quote_plus(username)}/",
            "Reddit": f"https://www.reddit.com/user/{quote_plus(username)}/",
            "TikTok": f"https://www.tiktok.com/@{quote_plus(username)}",
            "YouTube": f"https://www.youtube.com/@{quote_plus(username)}",
            "Twitch": f"https://www.twitch.tv/{quote_plus(username)}",
            "Telegram": f"https://t.me/{quote_plus(username)}",
            "Pinterest": f"https://www.pinterest.com/{quote_plus(username)}/",
            "Medium": f"https://medium.com/@{quote_plus(username)}",
            "Dev.to": f"https://dev.to/{quote_plus(username)}",
            "Keybase": f"https://keybase.io/{quote_plus(username)}",
            "Snapchat": f"https://www.snapchat.com/add/{quote_plus(username)}",
            "Discord": f"https://discord.com/users/{quote_plus(username)}",
            "Steam": f"https://steamcommunity.com/id/{quote_plus(username)}",
            "Spotify": f"https://open.spotify.com/user/{quote_plus(username)}",
            "Patreon": f"https://www.patreon.com/{quote_plus(username)}",
            "ProductHunt": f"https://www.producthunt.com/@{quote_plus(username)}",
            "HackerNews": f"https://news.ycombinator.com/user?id={quote_plus(username)}",
            "Chess.com": f"https://www.chess.com/member/{quote_plus(username)}",
            "SoundCloud": f"https://soundcloud.com/{quote_plus(username)}",
            "Dribbble": f"https://dribbble.com/{quote_plus(username)}",
            "Behance": f"https://www.behance.net/{quote_plus(username)}",
            "Vimeo": f"https://vimeo.com/{quote_plus(username)}",
            "Flickr": f"https://www.flickr.com/people/{quote_plus(username)}/",
            "Wikipedia": f"https://en.wikipedia.org/wiki/User:{quote_plus(username)}",
            "GitLab": f"https://gitlab.com/{quote_plus(username)}",
            "BitBucket": f"https://bitbucket.org/{quote_plus(username)}/",
            "Wattpad": f"https://www.wattpad.com/user/{quote_plus(username)}",
            "DeviantArt": f"https://www.deviantart.com/{quote_plus(username)}",
            "Imgur": f"https://{quote_plus(username)}.imgur.com/",
            "Replit": f"https://replit.com/@{quote_plus(username)}",
            "CodePen": f"https://codepen.io/{quote_plus(username)}",
            "Gravatar": f"https://en.gravatar.com/{quote_plus(username)}",
            "About.me": f"https://about.me/{quote_plus(username)}",
            "AngelList": f"https://angel.co/u/{quote_plus(username)}",
            "Mastodon.social": f"https://mastodon.social/@{quote_plus(username)}",
            "TryHackMe": f"https://tryhackme.com/p/{quote_plus(username)}",
            "HackerOne": f"https://hackerone.com/{quote_plus(username)}",
            "Bugcrowd": f"https://bugcrowd.com/{quote_plus(username)}",
            # Forums / Communities
            "HackTheBox": f"https://app.hackthebox.com/profile/{quote_plus(username)}",
            "StackOverflow": f"https://stackoverflow.com/users/{quote_plus(username)}",
            "Quora": f"https://www.quora.com/profile/{quote_plus(username)}",
            "Trello": f"https://trello.com/{quote_plus(username)}",
            "Pastebin": f"https://pastebin.com/u/{quote_plus(username)}",
            "Roblox": f"https://www.roblox.com/user.aspx?username={quote_plus(username)}",
            "Fiverr": f"https://www.fiverr.com/{quote_plus(username)}",
            "Upwork": f"https://www.upwork.com/freelancers/{quote_plus(username)}",
            "Linktree": f"https://linktr.ee/{quote_plus(username)}",
            "Carrd": f"https://{quote_plus(username)}.carrd.co/",
            "BuyMeACoffee": f"https://www.buymeacoffee.com/{quote_plus(username)}",
            "Ko-fi": f"https://ko-fi.com/{quote_plus(username)}",
            "Substack": f"https://{quote_plus(username)}.substack.com/",
            "Linktree": f"https://linktr.ee/{quote_plus(username)}",
            "BeReal": f"https://bere.al/{quote_plus(username)}",
            "Threads": f"https://www.threads.net/@{quote_plus(username)}",
            "Bluesky": f"https://bsky.app/profile/{quote_plus(username)}",
            "Mastodon": f"https://mastodon.social/@{quote_plus(username)}",
            # Gaming
            "Minecraft": f"https://namemc.com/profile/{quote_plus(username)}",
            "EpicGames": f"https://www.epicgames.com/id/{quote_plus(username)}",
            "Xbox": f"https://account.xbox.com/en-us/Profile?gamertag={quote_plus(username)}",
            "PSNProfiles": f"https://psnprofiles.com/{quote_plus(username)}",
            "Speedrun.com": f"https://www.speedrun.com/user/{quote_plus(username)}",
            "FortniteTracker": f"https://fortnitetracker.com/profile/all/{quote_plus(username)}",
            "RiotGames": f"https://tracker.gg/valorant/profile/riot/{quote_plus(username)}",
            "SteamCommunity": f"https://steamcommunity.com/id/{quote_plus(username)}",
            # Dev / Tech
            "NPM": f"https://www.npmjs.com/~{quote_plus(username)}",
            "PyPI": f"https://pypi.org/user/{quote_plus(username)}/",
            "DockerHub": f"https://hub.docker.com/u/{quote_plus(username)}",
            "Codeberg": f"https://codeberg.org/{quote_plus(username)}",
            "SourceForge": f"https://sourceforge.net/u/{quote_plus(username)}/",
            "Launchpad": f"https://launchpad.net/~{quote_plus(username)}",
            "Kaggle": f"https://www.kaggle.com/{quote_plus(username)}",
            "LeetCode": f"https://leetcode.com/{quote_plus(username)}",
            "Codewars": f"https://www.codewars.com/users/{quote_plus(username)}",
            "Exercism": f"https://exercism.org/profiles/{quote_plus(username)}",
            "HackerRank": f"https://www.hackerrank.com/{quote_plus(username)}",
            "CodinGame": f"https://www.codingame.com/profile/{quote_plus(username)}",
            "TopCoder": f"https://profiles.topcoder.com/{quote_plus(username)}",
            # Finance / Crypto
            "Coinbase": f"https://www.coinbase.com/{quote_plus(username)}",
            "Binance": f"https://www.binance.com/en/user/{quote_plus(username)}",
            # Creative / Art
            "Pixiv": f"https://www.pixiv.net/en/users/{quote_plus(username)}",
            "ArtStation": f"https://www.artstation.com/{quote_plus(username)}",
            "Bandcamp": f"https://{quote_plus(username)}.bandcamp.com/",
            "Mixcloud": f"https://www.mixcloud.com/{quote_plus(username)}/",
            "500px": f"https://500px.com/p/{quote_plus(username)}",
            "Unsplash": f"https://unsplash.com/@{quote_plus(username)}",
            "VSSG": f"https://vsco.co/{quote_plus(username)}/gallery",
            "Giphy": f"https://giphy.com/{quote_plus(username)}",
            # Blogging / Writing
            "WordPress": f"https://{quote_plus(username)}.wordpress.com/",
            "Blogger": f"https://{quote_plus(username)}.blogspot.com/",
            "LiveJournal": f"https://{quote_plus(username)}.livejournal.com/",
            "Tumblr": f"https://{quote_plus(username)}.tumblr.com/",
            "Hashnode": f"https://hashnode.com/@{quote_plus(username)}",
            # Travel / Lifestyle
            "TripAdvisor": f"https://www.tripadvisor.com/members/{quote_plus(username)}",
            "Couchsurfing": f"https://www.couchsurfing.com/people/{quote_plus(username)}",
            "Strava": f"https://www.strava.com/athletes/{quote_plus(username)}",
            # Misc
            "IFTTT": f"https://ifttt.com/p/{quote_plus(username)}",
            "Gravatar": f"https://gravatar.com/{quote_plus(username)}",
            "Disqus": f"https://disqus.com/by/{quote_plus(username)}/",
            "VirusTotal": f"https://www.virustotal.com/gui/user/{quote_plus(username)}",
            "Shodan": f"https://www.shodan.io/search?query={quote_plus(username)}",
            "Cracked.io": f"https://cracked.io/{quote_plus(username)}",
            "BitcoinTalk": f"https://bitcointalk.org/index.php?action=profile;u={quote_plus(username)}",
        }
        # Parallel async HTTP check across all sites
        found = {}
        with ThreadPoolExecutor(max_workers=20) as pool:
            futures = {pool.submit(self._check_site, site, url): site for site, url in sites.items()}
            try:
                for future in concurrent.futures.as_completed(futures, timeout=12):
                    site = futures[future]
                    try:
                        url = future.result(timeout=3)
                        if url:
                            found[site] = url
                    except:
                        pass
            except concurrent.futures.TimeoutError:
                pass
            # Cleanup remaining futures
            for f in futures:
                f.cancel()
        return found

    def _check_site(self, site, url):
        try:
            r = requests.get(url, headers=self._headers(), timeout=3, allow_redirects=True)
            if r.status_code == 200:
                return url
        except:
            pass
        return None

    # --- Email search ---
    def search_email(self, email):
        results = {}

        # Breach check via leak-check.net (free API)
        try:
            r = requests.get(f"https://leak-check.net/api/public/check-email?email={quote_plus(email)}",
                             headers=self._headers(), timeout=8)
            if r.status_code == 200:
                data = r.json()
                results["breaches"] = data.get("breaches", [])
                results["total_breaches"] = data.get("total", 0)
        except:
            pass

        # EmailRep.io
        try:
            r = requests.get(f"https://emailrep.io/{quote_plus(email)}",
                             headers={**self._headers(), "Accept": "application/json"}, timeout=8)
            if r.status_code == 200:
                data = r.json()
                results["reputation"] = {
                    "reputation": data.get("reputation"),
                    "suspicious": data.get("suspicious"),
                    "details": data.get("details", {}),
                }
        except:
            pass

        # Hunter.io-style pattern check (social profiles)
        try:
            domain = email.split("@")[-1] if "@" in email else ""
            if domain:
                username = email.split("@")[0]
                # Check if email format gives us social leads
                results["domain"] = domain
                results["local_part"] = username
        except:
            pass

        return results

    # --- Phone lookup ---
    def search_phone(self, phone):
        results = {}
        cleaned = re.sub(r"[^\d]", "", phone)

        # Try numlookupapi (free tier)
        try:
            r = requests.get(
                f"https://api.numlookupapi.com/v1/validate/{quote_plus(cleaned)}",
                headers=self._headers(), timeout=8
            )
            if r.status_code == 200:
                data = r.json()
                results["valid"] = data.get("valid", False)
                results["country"] = data.get("country", "")
                results["carrier"] = data.get("carrier", "")
                results["line_type"] = data.get("line_type", "")
        except:
            pass

        results["raw"] = cleaned
        return results

    # --- Reverse image search ---
    def search_image(self, image_path=None, image_url=None):
        results = {}

        # Google reverse image search via direct URL
        if image_url:
            search_url = f"https://lens.google.com/uploadbyurl?url={quote_plus(image_url)}"
            results["google_lens"] = search_url

        # Generate a search URL for manual use
        if image_path:
            path = Path(image_path)
            if path.exists():
                results["local_file"] = str(path.resolve())
                results["size_kb"] = path.stat().st_size // 1024

        return results

    # --- People search sites ---
    def search_people_sites(self, name, city=""):
        results = {}
        encoded = quote_plus(name)

        # TruePeopleSearch
        try:
            url = f"https://www.truepeoplesearch.com/search?name={encoded}"
            r = requests.get(url, headers=self._headers(), timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                cards = soup.select(".card-body")
                people = []
                for card in cards[:5]:
                    text = card.get_text(strip=True)
                    if text:
                        people.append(text[:200])
                if people:
                    results["truepeoplesearch"] = people
        except:
            pass

        # Try whitepages
        try:
            url = f"https://www.whitepages.com/name/{encoded}"
            r = requests.get(url, headers=self._headers(), timeout=8)
            if r.status_code == 200:
                results["whitepages"] = url
        except:
            pass

        return results

    # --- Social profile scraping (basic) ---
    def scrape_social_profile(self, platform, username):
        try:
            if platform.lower() == "github":
                r = requests.get(f"https://api.github.com/users/{quote_plus(username)}",
                                 headers=self._headers(), timeout=8)
                if r.status_code == 200:
                    data = r.json()
                    return {
                        "name": data.get("name"),
                        "bio": data.get("bio"),
                        "location": data.get("location"),
                        "public_repos": data.get("public_repos"),
                        "followers": data.get("followers"),
                        "following": data.get("following"),
                        "blog": data.get("blog"),
                        "twitter": data.get("twitter_username"),
                        "created_at": data.get("created_at"),
                        "avatar": data.get("avatar_url"),
                    }

            elif platform.lower() == "reddit":
                r = requests.get(f"https://www.reddit.com/user/{quote_plus(username)}/about.json",
                                 headers={**self._headers(), "Accept": "application/json"},
                                 timeout=8)
                if r.status_code == 200:
                    data = r.json().get("data", {})
                    return {
                        "name": data.get("name"),
                        "created": datetime.fromtimestamp(data.get("created", 0)).strftime("%Y-%m-%d") if data.get("created") else "",
                        "link_karma": data.get("link_karma", 0),
                        "comment_karma": data.get("comment_karma", 0),
                        "is_gold": data.get("is_gold", False),
                        "is_employee": data.get("is_employee", False),
                    }
        except:
            pass
        return {}

    # --- Cross-reference ---
    def cross_reference(self, known_data):
        links = {}
        emails = known_data.get("emails", [])
        usernames = known_data.get("usernames", [])
        phones = known_data.get("phones", [])

        for email in emails:
            local = email.split("@")[0] if "@" in email else email
            # Check if email local part matches any username
            matching = [u for u in usernames if u.lower() in local.lower() or local.lower() in u.lower()]
            if matching:
                links[email] = {"related_usernames": matching}

        for phone in phones:
            # Check if any username matches common phone-as-username patterns
            clean = re.sub(r"[^\d]", "", phone)
            matching = [u for u in usernames if clean[-4:] in u or u in clean]
            if matching:
                links[phone] = {"related_usernames": matching}

        return links

    # --- Main orchestrator ---
    def run_deep_dive(self, name="", email="", username="", phone="", image_path=""):
        start = time.time()
        dossier = {
            "target": name or email or username or phone,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sections": {},
            "summary": "",
            "total_finds": 0,
        }

        if username:
            found_sites = self.search_username(username)
            dossier["sections"]["username_search"] = {
                "query": username,
                "profiles_found": len(found_sites),
                "sites": found_sites,
            }
            dossier["total_finds"] += len(found_sites)

            # Scrape deeper profiles
            detailed = {}
            for platform in ["github", "reddit"]:
                if any(platform.lower() in site.lower() for site in found_sites):
                    prof = self.scrape_social_profile(platform, username)
                    if prof:
                        detailed[platform] = prof
            if detailed:
                dossier["sections"]["detailed_profiles"] = detailed

        if email:
            email_data = self.search_email(email)
            dossier["sections"]["email_intel"] = email_data
            dossier["total_finds"] += len(email_data.get("breaches", []))

        if phone:
            phone_data = self.search_phone(phone)
            dossier["sections"]["phone_intel"] = phone_data

        if name:
            people_data = self.search_people_sites(name)
            dossier["sections"]["people_search"] = people_data
            dossier["total_finds"] += sum(len(v) for v in people_data.values() if isinstance(v, list))

        if image_path:
            image_data = self.search_image(image_path=image_path)
            dossier["sections"]["image_search"] = image_data

        # Cross-reference
        cross = self.cross_reference({
            "emails": [email] if email else [],
            "usernames": [username] if username else [],
            "phones": [phone] if phone else [],
        })
        if cross:
            dossier["sections"]["cross_references"] = cross

        elapsed = time.time() - start
        dossier["elapsed_seconds"] = round(elapsed, 1)

        # Generate summary
        lines = []
        if dossier["total_finds"] > 0:
            lines.append(f"Found {dossier['total_finds']} data points across multiple sources.")
        if username and dossier["sections"].get("username_search", {}).get("profiles_found", 0) > 0:
            lines.append(f"Username '{username}' appears on {dossier['sections']['username_search']['profiles_found']} platforms.")
        if email:
            breaches = dossier["sections"].get("email_intel", {}).get("breaches", [])
            if breaches:
                lines.append(f"Email appears in {len(breaches)} known breaches.")
            rep = dossier["sections"].get("email_intel", {}).get("reputation", {})
            if rep.get("suspicious"):
                lines.append("Email reputation is suspicious.")
        dossier["summary"] = " ".join(lines) if lines else "No significant data found for this target."

        return dossier

    def format_dossier_for_speech(self, dossier):
        parts = [f"Deep dive complete on {dossier['target']}."]
        if dossier["summary"]:
            parts.append(dossier["summary"])

        if "username_search" in dossier["sections"]:
            us = dossier["sections"]["username_search"]
            if us.get("profiles_found", 0) > 0:
                sites = list(us["sites"].keys())[:8]
                parts.append(f"Profiles on {', '.join(sites)}.")

        if "email_intel" in dossier["sections"]:
            ei = dossier["sections"]["email_intel"]
            breaches = ei.get("breaches", [])
            if breaches:
                breach_names = [b.get("Name", b) if isinstance(b, dict) else str(b) for b in breaches[:5]]
                parts.append(f"Breached in {', '.join(breach_names)}.")

        if "phone_intel" in dossier["sections"]:
            pi = dossier["sections"]["phone_intel"]
            if pi.get("carrier"):
                parts.append(f"Phone carrier is {pi['carrier']}.")

        if "people_search" in dossier["sections"]:
            ps = dossier["sections"]["people_search"]
            for source, entries in ps.items():
                if entries:
                    parts.append(f"Found {len(entries)} records on {source}.")

        parts.append(f"Search took {dossier.get('elapsed_seconds', 0)} seconds.")
        return " ".join(parts)

    def format_dossier_for_text(self, dossier):
        lines = []
        lines.append(f"{'='*60}")
        lines.append(f"DEEP DIVE REPORT: {dossier['target']}")
        lines.append(f"Timestamp: {dossier['timestamp']}")
        lines.append(f"Duration: {dossier.get('elapsed_seconds', 0)}s")
        lines.append(f"{'='*60}")

        for section, data in dossier["sections"].items():
            lines.append(f"\n--- {section.upper()} ---")
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        lines.append(f"  {k}:")
                        for sk, sv in v.items():
                            lines.append(f"    {sk}: {sv}")
                    elif isinstance(v, list):
                        lines.append(f"  {k}: {len(v)} items")
                        for item in v[:5]:
                            if isinstance(item, dict):
                                lines.append(f"    - {json.dumps(item)[:120]}")
                            else:
                                lines.append(f"    - {item}")
                    else:
                        lines.append(f"  {k}: {v}")
            elif isinstance(data, list):
                for item in data[:5]:
                    lines.append(f"  - {item}")

        lines.append(f"\n{'='*60}")
        lines.append(f"SUMMARY: {dossier['summary']}")
        lines.append(f"{'='*60}")
        return "\n".join(lines)
