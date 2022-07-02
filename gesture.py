import json

filename = 'gestures.json'

class gesture:

    def __init__(self, name, cords):
        self.name = name
        self.cords = cords

    def toJson(self):
        with open(filename) as file:
            temp = json.load(file)
        temp.update( { self.name: self.cords } )
        with open(filename, 'w') as outfile:
            json.dump(temp, outfile, indent=4, separators=(',',': '))
    
    def disregard(self, points_list):
        for point in points_list:
            self.cords[point] = -1
        self.toJson()

def newGesture(name, cords):
    return gesture(name, norm(cords))

#normalize cords    
def norm(cords):
    #raw list of just radii
    #raw = [r.get('radius') for r in cords]
    return [float(i)/max(cords) for i in cords]

def getGesture(name):
    with open(filename) as file:
        dictionary = json.load(file)
        for g in list(dictionary):
            if g == name:
                return gesture(name, dictionary.get(name))    
            
