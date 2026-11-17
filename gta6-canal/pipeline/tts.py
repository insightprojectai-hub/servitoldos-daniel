# -*- coding: utf-8 -*-
"""Locución en español con Kokoro (sherpa-onnx), 100 % local.

Modelo: kokoro-multi-lang-v1_0 (release 'tts-models' de k2-fsa/sherpa-onnx).
Voz: em_alex (sid 29), masculina en español.
"""
import os, re
import numpy as np

MODEL_DIR = os.environ.get("KOKORO_DIR", "/tmp/claude-0/tts/kokoro-multi-lang-v1_0/")
SID = int(os.environ.get("KOKORO_SID", "29"))
SPEED = float(os.environ.get("KOKORO_SPEED", "1.07"))

# Pronunciación: lo que se lee en pantalla -> lo que dice la voz
PRON = [
    (r"GTA\s*\+", "Ge Te A plus"),
    (r"GTA\s*(6|VI)\b", "Ge Te A seis"),
    (r"GTA\s*(5|V)\b", "Ge Te A cinco"),
    (r"\bGTA\b", "Ge Te A"),
    (r"PS5 Pro", "Pe, Ese, cinco Pro"),
    (r"\bPS5\b", "Pe, Ese, cinco"),
    (r"\bPSN\b", "Pe Ese Ene"),
    (r"\bPSSR\b", "Pe Ese Ese Erre"),
    (r"Xbox", "Équis Box"),
    (r"Series X\|S", "Series Equis y Ese"),
    (r"Series X\b", "Series Equis"),
    (r"Series S\b", "Series Ese"),
    (r"\bHDR\b", "Hache De Erre"),
    (r"\bPC\b", "Pe Ce"),
    (r"\bray tracing\b", "réi tréisin"),
    (r"Rockstar", "Rócstar"),
    (r"Take-Two", "Téik Tu"),
    (r"Vice City", "Váis Síti"),
    (r"Leonida Keys", "Leonida Kis"),
    (r"\bKeys\b", "Kis"),
    (r"Grassrivers", "Gras Rívers"),
    (r"Port Gellhorn", "Port Guélhorn"),
    (r"Mount Kalaga", "Máunt Kalaga"),
    (r"Jason", "Yéison"),
    (r"Brian Heder", "Bráian Jéder"),
    (r"Boobie Ike", "Búbi Áik"),
    (r"Dre'Quan", "Dre Cuán"),
    (r"Real Dimez", "Ríal Dáims"),
    (r"Cal Hampton", "Cal Jámpton"),
    (r"Bonnie y Clyde", "Bóni y Cláid"),
    (r"Red Dead Redemption", "Red Ded Ridémpshon"),
    (r"Vintage", "Víntach"),
    (r"Ultimate", "Últimeit"),
    (r"Standard", "Estándar"),
    (r"PlayStation", "Pléisteishon"),
    (r"Microsoft", "Máicrosoft"),
    (r"\bonline\b", "onláin"),
    (r"\bOnline\b", "Onláin"),
    (r"spoilers?", "espóilers"),
    (r"Store", "Estor"),
    (r"\bUSB\b", "U Ese Be"),
    (r"\bSSD\b", "Ese Ese De"),
    (r"\bfps\b|\bFPS\b", "efe pe ese"),
]


def to_speech(text):
    s = text
    for pat, rep in PRON:
        s = re.sub(pat, rep, s)
    s = s.replace("«", "").replace("»", "").replace("…", ".")
    return s


_tts = None


def _engine():
    global _tts
    if _tts is None:
        import sherpa_onnx
        d = MODEL_DIR
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=d + "model.onnx", voices=d + "voices.bin", tokens=d + "tokens.txt",
                    data_dir=d + "espeak-ng-data", dict_dir=d + "dict", lang="es"),
                num_threads=int(os.environ.get("TTS_THREADS", "2"))))
        _tts = sherpa_onnx.OfflineTts(cfg)
    return _tts


def synth(text):
    """Devuelve (samples float32 mono, sample_rate) sin silencios en los extremos."""
    a = _engine().generate(to_speech(text), sid=SID, speed=SPEED)
    x = np.asarray(a.samples, dtype=np.float32)
    sr = a.sample_rate
    thr = 0.01
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx):
        x = x[max(0, idx[0] - int(0.02 * sr)): idx[-1] + int(0.06 * sr)]
    return x, sr
