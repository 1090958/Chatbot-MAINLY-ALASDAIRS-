from character import character
from math import sqrt as root
def LCM(self, Num1, Num2):
    if Num1 >= Num2:
        Greater = Num1
    else:
        Greater = Num2
    
    while True:
        if((Greater % Num1 == 0) and (Greater % Num2 == 0)):
            LCM = Greater
            break
        Greater += 1
    return LCM

def distance(point1:character|list[int,int], point2:character|list[int,int], accuracy=15):
    
    if type(point1) == character:
        point1=point1.coordinates
    if type(point2) == character:
        point2=point2.coordinates
    
    return round(root((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2),accuracy)


p1=character(10,5,15)
p2=character(10,5,15)
p2.coordinates = [8,8]


print(distance(p1,p2))