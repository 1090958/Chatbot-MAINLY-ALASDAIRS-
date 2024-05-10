import pygame, sys, moderngl, frontend.settings as settings, pygame.freetype, variables, frontend.prompt as prompt

from frontend.partitions.partitions import partition
from frontend.partitions.terminal import terminal
from frontend.partitions.bar import bar
#display stuff

pygame.freetype.init()
screen = pygame.display.set_mode(settings.resolution, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
display = pygame.Surface((256*3,256*3))


#create moderngl context for applying shaders in the future
import frontend.moderngl_tools as mgltools
quad = mgltools.quad_buffer
program = mgltools.import_shader('blur')

render_object = mgltools.ctx.vertex_array(program, [(mgltools.quad_buffer, '2f 2f', 'vert', 'texcoord')])


# pygame things
clock = pygame.time.Clock()
variables.running = True

# image items
bg = pygame.image.load('images/bg.png')
map = pygame.image.load('images/map.png')
fr = pygame.image.load('images/front.png')


bg = pygame.transform.scale_by(bg, 6)
map = pygame.transform.scale_by(map, 6)

# map stuff
# rectangles
    # for rooms
rect_up = pygame.Rect(60, 12, 52, 36)
rect_down = pygame.Rect((60, 12+112), (52, 36))
rect_left = pygame.Rect((12, 66), (38, 40))
rect_right = pygame.Rect((124, 66), (36, 40))
    # for others
attack_rect1 = pygame.Rect(22, 12, 128, 148)
attack_rect2 = pygame.Rect(12, 22, 148, 128)
# shader variables
    # blur radius
r = 1
variables.blur = False
variables.pixel = 1
    # chromatic abberation
abberationY = [4,2,2]
abberationX = [2,2,5]

#partition variables: no longer using these after switching to opengl
partitions = []
partitions.append(terminal(partition=partition((0.1,0.6),(0.6,0.95))))




#all colours are from the list of colours usable for the apple 2
'''#healthbar
partitions.append(bar(partition=partition((0.67,0.185),(0.933,0.24)),colour=(153,3,95)))
partitions[-1].type='health'
#stamina
vertical_difference=0.10
partitions.append(bar(partition=partition((0.67,0.185+vertical_difference),(0.933,0.24+vertical_difference)),colour=(36,155,255)))
partitions[-1].type='stamina'''


#game integration



import items.main as main
variables.game:main.Game = main.Game()
# GameGUI(Game(),  [True,True],  filename:"",  defaultColour: recommend(0,200,0),  defaultFont: recommend "font_minecraft.ttf")

variables.gui:main.GameGUI = main.GameGUI(variables.game,  [True,False])

def load_item(item)->pygame.surface:
    
    filename =  'images/items/'+ ''.join(item.type.name.lower().split())
    try:
        return pygame.transform.scale_by(pygame.image.load(filename),1.2)
    except:
        return pygame.transform.scale_by(pygame.image.load('images/items/unknownitem.png'),1.2)


while variables.running:
    
    events = pygame.event.get()
    render = False
    for event in events:
        if event.type in [pygame.QUIT,pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            render = True
            break
    if not render and not variables.blur and variables.gui.mode[0]!="map":
        continue
    display.fill((0,0,0))
    
    display.blit(bg,(0,0))
    # second gui stuff
    
    ui2 = pygame.transform.scale_by(variables.gui.step(events),0.58)
    
    #map stuff
    '''display.blit(map,(0,0))
    player_room = variables.game.map.rooms[variables.game.player.loc[0]][variables.game.player.loc[1]]
    rooms = player_room.connections
    #print(player_room.connections)
    if not rooms[0]: pygame.draw.rect(display, (0,0,0),rect_up)
    if not rooms[1]: pygame.draw.rect(display, (0,0,0),rect_down)
    if not rooms[2]: pygame.draw.rect(display, (0,0,0),rect_left)
    if not rooms[3]: pygame.draw.rect(display, (0,0,0),rect_right)
    if variables.game.state == "fighting": 
        # get rid of the map ui
        pygame.draw.rect(display, (0,0,0),attack_rect1) 
        pygame.draw.rect(display, (0,0,0),attack_rect2)
        # for each item in inventory, display the item
        position = (22,22)
        for item in variables.game.player.inv:
            if item: 
                display.blit(load_item(item),position)
                pygame.freetype.Font("frontend/apple2.ttf", 6).render_to(display, (position[0]+int(16*1.2)+3, position[1]+3), item.type.name,(255,255,255))
                pygame.freetype.Font("frontend/apple2.ttf", 6).render_to(display, (position[0]+int(16*1.2)+3, position[1]+11), item.type.rarity.name,(255,255,255))
                position=(position[0], position[1]+int(16*1.2)+3)'''
    #partition stuff
    
    for partition in partitions:
        partition.run(events)
    for partition in partitions:
        partition.draw(display)
    #draw ui
    display.blit(ui2, (36,35))
    #event stuff
    dt = 0.1
    for event in events:
        if event.type == pygame.QUIT:
            variables.running = False
        if event.type == pygame.KEYDOWN:
            variables.blur=False
            variables.r=1
            if event.key == pygame.K_SLASH:
                prompt.prompt(variables.game.help())
        if event.type == pygame.VIDEORESIZE:
            settings.resolution = ((event.w+event.h)/2,(event.w+event.h)/2)
            
            screen = pygame.display.set_mode(settings.resolution, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
            
            
    #partition stuff cont.
        
            
    
    #mgl stuff
    program['blur'] = False
    program['chromaticAbberationY'] = abberationY
    program['chromaticAbberationX'] = abberationX
    frame_tex = mgltools.surf_to_texture(display)
    frame_tex.use(0)
    program['type'] = 1
    program['tex'] = 0
    if variables.blur:
        program['r'] = 20
    else:
        program['r'] = 1
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
    #second pass to render the next window
    if variables.blur:
        frame_tex1 = mgltools.surf_to_texture(variables.prompt)
        frame_tex1.use(1)
        program['blur'] = variables.blur
        render_object.render(mode=moderngl.TRIANGLE_STRIP)
        program['resolution'] = settings.resolution
        program['blur'] = False
        program['type'] = 2
        
        program['tex'] = 1
        render_object.render(mode=moderngl.TRIANGLE_STRIP)

    pygame.display.flip()
    
    frame_tex.release()
    
    dt = clock.tick(10)
    
    
            