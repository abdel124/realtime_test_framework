import httpx

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.client = httpx.Client(base_url=base_url)  # ✅ not AsyncClient

    def send_message(self, user_id: str, content: str):
        return self.client.post("/api/message", json={
            "user_id": user_id,
            "content": content
        })