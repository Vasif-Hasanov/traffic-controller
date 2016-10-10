from zcm import *
import socket
import logging
import pprint
logging.basicConfig(level=logging.DEBUG)

class simServer_Component(Component):
    def __init__(self):
        """Register the server operation"""
        Component.__init__(self)

        self.register_server_operation("send",
        self.send)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data_string):
        self.sock.settimeout(1) #need this in case of message loss
        self.sock.sendto(data_string, ("192.168.0.111",11000))
        #logging.debug('@send, I: %s, msg: %s\n', self.name, pprint.pformat(data_string))
        try:
            response, srvr = self.sock.recvfrom(1024)
            logging.debug('@send, response: %s', response )
        except socket.timeout:
            logging.error('Request timed out')
            response =  0
        return response
