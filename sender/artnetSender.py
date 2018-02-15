import logging
import socket
import time

from artnet import packet, STANDARD_PORT

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class ArtNetSender():
    def __init__(self, address='2.0.0.9', port=STANDARD_PORT):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.address = address
        self.port = port
        self.log.info('Le service artnet est pret')
        self.packet = packet.DmxPacket()

    def sendFrames(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(self.packet.encode(), (self.address, self.port))

    def sendFramesWithLog(self):
        self.log.info("Sending " + str(self.packet.frame))
        self.sendFrames()


if __name__ == "__main__":
    i = 0
    artnetSender = ArtNetSender()
    while True:
        if (i == 254):
            i = 0
        artnetSender.packet.frame[1] = i
        artnetSender.packet.universe = 6
        i = i + 1
        time.sleep(0.01)
        print("send artnet")
        artnetSender.sendFrames()
