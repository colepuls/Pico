import os, tempfile, subprocess
from .config import PIPER_BIN, PIPER_VOICE

def say(text: str, *, device: str | None = None):
    if not text or not text.strip(): return
    if not PIPER_BIN:
        print("[TTS] Piper binary not found; skipping speech."); return
    if not PIPER_VOICE or not os.path.exists(PIPER_VOICE):
        print(f"[TTS] Voice model not found at {PIPER_VOICE or '(unset)'}; skipping speech."); return

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
    try:
        subprocess.run([PIPER_BIN, "--model", PIPER_VOICE, "--output_file", wav_path],
                       input=text.encode("utf-8"), check=True)
        play_cmd = ["aplay", "-q", wav_path] if not device else ["aplay", "-q", "-D", device, wav_path]
        subprocess.run(play_cmd, check=True)
    finally:
        try: os.remove(wav_path)
        except OSError: pass
