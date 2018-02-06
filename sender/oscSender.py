import argparse

import OSC

parser = argparse.ArgumentParser(description='Send an OSC Message.')
parser.add_argument('host', help='IP Address')
parser.add_argument('port', help='Port')
# args = parser.parse_args()

# ip_address = args.host
# port = int(args.port)

msg = OSC.OSCMessage("/OGA")

oscClient = OSC.OSCClient()
oscClient.sendto(msg, ("192.168.0.155", 8888))
