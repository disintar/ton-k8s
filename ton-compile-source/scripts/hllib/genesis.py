import json
import os
import shutil
import subprocess

from hllib.command_line import run
from hllib.key_storage import KeyStorage
from hllib.log import logger
import base64 as b
import struct
import socket
from pprint import pprint


def ip2int(addr: str):
    return struct.unpack("!i", socket.inet_aton(addr))[0]


class Genesis:
    def __init__(self, db_path: str, config: dict, config_path: str):
        self.db_path = db_path
        self.config = config
        self.config_path = config_path

        self.key_storage = KeyStorage(db_path=db_path, config=config, config_path=config_path)

    def run_genesis(self):
        for item in ['keyring', 'keyring_pub', 'import']:
            if item not in os.listdir(self.db_path):
                os.mkdir(f'{self.db_path}/{item}')

        if 'import' not in os.listdir(self.db_path):
            os.mkdir(f'{self.db_path}/import')

        validator_key_hex, validator_key_b64 = self.key_storage.get_key(f'{self.db_path}/keyring/validator',
                                                                        store_to_keyring=True)
        logger.debug(f"🔑  Validator: b64: {validator_key_b64}, hex: {validator_key_hex}")

        # save validator keys to other node
        if 'keyring' not in os.listdir('/var/ton-work/network'):
            os.mkdir('/var/ton-work/network/keyring')

        if 'keyring_pub' not in os.listdir('/var/ton-work/network'):
            os.mkdir('/var/ton-work/network/keyring_pub')

        shutil.copy(f"{self.db_path}/keyring/{validator_key_hex}", '/var/ton-work/network/keyring/')
        shutil.copy(f"{self.db_path}/keyring/validator", '/var/ton-work/network/keyring/')
        shutil.copy(f"{self.db_path}/keyring_pub/validator.pub", '/var/ton-work/network/keyring_pub/')

        with open(f"{self.db_path}/keyring_pub/{validator_key_hex}.pub", 'rb') as f:
            key_with_prefix = f.read()

        with open(f"/var/ton-work/contracts/validator-keys.pub", 'wb') as f:
            f.write(key_with_prefix[4:])

        run(['/var/ton-work/contracts/create-state', '-I', '/usr/local/lib/fift/lib', 'gen-zerostate.fif'],
            cwd="/var/ton-work/contracts/")

        with open(f"/var/ton-work/contracts/zerostate.fhash", 'rb') as f:
            zerostate_hex = f.read().hex().upper()

        logger.debug(f"✌  Zerostate: {zerostate_hex}")

        if 'static' not in os.listdir(self.db_path):
            os.mkdir(f'{self.db_path}/static')

        shutil.move('/var/ton-work/contracts/zerostate.boc', f'{self.db_path}/static/{zerostate_hex}')
        shutil.copy(f'{self.db_path}/static/{zerostate_hex}', f'{self.db_path}/import/{zerostate_hex}')

        with open(f"/var/ton-work/contracts/basestate0.fhash", 'rb') as f:
            basestate0_hex = f.read().hex().upper()

        logger.debug(f"✌  basestate0: {basestate0_hex}")

        shutil.move('/var/ton-work/contracts/basestate0.boc', f'{self.db_path}/static/{basestate0_hex}')
        shutil.copy(f'{self.db_path}/static/{basestate0_hex}', f'{self.db_path}/import/{basestate0_hex}')

        with open("/var/ton-work/contracts/zerostate.rhash", 'rb') as f:
            zerostate_rhash_b64 = b.b64encode(f.read()).decode()

        with open("/var/ton-work/contracts/zerostate.fhash", 'rb') as f:
            zerostate_fhash_b64 = b.b64encode(f.read()).decode()

        if 'dht-server' not in os.listdir(self.db_path):
            os.mkdir(f'{self.db_path}/dht-server')

        shutil.move(self.config_path, f'{self.db_path}/dht-server/example.json')

        run(['dht-server', '-C', f'{self.db_path}/dht-server/example.json', '-v', '5', '-D', '.', '-I',
             f'{self.config["PUBLIC_IP"]}:{self.config["DHT_PORT"]}'], cwd=f'{self.db_path}/dht-server')

        logger.debug(f"🧐 DHT server inited...")

        nodes_info = {
            "@type": "adnl.addressList",
            "addrs": [
                {
                    "@type": "adnl.address.udp",
                    "ip": ip2int(self.config['PUBLIC_IP']),
                    "port": self.config["DHT_PORT"]
                }
            ],
            "version": 0,
            "reinit_date": 0,
            "priority": 0,
            "expire_at": 0
        }

        key = os.listdir(f'{self.db_path}/dht-server/keyring')[0]
        dht_nodes = run([
            'generate-random-id', '-m', 'dht', '-k', f'{self.db_path}/dht-server/keyring/{key}', '-a',
            json.dumps(nodes_info)
        ], cwd=f'{self.db_path}/dht-server')

        dht_nodes = json.loads(dht_nodes)
        logger.debug(f"🧐 DHT Nodes json generated...")

        own_net_config = {
            "@type": "config.global",
            "dht": {
                "@type": "dht.config.global",
                "k": 3,
                "a": 3,
                "static_nodes": {
                    "@type": "dht.nodes",
                    "nodes": [dht_nodes]
                }
            },
            "validator": {
                "@type": "validator.config.global",
                "zero_state": {
                    "workchain": -1,
                    "shard": -9223372036854775808,
                    "seqno": 0,
                    "root_hash": zerostate_rhash_b64,
                    "file_hash": zerostate_fhash_b64
                },
                "init_block": {
                    "workchain": -1,
                    "shard": -9223372036854775808,
                    "seqno": 0,
                    "root_hash": zerostate_rhash_b64,
                    "file_hash": zerostate_fhash_b64
                }
            }
        }

        logger.debug(f"✍ Write config to {self.config_path}")
        pprint(own_net_config)

        with open(self.config_path, 'w') as config_file:
            json.dump(own_net_config, config_file)
