import os
import shutil

from hllib.command_line import run
from hllib.key_storage import KeyStorage
from hllib.log import logger


class Genesis:
    def __init__(self, db_path: str, config: dict):
        self.db_path = db_path
        self.config = config

        self.key_storage = KeyStorage(db_path=db_path, config=config)

    def run_genesis(self):
        if 'keyring' not in os.listdir(self.db_path):
            os.mkdir(f'{self.db_path}/keyring')
        if 'keyring_pub' not in os.listdir(self.db_path):
            os.mkdir(f'{self.db_path}/keyring_pub')

        validator_key_hex, validator_key_b64 = self.key_storage.get_key(f'{self.db_path}/keyring/validator',
                                                                        store_to_keyring=True)
        logger.debug(f"🔑 Validator: b64: {validator_key_b64}, hex: {validator_key_hex}")

        with open(f"{self.db_path}/keyring_pub/{validator_key_hex}.pub", 'rb') as f:
            key_with_prefix = f.read()

        with open(f"/var/ton-work/contracts/validator-keys.pub", 'wb') as f:
            f.write(key_with_prefix[4:])

        run(['/var/ton-work/contracts/create-state', 'gen-zerostate.fif'], cwd="/var/ton-work/contracts/")

        with open(f"/var/ton-work/contracts/zerostate.fhash", 'rb') as f:
            zerostate_hex = f.read().hex().upper()

        logger.debug(f"✌ Zerostate: {zerostate_hex}")

        if 'static' not in os.listdir(self.db_path):
            os.mkdir(f'{self.db_path}/static')

        shutil.move('/var/ton-work/contracts/zerostate.boc', f'{self.db_path}/static/{zerostate_hex}')

        with open(f"/var/ton-work/contracts/basestate0.fhash", 'rb') as f:
            basestate0_hex = f.read().hex().upper()

        logger.debug(f"✌ basestate0: {basestate0_hex}")

        shutil.move('/var/ton-work/contracts/basestate0.boc', f'{self.db_path}/static/{basestate0_hex}')
