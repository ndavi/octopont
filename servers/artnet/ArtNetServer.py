import ConfigParser
import logging
import socket
import threading
import time

from artnet import packet, STANDARD_PORT, STYLE_CODES

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class ArtNetServer(threading.Thread):
    def __init__(self, address="127.0.0.1", nodaemon=False, runout=False):
        super(ArtNetServer, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.log = logging.getLogger("artnetserver")
        self.log.setLevel(logging.INFO)

        self.sock.bind(('', STANDARD_PORT))
        self.sock.settimeout(0.0)

        self.broadcast_address = '<broadcast>'
        self.last_poll = 0
        self.address = address
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()

        self.nodaemon = nodaemon
        self.daemon = not nodaemon
        self.running = True

        self.data_callback = None

    def readConfig(self):
        self.config.read('config.cfg')
        self.address = self.config.get("RECEIVERIP", "ARTNETIP")

    def run(self, data_callback):
        self.data_callback = data_callback
        self.log.info("Lancemenent du serveur artnetReceiver")
        while (self.running):
            self.handle_artnet()

    def read_artnet(self):
        try:
            data, addr = self.sock.recvfrom(1024)
        except socket.error, e:
            time.sleep(0.1)
            return None

        return packet.ArtNetPacket.decode(addr, data)

    def handle_artnet(self):
        if (time.time() - self.last_poll >= 4):
            self.last_poll = time.time()
            self.send_poll()

        artNetData = self.read_artnet()
        if (artNetData is None or not hasattr(artNetData, "framedata")):
            return

        self.log.info("Conversion d'une trame artnet : " + str(artNetData.framedata))
        self.data_callback(artNetData)

    def send_dmx(self, frame, universe=0):
        p = packet.DmxPacket(frame, universe=universe)
        self.sock.sendto(p.encode(), (self.address, STANDARD_PORT))

    def send_poll(self):
        p = packet.PollPacket(address=self.broadcast_address)
        # TODO : See what this line crash when IP is loopback

    #        self.sock.sendto(p.encode(), (p.address, STANDARD_PORT))

    def send_poll_reply(self, poll):
        ip_address = socket.gethostbyname(socket.gethostname())
        style = STYLE_CODES['StNode'] if isinstance(self, ArtNetServer) else STYLE_CODES['StController']

        r = packet.PollReplyPacket(address=self.broadcast_address)
        r.style = style

        log.debug("send: %s" % r)

        self.sock.sendto(r.encode(), (r.address, STANDARD_PORT))
