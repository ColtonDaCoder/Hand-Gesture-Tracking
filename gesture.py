import json

filename = 'gestures.json'

class gesture:

    def __init__(self, name, cords):
        self.name = name
        self.cords = cords

    #normalize cords    
    def norm(self, cords):
        #raw list of just radii
        raw = [d.get('radius') for d in cords]
        return [float(i)/max(raw) for i in raw]

    def toJson(self):
        with open(filename) as file:
            temp = json.load(file)
        temp.update( { self.name: self.cords } )
        with open(filename, 'w') as outfile:
            json.dump(temp, outfile, indent=4, separators=(',',': '))


def getGesture(name):
    with open(filename) as file:
        dictionary = json.load(file)
        for g in list(dictionary):
            if g == name:
                return gesture(name, dictionary.get(name))    
            
