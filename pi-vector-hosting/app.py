import io, subprocess
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from flask import Flask, request, jsonify

#local imports
from stt_core import load_f32_mono16k_ffmpeg, transcribe_full, MODEL_NAME, COMPUTE
from tts_core import tts_to_base64_wav
from vector_brain import detect_intent, act

# ---- Flask app ----

app = Flask(__name__)

@app.route("/stt", methods=["POST"])
def stt():

    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    data = request.files["file"].read()

    try:
        audio = load_f32_mono16k_ffmpeg(data)
        text = transcribe_full(audio)
        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form.get("text", "")

    if not text:
        return jsonify({"error": "no text provided"}), 400
    
    try:
        wav_b64 = tts_to_base64_wav(text)
        return jsonify({"wav_base64": wav_b64})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    #convert text into speech using piper

@app.route("/health")
def health():
    return {"ok": True, "model": "small"}, 200

@app.route("/brain", methods=["POST"])
def brain_text():

## Send JSON: { "text": "..." }
## Returns: { "text", "action", "reply_wav_base64"? }

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "no text provided"}), 400

    action = detect_intent(text)
    result = act(action)

    # auto-reply with TTS if the brain provided "say"
    resp = {"text": text, "action": action, "result": result}
    say = action.get("say")

    if say:

        try:
            resp["reply_wav_base64"] = tts_to_base64_wav(say)

        except Exception as e:
            resp["tts_error"] = str(e)

    return jsonify(resp)

@app.route("/command", methods=["POST"])
def command():

## Upload audio as form-data 'file'.
## Returns transcript + chosen action (+ optional TTS reply)

    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400
    data = request.files["file"].read()

    # Use your existing decode/transcribe from this file
    try:
        audio = load_f32_mono16k_ffmpeg(data)
        text = transcribe_full(audio)
    except Exception as e:
        return jsonify({"error": f"stt_failed: {e}"}), 500

    action = detect_intent(text)
    result = act(action)

    resp = {"text": text, "action": action, "result": result}
    say = action.get("say")
    if say:
        try:
            resp["reply_wav_base64"] = tts_to_base64_wav(say)
        except Exception as e:
            resp["tts_error"] = str(e)
    return jsonify(resp)


# ---- Run until you close the terminal ----

if __name__ == "__main__":

    print("🎙️  STT service running on http://127.0.0.1:5000")
    print("POST an audio file to /stt to get a transcript.")
    print("Press Ctrl+C or close the window to stop.")
    app.run(host="127.0.0.1", port=5000)