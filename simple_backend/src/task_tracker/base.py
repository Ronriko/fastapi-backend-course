import requests
from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {**self.default_headers(), **kwargs.pop("headers", {})}
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code == 404:
            return self.handle_404(response)
        response.raise_for_status()
        return self.parse(response)

    @abstractmethod
    def parse(self, response: requests.Response):
        """Как парсить ответ конкретного API (json → нужный тип)."""
        pass

    @abstractmethod
    def default_headers(self) -> dict:
        """Заголовки по умолчанию для клиента."""
        pass

    def handle_404(self, response: requests.Response):
        """Поведение при 404. Можно переопределить в наследниках."""
        return {"error": "Not found"}
