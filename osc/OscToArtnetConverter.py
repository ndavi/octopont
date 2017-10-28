#!/usr/bin/python2
import threading
from liblo import *
import logging

from test import ArtNetSender

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class OscToArtnetConverter(object):

    def sendTopDepart(self,addr, tags, stuff, source):
        self.log.info("Receiving TOP DEPART")
        artnetSender = ArtNetSender("2.0.0.69")
        artnetSender.packet.frame[0] = 255
        artnetSender.packet.universe = 5
        artnetSender.sendFrames()

    def sendTop(self,addr, tags, stuff, source):
        self.log.info("Received TOP")
        artnetSender = ArtNetSender("2.0.0.69")
        artnetSender.packet.universe = 5
        artnetSender.packet.frame[1] = 255
        artnetSender.sendFrames()

    def __init__(self, osc):
        self.log = logging.getLogger("dmxtooscconverter")
        self.log.setLevel(logging.INFO)
        self.osc = osc

    def start(self):
        self.osc.s.addMsgHandler("/TopDepart", self.sendTopDepart)
        self.osc.s.addMsgHandler("/Top", self.sendTop)
        self.log.info("Receiver OSC activated")
        st = threading.Thread(target=self.osc.s.serve_forever)

        st.start()






