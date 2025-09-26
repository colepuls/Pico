import re
import numpy as np
import sounddevice as sd
from .config import WAKE_PHRASES, SLEEP_PHRASES, GREET_TOKENS, WHO_PATTERNS

def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def contains_wake(text: str) -> bool:
    return any(p in normalize(text) for p in WAKE_PHRASES)

def strip_wake_phrase(text: str) -> str:
    return re.sub(r'^\s*(?:hey|ok)?\s*pico[\s,:\-]*', '', text, flags=re.IGNORECASE).strip()

def is_sleep_cmd(text: str) -> bool:
    return any(p in normalize(text) for p in SLEEP_PHRASES)

def is_greeting(text: str) -> bool:
    t = normalize(text)
    if any(t == g or t.startswith(g) for g in GREET_TOKENS):
        return True
    if set(t.split()) & {"hi","hello","hey","yo","sup"}:
        return True
    return False

def is_who(text: str) -> bool:
    return any(p in normalize(text) for p in WHO_PATTERNS)

def chime(freq=1000, ms=120, sr=22050):
    try:
        t = np.linspace(0, ms/1000.0, int(sr*ms/1000.0), False)
        tone = 0.2 * np.sin(2*np.pi*freq*t).astype(np.float32)
        sd.play(tone, sr); sd.wait()
    except Exception:
        pass
