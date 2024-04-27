from locust import HttpUser, task, between

class MyUser(HttpUser):
    host="http://127.0.0.1:8080"
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks

    @task
    def contact(self):
        # Define the data for the POST request
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "webURL": "http://example.com",
            "text": "This is a test message"
        }
        # Send a POST request to the /contact endpoint
        self.client.post("/contact", data=data)
