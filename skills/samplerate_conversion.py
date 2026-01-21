import numpy as np

def resample(data, old_sr, new_sr):
    data = np.asarray(data, dtype=np.float32)

    if data.ndim == 2 and data.shape[1] == 1:
        data = data[:, 0]

    n = data.shape[0]
    if n == 0 or old_sr == new_sr:
        return data

    new_len = max(1, int(round(n * new_sr / old_sr)))

    xp = np.arange(n, dtype=np.float32)
    x = np.linspace(0, n - 1, new_len, dtype=np.float32)

    if data.ndim == 1:
        return np.interp(x, xp, data)

    out = np.empty((new_len, data.shape[1]), dtype=np.float32)
    for i in range(data.shape[1]):
        out[:, i] = np.interp(x, xp, data[:, i])
    return out