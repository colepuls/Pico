import argparse, os
from faster_whisper import WhisperModel
from llama_cpp import Llama

from .config import GEN_KW, MAX_UTTERANCE_SEC, MODEL_PATH
from .utils import chime, contains_wake, strip_wake_phrase, is_sleep_cmd, is_greeting, is_who, normalize
from .audio_stt import list_devices, get_utterance_text
from .tts import say

def run():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", type=str, default=None, help="Input mic device index or name")
    ap.add_argument("--list", action="store_true", help="List audio devices and exit")
    ap.add_argument("--stt_model", default="tiny.en", help="faster-whisper model (tiny.en/base.en)")
    ap.add_argument("--compute_type", default="int8", help="int8 or int8_float16")
    ap.add_argument("--no_chime", action="store_true", help="Disable wake chime")
    ap.add_argument("--tts_out", type=str, default=None, help="ALSA output device for TTS (e.g., 'plughw:1,0')")
    args = ap.parse_args()

    if args.list:
        list_devices(); return

    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=os.cpu_count(),
                n_batch=128, use_mlock=False, embedding=False, verbose=False, chat_format="chatml")
    print("Say Pico")

    stt = WhisperModel(args.stt_model, device="cpu", compute_type=args.compute_type)

    if args.device is not None:
        import sounddevice as sd
        try: sd.default.device = int(args.device)
        except ValueError: sd.default.device = args.device

    mode = "wake"
    while True:
        try:
            if mode == "wake":
                text = get_utterance_text(stt, max_seconds=3)
                if not text: continue
                if contains_wake(text):
                    if not args.no_chime: chime()
                    first_query = strip_wake_phrase(text)
                    print("Awake."); mode = "engaged"
                    if first_query:
                        print(f"\n-> {first_query}")
                        if is_sleep_cmd(first_query):
                            print("Okay, going back to wake mode."); mode = "wake"; continue
                        if is_greeting(first_query):
                            reply = "Hello, I'm Pico."; print(reply + "\n"); say(reply, device=args.tts_out); continue
                        if is_who(first_query):
                            reply = "My name is Pico, your friendly AI assistant."
                            print(reply + "\n"); say(reply, device=args.tts_out); continue
                        messages = [{"role": "user", "content": first_query}]
                        reply_chunks = []
                        for tok in llm.create_chat_completion(messages=messages, stream=True, **GEN_KW):
                            piece = tok["choices"][0]["delta"].get("content", "")
                            if piece: reply_chunks.append(piece)
                            print(piece, end="", flush=True)
                        print("\n")
                        full_reply = "".join(reply_chunks).strip()
                        if full_reply: say(full_reply, device=args.tts_out)
                    continue

            # engaged mode (explicit sleep only)
            text = get_utterance_text(stt, max_seconds=MAX_UTTERANCE_SEC)
            if not text: continue
            print(f"\n-> {text}")
            if is_sleep_cmd(text):
                print("Okay, going back to wake mode."); mode = "wake"; continue
            if is_greeting(text):
                reply = "Hello, I'm Pico."; print(reply + "\n"); say(reply, device=args.tts_out); continue
            if is_who(text):
                reply = "My name is Pico, your friendly AI assistant."
                print(reply + "\n"); say(reply, device=args.tts_out); continue
            if normalize(text) in {"quit"}:
                print("Bye."); say("Goodbye.", device=args.tts_out); break

            messages = [{"role": "user", "content": text}]
            reply_chunks = []
            for tok in llm.create_chat_completion(messages=messages, stream=True, **GEN_KW):
                piece = tok["choices"][0]["delta"].get("content", "")
                if piece: reply_chunks.append(piece)
                print(piece, end="", flush=True)
            print("\n")
            full_reply = "".join(reply_chunks).strip()
            if full_reply: say(full_reply, device=args.tts_out)

        except KeyboardInterrupt:
            print("\nBye.")
            try: say("Goodbye.", device=args.tts_out)
            except Exception: pass
            break
        except Exception as e:
            print(f"\n[Error] {e}\n")
