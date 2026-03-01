import requests
import json

keys = [
    "sk_238fd2b3c3184adadcb8b4e3c34a017a78521b6d7a368569",
    "sk_3b59ac9a39e203d0df16d74294974833a997dca63964da85",
    "sk_e40ff8ea53cfe89881104be1e5b078213004a85132952dc9"
]

for key in keys:
    print(f"--- Trying key: {key[:10]}... ---")
    headers = {
        "Accept": "application/json",
        "xi-api-key": key
    }
    response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
    if response.status_code == 200:
        voices = response.json().get('voices', [])
        for voice in voices:
            # We want something young, maybe a 'Boy' or 'Youthful' label
            if 'young' in str(voice.get('labels', {})).lower() or 'boy' in str(voice.get('labels', {})).lower():
                print(f"Name: {voice['name']} | ID: {voice['voice_id']} | Labels: {voice.get('labels', {})}")
        break
    else:
        print(f"Failed: {response.status_code}")
