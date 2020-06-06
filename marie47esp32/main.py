#!/usr/bin/env python3
import sys
import click
import os
import time
import math
import traceback
import threading
import json

from datetime import datetime
from datetime import timedelta

from marie47esp32.webserver.webserver import WebServer
from marie47esp32.util.log import log
from marie47esp32.util.config import Config
#
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


    while(True):
        try:
          time.sleep(1000)
          log.error('still alive '+configpath)
        except Exception as e:
            log.warn('main: an exception occured! ignoring!')
            traceback.print_exc()
    log.debug('main: exiting.')
    
if __name__ == "__main__":
    sys.exit(main())
