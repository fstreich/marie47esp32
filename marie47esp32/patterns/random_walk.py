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
        return None
    
    def __str__(self):
        return '{ pclass: random_walk, name: '+self.name+'] }'
