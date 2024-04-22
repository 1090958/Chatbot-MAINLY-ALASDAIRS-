import pygame, pygame.freetype,variables
pygame.freetype.init()
image=pygame.transform.scale2x(pygame.image.load("images\images.png"))

def prompt(prompt:str,options:dict = {}):
    surface = pygame.Surface((256,256))
    font = pygame.freetype.Font("frontend/apple2.ttf",5)
    font.render_to(surface,(0,0),prompt,(255,255,255))
    surface.blit(image,(0,0))
    variables.prompt = surface
    variables.blur = True
    
    
prompt("test 1")