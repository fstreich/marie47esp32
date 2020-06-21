from marie47esp32.util.log import log
from marie47esp32.patterns.random_walk import Random_walk

class Program(object):
    
    def __init__(self, jsonobject):
        
        self.name = jsonobject['name']
        self.patterns = []
        for p in jsonobject["patterns"]:
            if p['pclass'] == "random walk":
                self.patterns.append(Random_walk(p))
            elif p['pclass'] == "disco":
                self.patterns.append(Random_walk(p))
            else:
                log.error("program: don't know pattern: "+str(p))
        log.debug("program: all parsed: "+str(self))
    
    def getJSONobj(self):
        jsonObj = { "name": self.name, "patterns": [] }
        for p in self.patterns:
            jsonObj["patterns"].append(p.getJSONobj())
        return jsonObj
    
    def getUDPbytes(self):
        return None
    
    def __str__(self):
        return '{ name: '+self.name+', patterns: ['+str(len(self.patterns))+'] }'