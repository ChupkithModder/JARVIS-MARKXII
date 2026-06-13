"""
Computer Use for JARVIS — reads screen, clicks text, types, controls any app.
"JARVIS, click the Save button" / "JARVIS, type hello into Notepad"
"""
import threading
import time
import re
from pathlib import Path

_COMPUTER_INSTANCE = None
_COMPUTER_LOCK = threading.Lock()


class ComputerUse:
    def __init__(self):
        self._scroll_amount = 3
        self._setup_tesseract()

    def _setup_tesseract(self):
        """Auto-find Tesseract if not in PATH."""
        import os
        if os.system("tesseract --version 2>nul") != 0:
            paths = [
                r"C:\Program Files\Tesseract-OCR",
                r"C:\Program Files (x86)\Tesseract-OCR",
            ]
            for p in paths:
                if Path(p).joinpath("tesseract.exe").exists():
                    os.environ["PATH"] += os.pathsep + p
                    break

    def find_text_on_screen(self, target_text, case_sensitive=False, threshold=0.7):
        """Find text on screen via OCR. Returns (x, y, width, height) or None."""
        try:
            import pyautogui, pytesseract
            from PIL import Image

            screenshot = pyautogui.screenshot()
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

            best_match = None
            best_confidence = 0
            target = target_text if case_sensitive else target_text.lower()

            for i, text in enumerate(data["text"]):
                if not text or not text.strip():
                    continue
                match_text = text if case_sensitive else text.lower()
                confidence = 0
                if target in match_text:
                    confidence = len(target) / max(len(match_text), 1)
                elif match_text in target:
                    confidence = len(match_text) / max(len(target), 1)

                if confidence >= threshold and confidence > best_confidence:
                    x = data["left"][i]
                    y = data["top"][i]
                    w = data["width"][i]
                    h = data["height"][i]
                    best_match = (x + w // 2, y + h // 2, w, h, text.strip())
                    best_confidence = confidence

            return best_match
        except ImportError:
            return None

    def click_text(self, text, double=False, right=False):
        """Find text on screen and click it."""
        try:
            import pyautogui

            result = self.find_text_on_screen(text)
            if not result:
                return f"Could not find '{text}' on screen."

            x, y, w, h, found_text = result
            pyautogui.moveTo(x, y, duration=0.2)

            if double:
                pyautogui.doubleClick()
            elif right:
                pyautogui.rightClick()
            else:
                pyautogui.click()

            return f"Clicked '{found_text}' at ({x},{y})."
        except Exception as e:
            return f"Click failed: {e}"

    def type_at(self, text):
        """Type text into the active window."""
        try:
            import pyautogui, pyperclip
            # For long text, use clipboard + paste for speed
            if len(text) > 50:
                pyperclip.copy(text)
                pyautogui.hotkey("ctrl", "v")
                return f"Pasted {len(text)} characters sir."
            else:
                pyautogui.write(text, interval=0.02)
                return f"Typed '{text[:50]}' sir."
        except Exception as e:
            return f"Type failed: {e}"

    def press_key(self, key):
        """Press a key or key combo. Examples: 'enter', 'ctrl+s', 'alt+tab'."""
        try:
            import pyautogui
            key = key.lower().strip()
            if "+" in key:
                parts = key.split("+")
                pyautogui.hotkey(*parts)
                return f"Pressed {key}."
            else:
                pyautogui.press(key)
                return f"Pressed {key}."
        except Exception as e:
            return f"Key failed: {e}"

    def read_screen(self):
        """OCR everything on screen and return the text."""
        try:
            import pyautogui, pytesseract
            screenshot = pyautogui.screenshot()
            text = pytesseract.image_to_string(screenshot, timeout=10)
            cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            if not cleaned:
                return "No readable text on screen."
            return cleaned[:2000]
        except Exception as e:
            return f"Screen read failed: {e}"

    def find_and_type(self, field_label, text):
        """Find a text field by its label, click it, then type."""
        try:
            import pyautogui

            result = self.find_text_on_screen(field_label)
            if not result:
                # Try clicking into a reasonable area near the label position
                return f"Could not find '{field_label}' sir."

            x, y = result[0], result[1] + result[3] + 10  # click below the label
            pyautogui.click(x, y)
            time.sleep(0.2)

            # Type
            import pyperclip
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
            return f"Typed into field near '{field_label}' sir."
        except Exception as e:
            return f"Field type failed: {e}"

    def get_active_window(self):
        """Get the title of the active window."""
        try:
            import pygetwindow as gw
            win = gw.getActiveWindow()
            if win:
                return f"Active window: {win.title}"
            return "No active window detected."
        except:
            return "Could not detect active window."

    def focus_window(self, title):
        """Bring a window to focus by title substring."""
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(title)
            if windows:
                windows[0].activate()
                return f"Focused '{windows[0].title}'."
            return f"No window matching '{title}'."
        except Exception as e:
            return f"Focus failed: {e}"

    def click_coord(self, x, y, double=False):
        """Click at specific screen coordinates."""
        try:
            import pyautogui
            pyautogui.moveTo(int(x), int(y), duration=0.2)
            if double:
                pyautogui.doubleClick()
            else:
                pyautogui.click()
            return f"Clicked ({x},{y})."
        except Exception as e:
            return f"Coordinate click failed: {e}"

    def scroll(self, clicks=3):
        """Scroll the mouse wheel."""
        try:
            import pyautogui
            pyautogui.scroll(int(clicks))
            return f"Scrolled {clicks}."
        except Exception as e:
            return f"Scroll failed: {e}"

    def hover(self, x, y):
        """Move mouse to coordinates without clicking."""
        try:
            import pyautogui
            pyautogui.moveTo(int(x), int(y), duration=0.3)
            return f"Moved to ({x},{y})."
        except Exception as e:
            return f"hover failed: {e}"

    def drag(self, x1, y1, x2, y2):
        """Drag from one coordinate to another."""
        try:
            import pyautogui
            pyautogui.moveTo(int(x1), int(y1), duration=0.2)
            pyautogui.drag(int(x2 - x1), int(y2 - y1), duration=0.5)
            return f"Dragged from ({x1},{y1}) to ({x2},{y2})."
        except Exception as e:
            return f"Drag failed: {e}"


def get_computer():
    global _COMPUTER_INSTANCE
    with _COMPUTER_LOCK:
        if _COMPUTER_INSTANCE is None:
            try:
                _COMPUTER_INSTANCE = ComputerUse()
            except:
                _COMPUTER_INSTANCE = False
    return _COMPUTER_INSTANCE if _COMPUTER_INSTANCE is not False else None
