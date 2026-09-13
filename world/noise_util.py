"""Simple value noise + FBM without external deps beyond numpy."""
from __future__ import annotations
import numpy as np

def _hash2(x: int, z: int, seed: int) -> float:
    n = (x * 374761393 + z * 668265263 + seed * 982451653) & 0x7FFFFFFF
    n = (n ^ (n >> 13)) * 1274126177
    return ((n ^ (n >> 16)) & 0x7FFFFFFF) / 0x7FFFFFFF

def value_noise_2d(x: float, z: float, seed: int = 0) -> float:
    x0, z0 = int(np.floor(x)), int(np.floor(z))
    fx, fz = x - x0, z - z0
    u = fx * fx * (3 - 2 * fx)
    v = fz * fz * (3 - 2 * fz)
    a = _hash2(x0, z0, seed)
    b = _hash2(x0 + 1, z0, seed)
    c = _hash2(x0, z0 + 1, seed)
    d = _hash2(x0 + 1, z0 + 1, seed)
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v

def fbm(x: float, z: float, seed: int = 0, octaves: int = 4, lacunarity: float = 2.0, gain: float = 0.5) -> float:
    amp, freq, total, norm = 1.0, 1.0, 0.0, 0.0
    for i in range(octaves):
        total += amp * value_noise_2d(x * freq, z * freq, seed + i * 1013)
        norm += amp
        amp *= gain
        freq *= lacunarity
    return total / max(norm, 1e-9)
