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
from marie47esp32.udp.udpserver import UdpClient
from marie47esp32.patterns.program import Program

class WebServer(tornado.web.Application):

    websocket_clients = []
    websocket_send_data = []
    main_loop = None
    
    def __init__(self):
        handlers = [ (r"/api/.*", ApiHandler),
                     (r"/test", TestHandler),
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
        UdpClient.sendto(1,b'\x46\x53\x01\x01\x00') ## type 1, id 1, ping

class ApiHandler(tornado.web.RequestHandler):
    
    editslot = '{ "name": "test", "patterns": [ ] }'
    programslots = ['{ "name": "test1", "patterns": [ ] }',
                    '{ "name": "test2", "patterns": [ ] }',
                    '{ "name": "test3", "patterns": [ ] }',
                    '{ "name": "test4", "patterns": [ ] }',
                    '{ "name": "test5", "patterns": [ ] }',
                    '{ "name": "test6", "patterns": [ ] }',
                    '{ "name": "test7", "patterns": [ ] }',
                    '{ "name": "test8", "patterns": [ ] }',
                    '{ "name": "test9", "patterns": [ ] }']
    
    editor_cookie = None
    editor_last_seen = None
    
    def get(self):
        if not self.get_cookie("mycookie"):
            self.set_cookie("mycookie", str(random.randint(100000, 999999)))
        self.set_header("Content-Type", 'application/json')
        pathparts = self.request.path.split("/")
        ## results in ['', 'api', 'program', '1'] for /api/program/1
        if pathparts[2] == 'program':
            if len(pathparts)==4:
                self.write(self.getProgramBySlot(int(pathparts[3])))
        if pathparts[2] == 'endedit':
            if ApiHandler.editor_cookie == self.get_cookie("mycookie"):
                ApiHandler.editor_cookie = None
        
    def post(self):
        self.set_header("Content-Type", 'application/json')
        pathparts = self.request.path.split("/")
        ## results in ['', 'api', 'program', '1'] for /api/program/1
        if pathparts[2] == 'program':
            if len(pathparts)==4:
                self.write(self.setProgramBySlot(int(pathparts[3]), self.request.body))
        if pathparts[2] == 'edit':
            self.write(self.setProgramBySlot(-1, self.request.body))
        
    def getProgramBySlot(self, slotId):
        if slotId>=0 and slotId<len(ApiHandler.programslots):
            return ApiHandler.programslots[slotId]
        return ApiHandler.editslot
        
    def setProgramBySlot(self, slotId, programstring):
        if not (ApiHandler.editor_cookie is None or ApiHandler.editor_cookie == self.get_cookie("mycookie")):
            return 'someone else is editing right now!'
        ##jsonobj = json.loads(self.request.body)
        ##program = Program(jsonobj)
        ##print(json.dumps(program.getJSONobj()))
        
        if slotId>=0 and slotId<len(ApiHandler.programslots):
            ApiHandler.programslots[slotId] = programstring
            ApiHandler.editor_cookie = None
        if slotId==-1:
            ApiHandler.editslot = programstring
            ApiHandler.editor_cookie = self.get_cookie("mycookie")
            ApiHandler.editor_last_seen = datetime.datetime.now()
        return "ok"


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

        