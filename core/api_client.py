import httpx

class APIClient:
    def __init__(self, base_url):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def send_message(self, user_id, content):
        response = await self.client.post("/api/message", json={
            "user_id": user_id,
            "content": content
        })
        return response