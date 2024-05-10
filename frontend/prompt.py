import pygame, pygame.freetype,variables
pygame.font.init()
image=pygame.transform.scale2x(pygame.image.load("images/images.png"))

#I will acknowledge that the whole prompt system is super botched and will be revisited after the project
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 0

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            return False

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word or newline  
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        if "\n" in text[:i]:
            i = text.rfind("\n", 0, i) + 1
        if "@" in text[:i]:
            i = text.rfind("@", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i].replace('@', ''), 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i].replace('@', ''), aa, color)
        if text[i-1] == '\n':
            #print('newline')
            y+=10
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted from the queue
        text = text[i:]

    return True

bounds = pygame.rect.Rect(128+40,128+40,256*2-70,256*2-70)

#font = pygame.font.Font("frontend/apple2.ttf",9)
def prompt(prompt:str,options:dict = {}):
    
    font = pygame.font.Font("frontend/apple2.ttf",11)
    surface = pygame.Surface((256*3,256*3))
    surface.fill((255,0,0))
    
    surface.blit(pygame.transform.scale_by(image,2),(128,128))
    
    text = drawText(surface,prompt,(255,255,255),bounds,font)
    pygame.freetype.Font("frontend/apple2.ttf",11).render_to(surface,(512/2,512),'type to escape these menus',[255]*3)
    variables.prompt = surface
    variables.blur = True
    variables.update=True
    
    