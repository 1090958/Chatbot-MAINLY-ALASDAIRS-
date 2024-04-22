import frontend.partitions.partitions as partitions,frontend.settings as settings

import pygame

class map:
    def __init__(self, partition:partitions.partition, colour:tuple[int,int,int] = (255,255,255)):
        self.partition:partitions.partition = partition
        self.colour = colour
        self.img:pygame.Surface = pygame.image.load("images/front.png")
        self.pos = (0,0)
        self.scale = 1
    def draw(self, display):
        
        display.blit(pygame.transform.scale_by(self.img,self.scale),self.pos)
    def run(self, events:list[pygame.event.Event]):
        events = pygame.event.get()
        
        for button in pygame.mouse.get_pressed(num_buttons=5)[-2:-1]:
            print(button)
            
            
            
        #mouse stuff
        movement = pygame.mouse.get_rel()
        if not pygame.mouse.get_pressed()[0]:
            movement:tuple[int,int] = (0,0)
        self.pos=(self.pos[0]+movement[0], self.pos[1]+movement[1])
        