
from __future__ import print_function

import ConfigParser
import logging

from inputs import UnpluggedError
from inputs import get_gamepad

from sender import ArtNetSender

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')

MAX_JOYSTICK_VALUE_RIGHT = 32767.0
MAX_JOYSTICK_VALUE_LEFT = 32768.0


class XinputToArtnetConverter(object):

    def __init__(self):
        self.log = logging.getLogger("dmxtooscconverter")
        self.log.setLevel(logging.INFO)
        self.keyMapping = {"BTN_SOUTH": 0,  # Croix
                           "BTN_WEST": 1,  # Triangle
                           "BTN_NORTH": 2,  # Carre
                           "BTN_EAST": 3,  # Rond
                           "BTN_TL": 4,  # L1
                           "BTN_TR": 5,  # R1
                           "BTN_START": 6,  # Start
                           "BTN_SELECT": 7,  # Select
                           "BTN_THUMBL": 8,  # Click Joystick Gauche
                           "BTN_THUMBR": 9,  # Click Joystick Droit
                           "ABS_RZ": 10,  # R2
                           "ABS_Z": 11,  # L2
                           "ABS_X_LEFT": 12,  # Joystick gauche a gauche
                           "ABS_X_RIGHT": 13,  # Joystick gauche a droite
                           "ABS_Y_LEFT": 14,  # Joystick gauche en haut
                           "ABS_Y_RIGHT": 15,  # Joystick gauche en bas
                           "ABS_RX_LEFT": 16,  # Joystick droite a gauche
                           "ABS_RX_RIGHT": 17,  # Joystick droite a droite
                           "ABS_RY_LEFT": 18,  # Joystick droite en haut
                           "ABS_RY_RIGHT": 19,  # Joystick droite en bas
                           "ABS_HAT0Y_LEFT": 20,  # Fleche haut
                           "ABS_HAT0Y_RIGHT": 21,  # Fleche bas
                           "ABS_HAT0X_LEFT": 22,  # Fleche gauche
                           "ABS_HAT0X_RIGHT": 23,  # Fleche droite
                           "BTN_MODE": 24,  # Bouton du milieu
                           }
        self.joysticksCode = [
            "ABS_X", "ABS_Y",
            "ABS_RX", "ABS_RY",
        ]
        self.YJoystick = [
            "ABS_Y", "ABS_RY"
        ]
        self.backButtons = [
            "ABS_RZ", "ABS_Z"
        ]
        self.leftButtonsCode = [
            "ABS_HAT0Y", "ABS_HAT0X"
        ]
        self.config = ConfigParser.RawConfigParser()
        self.readConfig()
        self.artnetSender = ArtNetSender(self.artNetIp)
        self.artnetSender.packet.universe = self.senderUniverse
        self.start()

    def start(self):
        self.log.info("Le recepteur Xinput est pret")
        while True:
            try:
                events = get_gamepad()
                self.getInputs(events)
            except UnpluggedError, err:
                self.log.error(err.message)
                exit(200)
            except IOError, err:
                self.log.error("Gamepad disconnected " + err.message)
                exit(201)
            except KeyError, err:
                self.log.error("Le gamepad n'est pas dans le bon mode ; reception de : " + err.message)
                exit(202)

    def getInputs(self, events):
        for event in events:
            if event.ev_type == "Key":
                self.btnClicked(event)
            elif event.ev_type == "Absolute":
                self.absoluteMoved(event)
        if not (len(events) == 1 and events[0].ev_type == "Sync"):
            self.artnetSender.sendFramesWithLog()

    def btnClicked(self, e):
        if e.state == 0:
            self.artnetSender.packet.frame[self.keyMapping[e.code]] = 0
        elif e.state == 1:
            self.artnetSender.packet.frame[self.keyMapping[e.code]] = 255

    def absoluteMoved(self, e):
        if e.code in self.backButtons:
            self.sendBackButtons(e)
        elif e.code in self.joysticksCode:
            self.sendJoysticks(e)
        elif e.code in self.leftButtonsCode:
            self.leftButtonsClicked(e)

    def leftButtonsClicked(self, e):
        if e.state == 0:
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = 0
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = 0
        elif e.state == 1:
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = 255
        elif e.state == -1:
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = 255

    def sendJoysticks(self, e):
        if e.state == 255 and e.code in self.YJoystick:
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = 0
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = 0
        elif e.state == 0:
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = 0
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = 0
        # Go to right
        elif e.state > 0:
            dmxToSend = int((e.state / MAX_JOYSTICK_VALUE_RIGHT) * 255)
            dmxToSend = self.checkDmxToSend(dmxToSend, e)
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = dmxToSend
        # Go to left
        elif e.state < 0:
            dmxToSend = int(((e.state * -1) / MAX_JOYSTICK_VALUE_LEFT) * 255)
            dmxToSend = self.checkDmxToSend(dmxToSend, e)
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = dmxToSend

    def sendBackButtons(self, e):
        self.artnetSender.packet.frame[self.keyMapping[e.code]] = e.state

    def checkDmxToSend(self, dmxToSend, e):
        if dmxToSend > 255 or dmxToSend < 0:
            self.log.warning("Valeurs incorrectes de la manette sur " + e.code)
            dmxToSend = 255
        return dmxToSend

    def readConfig(self):
        self.config.read('config.cfg')
        self.artNetIp = self.config.get("SENDERIP", "ARTNETIP")
        self.senderUniverse = int(self.config.get("SENDERIP", "ARTNETUNIVERSE"))


if __name__ == "__main__":
    converter = XinputToArtnetConverter()
