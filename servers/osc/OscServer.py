#!/usr/bin/python2

import logging
from liblo import *

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class OscServer(ServerThread):
    def __init__(self, port=7969):
        super(OscServer, self).__init__(port, UDP)
        self.log = logging.getLogger('octopont.oscserver')
        self.log.setLevel(logging.INFO)
        self.ready = True

    def start(self):
        self.log.info('Le service OSC demarre.')
        super(OscServer, self).start()

    def send(self, dst, msg):
        super(OscServer, self).send(Address(dst.get_hostname(), dst.get_port()), msg)

    def setConfig(self, c):
        for k, l in c:
            if k in ('feedback',):
                if k == 'feedback':
                    self.feedback = bool(*l)

    def getConfig(self):
        rtn = dict()
        rtn.update({'feedback', int(self.feedback), })

        return rtn
