import ConfigParser
import logging

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class ArtNetToOSCConverter(object):

    def __init__(self, osc):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.osc = osc
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()
        self.firstMessage = "/color/light/1"
        self.secondMessage = "/color/light/2"

    def readConfig(self):
        self.config.read('config.cfg')

    def convert(self, artnetArray):
        firstMessageValues = [
            artnetArray.framedata[0],
            artnetArray.framedata[1],
            artnetArray.framedata[2]
        ]
        secondMessageValues = [
            artnetArray.framedata[3],
            artnetArray.framedata[4],
            artnetArray.framedata[5]
        ]
        self.osc.sendDefault(self.firstMessage, "VIDEO", firstMessageValues, firstMessageValues)
        self.osc.sendDefault(self.secondMessage, "VIDEO", secondMessageValues, secondMessageValues)