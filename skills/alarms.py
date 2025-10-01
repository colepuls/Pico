import datetime as dt
import threading
import numpy as np
import sounddevice as sd
import re

# =========================
# Audio: looping alarm tone
# =========================
_alarm_stop = threading.Event()
_alarm_thread = None

def _alarm_sound(sr=44100):
    """Loop a harsh alarm tone until stop_alarm() is called."""
    dur_beep, dur_pause = 0.3, 0.2
    t_beep = np.linspace(0, dur_beep, int(sr * dur_beep), endpoint=False, dtype=np.float32)
    t_pause = np.zeros(int(sr * dur_pause), dtype=np.float32)

    # Two tones for a sharper sound
    wave1 = 0.3 * np.sin(2 * np.pi * 1000 * t_beep, dtype=np.float32)
    wave2 = 0.3 * np.sin(2 * np.pi * 1500 * t_beep, dtype=np.float32)
    beep = (wave1 + wave2).astype(np.float32)

    pattern = np.concatenate([beep, t_pause, beep, t_pause, beep]).astype(np.float32)

    while not _alarm_stop.is_set():
        sd.play(pattern, sr)
        sd.wait()

def start_alarm():
    """Start the alarm sound if not already ringing."""
    global _alarm_thread
    if _alarm_thread and _alarm_thread.is_alive():
        return
    _alarm_stop.clear()
    _alarm_thread = threading.Thread(target=_alarm_sound, daemon=True)
    _alarm_thread.start()

def stop_alarm():
    """Stop the alarm sound."""
    _alarm_stop.set()
    sd.stop()

# ======================================
# Scheduling: next occurrence of 12h time
# ======================================
_timers = []  # keep strong refs so Timer objects aren't GC'd

def _next_occurrence_12h(time_str: str, *, grace_seconds: int = 0) -> dt.datetime:
    now = dt.datetime.now()
    target_today = dt.datetime.strptime(time_str.upper(), "%I:%M %p").replace(
        year=now.year, month=now.month, day=now.day, second=0, microsecond=0
    )
    if target_today < (now - dt.timedelta(seconds=grace_seconds)):
        target_today += dt.timedelta(days=1)
    return target_today

def set_alarm(time_str: str, *, grace_seconds: int = 0) -> dt.datetime:
    target = _next_occurrence_12h(time_str, grace_seconds=grace_seconds)
    delay = max(0.0, (target - dt.datetime.now()).total_seconds())
    timer = threading.Timer(delay, start_alarm)
    timer.daemon = True
    timer.start()
    _timers.append(timer)
    return target

# ==========================================
# Parsing helper: extract time from free text
# ==========================================
_TIME_RE = re.compile(r"\b(1[0-2]|0?[1-9]):([0-5]\d)\s*([AaPp][Mm])\b")

def extract_time_12h(text: str) -> str | None:
    m = _TIME_RE.search(text)
    if not m:
        return None
    h, mm, ampm = m.groups()
    return f"{int(h)}:{mm} {ampm.upper()}"

def set_output_device(index: int | None):
    if index is None:
        sd.default.device = (sd.default.device[0], None) if isinstance(sd.default.device, tuple) else None
    else:
        # (input_device, output_device)
        sd.default.device = (None, index)
