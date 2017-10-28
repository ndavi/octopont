#!/usr/bin/python2
import OSC

import OscServer as osc
from liblo import make_method, Address, Message
import sys
import logging
import ConfigParser

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class OctoPontOSCServer(osc.OscServer):
    def __init__(self, port=7969):
        self.config = ConfigParser.RawConfigParser()
        super(OctoPontOSCServer, self).__init__(port)
        self.log = logging.getLogger('octopont.oscserver')
        self.log.setLevel(logging.INFO)
        self.readConfig()
        self.s = OSC.ThreadingOSCServer(self.receive_address)
        self.s.addDefaultHandlers()
        #self.feedbackPort = 7333

    def start(self):
        self.log.info('Le serveur OSC demarre.')
        super(OctoPontOSCServer, self).start()

    def readConfig(self):
        self.config.read('config.cfg')
        moteurs, portmoteurs = self.config.get("OSCTARGET","MOTEURS").split(":")
        video, portvideo = self.config.get("OSCTARGET","VIDEO").split(":")
        tablette, porttablette = self.config.get("OSCTARGET","TABLETTE").split(":")
        ipReceiveOsc, portIpReceiveOsc = self.config.get("RECEIVERIP","IPOSCRECEIVE").split(":")
        self.receive_address = ipReceiveOsc, portIpReceiveOsc
        self.targets = {'MOTEURS': Address(moteurs,portmoteurs,1), 'VIDEO':Address(video,portvideo,1), 'TABLETTE':Address(tablette,porttablette,1)}


    def sendDefault(self, strMsg, target, dmxinfos , args=[]):
        address = self.targets[target]
        self.log.info(
            "Convertion du channel " + str(dmxinfos[0]) + " a " + str(dmxinfos[1]) + " en "
            + strMsg + " args : " + str(args) + " a " + str(address.get_hostname()) + ":" + str(address.get_port()))
        msg = Message(strMsg)
        for arg in args:
            msg.add(arg)
        self.send(address, msg)

    @make_method(None, None)
    def defaultCallback(self, path, args, types, sender):
        self.log.warn('Unknown command: %s %s' % (path, ','.join([str(i) for i in args])))
