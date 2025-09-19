import time
from locust import HttpUser, task, constant

class CapBoxUser(HttpUser):
    wait_time = constant(1)

    #connexion à CapBox
    def on_start(self):
        self.client.post("/login", json={"login":"*******", "password":"********"})

    #navigation sur pluieurs pages (Devis, Factures et Catalogues)
    @task
    def navigate_on_capbox(self):
        self.client.get("/https://www.capbox.fr/logiciel/index.php?action=c-quotes-list")
        time.sleep(2)
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-invoices-list")
        time.sleep(2)
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-catalogs-list")

    #sortie du site
    def on_stop(self):
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=logout")

        

