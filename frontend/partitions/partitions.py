import frontend.settings as settings
original_resolution = settings.resolution

class partition:
    def __init__(self,p1:tuple[float,float],p2:tuple[float,float]):
        self.p1:tuple[float,float] = p1
        self.p2:tuple[float,float] = p2
        # you need two points to make a rectangle
    def adjust_point(self,point:tuple[float,float]):
        """takes a coordinate in x,y space that ranges from 0, 1 and converts it into screen space"""
        
        x,y=point[0],point[1]
        
        # simple linear equation for a remap, i recommend checking out the full equation
        # this converts the point into the range of the two points
        x = ((x)) * (max(self.p1[0],self.p2[0]) - min(self.p1[0],self.p2[0])) + min(self.p1[0],self.p2[0])
        y = ((y)) * (max(self.p1[1],self.p2[1]) - min(self.p1[1],self.p2[1])) + min(self.p1[1],self.p2[1])
        
        # proceed to convert to screen space
        x *= settings.resolution[0]
        y *= settings.resolution[1]
        return (x,y)
    def adjust_value(self, value:int|float, axis:str = "x"):
        
        modifierx = settings.resolution[0]/original_resolution[0]
        modifiery = settings.resolution[1]/original_resolution[1]
        
        if axis == 'x':
            value1 = (value*modifierx) * (max(self.p1[0],self.p2[0]) - min(self.p1[0],self.p2[0])) + min(self.p1[0],self.p2[0])
        elif axis == 'y':
            value1 = (value*modifiery) * (max(self.p1[1],self.p2[1]) - min(self.p1[1],self.p2[1])) + min(self.p1[1],self.p2[1])
        else:
            #else average from both axis
            value1 = ((value*modifierx) * (max(self.p1[0],self.p2[0]) - min(self.p1[0],self.p2[0])) + min(self.p1[0],self.p2[0]) +(value*modifiery) * (max(self.p1[1],self.p2[1]) - min(self.p1[1],self.p2[1])) + min(self.p1[1],self.p2[1]))/2
        return value1
