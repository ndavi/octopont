import socket
from artnet import packet, STANDARD_PORT, OPCODES, STYLE_CODES
import logging
import time
logging.basicConfig()
log = logging.getLogger(__name__)


class ArtNetSender():
    def __init__(self,address='192.168.1.26', port=STANDARD_PORT):
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
    i = 0
    artnetSender = ArtNetSender()
    while True:
        if(i == 254):
            i = 0
        artnetSender.packet.frame[1] = i
        artnetSender.packet.universe = 6
        i = i + 1
        time.sleep(0.01)
        print("send artnet")
        artnetSender.sendFrames()
