import select
import socket

from hllib.log import logger


def listen_ports():
    sockets = {}

    for port in [46731, 50000, 43679, 46732, 50001, 43680]:
        # Create a UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address = ("0.0.0.0", port)
        s.bind(server_address)
        sockets[port] = s

    while True:
        for port, s in sockets.items():
            ready = select.select([s], [], [], 0.1)
            if ready[0]:
                data, address = s.recvfrom(4096)

                logger.info(f"Server {port} received: ", data.decode('utf-8'))
                s.sendto("👋".encode('utf-8'), address)


if __name__ == "__main__":
    listen_ports()