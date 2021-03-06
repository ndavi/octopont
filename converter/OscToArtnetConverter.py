#!/usr/bin/python2
import ConfigParser
import logging
import signal
import threading
import time

from sender import ArtNetSender

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class OscToArtnetConverter(object):

    def __init__(self, osc):
        self.log = logging.getLogger("dmxtooscconverterr")
        self.log.setLevel(logging.INFO)
        self.osc = osc
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()
        self.oscThread = None
        self.running = True

    def sendTopDepart(self, addr, tags, stuff, source):
        self.log.info("Receiving TOP DEPART")
        artnetSender = ArtNetSender(self.artNetIp)
        artnetSender.packet.frame[0] = 255
        artnetSender.packet.universe = self.senderUniverse
        artnetSender.sendFrames()

    def sendTop(self, addr, tags, stuff, source):
        self.log.info("Received TOP")
        artnetSender = ArtNetSender(self.artNetIp)
        artnetSender.packet.universe = self.senderUniverse
        artnetSender.packet.frame[1] = 255
        artnetSender.sendFrames()

    def start(self):
        self.osc.s.addMsgHandler("/TopDepart", self.sendTopDepart)
        self.osc.s.addMsgHandler("/Top", self.sendTop)
        self.log.info("Receiver OSC activated")
        self.oscThread = threading.Thread(target=self.osc.s.serve_forever)
        self.oscThread.setDaemon(True)
        signal.signal(signal.SIGINT, self.closeThread)
        self.oscThread.start()
        while self.running:
            time.sleep(0.5)

    def closeThread(self, signal, frame):
        self.osc.s.close()
        self.running = False


    def readConfig(self):
        self.config.read("" + '/config.cfg')
        self.artNetIp = self.config.get("SENDERIP", "ARTNETIP")
        self.senderUniverse = int(self.config.get("SENDERIP", "ARTNETUNIVERSE"))
