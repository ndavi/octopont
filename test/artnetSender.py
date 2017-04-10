import socket
from artnet import packet, STANDARD_PORT, OPCODES, STYLE_CODES
import logging
import time
logging.basicConfig()
log = logging.getLogger(__name__)


class ArtNetSender():
    def __init__(self,address='127.0.0.1', port=STANDARD_PORT):
        self.log = logging.getLogger('motherboard.artnet')
        self.address = address
        self.port = port
        self.log.info('Le service artnet est pret')
        self.packet = packet.DmxPacket()


    def sendFrames(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(self.packet.encode(), (self.address, self.port))

if __name__ == "__main__":
    artnetSender = ArtNetSender()
    artnetSender.packet.frame[1] = 200
    while True:
        time.sleep(1)
        print("send artnet")
        artnetSender.sendFrames()
