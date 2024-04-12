import pygame, sys, moderngl, frontend.settings as settings, pygame.freetype

from frontend.partitions.partitions import partition
from frontend.partitions.terminal import terminal

#display stuff

pygame.freetype.init()
screen = pygame.display.set_mode(settings.resolution, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
display = pygame.Surface(settings.resolution)


#create moderngl context for applying shaders in the future
import frontend.moderngl_tools as mgltools
quad = mgltools.quad_buffer
program = mgltools.import_shader('blur')

render_object = mgltools.ctx.vertex_array(program, [(mgltools.quad_buffer, '2f 2f', 'vert', 'texcoord')])


#pygame things
clock = pygame.time.Clock()
running = True

#image
img = pygame.image.load('images/bg.png')

r = 10

partitions = []
partitions.append(terminal(partition=partition((0.1,0.6),(0.6,0.95))))
while running:
    display.fill((0,0,0))
    
    img = pygame.transform.scale(img, settings.resolution)
    display.blit(img,(0,0))
    #partition stuff
    for partition in partitions:
        partition.draw(display)
    
    events = pygame.event.get()
    #event stuff
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                r-=1
            if event.key == pygame.K_EQUALS:
                r+=1
        if event.type == pygame.VIDEORESIZE:
            settings.resolution = ((event.w+event.h)/2,(event.w+event.h)/2)
            
            display = pygame.Surface(settings.resolution)
            screen = pygame.display.set_mode(settings.resolution, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
    
    #partition stuff cont.
    for partition in partitions:
        partition.run(events)
    
    #mgl stuff
    frame_tex = mgltools.surf_to_texture(display)
    frame_tex.use(0)
    program['tex'] = 0
    program['r'] = r
    program['resolution'] = settings.resolution
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    
    pygame.display.flip()
    
    frame_tex.release()
    
    clock.tick(60)
    
    
            