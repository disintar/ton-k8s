import os
import shutil
import subprocess
import sys
from pprint import pformat

from hllib.command_line import run
from hllib.genesis import Genesis
from hllib.key_storage import KeyStorage
from hllib.log import logger
from hllib.net import get_my_ip, download

ip = get_my_ip(os.getenv('IP_GET_MODE', 'internet'))
cpu_count = os.cpu_count() - 1

config = {
    "PUBLIC_IP": os.getenv('PUBLIC_IP', ip),
    "CONFIG": os.getenv('CONFIG', 'https://test.ton.org/ton-global.config.json'),
    "PRIVATE_CONFIG": os.getenv('PRIVATE_CONFIG', 'false') == 'true',
    "LITESERVER": os.getenv('LITESERVER', 'true') == 'true',  # convert to bool
    "CONSOLE_PORT": int(os.getenv("CONSOLE_PORT", 46732)),
    "PUBLIC_PORT": int(os.getenv("PUBLIC_PORT", 50001)),
    "DHT_PORT": os.getenv("DHT_PORT", None),
    "LITESERVER_PORT": int(os.getenv("LITESERVER_PORT", 43680)),
    "NAMESPACE": os.getenv("NAMESPACE", None),
    "THREADS": int(os.getenv("CPU_COUNT", cpu_count)),
    "GENESIS": os.getenv("GENESIS", False) == 'true',
    "GENESIS_VALIDATOR": os.getenv("GENESIS_VALIDATOR", False) == 'true',
    "VERBOSE": os.getenv("VERBOSE", 3)
}

if config['DHT_PORT'] is not None:
    config['DHT_PORT'] = int(config['DHT_PORT'])

logger.info("👋 Hi there!\n"
            f"My config:\n"
            f"<======= CONFIG 👻 =======>\n"
            f"{pformat(config)}\n"
            f"<======= END CONFIG 👻 =======>\n"
            f"Installing ton-full node\n")

if __name__ == "__main__":
    # First we need to download config of net
    config_path = '/var/ton-work/network/config.json'

    if 'network' not in os.listdir("/var/ton-work/"):
        os.mkdir("/var/ton-work/network")

    db_path = '/var/ton-work/db'
    log_path = '/var/ton-work/log'
    hard_rewrite = False

    if not config['PRIVATE_CONFIG']:
        logger.info(f"Download config from 👾 [{config['CONFIG']}]")
        download(config['CONFIG'], config_path)
    else:
        logger.info(f"Will use 🧬 GENESIS 🧬 config")
        hard_rewrite = True

    if config['GENESIS']:
        files = os.listdir("/var/ton-work/network")

        if not os.path.exists(f'{db_path}/dht-server/') \
                or len(os.listdir(f'{db_path}/dht-server/')) < 1:
            logger.info(f"🧬 Run GENESIS process 🧬")
            genesis = Genesis(db_path=db_path, config=config, config_path=config_path)
            genesis.run_genesis()

        sys.exit(0)

    elif config['GENESIS_VALIDATOR']:
        logger.info(f"🧬 Run GENESIS VALIDATOR process 🧬")
        genesis = Genesis(db_path=db_path, config=config, config_path=config_path)
        genesis.setup_genesis_validator()

    elif config['DHT_PORT']:
        logger.info("🥂 Start DHT server...")
        # if StateInit already generated, just run dht server
        command = ['dht-server', '-C', config_path, '-D', '.', '-I',
                   f"{config['PUBLIC_IP']}:{config['DHT_PORT']}", '-v', str(config['VERBOSE'])]
        subprocess.run(command, cwd=f'{db_path}/dht-server/')

        sys.exit(0)

    #
    # Init config.json
    #

    logger.info(f"Download success, initializing validator-engine 🤓")

    if 'config.json' not in os.listdir(db_path):
        # Main command from https://ton.org/docs/#/howto/full-node?id=_5-initializing-the-local-configuration
        initializing_command = [f"/usr/local/bin/validator-engine",
                                "--global-config", f"{config_path}",
                                "--db", f"{db_path}",
                                "--ip", f"{config['PUBLIC_IP']}:{config['PUBLIC_PORT']}"]

        output = run(initializing_command)

        if 'config.json' in os.listdir(db_path):
            logger.info(f"Basic config successfully created! 😉\n"
                        f"Start key management process... 🔑")
        else:
            raise ValueError(f"✋ Can't create initial config file with {pformat(initializing_command)}")

    #
    # Create / use keys
    #

    key_storage = KeyStorage(db_path=db_path, config=config, config_path=config_path)
    key_storage.init_console_client_keys(hard_rewrite)

    logger.info(f"All stuff with keys done! 🤴\n"
                f"I'll try to run full-node 4you 🤖")

    if config['PRIVATE_CONFIG']:
        if 'keyring' in os.listdir('/var/ton-work/network'):
            for file in os.listdir('/var/ton-work/network/keyring'):
                shutil.copy(f'/var/ton-work/network/keyring/{file}', f"{db_path}/keyring/")

        if 'keyring_pub' in os.listdir('/var/ton-work/network'):
            for file in os.listdir('/var/ton-work/network/keyring_pub'):
                shutil.copy(f'/var/ton-work/network/keyring_pub/{file}', f"{db_path}/keyring_pub/")

    run_command = [f"/usr/local/bin/validator-engine",
                   "--global-config", f"{config_path}",
                   "--db", f"{db_path}",
                   "--threads", f"{config['THREADS']}",
                   "--state-ttl", "604800",
                   "--verbosity", f"{config['VERBOSE']}",
                   "--ip", f"{config['PUBLIC_IP']}:{config['PUBLIC_PORT']}"]
    subprocess.run(run_command)

else:
    logger.error("Can't download config, please do something 😩")

"""

read -r t1 t2 t3 NEW_NODE_KEY <<< $(echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "newkey"|tail -n 1)
read -r t1 t2 t3 NEW_VAL_ADNL <<< $(echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "newkey"|tail -n 1)

echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "addpermkey $VAL_ID_HEX 0 $(($(date +"%s")+31414590))" 2>&1
echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "addtempkey $VAL_ID_HEX $VAL_ID_HEX $(($(date +"%s")+31414590))" 2>&1
echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "addadnl $NEW_VAL_ADNL 0" 2>&1
echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "addadnl $VAL_ID_HEX 0" 2>&1

echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "addvalidatoraddr $VAL_ID_HEX $NEW_VAL_ADNL $(($(date +"%s")+31414590))" 2>&1
echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "addadnl $NEW_NODE_KEY 0" 2>&1
echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a  "$PUBLIC_IP:$CONSOLE_PORT" -rc "changefullnodeaddr $NEW_NODE_KEY" 2>&1
echo | validator-engine-console -k keyring/client -p keyring_pub/server.pub -v 0 -a "$PUBLIC_IP:$CONSOLE_PORT" -rc "importf keyring/$VAL_ID_HEX" 2>&1
"""
