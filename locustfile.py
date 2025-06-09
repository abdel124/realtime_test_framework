from locust import HttpUser, task, between

class ChatUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def send_message(self):
        self.client.post("/api/message", json={"user_id": "u123", "content": "hi from locust"})
