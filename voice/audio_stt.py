import sys, queue
import numpy as np
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel
from .config import RATE, CHUNK_MS, FRAME_SAMPLES, FRAME_BYTES, SILENCE_MS, VAD_AGGR

audio_q = queue.Queue()

def list_devices():
    for i, d in enumerate(sd.query_devices()):
        print(f"{i}: {d['name']} (inputs={d['max_input_channels']}, outputs={d['max_output_channels']})")

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    mono = indata[:, 0]
    pcm16 = (np.clip(mono, -1.0, 1.0) * 32767).astype(np.int16).tobytes()
    for i in range(0, len(pcm16), FRAME_BYTES):
        chunk = pcm16[i:i + FRAME_BYTES]
        if len(chunk) == FRAME_BYTES:
            audio_q.put(chunk)

def collect_utterance(vad: webrtcvad.Vad, max_seconds: float | None = None) -> bytes:
    while not audio_q.empty():
        try: audio_q.get_nowait()
        except queue.Empty: break

    voiced = bytearray(); have_voice = False; silence_ms = 0
    while True:
        frame = audio_q.get()
        if vad.is_speech(frame, RATE):
            have_voice = True; voiced.extend(frame); silence_ms = 0
        elif have_voice:
            silence_ms += CHUNK_MS

        dur = (len(voiced) // 2) / RATE
        if have_voice and silence_ms >= SILENCE_MS: break
        if max_seconds is not None and dur >= max_seconds: break
    return bytes(voiced)

def pcm16_to_float32(pcm: bytes) -> np.ndarray:
    if not pcm: return np.zeros(0, dtype=np.float32)
    return np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0

def get_utterance_text(model: WhisperModel, *, max_seconds=None) -> str:
    vad = webrtcvad.Vad(VAD_AGGR)
    with sd.InputStream(channels=1, samplerate=RATE, dtype='float32',
                        blocksize=FRAME_SAMPLES, callback=audio_callback):
        pcm = collect_utterance(vad, max_seconds=max_seconds)
    if not pcm: return ""
    audio = pcm16_to_float32(pcm)
    if audio.size == 0: return ""
    segments, _ = model.transcribe(audio, language="en", vad_filter=False, beam_size=1, temperature=0.0)
    return "".join(s.text for s in segments).strip()
