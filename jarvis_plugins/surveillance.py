"""
Webcam Surveillance for JARVIS.
Features:
- Motion detection with sensitivity threshold
- Face detection (optional)
- Auto-capture on motion
- Voice alerts
- "Jarvis, enable surveillance" / "Jarvis, has anyone entered my room?"
"""
import threading
import time
from datetime import datetime
from pathlib import Path

_SURV_INSTANCE = None
_SURV_LOCK = threading.Lock()


class SurveillanceEngine:
    def __init__(self):
        self.cap = None
        self._running = False
        self._thread = None
        self._last_alert_time = 0
        self._alert_cooldown = 5  # seconds between alerts
        self._motion_threshold = 25  # pixel difference threshold
        self._sensitivity = 2  # 1-5, higher = more sensitive
        self._face_cascade = None
        self._alert_callback = None
        self._captures_dir = Path.home() / "Desktop" / "jarvis_surveillance"
        self._captures_dir.mkdir(exist_ok=True)
        self._motion_count = 0
        self._last_frame = None
        self._detected_faces = 0

    def start(self, alert_callback=None):
        if self._running:
            return "Surveillance already active sir."

        import cv2
        import numpy as np

        self._alert_callback = alert_callback

        # Try to load face cascade
        try:
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            if Path(cascade_path).exists():
                self._face_cascade = cv2.CascadeClassifier(cascade_path)
        except:
            pass

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return "Could not access webcam sir."

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 10)

        self._running = True
        self._motion_count = 0
        self._thread = threading.Thread(target=self._surveillance_loop, daemon=True)
        self._thread.start()

        return "Surveillance active sir. I will alert you of any motion."

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        self.cap = None
        return "Surveillance deactivated sir."

    def _surveillance_loop(self):
        import cv2
        import numpy as np

        while self._running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.5)
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                if self._last_frame is not None:
                    delta = cv2.absdiff(self._last_frame, gray)
                    thresh = cv2.threshold(delta, int(self._motion_threshold / self._sensitivity), 255, cv2.THRESH_BINARY)[1]
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    motion_detected = False
                    faces_detected = 0

                    for contour in contours:
                        if cv2.contourArea(contour) < 500 * self._sensitivity:
                            continue
                        motion_detected = True
                        (x, y, w, h) = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Face detection
                    if self._face_cascade and motion_detected:
                        faces = self._face_cascade.detectMultiScale(gray, 1.1, 4)
                        faces_detected = len(faces)
                        for (fx, fy, fw, fh) in faces:
                            cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (0, 0, 255), 2)

                    if motion_detected:
                        self._motion_count += 1
                        now = time.time()
                        if now - self._last_alert_time > self._alert_cooldown:
                            self._last_alert_time = now
                            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            cap_path = self._captures_dir / f"motion_{ts}.jpg"
                            cv2.imwrite(str(cap_path), frame)
                            msg = f"Motion detected. {faces_detected} face(s). Capture saved."
                            if self._alert_callback:
                                self._alert_callback(msg, str(cap_path))

                self._last_frame = gray.copy()
                time.sleep(0.1)

            except Exception as e:
                print(f"[SURVEILLANCE] Error: {e}")
                time.sleep(1)

    def status(self):
        if not self._running:
            return "Surveillance is offline."
        return f"Surveillance active. {self._motion_count} motion events captured. Directory: {self._captures_dir}"

    def list_captures(self):
        files = sorted(self._captures_dir.glob("motion_*.jpg"), reverse=True)[:10]
        if not files:
            return "No captures yet sir."
        return "Recent captures: " + ", ".join(f.name for f in files)

    def set_sensitivity(self, level):
        self._sensitivity = max(1, min(5, int(level)))
        return f"Sensitivity set to {self._sensitivity}/5."


def get_surveillance():
    global _SURV_INSTANCE
    with _SURV_LOCK:
        if _SURV_INSTANCE is None:
            try:
                _SURV_INSTANCE = SurveillanceEngine()
            except Exception as e:
                _SURV_INSTANCE = False
                print(f"[JARVIS] Surveillance unavailable: {e}")
    return _SURV_INSTANCE if _SURV_INSTANCE is not False else None
