import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import sherpa_onnx
from data_stream.samplerate_conversion import resample

SHERPA_MODEL_DIR = "/home/cole/Pico/sherpa-onnx-stt"
sherpa_recognizer = None # keep single recognizer for single load
# default_device = sd.default.device = 'USB PnP Sound Device'

def record_audio(sleep_delay):
    samplerate = 48000
    #threshold = 0.3
    threshold = 0.02
    silence_time = sleep_delay
    block_size = 1024
    silence_time_tracker = 0
    audio = []
    speech_detected = False

    # Open mic stream
    with sd.InputStream(samplerate=samplerate, channels=1) as stream:
        while True:
            block = stream.read(block_size)[0]
            #volume = np.linalg.norm(block)
            volume = float(np.sqrt((block**2).mean()))
            audio.append(block)
            if volume < threshold:
                silence_time_tracker += block_size / samplerate
                if silence_time_tracker > silence_time:
                    break
            else:
                silence_time_tracker = 0
                speech_detected = True
        
    data = np.concatenate(audio, axis=0) # combine all audio chunks
    # resample:
    data_16sr = resample(data, samplerate, 16000)
    sf.write("/home/cole/Pico/audio_files/audio.wav", data, samplerate)
    return data_16sr, 16000, speech_detected


# STT MODEL SETUP -----
def create_sherpa_recognizer():

    encoder = os.path.join(
        SHERPA_MODEL_DIR,
        "encoder-epoch-99-avg-1-chunk-16-left-128.int8.onnx",
    )

    decoder = os.path.join(
        SHERPA_MODEL_DIR,
        "decoder-epoch-99-avg-1-chunk-16-left-128.int8.onnx",
    )

    joiner = os.path.join(
        SHERPA_MODEL_DIR,
        "joiner-epoch-99-avg-1-chunk-16-left-128.int8.onnx",
    )

    tokens = os.path.join(SHERPA_MODEL_DIR, "tokens.txt")

    recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens=tokens,
        encoder=encoder,
        decoder=decoder,
        joiner=joiner,
        num_threads=2,
        sample_rate=16000,
        feature_dim=80,
        enable_endpoint_detection=False,  # single utterance from file
        provider="cpu",
        debug=False,
    )

    return recognizer


def get_sherpa_recognizer():
    global sherpa_recognizer
    if sherpa_recognizer is None:
        sherpa_recognizer = create_sherpa_recognizer()
    return sherpa_recognizer
# -----


# STT
def translate_audio_to_text():
    audio_path="/home/cole/Pico/audio_files/audio.wav" # user audio path
    recognizer = get_sherpa_recognizer() # get model
    samples, sr = sf.read(audio_path, dtype="float32") # read audio

    # if stereo, average to mono
    if samples.ndim > 1:
        samples = samples.mean(axis=1)

    stream = recognizer.create_stream()
    # resample if needed
    stream.accept_waveform(sr, samples)

    # process
    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    # result
    text = recognizer.get_result(stream).strip()
    # reset
    recognizer.reset(stream)

    return text