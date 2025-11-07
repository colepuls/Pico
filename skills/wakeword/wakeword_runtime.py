# wakeword_runtime.py
import torch, torch.nn.functional as F, torchaudio
from torchaudio.transforms import MelSpectrogram, AmplitudeToDB
from skills.wakeword.model import WakewordRNN

SAMPLE_RATE = 16000
TARGET_LEN = 16000

# Load model
_device = torch.device("cpu")
_model = WakewordRNN().to(_device)
_model.load_state_dict(torch.load("/home/colecodes/projects/Pico/skills/wakeword/wakeword_model.pth", map_location=_device))
_model.eval()

# Audio transforms
_mel = MelSpectrogram(sample_rate=SAMPLE_RATE, n_fft=400, hop_length=160, n_mels=40, center=False)
_db  = AmplitudeToDB()

def _to_mono_1d(x):
    if x.ndim == 2:
        x = x.mean(axis=1)
    return torch.tensor(x, dtype=torch.float32)

def _prep_waveform(x, sr):
    if sr != SAMPLE_RATE:
        x = torchaudio.functional.resample(x, sr, SAMPLE_RATE)
    if x.numel() > TARGET_LEN:
        x = x[-TARGET_LEN:]
    else:
        x = F.pad(x, (0, TARGET_LEN - x.numel()))
    return x

def prob_from_np(np_audio, sr):
    """np_audio: numpy array (N,) float32 mono"""
    x = _to_mono_1d(np_audio)
    x = _prep_waveform(x, sr)
    mel = _mel(x)
    mel_db = _db(mel).unsqueeze(0)  # (1, 40, T)
    with torch.no_grad():
        p = _model(mel_db.to(_device)).item()
    return p
