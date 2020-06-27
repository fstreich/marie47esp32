from marie47esp32.util.log import log
from marie47esp32.patterns.blender import Blender
from marie47esp32.patterns.color import Color


class Random_walk(object):
    
    def __init__(self, jsonobject):
        
        self.name = jsonobject['name']
        self.speed = jsonobject['speed']
        self.hmirror = jsonobject['hmirror']
        self.vmirror = jsonobject['vmirror']
        self.rotate = jsonobject['rotate']
        
        self.blender = Blender(jsonobject['blender'])
        self.color = Color(jsonobject['color'])

        log.debug("pattern: random_walk: all parsed: "+str(self))
        
    def getJSONobj(self):
        jsonObj = { "pclass": "random walk",
                    "name": self.name,
                    "speed": self.speed,
                    "hmirror": self.hmirror,
                    "vmirror": self.vmirror,
                    "rotate": self.rotate,
                    "blender": self.blender.getJSONobj(),
                    "color": self.color.getJSONobj()
                     }
        
        return jsonObj
    
    def getUDPbytes(self):
        ## 'A': pattern
        ## 'A': random_walk
        data = bytearray(b'\x41\x41\x00\x00\x00\x00')
        data[2] = self.speed
        data[3] = self.hmirror
        data[4] = self.vmirror
        data[5] = self.rotate
        data.extend(self.blender.getUDPbytes())
        data.extend(self.color.getUDPbytes())
        return data
    
    def __str__(self):
        return '{ pclass: random_walk, name: '+self.name+'] }'
