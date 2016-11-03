#!/usr/bin/python2

from liblo import *
import logging

from osc import OctoPontOscServer
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class DmxConverter(object):

    def __init__(self, osc):
        self.dmxArray = None
        self.osc = osc


    def setDmxArray(self,dmxArray):
        self.dmxArray = dmxArray
        self.convert()

    def convert(self):
        msg = Message("/stage/test/config")
        msg.add(self.dmxArray[0])
        self.osc.sendDefault(msg)
