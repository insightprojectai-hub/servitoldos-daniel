# -*- coding: utf-8 -*-
"""Música synthwave generada por código (sin derechos de autor) + efectos."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000

PROGS = {
    # tónica MIDI, acordes (semitonos sobre la tónica)
    "sunset":  (57, [[0, 3, 7], [-4, 0, 3], [-9, -5, -2], [-2, 2, 5]]),   # Am F C G
    "sunset2": (52, [[0, 3, 7], [-4, 0, 3], [-9, -5, -2], [-2, 2, 5]]),
    "miami":   (53, [[0, 3, 7], [-2, 2, 5], [-4, 0, 3], [-5, -2, 2]]),
    "neon":    (55, [[0, 3, 7], [-4, 0, 3], [1, 5, 8], [-2, 2, 5]]),
    "cyber":   (50, [[0, 3, 7], [3, 7, 10], [-4, 0, 3], [-2, 2, 5]]),
    "ocean":   (59, [[0, 4, 7], [-3, 0, 4], [-7, -3, 0], [-5, -1, 2]]),
}


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0, detune) if detune else (0,):
        ph = (t * f * (1 + d)) % 1.0
        out += 2 * ph - 1
    return out / (3 if detune else 1)


def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def kick(n):
    t = np.arange(n) / SR
    f = 50 + 120 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7)


def snare(n, rng):
    t = np.arange(n) / SR
    noise = hp(rng.standard_normal(n), 1200) * np.exp(-t * 9)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 20)
    return 0.6 * noise + 0.5 * body


def hat(n, rng):
    t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t * 60)


def track(palette, seconds, bpm=None, seed=1):
    rng = np.random.default_rng(seed)
    root, prog = PROGS.get(palette, PROGS["sunset"])
    bpm = bpm or {"sunset": 96, "sunset2": 92, "miami": 100, "neon": 104, "cyber": 108, "ocean": 90}.get(palette, 98)
    beat = 60.0 / bpm
    bar = 4 * beat
    nbars = int(np.ceil(seconds / bar)) + 1
    N = int(nbars * bar * SR)
    pad = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N); arp = np.zeros(N)
    nb = int(beat * SR)
    K = kick(int(0.45 * SR)); S = snare(int(0.35 * SR), rng); H = hat(int(0.06 * SR), rng)
    for b in range(nbars):
        ch = prog[b % len(prog)]
        s0 = int(b * bar * SR)
        nbar = int(bar * SR)
        # pad
        p = np.zeros(nbar)
        for iv in ch:
            p += saw(mtof(root + iv), nbar, detune=0.004)
        p = lp(p, 1400) * env(nbar, 0.25, 0.25)
        pad[s0:s0 + nbar] += p[: N - s0]
        # bajo a corcheas (octava)
        for e in range(8):
            m = root - 24 + ch[0] + (12 if e % 2 else 0)
            ln = int(beat / 2 * SR)
            st = s0 + e * ln
            if st + ln > N:
                break
            bass[st:st + ln] += lp(saw(mtof(m), ln), 600) * env(ln, 0.005, 0.05)
        # arpegio a semicorcheas (entra a partir del compás 4)
        if b >= 4:
            notes = [root + 12 + ch[i % 3] for i in range(16)]
            ln = int(beat / 4 * SR)
            for i, m in enumerate(notes):
                st = s0 + i * ln
                if st + ln > N:
                    break
                tone = np.sign(np.sin(2 * np.pi * mtof(m) * np.arange(ln) / SR))
                arp[st:st + ln] += lp(tone, 2500) * env(ln, 0.003, 0.08) * (0.9 if i % 4 == 0 else 0.6)
        # batería (entra a partir del compás 2)
        if b >= 2:
            for q in range(4):
                st = s0 + q * nb
                if st + len(K) < N:
                    drums[st:st + len(K)] += K
                if q in (1, 3) and st + len(S) < N:
                    drums[st:st + len(S)] += S * 0.8
                for h in (0, nb // 2):
                    if st + h + len(H) < N:
                        drums[st + h:st + h + len(H)] += H * (0.25 if h else 0.15)
    # eco simple en el arpegio
    d = int(beat * 0.75 * SR)
    arp2 = arp.copy(); arp2[d:] += 0.35 * arp[:-d]
    mix = 0.22 * pad + 0.35 * bass + 0.55 * drums + 0.10 * arp2
    mix = mix[: int(seconds * SR)]
    # fade in/out
    mix *= env(len(mix), 1.5, 3.0)
    mix /= (np.max(np.abs(mix)) + 1e-9)
    return mix.astype(np.float32)


def whoosh(dur=0.5, seed=3):
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    x = rng.standard_normal(n)
    t = np.linspace(0, 1, n)
    # barrido de filtro por bloques
    out = np.zeros(n)
    blocks = 20
    for i in range(blocks):
        a, b = i * n // blocks, (i + 1) * n // blocks
        fc = 300 + 6000 * (i / blocks) ** 2
        out[a:b] = lp(x[a:b], fc)
    e = np.sin(np.pi * t) ** 2
    return (out * e / (np.max(np.abs(out * e)) + 1e-9)).astype(np.float32)


def pop(seed=5):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (900 - 3000 * t) * t) * np.exp(-t * 40)).astype(np.float32)
