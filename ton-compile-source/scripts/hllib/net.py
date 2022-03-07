from typing import Optional

import requests

from requests.adapters import HTTPAdapter, Retry

r = requests.Session()

retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 500, 502, 503, 504 ])

r.mount('http://', HTTPAdapter(max_retries=retries))
r.mount('https://', HTTPAdapter(max_retries=retries))


def get_my_ip(mode: str = 'internet') -> Optional[str]:
    """Return public IP address"""

    if mode == 'internet':
        response = r.get("https://ifconfig.me")

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
