"""Simple example showing how to get gamepad events."""

from __future__ import print_function

import ConfigParser

from inputs import get_gamepad
import logging

from sender import ArtNetSender
logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class XinputToArtnetConveter(object):

    def __init__(self):
        self.keyMapping = {"BTN_SOUTH" : 0,
                  "BTN_WEST" : 1,
                  "BTN_NORTH" : 2,
                  "BTN_EAST" : 3,
                  "BTN_TL" : 4,
                  "BTN_TR" : 5,
                  "BTN_START" : 6,
                  "BTN_SELECT" : 7,
                  "BTN_THUMBL": 8,
                  "BTN_THUMBR" : 9
        }
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()
        self.artnetSender = ArtNetSender(self.artNetIp)
        self.artnetSender.packet.universe = self.senderUniverse
        self.start()

    def start(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type == "Key":
                    self.btnClicked(event)
                elif event.ev_type == "Absolute":
                    self.absoluteMoved(event)

    def btnClicked(self, e):
        if(e.state == 0):
            self.artnetSender.packet.frame[self.keyMapping[e.code]] = 0;
        elif(e.state == 1):
            self.artnetSender.packet.frame[self.keyMapping[e.code]] = 255;
        self.artnetSender.sendFrames()



    def absoluteMoved(self, e):
        if(e.code == "ABS_Y"):
            print(e.ev_type, e.code, e.state)

    def readConfig(self):
        self.config.read('config.cfg')
        self.artNetIp = self.config.get("SENDERIP","ARTNETIP")
        self.senderUniverse = int(self.config.get("SENDERIP","ARTNETUNIVERSE"))


if __name__ == "__main__":
    converter = XinputToArtnetConveter()

