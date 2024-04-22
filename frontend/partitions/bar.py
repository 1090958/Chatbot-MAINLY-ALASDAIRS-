import frontend.partitions.partitions as partitions,frontend.settings as settings, variables

import pygame

class bar:
    def __init__(self, partition:partitions.partition, colour:tuple[int,int,int] = (255,255,255)):
        self.partition:partitions.partition = partition
        self.value = 0
        self.colour = colour
        self.type=None
        
    def draw(self, display):
        
        pygame.draw.rect(display, self.colour, pygame.Rect((
            (
                self.partition.p1[0]*256,
                self.partition.p1[1]*256
            ),
            (
                (self.partition.p2[0]*256-(self.partition.p1[0]*256))*(int(self.value*20)/20),
                self.partition.p2[1]*256-self.partition.p1[1]*256
            ))))
    def run(self, event):
        if self.type == 'health':
            self.value = variables.game.player.hp/variables.game.player.maxhp
        if self.type == 'stamina':
            self.value = variables.game.player.stamina/400