import array
from ola.ClientWrapper import ClientWrapper

from liblo import *
import logging

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class ArtNetToDMXConverter(object):

    def __init__(self, universe=1):
        self.log = logging.getLogger("artnetdmxconverter")
        self.log.setLevel(logging.INFO)
        self.universe = universe
        #self.wrapper = ClientWrapper()

    def DmxSent(self):
        self.wrapper.Stop()


    def convert(self,artnetArray):
        data = array.array('B')
        data.append(10)
        data.append(50)
        data.append(255)
        #client = self.wrapper.Client()
        #client.SendDmx(self.universe, data, self.DmxSent)
        #self.wrapper.Run()






