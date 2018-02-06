"""Simple example showing how to get gamepad events."""

from __future__ import print_function

import ConfigParser
import logging

from inputs import get_gamepad

from sender import ArtNetSender

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s')


class XinputToArtnetConverter(object):

    def __init__(self):
        self.keyMapping = {"BTN_SOUTH": 0, # Croix
                           "BTN_WEST": 1, # Triangle
                           "BTN_NORTH": 2, # Carre
                           "BTN_EAST": 3, # Rond
                           "BTN_TL": 4, # L1
                           "BTN_TR": 5, # R1
                           "BTN_START": 6, # Start
                           "BTN_SELECT": 7, # Select
                           "BTN_THUMBL": 8, # Click Joystick Gauche
                           "BTN_THUMBR": 9, # Click Joystick Droit
                           "ABS_RZ": 10,  # R2
                           "ABS_Z": 11,  # L2
                           "ABS_X_LEFT": 12, # Joystick gauche a gauche
                           "ABS_X_RIGHT": 13, # Joystick gauche a droite
                           "ABS_Y_LEFT": 14, # Joystick gauche en haut
                           "ABS_Y_RIGHT": 15, # Joystick gauche en bas
                           "ABS_RX_LEFT": 16, # Joystick droite a gauche
                           "ABS_RX_RIGHT": 17, # Joystick droite a droite
                           "ABS_RY_LEFT": 18, # Joystick droite en haut
                           "ABS_RY_RIGHT": 19, # Joystick droite en bas
                           "ABS_HAT0Y_LEFT": 20, # Fleche haut
                           "ABS_HAT0Y_RIGHT": 21, # Fleche bas
                           "ABS_HAT0X_LEFT": 22, # Fleche gauche
                           "ABS_HAT0X_RIGHT": 23, # Fleche droite

                           }
        self.joysticksCode = [
            "ABS_X", "ABS_Y",
            "ABS_RX","ABS_RY",
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
        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type == "Key":
                    self.btnClicked(event)
                elif event.ev_type == "Absolute":
                    self.absoluteMoved(event)
            self.artnetSender.sendFramesWithLog()

    def btnClicked(self, e):
        if e.state == 0:
            self.artnetSender.packet.frame[self.keyMapping[e.code]] = 0
        elif e.state == 1:
            self.artnetSender.packet.frame[self.keyMapping[e.code]] = 255

    def absoluteMoved(self, e):
        if e.code == "ABS_RZ" or e.code == "ABS_Z":
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
        # Go to right
        if e.state == 255 and e.code in ["ABS_Y", "ABS_RY"]:
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = 0
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = 0
        elif e.state == 0:
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = 0
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = 0
        elif e.state > 0:
            dmxToSend = int((e.state / 32767.0) * 255)
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_RIGHT"]] = dmxToSend
        # Go to left
        elif e.state < 0:
            dmxToSend = int(((e.state * -1) / 32768.0) * 255)
            self.artnetSender.packet.frame[self.keyMapping[e.code + "_LEFT"]] = dmxToSend

    def sendBackButtons(self, e):
        self.artnetSender.packet.frame[self.keyMapping[e.code]] = e.state

    def readConfig(self):
        self.config.read('config.cfg')
        self.artNetIp = self.config.get("SENDERIP", "ARTNETIP")
        self.senderUniverse = int(self.config.get("SENDERIP", "ARTNETUNIVERSE"))


if __name__ == "__main__":
    converter = XinputToArtnetConverter()
