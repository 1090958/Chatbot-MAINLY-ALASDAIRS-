from frontend.partitions.partitions import partition
import pygame
import variables
class terminal:
    def __init__(self, partition:partition):
        self.partition:partition = partition
        self.font = lambda size : pygame.freetype.Font("frontend/apple2.ttf", size)
        self.output = ''
        self.past = ['']
        self.size = 20
        self.line_limit = 6
    def input(self,character):
        self.output+=character
        self.past.pop(0)
        self.past.insert(0,self.output) 
    def delete(self):
        self.output=self.output[:-1]
        self.past.pop(0)
        self.past.insert(0,self.output) 
    def enter(self):
        output = variables.game.takeInput(self.output)
        print(output)
        try:
            self.past = list(reversed(output.split('\n'))) + self.past
        except:
            pass
        self.past.insert(0,'')
        
        self.output = ''
        
        
    def draw(self, display):
        #print(self.past)
        
        past = self.past[:self.line_limit]
        
        # i made a program to find the exponential equation for the relationship between the font and the char_limit
        fit_to_curve = lambda x: int(((x**-1.20899) * (3767.696))) # a bit overkill, i think not
        
        # 20 is the number of letters that can fit on a line in normal situations
        char_limit=15#int(fit_to_curve(self.size)*(max(self.partition.p1[0], self.partition.p2[0]) - min(self.partition.p1[0], self.partition.p2[0])))
        
        
        resolution = self.partition.adjust_point((1,1))
        
        for _ in range(len(past[1:])):
            item = past[_+1]
            
            self.font(self.partition.adjust_value(self.size,'y')).render_to(display,(self.partition.adjust_point((0,0))[0],resolution[-1]-(self.partition.adjust_value(self.size*1.25,'y'))*(_+2)),item.upper()[:char_limit],(255,255,255))
        item = past[0]
        self.font(self.partition.adjust_value(self.size,'y')).render_to(display,(self.partition.adjust_point((0,0))[0],resolution[-1]-(self.partition.adjust_value(self.size*1.25, 'y'))*(1)),'>>> ' + item.upper()[:char_limit],(255,255,255))
        
    
    def run(self, events):
        for event in events:
            #self.keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                try:
                    self.input((chr(int(event.key))).lower() if (chr(int(event.key))).lower() in "qwertyuiopasdfghjklzxcvbnm 1234567890" else '')
                except:
                    pass          
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    self.delete()
                if event.key == pygame.K_RETURN:
                    self.enter()
