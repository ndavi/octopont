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
        self.configVezerSend = [102, 7] #[0] = Start Channel [1] = Nbr Channel
        self.lastValueChan = []
        for i in range(0, 254):
            self.lastValueChan.append(None)
        self.configStrobeSend = [119,120]


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
            doConvert = True
            if(self.lastValueChan[i] == None):
                self.lastValueChan[i] = self.dmxArray[i]
            elif(self.lastValueChan[i] == self.dmxArray[i]):
                doConvert = False
            else:
                self.lastValueChan[i] = self.dmxArray[i]
            if(doConvert):
                if(self.dmxArray[i] <= 150):
                    strMsg = "/vezer/composition" + str((i - self.configVezerSend[0]) + 1) + "/play"
                    self.osc.sendDefault(strMsg, "MOTEURS", [i + 1, self.dmxArray[i]], [0])
                    strMsg = "/Leds"+ str((i - self.configVezerSend[0]) + 1) +"/value"
                    self.osc.sendDefault(strMsg, "TABLETTE", [i + 1, self.dmxArray[i]], [0])
                elif (self.dmxArray[i] <= 255):
                    strMsg = "/vezer/composition" + str((i - self.configVezerSend[0]) + 1) + "/play"
                    self.osc.sendDefault(strMsg, "MOTEURS", [i + 1, self.dmxArray[i]], [1])
                    strMsg = "/Leds"+ str((i - self.configVezerSend[0]) + 1) +"/value"
                    self.osc.sendDefault(strMsg, "TABLETTE", [i + 1, self.dmxArray[i]], [1])

    def convertToStrobeMsg(self):
        doConvert1 = True
        if (self.lastValueChan[self.configStrobeSend[0]] == None):
            self.lastValueChan[self.configStrobeSend[0]] = self.dmxArray[self.configStrobeSend[0]]
        elif (self.lastValueChan[self.configStrobeSend[0]] == self.dmxArray[self.configStrobeSend[0]]):
            doConvert1 = False
        else:
            self.lastValueChan[self.configStrobeSend[0]] = self.dmxArray[self.configStrobeSend[0]]
        doConvert2 = True
        if (self.lastValueChan[self.configStrobeSend[1]] == None):
            self.lastValueChan[self.configStrobeSend[1]] = self.dmxArray[self.configStrobeSend[1]]
        elif (self.lastValueChan[self.configStrobeSend[1]] == self.dmxArray[self.configStrobeSend[1]]):
            doConvert2 = False
        else:
            self.lastValueChan[self.configStrobeSend[1]] = self.dmxArray[self.configStrobeSend[1]]

        strMsg = "/composition/video/effect1/bypassed"
        target = "VIDEO"
        if(self.dmxArray[self.configStrobeSend[0]] == 0 and doConvert1):
            values = [1]
            self.osc.sendDefault(strMsg, target,[self.configStrobeSend[0] + 1, self.dmxArray[self.configStrobeSend[0]]], values)
        elif(self.dmxArray[self.configStrobeSend[0]] == 255 and doConvert1):
            values = [0]
            self.osc.sendDefault(strMsg, target, [self.configStrobeSend[0] +1, self.dmxArray[self.configStrobeSend[0]]],values)
        if(doConvert2):
            values = [float(self.dmxArray[self.configStrobeSend[1]]) / float(255)]
            if(values[0] >= 0.99):
                values[0] = 0.99
            strMsg = "/composition/video/effect1/param1/values"
            self.osc.sendDefault(strMsg, "VIDEO",[self.configStrobeSend[1]+1, self.dmxArray[self.configStrobeSend[1]]],values)



