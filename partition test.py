import pygame
import frontend.partitions.bar as bar, frontend.partitions.partitions as partitions
display = pygame.display.set_mode((720,720))
import frontend.settings as settings
#settings.resolution = (128,128)
bar = bar.bar(partitions.partition((0,0),(0.3,0.3)))
clock = pygame.time.Clock()
while True:
    display.fill((0,0,0))
    bar.draw(display)
    pygame.display.flip()
    if bar.value >= 1:
        bar.value=0
    else: bar.value+=0.001
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    clock.tick(60)