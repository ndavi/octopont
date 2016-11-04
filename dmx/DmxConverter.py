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
        self.effects = ["VEZERMOTOR", "STROBE"]
        self.configVezerSend = [100, 5, None] #[0] = Start Channel [1] = Nbr Channel
        self.configStrobeSend = [150,151]


    def setDmxArray(self,dmxArray):
        self.dmxArray = dmxArray
        self.convert()

    def convert(self):
        for effect in self.effects:
            if effect == "VEZERMOTOR":
                self.convertToVezerMotor()
            elif effect == "STROBE":
                self.convertToStrobeMsg()

    def convertToVezerMotor(self):
        for i in range (self.configVezerSend[0], self.configVezerSend[0] + self.configVezerSend[1]):
            if(self.dmxArray[i] == 255):
                if(self.configVezerSend[2] is not None and self.configVezerSend[2] != i):
                    strMsg = "/vezer/composition" + str(i - self.configVezerSend[2]) + "/start"
                    self.osc.sendDefault(strMsg, "MOTEURS", [i, self.dmxArray[i]])
                strMsg = "/vezer/composition" + str(i - self.configVezerSend[0]) + "/start"
                self.osc.sendDefault(strMsg, "MOTEURS", [i, self.dmxArray[i]])
                self.configVezerSend[2] = i

    def convertToStrobeMsg(self):
        strMsg = "/composition/video/effect9"
        target = "VIDEO"
        if(self.dmxArray[self.configStrobeSend[0]] == 0):
            values = [1]
            self.osc.sendDefault(strMsg, target,[self.configStrobeSend[0], self.dmxArray[self.configStrobeSend[0]]], values)
        elif(self.dmxArray[self.configStrobeSend[0]] == 255):
            values = [0]
            self.osc.sendDefault(strMsg, target, [self.configStrobeSend[0], self.dmxArray[self.configStrobeSend[0]]],values)
        values = [float(self.dmxArray[self.configStrobeSend[1]]) / float(255)]
        strMsg = "/composition/video/effect9/param1"
        self.osc.sendDefault(strMsg, "VIDEO",[self.configStrobeSend[1], self.dmxArray[self.configStrobeSend[1]]],values)


