import ConfigParser

from ola.ClientWrapper import ClientWrapper
from artnetReceiver import ArtNetServer
from time import sleep
import osc
import dmx
import logging
import signal
import sys
import traceback
import os
import argparse
import threading

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')

class OctoPont(object):
    def __init__(self):
        self.workingDir = os.getcwd()
        self.setLogs()
        self.osc = osc.OctoPontOSCServer()
        self.dmxToOscConverter = dmx.DmxToOSCConverter(self.osc)
        self.dmxToArtnetConverter = dmx.DmxToArtnetConverter()
        self.artnetToDmxConverter = dmx.ArtNetToDMXConverter()
        self.artnetNetworkChanger = dmx.ArtNetToArtnet()
        self.oscToArtNetConverter = osc.OscToArtnetConverter(self.osc)
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()

    def readConfig(self):
        self.config.read('config.cfg')
        self.receiveUniverse = int(self.config.get("RECEIVERIP","DMXUNIVERSE"))



    def setLogs(self):
        self.log = logging.getLogger('octopont')
        logFormat = logging.Formatter('%(asctime)s %(name)s - %(levelname)s: %(message)s')
        self.log.setLevel(logging.INFO)
        self.filelog = logging.FileHandler(os.path.join(self.workingDir, './log/octopont.log'))
        self.filelog.setLevel(logging.INFO)
        self.filelog.setFormatter(logFormat)
        self.log.addHandler(self.filelog)
        self.debuglog = logging.FileHandler(os.path.join(self.workingDir, './log/octopont.debug.log'))
        self.debuglog.setLevel(logging.DEBUG)
        self.debuglog.setFormatter(logFormat)
        self.log.addHandler(self.debuglog)

    def oscStart(self):
        try:
            self.osc.start()
        except Exception, e:
            tb = traceback.format_exc()
            self.log.error(e.message + " \n" + tb)
            exit(1)
        return True

    def newDmxToOscData(self, data):
        self.dmxToOscConverter.setDmxArray(data)

    def newArtNetData(self, data):
        self.artnetToDmxConverter.convert(data.framedata)

    def newArtNetDataNetworkChange(self, data):
        result = int(data.framedata[1] * 2.5)
        if(result <= 255):
            data.framedata[1] = result
        else:
            data.framedata[1] = 255
        self.artnetNetworkChanger.changeNetwork(data.framedata)

    def newDmxToArtnetData(self,data):
        self.dmxToArtnetConverter.convert(data)

    def runDmxToOsc(self):
        self.oscStart()
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.RegisterUniverse(self.receiveUniverse, client.REGISTER, self.newDmxToOscData)
        wrapper.Run()

    def runArtNetToDmx(self):
        artNetReceiver = ArtNetServer()
        artNetReceiver.run(self.newArtNetData)

    def runArtNetToOtherNetwork(self):
        artNetReceiver = ArtNetServer()
        artNetReceiver.run(self.newArtNetDataNetworkChange)

    def runOscToArtNet(self):
        self.oscToArtNetConverter.start()

    def runDmxToArtnet(self):
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.RegisterUniverse(self.receiveUniverse, client.REGISTER, self.newDmxToArtnetData)
        wrapper.Run()

    def runTest(self):
        while True:
            data = []
            for i in range(0,254):
                if (i == 100):
                    data.append(255)
                else:
                    data.append(0)
            self.dmxToOscConverter.setDmxArray(data)
            sleep(1)

def signal_handler(signal, frame):
        usbDmx.log.info("Fermeture de l\'octopont")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--artnetdmx', help='Lancement du programme en mode pont artnet -> dmx', action='store_true')
    parser.add_argument('--dmxosc', help='Lancement du programme en mode pont convertisseur dmx -> osc', action='store_true')
    parser.add_argument('--artnetchanger', help='Lancement du programme en mode pont routeur artnet -> artnet', action='store_true')
    parser.add_argument('--osctoartnet', help='Lancement du programme en mode pont routeur osc -> artnet', action='store_true')
    parser.add_argument('--node', help='Lancement du programme en mode node', action='store_true')
    args = parser.parse_args()
    usbDmx = OctoPont()
    if(args.artnetdmx):
        usbDmx.log.info('L\'octopont demarre en mode pont artnet -> dmx')
        usbDmx.runArtNetToDmx()
    elif(args.node):
        usbDmx.log.info('L\'octopont demarre en mode node')
        threading.Thread(target=usbDmx.runDmxToArtnet).start()
        usbDmx.runArtNetToDmx()
    elif(args.artnetchanger):
        usbDmx.log.info('L\'octopont demarre en mode pont artnet -> artnet')
        usbDmx.runArtNetToOtherNetwork()
    elif (args.osctoartnet):
        usbDmx.log.info('L\'octopont demarre en mode pont osc -> artnet')
        usbDmx.runOscToArtNet()
    else:
        usbDmx.log.info('L\'octopont demarre en mode convertisseur dmx -> osc')
        usbDmx.runDmxToOsc();
    signal.signal(signal.SIGINT, signal_handler)
