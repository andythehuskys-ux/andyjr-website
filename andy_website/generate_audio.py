import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "sk_238fd2b3c3184adadcb8b4e3c34a017a78521b6d7a368569"
}

data = {
    "text": "Ugh. I was sleeping. Look, I am a 2 month old puppy. Buy my coin, or don't... I literally just want to go back to sleep. Leave me alone.",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    with open('assets/andy_intro.mp3', 'wb') as f:
        f.write(response.content)
    print("Audio successfully generated and saved to assets/andy_intro.mp3")
else:
    print(f"Error: {response.text}")
