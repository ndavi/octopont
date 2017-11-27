#!/usr/bin/python2
import ConfigParser
from liblo import *
import logging

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class FixtureMoteurs(object):

    def __init__(self, osc):
        self.dmxArray = None
        self.log = logging.getLogger("dmxtooscconverter")
        self.log.setLevel(logging.INFO)
        self.osc = osc
        self.config = ConfigParser.RawConfigParser()
        self.nbrMoteurs = self.config.get("CHANNELMOTEURS","NBRMOTEURS")
        self.channelMoteurs = []
        for i in range(0,self.nbrMoteurs):
            self.channelMoteurs.append(self.config.get("CHANNELMOTEURS","MOTEUR" + str(i)))

    def setDmxArray(self,dmxArray):
        self.dmxArray = dmxArray
        self.convert()

    def convert(self):
        for i in range(0,self.nbrMoteurs):
            channels = self.channelMoteurs[i]
            vitesse = self.dmxArray[channels[0]]
            position = self.dmxArray[channels[1]]
            messagePosition = "/m"+i+"PositionControl"
            messageVitesse = "/m"+i+"Speed"
            self.osc.sendDefault(messagePosition, "MOTEURS", [vitesse])
            self.osc.sendDefault(messageVitesse, "MOTEURS", [position])




