import os
import requests
from dotenv import load_dotenv

load_dotenv()
CLOUDFLARE_URL = os.getenv("CLOUDFLARE_AI_URL")


class LLMClient:
    def __init__(self):
        self.url = CLOUDFLARE_URL
        self.headers = {"Content-Type": "application/json"}

    def generate_solution(self, task_text: str) -> str:
        promt = f"Объясни, как решить задачу: {task_text}"
        payload = {"messages": [{"role": "user", "content": promt}]}
        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("result", {}).get("response", "[Нет ответа от модели]")
