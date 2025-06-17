import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_message(self, user_id, content):
        payload = {"user_id": user_id, "content": content}
        return requests.post(f"{self.base_url}/messages", json=payload)