import pygame, settings, pygame.freetype, output

original_resolution = settings.resolution
pygame.freetype.init()
screen = pygame.display.set_mode(size = settings.resolution, flags = pygame.RESIZABLE)

running = True

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
    def adjust_value(self, value:int|float, axis:str = None):
        
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
                
    



class terminal:
    def __init__(self, partition:partition):
        self.partition:partition = partition
        self.font = lambda size : pygame.freetype.Font("apple2.ttf", size)
        self.output = ''
        self.past = ['']
        self.size = 80
        self.line_limit = 3
    def input(self,character):
        self.output+=character
        self.past.pop(0)
        self.past.insert(0,self.output) 
    def delete(self):
        self.output=self.output[:-1]
        self.past.pop(0)
        self.past.insert(0,self.output) 
    def enter(self):
        self.past.insert(0,'')
        self.output = ''
        
        
    def draw(self):
        #print(self.past)
        
        past = self.past[:self.line_limit]
        
        # i made a program to find the exponential equation for the relationship between the font and the char_limit
        fit_to_curve = lambda x: int(((x**-1.20899) * (3767.696))) # a bit overkill, i think not
        
        # 20 is the number of letters that can fit on a line in normal situations
        char_limit=int(fit_to_curve(self.size)*(max(self.partition.p1[0], self.partition.p2[0]) - min(self.partition.p1[0], self.partition.p2[0])))
        
        
        resolution = self.partition.adjust_point((1,1))
        print(self.partition.adjust_value(0,'x'),self.partition.adjust_point((0,0))[0])
        for _ in range(len(past[1:])):
            item = past[_+1]
            
            self.font(self.partition.adjust_value(self.size,'y')).render_to(screen,(self.partition.adjust_point((0,0))[0],resolution[-1]-(self.partition.adjust_value(self.size*1.25,'y'))*(_+2)),item.upper()[:char_limit],(255,255,255))
        item = past[0]
        self.font(self.partition.adjust_value(self.size,'y')).render_to(screen,(self.partition.adjust_point((0,0))[0],resolution[-1]-(self.partition.adjust_value(self.size*1.25, 'y'))*(1)),'>>> ' + item.upper()[:char_limit],(255,255,255))
        
    
    def run(self, events):
        for event in events:
            #self.keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                try:
                    self.input((chr(int(event.key))).lower() if (chr(int(event.key))).lower() in "qwertyuiopasdfghjklzxcvbnm " else '')
                except:
                    pass          
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    self.delete()
                if event.key == pygame.K_RETURN:
                    self.enter()
terminal = terminal(partition=partition((0.5,0.6),(1,1)))
while running:
    screen.fill((0,0,0))
    terminal.draw()
    pygame.display.flip()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                terminal.size-=1
            if event.key == pygame.K_EQUALS:
                terminal.size+=1
        if event.type == pygame.VIDEORESIZE:
            settings.resolution = ((event.w+event.h)/2,(event.w+event.h)/2)
            screen = pygame.display.set_mode(size = settings.resolution, flags = pygame.RESIZABLE)
    terminal.run(events)
    
    
    
    
    
            