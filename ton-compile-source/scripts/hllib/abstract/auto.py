import subprocess
from subprocess import Popen
from threading import Thread
from time import sleep
from hllib.net import r
from hllib.command_line import run
from hllib.key_storage import KeyStorage
from hllib.log import logger


class AbstractAuto(Thread):
    def __init__(self, db_path: str, config: dict, config_path: str):
        logger.debug(f"Init AbstractAuto")
        super().__init__()
        self.db_path = db_path
        self.config = config
        self.config_path = config_path
        self.stake_amount = 10001

        logger.debug(f"Init KeyStorage")
        self.key_storage = KeyStorage(db_path=db_path, config=config, config_path=config_path)

        logger.debug(f"Init wallet seqno")
        self.wallet = int(r.get(f"{self.config['HTTP_CONFIG_SERVER']}/wallet").content.decode())
        logger.debug(f"💵 My wallet number is: {self.wallet}")

    def wait_while_server_ready(self):
        while True:
            get_status = self.lite_query('known')
            sleep(2)

            if 'BLK#2' in get_status:
                logger.info("🍟 Node is ready!")
                break
            else:
                logger.info(f"🌟 Node is not ready yet")

    def lite_query(self, command: str, parse: bool = False):
        answer = None
        while answer is None:
            try:
                answer = run(['lite-client', '-C', self.config_path, '-v', '0', '--timeout', '1', '-rc', command])
                logger.debug(answer)
            except subprocess.CalledProcessError as exc:
                logger.error(f"FATAL {exc.returncode} {exc.output}")
                sleep(2)

        if parse:
            answer = list(filter(lambda x: 'result:' in x, answer.split('\n')))[0] \
                         .replace('result:  [ ', '') \
                         .replace(' ]', '')[:-1]
        return answer
