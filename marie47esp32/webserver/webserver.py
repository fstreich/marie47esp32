import random
import string
import os
from os.path import isfile, join
from os import listdir, remove
import string
import shutil
import base64
import asyncio
import tornado.web
import tornado.websocket
import json
import datetime
import pkg_resources

from marie47esp32.util.config import Config
from marie47esp32.util.log import log



class WebServer(tornado.web.Application):

    websocket_clients = []
    websocket_send_data = []
    main_loop = None
    
    def __init__(self):
        handlers = [ (r"/test", TestHandler),
                     (r"/websocket", WebSocket),
                     (r'/(.*)', tornado.web.StaticFileHandler, {'path': 'webstatic', "default_filename": "index.html"}),]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self, port=80):
        self.listen(port)
        WebServer.main_loop = tornado.ioloop.IOLoop().current()
        WebServer.main_loop.start()
        print("WebServer: TORNADO STARTED")
 
    def websocket_send(client,data,binary):
        WebServer.websocket_send_data.append([client,data,binary])
        WebServer.main_loop.add_callback(WebServer.send_to_socket)
        
    def send_to_socket():
        client,data,binary = WebServer.websocket_send_data.pop(0)
        if len(WebServer.websocket_clients)>0:
            if client == True:
                for c in WebServer.websocket_clients:
                    c.write_message(data,binary)
            else:
                client.write_message(data,binary)
        else:
            log.warn("webserver: send_to_socket: message dropped: no clients!")
             
class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test success")


class WebSocket(tornado.websocket.WebSocketHandler):
    
    def open(self):
        log.debug("WebSocket opened")
        self.nextIsBinary = None
        WebServer.websocket_clients.append(self)
        EchoWebSocket.instance = self
        
        ans = {
              "cmd": "version",
              "version": pkg_resources.get_distribution('marie47esp32').version
            }
        self.write_message(json.dumps(ans)) # hier ok!
        #WebServer.websocket_send(self,json.dumps(ans),False)
        
    def on_message(self, message):
        
        # process json messages
        jsonmsg = json.loads(message)
        log.debug("webserver: received message: "+str(jsonmsg))

        if jsonmsg['cmd']=='ping':
            ans = {
              "cmd": "pong",
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
       
        
        elif jsonmsg['cmd']=='test':
            ans = {
              "cmd": "toast",
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
                
    def on_close(self):
        print("WebSocket closed")
        WebServer.websocket_clients.remove(self)

        