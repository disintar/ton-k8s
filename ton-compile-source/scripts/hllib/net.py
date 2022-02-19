from typing import Optional

import requests


def get_my_ip(mode: str = 'internet') -> Optional[str]:
    """Return public IP address"""

    if mode == 'internet':
        response = requests.get("https://ifconfig.me")

        if response.status_code == 200:
            return response.content.decode()
    elif mode == 'docker':
        return open('/etc/hosts').read().split()[-2]


def download(url: str, path: str) -> bool:
    """
    Download file from url and save it locally

    :param url: http url to download from
    :param path: path to save file
    :return: bool - success or not
    """
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(path, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)
        return True
    return False
