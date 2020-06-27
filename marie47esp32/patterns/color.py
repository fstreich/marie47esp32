from marie47esp32.util.log import log

class Color(object):
    
    def __init__(self, jsonobject):
        log.debug("color: all parsed: "+str(self))
    
    def getJSONobj(self):
        jsonObj = { }
        return jsonObj
    
    def getUDPbytes(self):
        ## 'C' color
        ## 00  no blender
        data = bytearray(b'\x43\x00')
        return data
