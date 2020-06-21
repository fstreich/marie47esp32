from marie47esp32.util.log import log

class Color(object):
    
    def __init__(self, jsonobject):
        log.debug("color: all parsed: "+str(self))
    
    def getJSONobj(self):
        jsonObj = { }
        return jsonObj
    
    def getUDPbytes(self):
        return None