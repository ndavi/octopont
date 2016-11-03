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
        self.feedbackPort = 7376
        self.address = Address("127.0.0.1",7376,1)

    def start(self):
        self.log.info('Le serveur OSC demarre.')
        super(OctoPontOSCServer, self).start()

    def sendDefault(self, msg):
        self.send(self.address, msg)

    @make_method(None, None)
    def defaultCallback(self, path, args, types, sender):
        self.log.warn('Unknown command: %s %s' % (path, ','.join([str(i) for i in args])))
