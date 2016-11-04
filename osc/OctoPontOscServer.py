#!/usr/bin/python2

import OscServer as osc
from liblo import make_method, Address, Message
import sys
import logging

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class OctoPontOSCServer(osc.OscServer):
    def __init__(self, port=7969):
        super(OctoPontOSCServer, self).__init__(port)
        self.log = logging.getLogger('octopont.oscserver')
        self.log.setLevel(logging.INFO)
        self.feedback = False
        self.feedbackPort = 7333
        self.targets = {'MOTEURS': Address("127.0.0.1",self.feedbackPort,1), 'VIDEO':Address("127.0.0.1",self.feedbackPort,1)}
        self.address = Address("127.0.0.1",self.feedbackPort,1)

    def start(self):
        self.log.info('Le serveur OSC demarre.')
        super(OctoPontOSCServer, self).start()

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
