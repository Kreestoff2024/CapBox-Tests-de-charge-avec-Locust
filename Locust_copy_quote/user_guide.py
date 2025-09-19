from locust import HttpUser, task, between
from random import choice

class CapBoxUser(HttpUser):
    host = "https://api.capdevis.fr"
    wait_time = between(1, 3)  # plus réaliste qu'une constante fixe

    def on_start(self):
        """Connexion à CapBox à chaque démarrage de l'utilisateur"""
        response = self.client.post("/index.php?action=login", json={
            "loginId": "*********",
            "password": "*********"
        })

        if response.status_code != 200:
            print(f"[ERREUR] Connexion échouée: {response.status_code}")
        else:
            print("[INFO] Connexion réussie")

    @task
    def download_user_guide(self):
        # On simule une navigation avant le téléchargement
        self.client.get("/index.php?action=settings")

        # Téléchargement du fichier PDF
        with self.client.get(
            "/docs/notice_utilisation_cap_box.pdf",
            stream=True,
            name="notice_cap_box.pdf",
            catch_response=True
        ) as response:
            if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
                response.success()
            else:
                response.failure(f"Échec du téléchargement: {response.status_code} - {response.headers.get('Content-Type')}")

