#!/usr/bin/env python3
import subprocess, sys, os, numpy as np
from faster_whisper import WhisperModel

SR = 16000 # 16 kHz mono
MODEL_NAME = os.getenv("WHISPER_MODEL", "small")
COMPUTE = os.getenv("WHISPER_COMPUTE", "int8")
MODEL = WhisperModel(MODEL_NAME, device="cpu", compute_type=COMPUTE)

def load_f32_mono16k_ffmpeg(path: str, sr: int = SR) -> np.ndarray:

    if not os.path.exists(path):
        raise FileNotFoundError(path)
    cmd = [
    "ffmpeg", "-nostdin", "-y",
    "-i", path,
    "-ac", "1", "-ar", str(sr),
    "-f", "f32le", "pipe:1"
    ]
    raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    audio = np.frombuffer(raw, dtype=np.float32)

    # normalize so quiet recordings aren’t lost
    peak = np.max(np.abs(audio)) or 1.0

    return (audio / peak).astype(np.float32)

#adds a preroll so beggining text is not lost
def add_preroll(audio: np.ndarray, ms: int = 300, sr: int = SR) -> np.ndarray:

#add short silent pad to prevent chipping
    pad = np.zeros(int(sr * ms / 1000), dtype=np.float32)
    
    return np.concatenate([pad, audio])

def transcribe_full(audio: np.ndarray) -> str:
    #Always print every segment (timestamps + text)
    segs, info = MODEL.transcribe(
    audio,
    language="en",
    vad_filter=False,
    condition_on_previous_text=False,
    temperature=0.0,
    beam_size=1,
    without_timestamps=True
    )
    out = []

    for s in segs:
        if s.text:
            out.append(s.text.strip())

    return " ".join(out).strip()