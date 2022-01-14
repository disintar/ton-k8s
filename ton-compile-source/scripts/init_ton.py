import select
import socket

from lib.net import get_my_ip

ip = get_my_ip()


class KeyStorage:
    def __init__(self):
        """
        We can run Docker locally or in k8s cluster
        If we use k8s cluster - we need to take care of public / private keys

        """
        pass


sockets = {}

for port in [46731, 50000, 43679, 46732, 50001, 43680]:
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (ip, port)
    s.bind(server_address)
    sockets[port] = s

print("👋 Hi there!")
print(f"My ip is: {ip}")
print("Will listen ports ;)")

while True:
    for port, s in sockets.items():
        ready = select.select([s], [], [], 0.1)
        if ready[0]:
            data, address = s.recvfrom(4096)

            print(f"Server {port} received: ", data.decode('utf-8'))
            s.sendto("👋".encode('utf-8'), address)
