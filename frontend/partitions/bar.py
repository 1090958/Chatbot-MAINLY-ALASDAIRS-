import frontend.partitions.partitions as partitions,frontend.settings as settings

import pygame

class bar:
    def __init__(self, partition:partitions.partition, colour:tuple[int,int,int] = (255,255,255)):
        self.partition:partitions.partition = partition
        self.value = 0
        self.colour = colour
        self.rate = 0.01
        
    def draw(self, display):
        
        pygame.draw.rect(display, self.colour, pygame.Rect((
            (
                self.partition.p1[0]*settings.resolution[0],
                self.partition.p1[1]*settings.resolution[1]
            ),
            (
                (self.partition.p2[0]*settings.resolution[0]-(self.partition.p1[0]*settings.resolution[0]))*(int(self.value*20)/20),
                self.partition.p2[1]*settings.resolution[1]-self.partition.p1[1]*settings.resolution[1]
            ))))
    def run(self, event):
        
        self.value = 0 if self.value>=1 else self.value+self.rate