import ConfigParser
import logging

from sender import ArtNetSender

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class ArtNetToArtnet(object):

    def __init__(self, universe=1):
        self.log = logging.getLogger("artnetnetworkchanger")
        self.log.setLevel(logging.INFO)
        self.universe = universe
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()

    def changeNetwork(self, artnetArray):
        artnetSender = ArtNetSender(self.artNetIp)
        artnetSender.packet.frame = artnetArray
        artnetSender.sendFrames()

    def readConfig(self):
        self.config.read("" + '/config.cfg')
        self.artNetIp = self.config.get("SENDERIP", "ARTNETIP")
