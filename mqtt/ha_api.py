import requests


class HAAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def get_state(self, entity_id):
        url = f"{self.base_url}/api/states/{entity_id}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        return None

    def call_service(self, domain, service, data):
        url = f"{self.base_url}/api/services/{domain}/{service}"
        r = requests.post(url, headers=self.headers, json=data)
        return r.status_code == 200
