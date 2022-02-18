import os
import shutil
import subprocess
from pprint import pformat

from hllib.command_line import run
from hllib.genesis import Genesis
from hllib.key_storage import KeyStorage
from hllib.log import logger
from hllib.net import get_my_ip, download

ip = get_my_ip()
cpu_count = os.cpu_count() - 1

config = {
    "PUBLIC_IP": ip,
    "CONFIG": os.getenv('CONFIG', 'https://test.ton.org/ton-global.config.json'),
    "PRIVATE_CONFIG": os.getenv('PRIVATE_CONFIG', 'false') == 'true',
    "LITESERVER": os.getenv('LITESERVER', 'true') == 'true',  # convert to bool
    "CONSOLE_PORT": int(os.getenv("CONSOLE_PORT", 46732)),
    "PUBLIC_PORT": int(os.getenv("PUBLIC_PORT", 50001)),
    "DHT_PORT": int(os.getenv("DHT_PORT", 6302)),
    "LITESERVER_PORT": int(os.getenv("LITESERVER_PORT", 43680)),
    "NAMESPACE": os.getenv("NAMESPACE", None),
    "THREADS": int(os.getenv("CPU_COUNT", cpu_count)),
    "GENESIS": os.getenv("GENESIS", True),
    "VERBOSE": os.getenv("VERBOSE", 3)
}

logger.info("👋 Hi there!\n"
            f"My config:\n"
            f"<======= CONFIG 👻 =======>\n"
            f"{pformat(config)}\n"
            f"<======= END CONFIG 👻 =======>\n"
            f"Installing ton-full node\n")

if __name__ == "__main__":
    # First we need to download config of net
    config_path = '/tmp/config.json'
    db_path = '/var/ton-work/db'
    log_path = '/var/ton-work/log'
    hard_rewrite = False

    logger.info(f"Download config from 👾 [{config['CONFIG']}]")
    download(config['CONFIG'], config_path)

    if config['GENESIS']:
        logger.info(f"🧬 Run GENESIS 🧬")
        genesis = Genesis(db_path=db_path, config=config, config_path=config_path)
        genesis.run_genesis()
        hard_rewrite = True

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

    key_storage = KeyStorage(db_path=db_path, config=config)
    key_storage.init_console_client_keys(hard_rewrite)

    logger.info(f"All stuff with keys done! 🤴\n"
                f"I'll try to run full-node 4you 🤖")

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
