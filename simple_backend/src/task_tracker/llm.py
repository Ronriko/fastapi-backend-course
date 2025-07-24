import os
from dotenv import load_dotenv
from base import BaseHTTPClient
import requests

load_dotenv()
CLOUDFLARE_URL = os.getenv("CLOUDFLARE_AI_URL")


class LLMClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(CLOUDFLARE_URL)

    def generate_solution(self, task_text: str) -> str:
        promt = f"Объясни, как решить задачу: {task_text}"
        payload = {"messages": [{"role": "user", "content": promt}]}
        return self.request("post", "", json=payload)

    def parse(self, response: requests.Response) -> str:
        data = response.json()
        return data.get("result", {}).get("response", "[Нет ответа от модели]")

    def default_headers(self) -> dict:
        return {"Content-Type": "application/json"}
