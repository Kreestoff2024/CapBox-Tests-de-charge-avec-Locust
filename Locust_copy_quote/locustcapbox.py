import time
from locust import HttpUser, task, constant

class CapBoxUser(HttpUser):
    wait_time = constant(1)

    #connexion à CapBox
    def on_start(self):
        self.client.post("/login", json={"loginId":"*********", "password":"*********"})

    @task(2)
    def navigate_invoice_tabs(self):
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-invoices-list")
        time.sleep(2)
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-deposits-list")
        time.sleep(2)
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-credits-list")

    @task
    def copy_quote(self):
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-quotes-list")
        time.sleep(2)
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-quote&dup=21903")
        time.sleep(2)
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=c-quote&dup=21903#")

    @task
    def disconnect(self):
        self.client.get("https://www.capbox.fr/logiciel/index.php?action=logout")