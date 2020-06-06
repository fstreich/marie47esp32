import cv2
import numpy as np
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
                     (r"/upload", UploadHandler),
                     (r"/uploadconfig", UploadConfigHandler),
                     (r"/getconfig", GetConfigHandler),
                     (r"/websocket", EchoWebSocket),
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

## handles downloads of configurations at /getconfig
class GetConfigHandler(tornado.web.RequestHandler):
    def delete_all_files_in_folder(path):
        mypath = Config.workingpath+path
        for f in listdir(mypath):
            if isfile(join(mypath, f)):
                remove(join(mypath, f))
    def get(self):
        config = Config.getSingleton()
        filename = config.get("device.name")+"."+config.get("device.mac")+"."+str(datetime.datetime.now().date())+".tgz"
        filename = filename.replace(" ","_")
        log.debug("Webserver: config filename: "+str(filename))
        
        if not os.path.exists(Config.workingpath+'/temp'):
            os.makedirs(Config.workingpath+'/temp')
        GetConfigHandler.delete_all_files_in_folder('/temp')
        mypath = Config.workingpath+"/temp"
        
        if Framecontrol.originalframe is not None:
            img = Framecontrol.originalframe.copy()
            debugimagename = Config.workingpath+'/temp/currentimage.png'
            cv2.imwrite(debugimagename,img)
        
        shutil.make_archive("config", "gztar", Config.workingpath , '.')
        self.add_header("Content-Disposition","attachment; filename="+filename)
        data = open("config.tar.gz", "rb").read() 
        self.write(data)

## handles uploads of updates at /upload
class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['update'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename= fname+extension
        if not os.path.exists(Config.workingpath+'/update'):
            os.makedirs(Config.workingpath+'/update')
            os.makedirs(Config.workingpath+'/update/download')
        output_file = open(Config.workingpath+"/update/download/" + final_filename, 'wb')
        output_file.write(file1['body'])
        log.debug("file" + final_filename + " is uploaded")
        self.write( Updater.check_update_and_give_web_response() )

## handles uploads of configurations at /uploadconfig
class UploadConfigHandler(tornado.web.RequestHandler):
    def delete_all_files_in_folder(self, path):
        try:
            mypath = Config.workingpath+path
            for f in listdir(mypath):
                if isfile(join(mypath, f)):
                    remove(join(mypath, f))
        except Exception as e:
            log.warn('UploadConfigHandler: could not delete files in: '+str(mypath))
    def post(self):
        try:
            file1 = self.request.files['config'][0]
            original_fname = file1['filename']
            extension = os.path.splitext(original_fname)[1]
            fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
            final_filename= fname+extension
            if not os.path.exists(Config.workingpath+'/config'):
                os.makedirs(Config.workingpath+'/config')
                os.makedirs(Config.workingpath+'/config/download')
                os.makedirs(Config.workingpath+'/config/unpacked')
            output_file = open(Config.workingpath+"/config/download/" + final_filename, 'wb')
            output_file.write(file1['body'])
            output_file.flush()
            output_file.close()
            log.debug("config file" + final_filename + " is uploaded")
            self.delete_all_files_in_folder("/config/unpacked")
            self.delete_all_files_in_folder("/config/unpacked/debug")
            self.delete_all_files_in_folder("/config/unpacked/mask")
            self.delete_all_files_in_folder("/config/unpacked/maskhighpass")
            self.delete_all_files_in_folder("/config/unpacked/reference")
            self.delete_all_files_in_folder("/config/unpacked/temp")
            shutil.unpack_archive(Config.workingpath+"/config/download/" + final_filename,
                                  Config.workingpath+"/config/unpacked" , format="gztar")
            
            self.delete_all_files_in_folder("/config/download")
            shutil.copy(Config.workingpath+"/config/unpacked/config.xml", Config.workingpath+"/config.xml")
    
            if self.get_argument("usemask", default=None, strip=True) is not None:
                log.debug("webserver: copying masks:")
                self.delete_all_files_in_folder("/mask")
                self.delete_all_files_in_folder("/maskhighpass")
                mypath = Config.workingpath+"/config/unpacked/mask"
                for f in os.listdir(mypath):
                    log.debug("webserver: copying masks:" + str(f))
                    if isfile(join(mypath, f)):
                        shutil.copyfile(join(mypath,f), join(Config.workingpath+"/mask",f))
                mypath = Config.workingpath+"/config/unpacked/maskhighpass"
                for f in os.listdir(mypath):
                    log.debug("webserver: copying masks:" + str(f))
                    if isfile(join(mypath, f)):
                        shutil.copyfile(join(mypath,f), join(Config.workingpath+"/maskhighpass",f))
            else:
                log.debug("webserver: not copying masks.")
            self.write( "config ok, rebooting..." )
            Updater.reboot()
        except Exception as e:
            self.write( "Ein Fehler ist aufgetreten, Konfiguration konnte nicht eingespielt werden." )
            
class EchoWebSocket(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print("WebSocket opened")
        self.nextIsBinary = None
        WebServer.websocket_clients.append(self)
        EchoWebSocket.instance = self
        
        ans = {
              "cmd": "version",
              "version": pkg_resources.get_distribution('eempty').version,
              "date": IOModule.get().getDate().isoformat(),
              "outputoverride" : int(IOModule.force_overwrite_output_from_web_frontend)
            }
        self.write_message(json.dumps(ans)) # hier ok!
        #WebServer.websocket_send(self,json.dumps(ans),False)
        
    def on_message(self, message):
        IOModule.get().resetWebsocketActivityTimer()
        
        # process binary messages
        if self.nextIsBinary is not None:
            if self.nextIsBinary['cmd']=="savemaskimage":
                im = np.array(bytearray(message), dtype=np.uint8)
                im = im.reshape((480,640,3))
                Framecontrol.maskImage = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                Framecontrol.saveMask()
                self.nextIsBinary = None
                return
            if self.nextIsBinary['cmd']=="savemaskhighimage":
                im = np.array(bytearray(message), dtype=np.uint8)
                im = im.reshape((480,640,3))
                Framecontrol.maskHighImage = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                Framecontrol.saveMaskHigh()
                self.nextIsBinary = None
                return
            
            log.warn("webserver: unhandled binary message!")
            self.nextIsBinary = None
            return
        
        # process json messages
        jsonmsg = json.loads(message)
        log.debug("webserver: received message: "+str(jsonmsg))
        if jsonmsg['cmd']=='setdate':
            from eempty.I2C.i2c import I2C
            from eempty.I2C.mcp7940rtc import Mcp7940rtc
            Mcp7940rtc.set_time_MCP7940_RTC(I2C.getI2Cbus(),datetime.datetime.fromisoformat(jsonmsg['date'].replace('Z','+00:00')))
            #IOModule.get().set_time_MCP7940_RTC(datetime.datetime.fromisoformat(jsonmsg['date'].replace('Z','+00:00')))
            ans = {
              "cmd": "version",
              "version": pkg_resources.get_distribution('eempty').version,
              "date": IOModule.get().getDate().isoformat()
            }
            WebServer.websocket_send(self,json.dumps(ans),False)
        if jsonmsg['cmd']=='ping':
            ans = {
              "cmd": "pong",
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
        elif jsonmsg['cmd']=='getreferenceinfo':
            ans = {
              "cmd": "referenceinfo",
              "referencecount": len(Framecontrol.referenceImages)
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
        elif jsonmsg['cmd']=='addreferenceimage':
            Framecontrol.setReferenceImage();
            ans = {
              "cmd": "referenceinfo",
              "referencecount": len(Framecontrol.referenceImages)
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
        elif jsonmsg['cmd']=='delreferenceimage':
            Framecontrol.deleteReferenceImageFromSlot(int(jsonmsg['referenceindex']));
            ans = {
              "cmd": "referenceinfo",
              "referencecount": len(Framecontrol.referenceImages)
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
        elif jsonmsg['cmd']=='getliveimage':
            Framecontrol.addImageRequest( { 'type': jsonmsg['type'], 'referenceindex': int(jsonmsg['referenceindex']), 'age':0 })
        elif jsonmsg['cmd']=='getmaskimage':
            ans = {
              "cmd": "maskimage",
              "binary": True
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
            bytes = cv2.cvtColor(Framecontrol.maskImage, cv2.COLOR_GRAY2BGR)
            #self.write_message(bytes.tobytes(), binary=True)
            WebServer.websocket_send(self,bytes.tobytes(),True)
        elif jsonmsg['cmd']=='getmaskhighimage':
            ans = {
              "cmd": "maskhighimage",
              "binary": True
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
            bytes = cv2.cvtColor(Framecontrol.maskHighImage, cv2.COLOR_GRAY2BGR)
            #self.write_message(bytes.tobytes(), binary=True)
            WebServer.websocket_send(self,bytes.tobytes(),True)
        elif jsonmsg['cmd']=='savemaskimage':
            self.nextIsBinary = jsonmsg;
        elif jsonmsg['cmd']=='savemaskhighimage':
            self.nextIsBinary = jsonmsg;
        elif jsonmsg['cmd']=='getparameter':
            ans = {
                'cmd': 'configparameter',
                'config': Config.getSingleton().getAllParameter()
            }
            #self.write_message(json.dumps(ans))
            WebServer.websocket_send(self,json.dumps(ans),False)
        elif jsonmsg['cmd']=='defaultparameter':
            Config.getSingleton().defaultAllParameter();
        elif jsonmsg['cmd']=='setparameter':
            Config.getSingleton().setAllParameter(jsonmsg['config']);
        elif jsonmsg['cmd']=='cancelparameter':
            Config.getSingleton().cancelAllParameter();
        elif jsonmsg['cmd']=='saveparameter':
            Config.getSingleton().saveAllParameter();
        elif jsonmsg['cmd']=='nexttestimage':
            if Config.getSingleton().get('cam.driver') == 'testimages':
                TestImages.get().nextImage()
        elif jsonmsg['cmd']=='prevtestimage':
            if Config.getSingleton().get('cam.driver') == 'testimages':
                TestImages.get().prevImage()
        elif jsonmsg['cmd']=='stopwatchdogupdate':
            IOModule.trigger_watchdog = False
        elif jsonmsg['cmd']=='stopwifi':
            IOModule.get().stopWifi()
        elif jsonmsg['cmd']=='rebootnow':
            IOModule.get().reboot()
        elif jsonmsg['cmd']=='startfan':
            IOModule.get().start_fan()
        elif jsonmsg['cmd']=='stopfan':
            IOModule.get().stop_fan()
        elif jsonmsg['cmd']=='startaudiofeedback':
            IOModule.get().start_audiofeedback()
        elif jsonmsg['cmd']=='stopaudiofeedback':
            IOModule.get().stop_audiofeedback()
        elif jsonmsg['cmd']=='restartcamera':
            Framecontrol.camera.restart()
        elif jsonmsg['cmd']=='outputoverride':
            newoverride_state = int(jsonmsg['override'])
            if IOModule.force_overwrite_output_from_web_frontend != newoverride_state:
                ans = {
                  "cmd": "version",
                  "version": pkg_resources.get_distribution('eempty').version,
                  "date": IOModule.get().getDate().isoformat(),
                  "outputoverride" : int(newoverride_state)
                }
                self.write_message(json.dumps(ans)) # hier ok!
        #WebServer.websocket_send(self,json.dumps(ans),False)
            IOModule.force_overwrite_output_from_web_frontend = newoverride_state
            if IOModule.force_overwrite_output_from_web_frontend:
                IOModule.setOutput1(int(jsonmsg['output1']), True)
                IOModule.setOutput2(int(jsonmsg['output1']), True)
                IOModule.setOutput3(int(jsonmsg['output1']), True)
                
    def on_close(self):
        print("WebSocket closed")
        WebServer.websocket_clients.remove(self)

        