from locust import HttpUser, task, between

class HealthSystemUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        # Login
        self.client.post("/login/", {
            "username": "test@example.com",
            "password": "testpassword123"
        })
    
    @task(3)
    def view_dashboard(self):
        self.client.get("/")
    
    @task(2)
    def view_clients(self):
        self.client.get("/clients/")
    
    @task
    def view_programs(self):
        self.client.get("/programs/")
        
    @task
    def search_clients(self):
        self.client.get("/clients/?search=John")