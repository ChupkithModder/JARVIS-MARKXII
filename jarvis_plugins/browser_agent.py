"""
Autonomous Browser Agent for JARVIS.
Voice commands like "Jarvis, open amazon and search for X" 
or "Jarvis, find the best price for Y and tell me."

Uses Playwright under the hood. LLM-driven via tool actions.
"""
import threading
import time
from pathlib import Path

_AGENT_INSTANCE = None
_AGENT_LOCK = threading.Lock()


class BrowserAgent:
    def __init__(self):
        self.browser = None
        self.page = None
        self._running = False

    def start(self):
        from playwright.sync_api import sync_playwright
        self._running = True
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.chromium.launch(headless=False, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        context = self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        self.page = context.new_page()
        return "Browser started sir."

    def stop(self):
        self._running = False
        try:
            if self.page: self.page.close()
            if self.browser: self.browser.close()
            if hasattr(self, '_playwright'): self._playwright.stop()
        except:
            pass
        self.browser = None
        self.page = None
        return "Browser closed."

    def navigate(self, url):
        if not self.page:
            self.start()
        if not url.startswith("http"):
            url = "https://" + url
        self.page.goto(url, timeout=15000, wait_until="domcontentloaded")
        title = self.page.title()
        return f"Opened {url} - {title}"

    def search(self, engine, query):
        search_urls = {
            "google": f"https://www.google.com/search?q={query}",
            "youtube": f"https://www.youtube.com/results?search_query={query}",
            "amazon": f"https://www.amazon.com/s?k={query}",
            "ebay": f"https://www.ebay.com/sch/i.html?_nkw={query}",
            "wikipedia": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
            "github": f"https://github.com/search?q={query}",
            "reddit": f"https://www.reddit.com/search/?q={query}",
            "twitter": f"https://x.com/search?q={query}",
            "duckduckgo": f"https://duckduckgo.com/?q={query}",
            "bing": f"https://www.bing.com/search?q={query}",
        }
        url = search_urls.get(engine.lower(), f"https://www.google.com/search?q={query}")
        return self.navigate(url)

    def click_text(self, text):
        if not self.page:
            return "No browser open sir."
        try:
            self.page.get_by_text(text, exact=False).first.click(timeout=5000)
            return f"Clicked '{text}'."
        except:
            return f"Could not find '{text}' to click."

    def type_text(self, selector, text):
        if not self.page:
            return "No browser open sir."
        try:
            self.page.locator(selector).first.fill(text)
            return f"Typed '{text[:30]}' into {selector}."
        except:
            return f"Could not type into {selector}."

    def read_page(self):
        if not self.page:
            return "No browser open sir."
        try:
            text = self.page.inner_text("body")[:3000]
            title = self.page.title()
            url = self.page.url
            return f"Page: {title} ({url})\n\nContent:\n{text}"
        except:
            return "Could not read the page."

    def screenshot(self):
        if not self.page:
            return "No browser open sir."
        p = Path.home() / "Desktop" / "jarvis_browser_screenshot.png"
        self.page.screenshot(path=str(p))
        return str(p)

    def get_links(self):
        if not self.page:
            return "No browser open sir."
        try:
            links = self.page.locator("a[href]").all()
            results = []
            for link in links[:15]:
                href = link.get_attribute("href")
                text = link.inner_text().strip()[:60]
                if href and text and not href.startswith("#"):
                    results.append(f"{text} -> {href}")
            return f"Found {len(links)} links. Top results:\n" + "\n".join(results)
        except:
            return "Could not extract links."

    def scroll_down(self, amount=1):
        if not self.page:
            return "No browser open sir."
        for _ in range(amount):
            self.page.keyboard.press("PageDown")
        return f"Scrolled {amount} page(s)."

    def press_enter(self):
        if not self.page:
            return "No browser open sir."
        self.page.keyboard.press("Enter")
        time.sleep(0.5)
        return "Pressed Enter."

    def go_back(self):
        if not self.page:
            return "No browser open sir."
        self.page.go_back()
        return "Went back."


def get_agent():
    global _AGENT_INSTANCE
    with _AGENT_LOCK:
        if _AGENT_INSTANCE is None:
            try:
                _AGENT_INSTANCE = BrowserAgent()
            except Exception as e:
                _AGENT_INSTANCE = False
                print(f"[JARVIS] Browser agent unavailable: {e}")
    return _AGENT_INSTANCE if _AGENT_INSTANCE is not False else None
