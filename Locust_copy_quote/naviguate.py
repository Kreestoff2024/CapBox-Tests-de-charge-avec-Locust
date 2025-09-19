from locust import HttpUser, task, between
from random import choice

class CapBoxUser(HttpUser):
    host = "https://api.capdevis.fr"
    wait_time = between(1, 3)  

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

    @task(5)
    def navigate_random_tab(self):
        """Navigation aléatoire dans les onglets de CapBox"""
        tabs = [
            "/index.php?action=contactsList",
            "/index.php?action=quotesList",
            "/index.php?action=invoicesList",
            "/index.php?action=depositsList",
            "/index.php?action=marginsList",
            "/index.php?action=ordersList",
            "/index.php?action=creditList",
            "/index.php?action=catalogList",
            "/index.php?action=settings"
        ]
        selected_tab = choice(tabs)
        response = self.client.get(selected_tab)
        if response.status_code != 200:
            print(f"[ERREUR] Échec d'accès à {selected_tab} - Code {response.status_code}")

    @task(1)
    def logout(self):
        """Déconnexion ou retour à l'écran de connexion"""
        response = self.client.get("/login")
        if response.status_code != 200:
            print(f"[ERREUR] Échec de redirection vers login - Code {response.status_code}")



   