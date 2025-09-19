from locust import HttpUser, task, between

class CapBoxUser(HttpUser):
    host = "https://api.capdevis.fr"
    wait_time = between(1, 3)

    def on_start(self):
        """Connexion à CapBox via API"""
        response = self.client.post(
            "/index.php?action=login",
            json={
                "loginId": "*********",
                "password": "*********"
            }
        )

        if response.status_code != 200:
            print(f"[ERREUR] Connexion échouée : {response.status_code}")
            print(response.text)
        else:
            print("[INFO] Connexion réussie")

    @task
    def test_something(self):
        """Action simple après connexion"""
        response = self.client.get("/index.php?action=quotesList")
        if response.status_code != 200:
            print(f"[ERREUR] Accès échoué : {response.status_code}")


