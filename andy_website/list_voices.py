import requests
import json

headers = {
    "Accept": "application/json",
    "xi-api-key": "sk_238fd2b3c3184adadcb8b4e3c34a017a78521b6d7a368569"
}

response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)

if response.status_code == 200:
    voices = response.json().get('voices', [])
    for voice in voices:
        print(f"Name: {voice['name']} | ID: {voice['voice_id']} | Labels: {voice.get('labels', {})}")
else:
    print(f"Error: {response.text}")
