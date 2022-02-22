import subprocess
from subprocess import Popen
from threading import Thread
from time import sleep

from hllib.command_line import run
from hllib.key_storage import KeyStorage
from hllib.log import logger


class AbstractAuto(Thread):
    def __init__(self, db_path: str, config: dict, config_path: str):
        super().__init__()
        self.db_path = db_path
        self.config = config
        self.config_path = config_path
        self.stake_amount = 10001

        self.key_storage = KeyStorage(db_path=db_path, config=config, config_path=config_path)

    def wait_while_server_ready(self):
        while True:
            get_status = Popen(args=['lite-client', '-C', self.config_path, '-v', '3', '-rc', 'known'],
                               stdout=subprocess.PIPE)
            stdout = get_status.communicate()[0].decode()
            sleep(2)

            if 'BLK#2' in stdout:
                logger.info("🍟 Node is ready!")
                break
            else:
                logger.info(f"🌟 Node is not ready yet")

    def lite_query(self, command: str, parse: bool = False):
        try:
            answer = run(['lite-client', '-C', self.config_path, '-v', '5', '-rc', command])
            logger.debug(answer)
        except subprocess.CalledProcessError as exc:
            logger.error(f"FATAL {exc.returncode} {exc.output}")
            raise exc

        if parse:
            answer = list(filter(lambda x: 'result:' in x, answer.split('\n')))[0] \
                         .replace('result:  [ ', '') \
                         .replace(' ]', '')[:-1]
        return answer
