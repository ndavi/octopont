from ola.ClientWrapper import ClientWrapper
from time import sleep
import osc
import dmx
import logging
import signal
import sys
import traceback
import os

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')

class OctoPont(object):
    def __init__(self):
        self.workingDir = os.getcwd()
        self.setLogs()
        self.osc = osc.OctoPontOSCServer()
        self.dmxConverter = dmx.DmxConverter(self.osc)
        self.universe = 1


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

    def start(self):
        self.log.info('L\'octopont demarre')
        try:
            self.osc.start()
        except Exception, e:
            tb = traceback.format_exc()
            self.log.error(e.message + " \n" + tb)
            exit(1)
        return True

    def newData(self, data):
        self.dmxConverter.setDmxArray(data)

    def run(self):
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.RegisterUniverse(self.universe, client.REGISTER, self.newData)
        wrapper.Run()

    def runTest(self):
        while True:
            data = []
            for i in range(0,254):
                if (i == 151):
                    data.append(100)
                else:
                    data.append(0)
            self.dmxConverter.setDmxArray(data)
            sleep(1)

def signal_handler(signal, frame):
        usbDmx.log.info("Fermeture du l\'octopont")
        sys.exit(0)
if __name__ == "__main__":
    usbDmx = OctoPont()
    usbDmx.start()
    signal.signal(signal.SIGINT, signal_handler)
    usbDmx.runTest()
