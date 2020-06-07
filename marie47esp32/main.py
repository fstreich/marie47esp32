#!/usr/bin/env python3
import sys
import click
import os
import time
import math
import traceback
import threading
import json
import socket

from datetime import datetime
from datetime import timedelta

from marie47esp32.webserver.webserver import WebServer
from marie47esp32.util.log import log
from marie47esp32.util.config import Config
from marie47esp32.udp.udpserver import UdpServer

import asyncio
import tornado.web
import tornado.websocket
from pickle import FALSE


def millis(start, end):
    diff = end-start
    return (diff.days*24*60*60+diff.seconds)*1000+diff.microseconds/1000.0

ws = WebServer()

def start_tornado(port):
    asyncio.set_event_loop(asyncio.new_event_loop())
    ws.run(port=port)
## TORNADO END


def main():
    log.debug('marie47esp32: starting...')

    # load config
    configpath="."

    config = Config.getSingleton()
    config.init(configpath)

    t = threading.Thread(target=start_tornado, args=[config.getInt("webserverport")])
    t.daemon = True
    t.start()

    UDP_PORT = config.getInt("udpserverport")
    
    UdpServer.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    UdpServer.sock.bind(('', UDP_PORT)) # specify UDP_IP or INADDR_ANY
    MESSAGE = b"Hello, World!"
    
    while(True):
        try:
            udpdata, addr = UdpServer.sock.recvfrom(4096) # buffer size is 1024 bytes
            UdpServer.handle_udp_paket(udpdata, addr)
        except Exception as e:
            log.warn('main: an exception occured! ignoring!')
            traceback.print_exc()
    log.debug('main: exiting.')
    
if __name__ == "__main__":
    sys.exit(main())
