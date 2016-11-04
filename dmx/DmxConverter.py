#!/usr/bin/python2

from liblo import *
import logging

from osc import OctoPontOscServer
logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class DmxConverter(object):

    def __init__(self, osc):
        self.dmxArray = None
        self.log = logging.getLogger("dmxconverter")
        self.log.setLevel(logging.INFO)
        self.osc = osc
        self.nbrConvertingList = 1
        self.effects = ["VEZERMOTOR"]
        self.configVezerSend = [100, 5] #[0] = Start Channel [1] = Nbr Channel


    def setDmxArray(self,dmxArray):
        self.dmxArray = dmxArray
        self.convert()

    def convert(self):
        for i in range(0, self.nbrConvertingList):
            if self.effects[i] == "VEZERMOTOR":
                self.convertToVezerMotor()

    def convertToVezerMotor(self):
        for i in range (self.configVezerSend[0], self.configVezerSend[0] + self.configVezerSend[1]):
            if(self.dmxArray[i] == 255):
                msg = Message("/vezer/composition" + str((i - self.configVezerSend[0])) + "/start")
                self.log.info("Convertion du channel " + str(i) + " a " + str(self.dmxArray[i]) + " en /vezer/composition" + str((i - self.configVezerSend[0])) + "/start")
                self.osc.sendDefault(msg)
