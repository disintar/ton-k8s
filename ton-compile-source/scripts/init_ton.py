from hllib.log import logger
from hllib.net import get_my_ip
from hllib.udp_port_example import listen_ports

ip = get_my_ip()

logger.info("👋 Hi there!")
logger.info(f"My public ip is: {ip}")
logger.info("Will listen ports ;)")


class KeyStorage:
    def __init__(self):
        """
        We can run Docker locally or in k8s cluster
        If we use k8s cluster - we need to take care of public / private keys

        """
        pass


if __name__ == "__main__":
    listen_ports()
