import torch, torch.nn.functional as F, torchaudio
from torchaudio.transforms import MelSpectrogram, AmplitudeToDB
from wakeword.model import WakewordRNN


SAMPLE_RATE = 16000
TARGET_LEN = 16000


# Load model
device = torch.device("cpu")
model = WakewordRNN().to(device)
model.load_state_dict(torch.load("/home/cole/Pico/wakeword/wakeword_model.pth", map_location=device))
model.eval()


# Audio transforms
mel = MelSpectrogram(sample_rate=SAMPLE_RATE, n_fft=400, hop_length=160, n_mels=40, center=False)
db  = AmplitudeToDB()


# Convert from stereo to mono
def to_mono(x):
    if x.ndim == 2:
        x = x.mean(axis=1)
    return torch.tensor(x, dtype=torch.float32)


# pad sr
def prep_waveform(x, sr):
    if sr != SAMPLE_RATE:
        x = torchaudio.functional.resample(x, sr, SAMPLE_RATE)
    if x.numel() > TARGET_LEN:
        x = x[-TARGET_LEN:]
    else:
        x = F.pad(x, (0, TARGET_LEN - x.numel()))
    return x


# gets prob of wakeword
def get_prob(np_audio, sr):
    x = to_mono(np_audio)
    x = prep_waveform(x, sr)
    _mel = mel(x)
    mel_db = db(_mel).unsqueeze(0)  # (1, 40, T)
    with torch.no_grad():
        p = model(mel_db.to(device)).item()
    return p
