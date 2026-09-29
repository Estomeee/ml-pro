from locust import HttpUser, task, between
from tests.conftest import make_good_row


class PredictUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def predict(self):
        self.client.post(
            "/v1/predict",
            json=make_good_row(),
            timeout=10,
        )

    @task(1)
    def health(self):
        self.client.get("/health", timeout=10)
