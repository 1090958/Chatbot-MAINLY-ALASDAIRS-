import pygame,random
pygame.init()

SIZE = 5
CDR = 0.2
CDD = 0.2
MODES = 3
BIOMES = [(200,50,100),(150,0,150),(150,150,150),(80,150,200)]
TYPES = ["","D1","D2","D3","L","BS","GS","DS","B"]
FONT = pygame.font.SysFont("arial",20)

class Room:
    def __init__(self, pos, _type, state):
        self.x = pos[0]
        self.y = pos[1]
        self.biome = _type[0]
        self.roomType = _type[1]
        self.state = state
        
class Door:
    def __init__(self, pos1, pos2, state):
        self.x1 = pos1[0]
        self.y1 = pos1[1]
        self.x2 = pos2[0]
        self.y2 = pos2[1]
        self.state = state

class Map:
    def __init__(self, size, cdr, cdd):
        self.size = size
        self.rooms = []
        self.doors = []
        self.cdr = cdr
        self.cdd = cdd
        self.generate()
    def generate(self):
        for i in range(self.size):
            for j in range(self.size):
                self.rooms.append(Room([i,j],[0,0],True))
        for i in range(self.size):
            for j in range(self.size):
                if i<self.size-1: self.doors.append(Door((i,j),(i+1,j),True))
                if j<self.size-1: self.doors.append(Door((i,j),(i,j+1),True))
        for i in range(self.size**2):
            if self.cdr>random.random():
                self.rooms[i].state=False
        for door in self.doors:
            if self.rooms[door.x1*self.size+door.y1].state==False or self.rooms[door.x2*self.size+door.y2].state==False or self.cdd>random.random():
                door.state = False
    def get_seed(self,spawn):
        output = ""
        output += f"{self.size}.{len(BIOMES)}.{len(TYPES)}.{spawn[0]}.{spawn[1]} "
        for room in self.rooms:
            if room.state:
                con = [0,0,0,0]
                for door in self.doors:
                    if (door.x1==room.x and door.y1==room.y):
                        if door.x2==room.x+1 and door.y2==room.y and door.state: con[3]=1
                        if door.x2==room.x and door.y2==room.y+1 and door.state: con[1]=1
                    if (door.x2==room.x and door.y2==room.y):
                        if door.x1==room.x-1 and door.y1==room.y and door.state: con[2]=1
                        if door.x1==room.x and door.y1==room.y-1 and door.state: con[0]=1
                n = 34+((int("".join([str(i) for i in con]),base=2)*len(BIOMES)*len(TYPES)) + (room.biome*len(TYPES)) + room.roomType)
                if n>126: n+=34
            else:
                n = 33
            output += chr(n)
        return output
                    
screen = pygame.display.set_mode((800,800))
playing = True
mainMap = Map(SIZE,CDR,CDD)
mode = 0

while playing:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            playing = False
        if event.type==pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_m]:
                mode += 1
                if mode>MODES-1: mode=0
        if event.type==pygame.MOUSEBUTTONDOWN:
            mosX, mosY = pygame.mouse.get_pos()
            for room in mainMap.rooms:
                if pygame.Rect(squareSize*(2*room.x+0.5),squareSize*(2*room.y+0.5),squareSize,squareSize).collidepoint(mosX,mosY):
                    if mode==0: room.state = not room.state
                    if mode==1:
                        room.biome += 1
                        if room.biome>len(BIOMES)-1: room.biome=0
                    if mode==2:
                        room.roomType += 1
                        if room.roomType>len(TYPES)-1: room.roomType=0
            for door in mainMap.doors:
                if mainMap.rooms[door.x1*mainMap.size+door.y1].state==False or mainMap.rooms[door.x2*mainMap.size+door.y2].state==False:
                    door.state = False
                elif pygame.Rect(squareSize*(door.x1+door.x2+0.5),squareSize*(door.y1+door.y2+0.5),squareSize,squareSize).collidepoint(mosX,mosY):
                    door.state = not door.state
    squareSize = 800/(mainMap.size*2+1)
    for door in mainMap.doors:
        if door.state:
            pygame.draw.line(screen,(0,0,0),(squareSize*(2*door.x1+1),squareSize*(2*door.y1+1)),(squareSize*(2*door.x2+1),squareSize*(2*door.y2+1)),1)
    for room in mainMap.rooms:
        if room.state: pygame.draw.rect(screen,BIOMES[room.biome],pygame.Rect(squareSize*(2*room.x+0.5),squareSize*(2*room.y+0.5),squareSize,squareSize))
        text = FONT.render(TYPES[room.roomType],True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (squareSize*(2*room.x+1),squareSize*(2*room.y+1))
        screen.blit(text,textRect)
    x = ["Delete/Add Rooms","Change Biome","Change Room Type"]
    text = FONT.render(x[mode]+" [M to Change Mode]",True,(0,0,0))
    textRect = text.get_rect()
    textRect.center = (400,775)
    screen.blit(text,textRect)
    pygame.display.flip()

pygame.quit()
spawn = input("Enter Starting Position: ")
print("Generating Seed...")
print(mainMap.get_seed(spawn.split()))