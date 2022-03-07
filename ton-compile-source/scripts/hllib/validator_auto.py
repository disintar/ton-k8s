# TODO: use toncli
import subprocess
import traceback
from subprocess import Popen
from time import sleep

from hllib.abstract.auto import AbstractAuto
from hllib.command_line import run
from hllib.key_storage import KeyStorage
from hllib.log import logger
from threading import Thread

from hllib.net import get_my_ip


def address(subwallet: int):
    return int(f"0x{'1' * 64}", 16) - subwallet


class ValidatorAuto(AbstractAuto):
    def get_elector_address(self):
        config_1 = self.lite_query('getconfig 1')
        elector = config_1.split()[-1].replace('x{', '').replace('}', '')
        return f"-1:{elector}"

    def run(self):
        while True:
            try:
                logger.info(f"🙀  Wait while server start")
                # TODO: fix, try to get state automatically
                self.wait_while_server_ready()
                elector = self.get_elector_address()
                logger.info(f"🤓  Elector: {elector}")

                ip = get_my_ip('docker')
                sub_wallet_id = int(ip.split('.')[-1])
                my_address = f"-1:{format(address(sub_wallet_id), 'X')}"

                logger.info(f"👛  My sub wallet is: {sub_wallet_id};")
                logger.info(f"🐸  Address: {my_address};")

                seqno = self.lite_query(f'runmethod {my_address} seqno', True)
                logger.info(f"☣  Wallet seqno: {seqno}")

                logger.debug(f"🙈  Create recover-stake")
                command = ['fift', '-I', '/usr/local/lib/fift/lib/', '-s', '/var/ton-work/contracts/recover-stake.fif']
                logger.debug(' '.join(command))
                run(command, cwd='/tmp')

                logger.debug(f"🙈  Generate wallet-query.boc")
                command = ['fift', '-I', '/usr/local/lib/fift/lib/', '-s',
                           '/var/ton-work/network/wallet/valik-wallet.fif',
                           '/var/ton-work/network/wallet/valik.pk', 'Ef8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM0vF',
                           str(sub_wallet_id), str(seqno), '1', '-B', '/tmp/recover-query.boc']
                logger.debug(' '.join(command))
                run(command, cwd='/tmp')

                logger.debug(f"🙈  Send wallet-query.boc to net")
                self.lite_query('sendfile /tmp/wallet-query.boc')

                new_seqno = seqno

                while new_seqno == seqno:
                    new_seqno = self.lite_query(f'runmethod {my_address} seqno', True)
                    logger.debug(f"☣  New wallet seqno: {new_seqno}")

                    if new_seqno == seqno:
                        logger.debug("😴 Wait until seqno changes")
                    sleep(5)

                logger.info("🤪  Good news, recovery query was send!")

                election_timestamp = 0
                while election_timestamp == 0:
                    election_timestamp = int(self.lite_query(f'runmethod {elector} active_election_id', True))
                    logger.debug(f"🦻 election_timestamp: {election_timestamp}")

                    if election_timestamp == 0:
                        logger.debug("🤵 Elections not started yet. Wait...")
                        sleep(5)
                    else:
                        break

                # todo: get from config
                election_end = election_timestamp + 11

                logger.debug(f"🤵 Elections started: Start: {election_timestamp}; End: {election_end};")

                validator_command = ["validator-engine-console", "-k",
                                     f"{self.db_path}/keyring/client", "-p", f"{self.db_path}/keyring_pub/server.pub",
                                     "-v", "0", "-a", f"{self.config['PUBLIC_IP']}:{self.config['CONSOLE_PORT']}",
                                     "-rc"]
                logger.debug(" ".join(validator_command))

                key = run([*validator_command, 'newkey']).split()[-1]
                pub_key = run([*validator_command, f'exportpub {key}']).split()[-1]
                logger.info(f"🔐 Got keys: Key: {key}; Pub: {pub_key}")

                run([*validator_command, f'addpermkey {key} {election_timestamp} {election_end}'])
                run([*validator_command, f'addtempkey {key} {key} {election_end}'])

                adnl_key = run([*validator_command, 'newkey']).split()[-1]
                logger.info(f"🔐 Got adnl keys: Key: {adnl_key};")

                run([*validator_command, f'addadnl {adnl_key} 0'])
                run([*validator_command, f'addvalidatoraddr {key} {adnl_key} {election_end}'])

                logger.info(f"🔐 Key management done! Lets participate!")
                logger.info(f"Fift goes here")

                command = ['fift', '-I', '/usr/local/lib/fift/lib/', '-s',
                           '/var/ton-work/contracts/validator-elect-req.fif',
                           str(my_address), str(election_timestamp), str(10), str(adnl_key)]
                run(command, cwd='/tmp')

                with open('/tmp/validator-to-sign.bin', 'rb') as f:
                    message_hex = f.read().hex()

                command = [*validator_command, f'sign {key} {message_hex}']
                signature = run(command).split()[-1]

                logger.debug(f"🐬 Got signature for elections: {signature}")

                command = ['fift', '-I', '/usr/local/lib/fift/lib/', '-s',
                           '/var/ton-work/contracts/validator-elect-signed.fif',
                           str(my_address), str(election_timestamp), str(10), str(adnl_key), str(pub_key),
                           str(signature)]
                logger.debug(' '.join(command))

                run(command, cwd='/tmp')
                new_seqno = self.lite_query(f'runmethod {my_address} seqno', True)

                logger.debug(f"☣  New wallet seqno: {new_seqno}")

                logger.debug(f"🙈  Generate wallet-query.boc")
                command = ['fift', '-I', '/usr/local/lib/fift/lib/', '-s',
                           '/var/ton-work/network/wallet/valik-wallet.fif',
                           '/var/ton-work/network/wallet/valik.pk', 'Ef8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM0vF',
                           str(sub_wallet_id), str(new_seqno), f'{self.stake_amount}', '-B', '/tmp/validator-query.boc']

                run(command, cwd='/tmp')

                logger.debug(f"🙈  Send wallet-query.boc to net")
                self.lite_query('sendfile /tmp/wallet-query.boc')

                logger.debug("🐾 Success")

                new_election_timestamp = election_timestamp
                while election_timestamp == new_election_timestamp:
                    new_election_timestamp = int(self.lite_query(f'runmethod {elector} active_election_id', True))
                    logger.debug(f"🦻 New_election_timestamp: {new_election_timestamp}")

                    if election_timestamp == new_election_timestamp:
                        logger.debug("🤵 New elections not started yet. Wait...")
                        sleep(5)
                    else:
                        break
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
