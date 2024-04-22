import pygame
import frontend.partitions.map as map, frontend.partitions.partitions as partitions
display = pygame.display.set_mode((720,720))
import frontend.settings as settings
#settings.resolution = (128,128)
bar = map.map(partitions.partition((0,0),(0.3,0.3)))
clock = pygame.time.Clock()
while True:
    display.fill((0,0,0))
    
    bar.run(None)
    bar.draw(display)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    clock.tick(60)