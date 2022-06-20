import math

class handler:
    def __init__(self):
        self.left_hand = hand("left")
        self.right_hand = hand("right")
        self.hand_dict = {"left": self.left_hand, "right": self.right_hand}
    
    def update(self, handedness, landmarks, draw):
        i = 0
        for hand_landmarks in landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                self.hand_dict.get(self.getLabels(handedness)[i]).updatePoints([lm.x, lm.y, lm.z])
            i+=1
            draw(hand_landmarks)   
        self.left_hand.updateRadii()
        self.right_hand.updateRadii()

    #label the order which the hands are presented by mediapipe handedness
    def getLabels(self, handedness):
        return ['left' if label.classification[0].index else 'right' for label in handedness]

class hand:
    def __init__(self, name):
        self.points = []
        self.radii = []
        self.name = name
    
    def getList(self):
        cord_list = []
        index = 0
        for radius in self.radii:
            cord_list.append( [index, radius] )
            index += 1
        return cord_list
            
    
    def updatePoints(self, point):
        self.points.append(point)
    
    def updateRadii(self):
        self.radii = self.norm([math.dist(point, self.points[0]) for point in self.points])
        self.points = []
        
    #normalize cords    
    def norm(self, cords):
        return [float(i)/max(cords) for i in cords]
    

