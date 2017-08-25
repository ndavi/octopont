import array
from ola.ClientWrapper import ClientWrapper

from liblo import *
import logging
from test import ArtNetSender
logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class ArtNetToArtnet(object):

    def __init__(self, universe=1):
        self.log = logging.getLogger("artnetnetworkchanger")
        self.log.setLevel(logging.INFO)
        self.universe = universe


    def changeNetwork(self,artnetArray):
        artnetSender = ArtNetSender("2.0.0.69")
        artnetSender.packet.frame = artnetArray
        artnetSender.sendFrames()






