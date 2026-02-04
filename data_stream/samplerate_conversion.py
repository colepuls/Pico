import numpy as np


# sr conversion tool
def resample(data, old_sr, new_sr):
    data = np.asarray(data, dtype=np.float32) # to float

    if data.ndim == 2 and data.shape[1] == 1:
        data = data[:, 0]

    n = data.shape[0]
    if n == 0 or old_sr == new_sr:
        return data

    new_len = max(1, int(round(n * new_sr / old_sr))) # compute # of needed samples for new sr

    xp = np.arange(n, dtype=np.float32) # original pos
    x = np.linspace(0, n - 1, new_len, dtype=np.float32) # new pos

    if data.ndim == 1:
        return np.interp(x, xp, data) # estimate values between points

    out = np.empty((new_len, data.shape[1]), dtype=np.float32)
    for i in range(data.shape[1]):
        out[:, i] = np.interp(x, xp, data[:, i])
    return out