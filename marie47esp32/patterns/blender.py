from marie47esp32.util.log import log

class Blender(object):
    
    def __init__(self, jsonobject):
        log.debug("blender: all parsed: "+str(self))
    
    def getJSONobj(self):
        jsonObj = { }
        return jsonObj
    
    def getUDPbytes(self):
        return None