import ConfigParser
import logging

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')

#Artnet Usine Video Couleeeeeurs
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
        self.rgbFixtureOne = [self.config.get("CHANNELVIDEOCOULEURS", "R0"),
                             self.config.get("CHANNELVIDEOCOULEURS", "G0"),
                             self.config.get("CHANNELVIDEOCOULEURS", "B0")]
        self.rgbFixtureTwo = [self.config.get("CHANNELVIDEOCOULEURS", "R1"),
                             self.config.get("CHANNELVIDEOCOULEURS", "G1"),
                             self.config.get("CHANNELVIDEOCOULEURS", "B1")]

    def convert(self, artnetArray):
        framesToSend = []
        for i in range(2):
            framesToSend.append([0, 0, 0])
            offset = 0
            for p in range(3):
                framesToSend[i][p] = artnetArray.framedata[p + offset] / 255.0
            offset += 3

        self.osc.sendDefault(self.firstMessage, "VIDEO", framesToSend[0], framesToSend[0])
        self.osc.sendDefault(self.secondMessage, "VIDEO", framesToSend[1], framesToSend[1])