import base64
import os
import time

import requests

def genImage(prompt,index):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = "sk-KSvx3i62xF2JVdxR7pCaPkWlmFy1bS6k7f23ooJn8xCsuUCY"

    if api_key is None:
        raise Exception("Missing Stability API key.")

    # Construct the text_prompts list
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 10,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    for i, image in enumerate(data["artifacts"]):
        path = f"./out/v1_txt2img_{index}.png"
        with open(path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        print(path)
        time.sleep(10)
        return path

