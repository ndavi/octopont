import ConfigParser
import logging;

from sender import ArtNetSender

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class DmxToArtnetConverter(object):

    def __init__(self):
        self.dmxArray = None
        self.log = logging.getLogger("dmxtooscconverter")
        self.log.setLevel(logging.INFO)
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()

    def convert(self, data):
        self.log.info("Received TOP")
        artnetSender = ArtNetSender(self.artNetIp)
        artnetSender.packet.universe = self.senderUniverse
        artnetSender.packet.frame = data
        artnetSender.sendFrames()

    def readConfig(self):
        self.config.read('config.cfg')
        self.artNetIp = self.config.get("SENDERIP", "ARTNETIP")
        self.senderUniverse = int(self.config.get("SENDERIP", "ARTNETUNIVERSE"))
