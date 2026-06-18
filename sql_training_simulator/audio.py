from __future__ import annotations

import base64
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def lesson_to_audio(text: str) -> dict[str, Any]:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    if not api_key:
        return {
            "ok": False,
            "message": "ElevenLabs is optional. Add ELEVENLABS_API_KEY to your .env file to enable lesson audio."
        }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text[:4500],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    response = requests.post(url, json=payload, headers=headers, timeout=45)
    if response.status_code >= 400:
        return {"ok": False, "message": f"ElevenLabs request failed: {response.status_code} {response.text[:200]}"}

    encoded = base64.b64encode(response.content).decode("utf-8")
    return {"ok": True, "audio_base64": encoded, "mime_type": "audio/mpeg"}
