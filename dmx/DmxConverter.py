#!/usr/bin/python2

from liblo import *
import logging

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class DmxConverter(object):

    def __init__(self, osc):
        self.dmxArray = None
        self.log = logging.getLogger("dmxconverter")
        self.log.setLevel(logging.INFO)
        self.osc = osc
        self.nbrConvertingList = 2
        self.effects = ["VEZERMOTOR", "STROBE"]
        self.configVezerSend = [100, 5, None] #[0] = Start Channel [1] = Nbr Channel
        self.configStrobeSend = [150,151]


    def setDmxArray(self,dmxArray):
        self.dmxArray = dmxArray
        self.convert()

    def convert(self):
        for i in range(0, self.nbrConvertingList):
            if self.effects[i] == "VEZERMOTOR":
                self.convertToVezerMotor()
            elif self.effects[i] == "STROBE":
                self.convertToStrobeMsg()

    def convertToVezerMotor(self):
        for i in range (self.configVezerSend[0], self.configVezerSend[0] + self.configVezerSend[1]):
            if(self.dmxArray[i] == 255):
                msg = Message("/vezer/composition" + str((i - self.configVezerSend[0])) + "/start")
                self.log.info("Convertion du channel " + str(i) + " a " + str(self.dmxArray[i]) + " en /vezer/composition" + str((i - self.configVezerSend[0])) + "/start")
                self.osc.sendDefault(msg)

    def convertToStrobeMsg(self):
        msg = Message("/composition/video/effect9")
        if(self.dmxArray[self.configStrobeSend[0]] == 0):
            msg.add(0)
            self.osc.sendDefault(msg)
        elif(self.dmxArray[self.configStrobeSend[0]] == 255):
            msg.add(1)
            self.osc.sendDefault(msg)
        valStrobe = (self.dmxArray[self.configStrobeSend[1]] / 255)
        msg = Message("/composition/video/effect9/param1")
        msg.add(valStrobe)
        self.osc.sendDefault(msg)


