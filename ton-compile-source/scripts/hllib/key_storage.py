import json
import logging
import os
from typing import Tuple, List

from hllib.command_line import run


class KeyStorage:
    def __init__(self, db_path: str, config: dict):
        """
        We can run Docker locally or in k8s cluster
        If we use k8s cluster - we need to take care of public / private keys

        """
        self.db_path = db_path
        self.config = config

    def get_key(self, path: str, store_to_keyring: bool = False) -> Tuple[str, str]:
        """
        Create key pair and move key to db keyring if needed

        :param path: Where we need to create key
        :param store_to_keyring: Need to move private key to keyring?
        """

        key_hex, key_b64 = KeyStorage.generate_key('keys', path)

        if store_to_keyring:
            os.rename(path, f"{self.db_path}/keyring/{key_hex}")

        return key_hex, key_b64

    def init_console_client_keys(self):
        """
        Creates server / client keys, saves server key to keyring, add client key to config.json

        https://ton.org/docs/#/howto/full-node?id=_6-setting-up-remote-control-cli
        """

        # Check if keyring folder already exist and some keys contains in this folder
        if 'keyring' not in os.listdir(self.db_path) and len(os.listdir(f"{self.db_path}/keyring")) > 0:
            os.mkdir(f'{self.db_path}/keyring')
        else:
            logging.debug(f"🔒 Keyring folder already exist - so keys also")
            return

        server_key_hex, server_key_b64 = self.get_key(f'/tmp/server', store_to_keyring=True)
        logging.debug(f"🔑 Server: b64: {server_key_b64}, hex: {server_key_hex}")

        client_key_hex, client_key_b64 = self.get_key(f'/tmp/client')
        logging.debug(f"🔑 Client: b64: {client_key_b64}, hex: {client_key_hex}")

        liteserver_key_hex, liteserver_key_b64 = self.get_key(f'/tmp/liteserver', store_to_keyring=True)
        logging.debug(f"🔑 Liteserver: b64: {liteserver_key_b64}, hex: {liteserver_key_hex}")

        with open(f"{self.db_path}/config.json") as f:
            ton_config = json.load(f)

        # Add server key and client key (with specific CONSOLE_PORT) to control selection
        # Now we can access our server via validator-engine-console
        # validator-engine-console -k client -p server.pub -a <IP>:<CLIENT-PORT>

        ton_config['control'] = [{
            "id": server_key_b64,
            "port": self.config['CONSOLE_PORT'],
            "allowed": [
                {
                    "id": client_key_b64,
                    "permissions": 15
                }
            ]
        }]

        # If we need to add liteserver keys - we will do it! 😁
        # https://ton.org/docs/#/howto/full-node?id=_9-setting-up-the-full-node-as-a-lite-server
        if self.config['LITESERVER']:
            ton_config['liteservers'] = [
                {
                    "id": liteserver_key_b64,
                    "port": self.config['LITESERVER_PORT']
                }
            ]

        with open(f"{self.db_path}/config.json", "w") as f:
            json.dump(ton_config, f, indent=4)

    @staticmethod
    def generate_key(mode: str, path: str) -> Tuple[str, str]:
        """Runs ton generate-random-id
        Return HEX and base64 encode of public key
        """

        output: str = run(['generate-random-id', '-m', mode, '-n', path])
        output: List[str] = output.strip().split()

        if len(output) == 2:
            return output[0], output[1]

        raise ValueError(f"💬 generate-random-id returned WTF {output}")
