import math

def addVectors((angle1, magnitude1), (angle2, magnitude2)): #takes 2 vectors
    xComponent = magnitude1*math.cos(angle1) + magnitude2*math.cos(angle2)

    yComponent = magnitude1*math.sin(angle1) + magnitude2*math.sin(angle2)

    angle = 2*math.pi - math.atan2(-yComponent, xComponent)
    magitude = math.hypot(xComponent, yComponent)
    #print('angle mag', angle, magitude)
    return (angle, magitude)