"""
Gesture Control for JARVIS.
Use webcam + MediaPipe hand tracking to control mouse, click, scroll, zoom.
Tony Stark-style hand gesture interface.
Voice: "JARVIS, gesture mode" / "JARVIS, stop gestures"
"""
import threading
import time

_GESTURE_INSTANCE = None
_GESTURE_LOCK = threading.Lock()


class GestureController:
    def __init__(self):
        self._running = False
        self._thread = None
        self._mp_hands = None
        self._cap = None
        self._screen_w = 1920
        self._screen_h = 1080

    def start(self):
        if self._running:
            return "Gesture control already active sir."

        try:
            import mediapipe as mp
            import cv2
            import numpy as np
            import pyautogui

            self._mp_hands = mp.solutions.hands
            self._mp_draw = mp.solutions.drawing_utils

            self._cap = cv2.VideoCapture(0)
            if not self._cap.isOpened():
                return "Could not access webcam sir."

            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            self._screen_w, self._screen_h = pyautogui.size()
            pyautogui.FAILSAFE = False
            pyautogui.PAUSE = 0.01

            self._running = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

            return "Gesture control active sir. Use one finger to move, thumb+index pinch to click, two fingers to scroll."
        except Exception as e:
            return f"Gesture control failed: {e}"

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        if self._cap:
            self._cap.release()
        self._cap = None
        return "Gesture control deactivated."

    def _loop(self):
        import cv2
        import numpy as np
        import pyautogui

        hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )

        prev_x, prev_y = None, None
        prev_pinch = False
        prev_scroll = False
        move_smooth = 0.3  # smoothing factor

        while self._running:
            try:
                ret, frame = self._cap.read()
                if not ret:
                    time.sleep(0.05)
                    continue

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, _ = frame.shape

                results = hands.process(rgb)

                if results.multi_hand_landmarks:
                    for landmarks in results.multi_hand_landmarks:
                        # Get key points
                        index_tip = landmarks.landmark[8]   # Index finger tip
                        thumb_tip = landmarks.landmark[4]   # Thumb tip
                        index_mcp = landmarks.landmark[5]   # Index base
                        middle_tip = landmarks.landmark[12] # Middle finger tip
                        pinky_tip = landmarks.landmark[20]  # Pinky tip

                        # Map to screen coordinates (invert x axis due to mirror)
                        sx = int((1 - index_tip.x) * self._screen_w)
                        sy = int(index_tip.y * self._screen_h)

                        # Smooth movement
                        if prev_x is not None:
                            sx = int(prev_x + (sx - prev_x) * move_smooth)
                            sy = int(prev_y + (sy - prev_y) * move_smooth)
                        prev_x, prev_y = sx, sy

                        pyautogui.moveTo(sx, sy)

                        # Pinch detection (thumb + index close together)
                        pinch_dist = abs(thumb_tip.x - index_tip.x) + abs(thumb_tip.y - index_tip.y)
                        is_pinch = pinch_dist < 0.05

                        if is_pinch and not prev_pinch:
                            pyautogui.click()
                            prev_pinch = True
                        elif not is_pinch and prev_pinch:
                            prev_pinch = False

                        # Scroll detection (index + middle finger extended, other curled)
                        index_up = index_tip.y < index_mcp.y - 0.05
                        middle_up = middle_tip.y < landmarks.landmark[9].y - 0.05
                        pinky_curled = pinky_tip.y > landmarks.landmark[17].y

                        is_scroll = index_up and middle_up and pinky_curled and not is_pinch

                        if is_scroll and not prev_scroll:
                            # Scroll direction based on hand Y position
                            scroll_dir = -1 if sy < self._screen_h * 0.4 else 1
                            pyautogui.scroll(scroll_dir * 3)
                        prev_scroll = is_scroll
                else:
                    prev_x = prev_y = None
                    prev_pinch = False
                    prev_scroll = False

                time.sleep(0.016)  # ~60fps

            except Exception as e:
                time.sleep(0.1)

        self._cap.release()

    def status(self):
        return "Gesture control is active." if self._running else "Gesture control is offline."


def get_gesture():
    global _GESTURE_INSTANCE
    with _GESTURE_LOCK:
        if _GESTURE_INSTANCE is None:
            try:
                _GESTURE_INSTANCE = GestureController()
            except:
                _GESTURE_INSTANCE = False
    return _GESTURE_INSTANCE if _GESTURE_INSTANCE is not False else None
