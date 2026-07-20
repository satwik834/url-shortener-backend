import random
import string
from locust import HttpUser, task, between

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class URLShortenerUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """
        Runs when a user starts. We will register a new user and login.
        """
        self.email = f"testuser_{random_string()}@example.com"
        self.password = "securepassword123!"
        self.token = ""
        self.short_codes = []

        # Register the user
        self.client.post("/register", json={
            "email": self.email,
            "password": self.password
        })
        
        # Login to get the access token
        login_response = self.client.post("/login", json={
            "email": self.email,
            "password": self.password
        })
        
        if login_response.status_code == 200:
            self.token = login_response.json().get("access_token")

    def _get_headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    @task(3)
    def test_shorten_url(self):
        """
        Test the /shorten endpoint by providing a long URL.
        """
        long_url = f"https://www.example.com/{random_string(15)}"
        response = self.client.post("/shorten", json={
            "long_url": long_url
        }, headers=self._get_headers())
        
        if response.status_code == 200:
            short_url = response.json().get("short_url")
            if short_url:
                self.short_codes.append(short_url)

    @task(2)
    def test_get_links(self):
        """
        Test the /links endpoint to fetch all links for the user.
        """
        self.client.get("/links", headers=self._get_headers())

    @task(4)
    def test_redirect(self):
        """
        Test the /{short_code} endpoint to redirect to the long URL.
        """
        if self.short_codes:
            short_code = random.choice(self.short_codes)
            # using allow_redirects=False to only test our endpoint's performance, not the external site's.
            self.client.get(f"/{short_code}", allow_redirects=False)

    @task(1)
    def test_delete_link(self):
        """
        Test the DELETE /{short_code} endpoint.
        """
        if self.short_codes:
            short_code = self.short_codes.pop()
            self.client.delete(f"/{short_code}", headers=self._get_headers())
