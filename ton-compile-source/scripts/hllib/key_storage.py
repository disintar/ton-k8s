import json
import logging
import os
from base64 import b64encode
from typing import Tuple

import ed25519
from ed25519 import SigningKey, VerifyingKey


class KeyStorage:
    def __init__(self, db_path: str, config: dict):
        """
        We can run Docker locally or in k8s cluster
        If we use k8s cluster - we need to take care of public / private keys

        """
        self.db_path = db_path
        self.config = config

    def get_key(self, key_name: str, store_to_keyring: bool = False) -> Tuple[SigningKey, VerifyingKey]:
        """
        Create key pair and move key to db keyring if needed

        :param path: Where we need to create key
        :param store_to_keyring: Need to move private key to keyring?
        """

        signing_key, verifying_key = KeyStorage.generate_key()

        if store_to_keyring:
            private_hex = signing_key.to_ascii(encoding='hex').decode()
            private_bytes = signing_key.to_bytes()

            with open(f"{self.db_path}/keyring/{private_hex.upper()}", "wb") as f:
                f.write(private_bytes)

        return signing_key, verifying_key

    def init_console_client_keys(self):
        """
        Creates server / client keys, saves server key to keyring, add client key to config.json

        https://ton.org/docs/#/howto/full-node?id=_6-setting-up-remote-control-cli
        """

        # Check if keyring folder already exist and some keys contains in this folder
        if 'keyring' not in os.listdir(self.db_path):
            os.mkdir(f'{self.db_path}/keyring')
        elif len(os.listdir(f"{self.db_path}/keyring")) == 0:
            logging.debug(f"🔒 Keyring folder already exist, but no keys found, so continue")
        else:
            logging.debug(f"🔒 Keyring folder already exist - so keys also")
            return

        #
        # Server key
        #
        server_signing_key, server_verifying_key = self.get_key('server', store_to_keyring=True)
        server_verifying_key_base64 = b64encode(server_verifying_key.to_bytes()).decode()

        logging.debug(f"🔑 Server: b64: {server_verifying_key_base64}")

        #
        # Client key
        #
        client_signing_key, client_verifying_key = self.get_key('client')
        client_verifying_key_base64 = b64encode(client_verifying_key.to_bytes()).decode()

        logging.debug(f"🔑 Client: b64: {client_verifying_key_base64}")

        #
        # Liteserver key
        #
        liteserver_signing_key, liteserver_verifying_key = self.get_key('liteserver', store_to_keyring=True)
        liteserver_verifying_key_base64 = b64encode(liteserver_verifying_key.to_bytes()).decode()

        logging.debug(f"🔑 Liteserver: b64: {liteserver_verifying_key_base64}")
        with open(f"{self.db_path}/config.json") as f:
            ton_config = json.load(f)

        # Add server key and client key (with specific CONSOLE_PORT) to control selection
        # Now we can access our server via validator-engine-console
        # validator-engine-console -k client -p server.pub -a <IP>:<CLIENT-PORT>

        ton_config['control'] = [{
            "id": server_verifying_key_base64,
            "port": self.config['CONSOLE_PORT'],
            "allowed": [
                {
                    "id": client_verifying_key_base64,
                    "permissions": 15
                }
            ]
        }]

        # If we need to add liteserver keys - we will do it! 😁
        # https://ton.org/docs/#/howto/full-node?id=_9-setting-up-the-full-node-as-a-lite-server
        if self.config['LITESERVER']:
            ton_config['liteservers'] = [
                {
                    "id": liteserver_verifying_key_base64,
                    "port": self.config['LITESERVER_PORT']
                }
            ]

        with open(f"{self.db_path}/config.json", "w") as f:
            json.dump(ton_config, f, indent=4)

    @staticmethod
    def generate_key():
        # similar to generate-random-id
        # https://github.com/newton-blockchain/ton/blob/9875f02ef4ceba5b065d5e63c920f91aec73224e/utils/generate-random-id.cpp#L102
        signing_key, verifying_key = ed25519.create_keypair()
        return signing_key, verifying_key
