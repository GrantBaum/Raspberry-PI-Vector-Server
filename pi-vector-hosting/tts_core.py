# tts_core.py
import subprocess, tempfile, base64, os, sys, shutil

VOICE = os.getenv("PIPER_VOICE", "en_US-amy-medium")

def _piper_cmd():
# Prefer the CLI if available; otherwise use "python -m piper"
    if shutil.which("piper"):
        return ["piper"]
    return [sys.executable, "-m", "piper"]

def tts_to_base64_wav(text: str) -> str:
    if not text.strip():
        raise ValueError("Empty text for TTS")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        out_path = tmp.name
    try:
        cmd = _piper_cmd() + ["--model", VOICE, "--output_file", out_path]
        p = subprocess.run(cmd, input=text.encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.returncode != 0:
            raise RuntimeError(p.stderr.decode("utf-8") or "piper failed")
            
        with open(out_path, "rb") as f:
                wav_bytes = f.read()
                return base64.b64encode(wav_bytes).decode("ascii")
    finally:
        try: os.remove(out_path)
        except FileNotFoundError: pass