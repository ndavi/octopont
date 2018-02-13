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
        self.frameToSendFirstMessage = [0,0,0]
        self.frameToSendSecondMessage = [0,0,0]

    def readConfig(self):
        self.config.read('config.cfg')

    def convert(self, artnetArray):
        if artnetArray.framedata[0] != 0:
            self.frameToSendFirstMessage[0] = artnetArray.framedata[0] / 255.0
        if artnetArray.framedata[1] != 0:
            self.frameToSendFirstMessage[1] = artnetArray.framedata[1] / 255.0
        if artnetArray.framedata[2] != 0:
            self.frameToSendFirstMessage[2] = artnetArray.framedata[2] / 255.0

        if artnetArray.framedata[3] != 0:
            self.frameToSendSecondMessage[0] = artnetArray.framedata[3] / 255.0
        if artnetArray.framedata[4] != 0:
            self.frameToSendSecondMessage[1] = artnetArray.framedata[4] / 255.0
        if artnetArray.framedata[5] != 0:
            self.frameToSendSecondMessage[2] = artnetArray.framedata[5] / 255.0

        self.osc.sendDefault(self.firstMessage, "VIDEO", self.frameToSendFirstMessage, self.frameToSendFirstMessage)
        self.osc.sendDefault(self.secondMessage, "VIDEO", self.frameToSendSecondMessage, self.frameToSendSecondMessage)