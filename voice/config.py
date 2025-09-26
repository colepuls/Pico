import os, shutil

# -------- STT / Audio --------
RATE = 16000
CHUNK_MS = 30
FRAME_SAMPLES = RATE * CHUNK_MS // 1000
FRAME_BYTES = FRAME_SAMPLES * 2
SILENCE_MS = 600
MAX_UTTERANCE_SEC = 12
VAD_AGGR = 2

# -------- Wake / Engage --------
WAKE_PHRASES = ("pico", "hey pico", "ok pico", "wake up", "wake", "yo")
SLEEP_PHRASES = ("go to sleep", "stop listening", "goodbye pico", "sleep", "stop", "exit", "shut up", "see ya", "see ya bro")

# -------- LLM --------
MODEL_PATH = "/home/colecodes/projects/Pico/llm/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
GEN_KW = dict(
    max_tokens=300,
    temperature=0.2,
    top_p=0.85,
    top_k=40,
    repeat_penalty=1.12,
    seed=42,
    stop=["<|im_end|>", "</s>"],
)

# -------- Piper TTS --------
PIPER_BIN_CANDIDATES = [
    os.path.expanduser("~/piper/piper/piper"),
    shutil.which("piper"),
]
PIPER_BIN = next((p for p in PIPER_BIN_CANDIDATES if p and os.path.exists(p)), None)

PIPER_VOICE_CANDIDATES = [os.path.expanduser("~/piper/en_US-amy-medium.onnx")]
PIPER_VOICE = next((v for v in PIPER_VOICE_CANDIDATES if os.path.exists(v)), None)

# Greetings / patterns
GREET_TOKENS = {"hi","hello","hey","yo","sup","good morning","good afternoon","good evening"}
WHO_PATTERNS = ("who are you","what is your name","whats your name","your name","who r u","who are u")
