from typing import Optional

import requests


def get_my_ip() -> Optional[str]:
    response = requests.get("https://ifconfig.me")

    if response.status_code == 200:
        return response.content.decode()
