#!/usr/bin/python2
import ConfigParser
import logging

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class FixtureMoteurs(object):

    def __init__(self, osc, workingDir):
        self.dmxArray = None
        self.log = logging.getLogger("dmxtooscconverter")
        self.log.setLevel(logging.INFO)
        self.osc = osc
        self.config = ConfigParser.RawConfigParser()
        self.config.read(workingDir + '/config.cfg')
        self.nbrMoteurs = self.config.get("CHANNELMOTEURS", "NBRMOTEURS")
        self.channelMoteurs = []
        for i in range(0, int(self.nbrMoteurs)):
            self.channelMoteurs.append(self.config.get("CHANNELMOTEURS", "MOTEUR" + str(i)).split(','))

    def setDmxArray(self, dmxArray):
        self.dmxArray = dmxArray
        self.convert(dmxArray)

    def convert(self, dmxArray):
        self.dmxArray = dmxArray
        for i in range(0, int(self.nbrMoteurs)):
            channels = self.channelMoteurs[i]
            position = self.dmxArray.framedata[int(channels[0])]
            position = (position / 2.55) / 100
            vitesse = self.dmxArray.framedata[int(channels[1])]
            vitesse = (vitesse / 2.55) / 100
            messagePosition = "/m" + str(i) + "PositionControl"
            messageVitesse = "/m" + str(i) + "Speed"
            self.osc.sendDefault(messageVitesse, "MOTEURS", None, [vitesse])
            self.osc.sendDefault(messagePosition, "MOTEURS", None, [position])
