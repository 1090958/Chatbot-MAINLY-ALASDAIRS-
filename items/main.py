from items.stuff import Object,Character,Encounter
import items.stuff as stuff, items.settings as settings, pygame
import variables, frontend.settings as resolution, math
from frontend.prompt import prompt
def remapMouse(mousePosition:list[int,int]):
    # adjust for the difference between the openGL display and the pygame render surface
    # the render surface is always 256*3 (768) on the x axis and is 1:1 aspect ratio
    # only scale factor is needed
    resolutionCoefficient = (256*3)/resolution.resolution[0]

    #apply the scale factor
    mousePosition=[mousePosition[0]*resolutionCoefficient, mousePosition[1]*resolutionCoefficient]
    
    
    # Made a remap function for legibility
    def remap(val, old:tuple[float|int,float|int], new:tuple[float|int,float|int]):
        return (new[1] - new[0])*(val - old[0]) / (old[1] - old[0]) + new[0]
    
    #remap the x, adjusting the values when necessary
    mousePosition[0] = remap(mousePosition[0],(36,36 + 1200*0.58),(0,1200))
    mousePosition[1] = remap(mousePosition[1],(35,35 + 800*0.58),(0,800))
    
    
    #
    return mousePosition



class Game:
    def __init__(self):
        self.state = "normal"
        self.map = stuff.generateMap(settings.seed)
        self.player = Character(stuff.player, "Jeff")
        self.player.loc = list(self.map.spawn)
        self.player.balance = 200
        self.player.friends = []
        self.player.explored = [False] * 4
        self.encounter = None
    
    def start(self):
        self.player.inv = [Object(stuff.sword02),Object(stuff.armour01),None,None,None]
        self.player.armour = [None,None,None,None]
        return ["Welcome to the dungon! You've got a lot to learn young warrior.",
                "As you explore this dark, dangerous world you'll find that the world is",
                "controlled by 4 main forces. Your goal is to defeat these 4 gods:",
                "Fayre, Alexander, Gabriel and Lux.",
                "We've brought you here to defeat these gods.",
                "I can't explain much more, but I've given you a compass to show you",
                "the way to each boss, only fight them when you are ready."]
   
    def update(self, time):
        output = []
        self.map.rooms[self.player.loc[0]][self.player.loc[1]].seen = True
        for char in [self.player]+self.player.friends:
            char.hp += sum([e.level for e in char.effects if e.effect=="health"])
            maxHp = char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100)
            if char.hp>maxHp: char.hp = maxHp
            for eff in char.effects[:]:
                eff.time -= time
                if eff.time <= 0:
                    char.effects.remove(eff)
            for eff in char.effects[:]:
                if any([e!=eff and e.effect==eff.effect and e.time>=eff.time for e in char.effects]): char.effects.remove(eff)
            for item in char.inv:
                if item and "uses" in item.type.data and item.uses<1:
                    char.inv[self.player.inv.index(item)] = None
        if (self.map.rooms[self.player.loc[0]][self.player.loc[1]].type in settings.rooms["fighting"]) and self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters!=[]:
            self.state = "fighting"
            self.encounter = Encounter([self.player]+self.player.friends, self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters)
            output += self.encounter.update([])
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].type in settings.rooms["boss"]:
                self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome] = True
        if self.state=="fighting":
            if self.encounter.winner:
                self.state = "normal"
                if self.encounter.winner==1:
                    x = self.encounter.endUpdate()
                    self.player = x[0]
                    self.player.friends = x[1]
                    self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters = []
                    self.player.balance += 50
                    [self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.append(item) for item in x[2]]
                elif self.encounter.winner==2:
                    self.state = None
        if all(self.player.explored):
            self.state = None
        return output

    def move(self,input1):
        output = []
        moved = False
        if input1.lower()=="up":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[0]:
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]-1].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[1] -= 1
                    moved = True
                    output += [f"moved {input1.lower()}"]
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[1] -= 1
                    moved = True
                    output += [f"Moved {input1.lower()}"]
                else:
                    output += [f"!!!Couldn't move: Must defeat boss of the biome you are in"]
                    return output
            else:
                output += [f"!!!Couldn't move: No pathway"]
                return output
        elif input1.lower()=="down":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[1]:
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]+1].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[1] += 1
                    moved = True
                    output += [f"Moved {input1.lower()}"]
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[1] += 1
                    moved = True
                    output += [f"Moved {input1.lower()}"]
                else:
                    output += [f"!!!Couldn't move: Must defeat boss of the biome you are in"]
                    return output
            else:
                output += [f"!!!Couldn't move: No pathway"]
                return output
        elif input1.lower()=="left":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[2]:
                if self.map.rooms[self.player.loc[0]-1][self.player.loc[1]].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[0] -= 1
                    moved = True
                    output += [f"Moved {input1.lower()}"]
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[0] -= 1
                    moved = True
                    output += [f"Moved {input1.lower()}"]
                else:
                    output += [f"!!!Couldn't move: Must defeat boss of the biome you are in"]
                    return output
            else:
                output += [f"!!!Couldn't move: No pathway"]
                return output
        elif input1.lower()=="right":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[3]:
                if self.map.rooms[self.player.loc[0]+1][self.player.loc[1]].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[0] += 1
                    moved = True
                    output += [f"Moved {input1.lower()}"]
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[0] += 1
                    moved = True
                    output += [f"Moved {input1.lower()}"]
                else:
                    output += [f"!!!Couldn't move: Must defeat boss of the biome you are in"]
                    return output
            else:
                output += [f"!!!Couldn't move: No pathway"]
                return output
        else:
            output += [f"!!!Invalid input"]
            return output
        if moved:
            output += [f"You found a {settings.roomNames[self.map.rooms[self.player.loc[0]][self.player.loc[1]].type]}"]
            if len(self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents)>0:
                output += [f"You found a {len(self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents)} items in the room"]
            if len(self.map.rooms[self.player.loc[0]][self.player.loc[1]].entries)>0:
                output += [f"You found a diary entry in the room"]
        return output + self.update(settings.timeTo["move"])
    
    def pickup(self,input1):
        output = []
        for i in range(len(self.player.inv)):
            if self.player.inv[i]==None:
                self.player.inv[i] = self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents[int(input1)]
                self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.pop(int(input1))
                output += [f"You picked up {self.player.inv[i].type.name}"]
                break
        if i==len(self.player.inv)-1:
            output += [f"!!!Couldn't pickup item: No space in inventory"]
            return output
        return output + self.update(settings.timeTo["pickup"])
    
    def drop(self,input1):
        output = []
        if int(input1)<5:
            item = self.player.inv[int(input1)]
            self.player.inv[int(input1)] = None
        elif int(input1)>4:
            item = self.player.armour[int(input1)-5]
            self.player.armour[int(input1)-5] = None
        if item:
            self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.append(item)
            output += [f"You dropped {item.type.name}"]
        return output + self.update(settings.timeTo["drop"])

    def use(self,input1):
        output = []
        item = self.player.inv[int(input1)]
        if item.type.use[:6]=="armour":
            item2 = self.player.armour[int(item.type.use[6:7])]
            self.player.armour[int(item.type.use[6:7])] = item
            self.player.inv[int(input1)] = item2
            output += [f"You equipped your {item.type.name}"]
        elif item.type.use=="instant":
            if "healing" in item.type.data:
                self.player.hp += item.type.data["healing"]
                maxHp = int(self.player.type.data["health"]*(self.player.skills["constitution"]/100)*(sum([100]+[e.level for e in self.player.effects if e.effect=="constitution"])/100))
                if self.player.hp>maxHp: self.player.hp = maxHp
            if "stamina" in item.type.data:
                self.player.stamina += item.type.data["stamina"]
            for skill in self.player.skills:
                if skill in item.type.data:
                    self.player.skills[skill] += item.type.data[skill]
            self.player.inv[int(input1)].uses -= 1
            output += [f"You used your {item.type.name}"]
        elif item.type.use=="effect":
            for eff in item.type.data["effects"]:
                self.player.effects.append(eff.copy())
            self.player.inv[int(input1)].uses -= 1
            output += [f"You used your {item.type.name}"]
        else:
            output += [f"Couldn't use item: Item unusable"]
            return output
        return output + self.update(settings.timeTo["use"])
    
    def shopbuy(self,input1):
        output = []
        if self.map.rooms[self.player.loc[0]][self.player.loc[1]].type in settings.rooms["shop"]:
            item = self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff[int(input1)]
            value = item.value
            if value<=self.player.balance:
                for i in range(len(self.player.inv)):
                    if self.player.inv[i]==None:
                        self.player.inv[i] = Object(item)
                        self.player.balance -= value
                        output += [f"You bought {item.name}"]
                        return output + self.update(settings.timeTo["shopb"])
                if i==len(self.player.inv)-1:
                    output += [f"!!!Couldn't buy item: No space in inventory"]
        else:
            output += [f"!!!Couldn't buy: Not in shop"]
        return output

    def shopsell(self,input1):
        output = []
        item = self.player.inv[int(input1)]
        room = self.map.rooms[self.player.loc[0]][self.player.loc[1]]
        if room.type in settings.rooms["shop"]:
            if "uses" in item.type.data: value = int(item.type.value*item.uses/item.type.data["uses"])
            else: value = item.type.value
            self.player.inv[int(input1)] = None
            self.player.balance += int(value*stuff.random.randint(92,100)/100)
            if item.type not in room.shopStuff: room.shopStuff.append(item.type)
            output += [f"You sold your {item.type.name}"]
            return output + self.update(settings.timeTo["shops"])
        else:
            output += [f"!!!Couldn't sell: not in shop"]
            return output
    
    def wait(self, n):
        try:
            return [f"You waited for {int(n)*10}s"] + self.update(int(n))
        except:
            return["Invalid Input"]

    def quit(self):
        self.state = None
        return ["!!!game exited"]
    
    def getCompass(self):
        roomDis = [0,-999]
        for x in self.map.rooms:
            for room in x:
                if room and (room.biome==self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome)and(room.type in settings.rooms["boss"]):
                    new = [room.place[0]-self.player.loc[0],room.place[1]-self.player.loc[1]]
                    if ((new[0]**2)+(new[1]**2))**0.5 < ((roomDis[0]**2)+(roomDis[1]**2))**0.5:
                        roomDis = new
        mag = ((roomDis[0]**2)+(roomDis[1]**2))**0.5
        if mag==0: return [0,-1]
        roomDis[0] /= mag
        roomDis[1] /= mag
        return roomDis
    
    def help(self):
        return"""                    Help:
    
                    OUT OF COMBAT

move [up,down,left,right] move in the specified direction


                    IN COMBAT@
                    
wait       wait for a turn@

use [item number]
The item number is shown in the toolbar and you can click on the item to use it as well.



    
    """
    
    def takeInput(self, _input):
        try:
            if self.state=="normal":
                if not _input:
                    return []
                if _input.split()[0]=="move":
                    return self.move(_input.split()[1])
                elif _input.split()[0]=="pickup":
                    return self.pickup(_input.split()[1])
                elif _input.split()[0]=="drop":
                    return self.drop(_input.split()[1])
                elif _input.split()[0]=="use":
                    return self.use(_input.split()[1])
                elif _input.split()[0]=="buy":
                    return self.shopbuy(_input.split()[1])
                elif _input.split()[0]=="sell":
                    return self.shopsell(_input.split()[1])
                elif _input.split()[0]=="wait":
                    return self.wait(_input.split()[1])
                elif _input.split()[0]=="quit":
                    return self.quit()
                else:
                    return [f"!!!Invalid input"]
            elif self.state=="fighting":
                if self.encounter.winner:
                    self.state = "normal"
                    if self.encounter.winner==1:
                        x = self.encounter.endUpdate()
                        self.player = x[0]
                        self.player.friends = x[1]
                        self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters = []
                        self.player.balance += 50
                        [self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.append(item) for item in x[2]]
                        return [f"!!!You won the battle"]
                    elif self.encounter.winner==2:
                        return self.quit()
                else: return self.encounter.update(_input.split())
        except:
            return [f"!!!Something went wrong"]

def generate_map(map_,size:tuple[int,int] = (36,24), spacing:tuple[int,int] = (5,4), line_width:int = 1, colour = (255, 255, 255)):
    surface = pygame.surface.Surface((size[0]*map_.size,size[1]*map_.size), pygame.SRCALPHA)

    # generate rooms
    for y in range(map_.size):
        for x in range(map_.size):
            if map_.rooms[x][y]:
                
                
                #draw the room
                
                pygame.draw.rect(surface,colour,pygame.rect.Rect((x*size[0]+spacing[0],y*size[1]+spacing[1]),(size[0]-spacing[0]*2,size[1]-spacing[1]*2)))
                pygame.draw.rect(surface,(0,0,0,0),pygame.rect.Rect((x*size[0]+spacing[0]+line_width,y*size[1]+spacing[1]+line_width),(size[0]-spacing[0]*2-line_width*2,size[1]-spacing[1]*2 - line_width*2)))
                
                #draw the room icon
                
                #blacksmith
                if settings.roomNames[map_.rooms[x][y].type]=="Blacksmith":
                    surface.blit(pygame.image.load('images/room_icons/black_smith_v2.png'), (x*size[0]+spacing[0]*1.4,y*size[1]+spacing[1]*1.4))
                #general shop
                elif settings.roomNames[map_.rooms[x][y].type]=="General Shop":
                    surface.blit(pygame.image.load('images/room_icons/general_shop.png'), (x*size[0]+spacing[0]*1.4,y*size[1]+spacing[1]*1.4))
                #library
                elif settings.roomNames[map_.rooms[x][y].type]=="Library":
                    surface.blit(pygame.image.load('images/room_icons/library.png'), (x*size[0]+spacing[0]*1.4,y*size[1]+spacing[1]*1.4))
                elif settings.roomNames[map_.rooms[x][y].type]=="Boss Fight":
                    surface.blit(pygame.image.load('images/room_icons/boss_fight.png'), (x*size[0]+spacing[0]*1.4,y*size[1]+spacing[1]*1.4))
                # for each connecting room:
                # upwards
                if map_.rooms[x][y].connections[0]:
                    # get the top_left room
                    top_left_position = (x*size[0]+spacing[0],(y-1)*size[1]+spacing[1] + size[1]-spacing[1]*2)
                    
                    
                    new_top_left = (top_left_position[0] + (size[0] - spacing[0]*2)/3, top_left_position[1])
                    new_spacing = (spacing[0]*2, spacing[1]*2)
                    
                    pygame.draw.rect(surface,colour,pygame.rect.Rect(new_top_left,new_spacing))
                    pygame.draw.rect(surface,(0,0,0,0),pygame.rect.Rect((new_top_left[0]+line_width,new_top_left[1]),(new_spacing[0] - line_width * 2, new_spacing[1])))
                    
                #leftwards
                if map_.rooms[x][y].connections[2]:
                    # get the top_left room
                    top_left_position = ((x-1)*size[0]+spacing[0] + size[0]-spacing[0]*2,y*size[1]+spacing[1] )
                    
                    
                    new_top_left = (top_left_position[0], top_left_position[1]+ (size[1] - spacing[1]*2)/3)
                    new_spacing = (spacing[0]*2, spacing[1]*2)
                    pygame.draw.rect(surface,colour,pygame.rect.Rect(new_top_left,new_spacing))
                    pygame.draw.rect(surface,(0,0,0,0),pygame.rect.Rect((new_top_left[0],new_top_left[1]+line_width),(new_spacing[0], new_spacing[1] - line_width*2)))
                pass
            else:
                pass
    return surface

class gui_map:
    def __init__(self, game:Game):
        self.game:Game = game
        self.range = 2
        
        self.size = (72, 48)
        self.spacing = (10,8)
        self.line_width = 2
        self.map:pygame.surface.Surface = generate_map(game.map, self.size, self.spacing, self.line_width)
        self.old_pos = self.game.player.loc
        self.scaled_map =self.map
        self.cropped = self.map
    def render(self):
        if self.range ==3:
            cropped_area = [(self.game.player.loc[0]-self.range+1)*self.size[0]+self.spacing[0],
                        (self.game.player.loc[1]-self.range+1)*self.size[1]+self.spacing[1],
                        
                        (self.size[0]-self.spacing[0])*(self.range*2-1)+self.spacing[0]*self.range,
                        (self.size[1]-self.spacing[1])*(self.range*2-1)+self.spacing[1]*self.range
            ]
        else:
            cropped_area = [(self.game.player.loc[0]-self.range+1)*self.size[0]+self.spacing[0],
                        (self.game.player.loc[1]-self.range+1)*self.size[1]+self.spacing[1],
                        
                        (self.size[0]-self.spacing[0])*(self.range*2-1)+self.spacing[0],
                        (self.size[1]-self.spacing[1])*(self.range*2-1)+self.spacing[1]
            ]
        output = pygame.surface.Surface((cropped_area[-2], cropped_area[-1]), pygame.SRCALPHA) #had an unknown splicing error here
        output.blit(self.scaled_map, (0,0), cropped_area)
        return output
        
class GameGUI:
    def __init__(self, game:Game, enabled:tuple[bool], filename:str|None = "frontend/", defaultColour:tuple[int,int,int] = (0,255,0), defaultFont:str = "font_minecraft.ttf") -> None:
        pygame.init()
        self.game = game
        self.screen = pygame.surface.Surface((1200,800),flags=pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.enabled = enabled
        self.time = 0
        self.buttons = []
        self.mode = ["",-1]
        self.filename = filename if filename else ""
        self.defaultColour = defaultColour
        self.defaultFont = defaultFont
        self.chat = ([None]*2) + [f"Buttons: {'enabled' if self.enabled[0] else 'disabled'}   Chat: {'enabled' if self.enabled[0] else 'disabled'}"] + self.game.start() + [None,"Chat disabled" if not self.enabled[1] else ""]
        self.chatPerson = [0,0,2,1,1,1,1,1,1,1,0]
        stuff.loadImages(filename+"images/")
        self.guiMap = gui_map(self.game)
        #player_character
        self.motion = 'move1'
        self.anim_move1=pygame.transform.scale_by(pygame.image.load('images\move1.png'),4)
        self.anim_move2=pygame.transform.scale_by(pygame.image.load('images\move2.png'),4)
    
    def text(self, text:str|int, size:int, pos:tuple, font:str="font_minecraft.ttf", colour:tuple|None=None, anchor:str="c") -> None:
        if not colour: colour=self.defaultColour
        f = pygame.font.Font(self.filename+font,size)
        x = f.render(str(text),True,colour)
        r = x.get_rect()
        if anchor=="c": r.center=pos
        elif anchor=="l": r.midleft=pos
        elif anchor=="r": r.midright=pos
        elif anchor=="t": r.midtop=pos
        elif anchor=="tl": r.topleft=pos
        elif anchor=="tr": r.topright=pos
        elif anchor=="bl": r.bottomleft=pos
        elif anchor=="br": r.bottomright=pos
        self.screen.blit(x, r)
    
    def rect(self, pos:tuple, size:tuple, colour:tuple|None=None, width:int=0, anchor:str="c") -> None:
        if not colour: colour=self.defaultColour
        r = pygame.Rect(0,0,size[0],size[1])
        if anchor=="c": r.center=pos
        elif anchor=="l": r.midleft=pos
        elif anchor=="r": r.midright=pos
        elif anchor=="t": r.midtop=pos
        elif anchor=="tl": r.topleft=pos
        elif anchor=="tr": r.topright=pos
        pygame.draw.rect(self.screen, colour, r, width)
    
    def image(self, name:str, pos:tuple, size:tuple, rotation:int=0, anchor:str="c") -> None:
        img = pygame.transform.scale(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(self.filename+"images/"+name),(300,300)),rotation),size)
        pos = list(pos)
        if anchor=="c": pos[0]-=size[0]/2; pos[1]-=size[1]/2
        elif anchor=="l": pos[1]-=size[1]/2
        elif anchor=="r": pos[0]-=size[0]; pos[1]-=size[1]/2
        elif anchor=="t": pos[0]-=size[0]/2
        elif anchor=="tl": pass
        elif anchor=="tr": pos[0]-=size[0]
        self.screen.blit(img, pos)
    
    def button(self, pos:tuple, size:tuple, func, args, retrunVar:bool, anchor:str="c") -> None:
        r = pygame.Rect(pos[0],pos[1],size[0],size[1])
        if anchor=="c": r.center=pos
        elif anchor=="l": r.midleft=pos
        elif anchor=="r": r.midright=pos
        elif anchor=="t": r.midtop=pos
        elif anchor=="tl": r.topleft=pos
        elif anchor=="tr": r.topright=pos
        self.buttons.append((r, func, args,retrunVar))
    
    def switchMode1(self, mode:str) -> None:
        self.mode[0] = mode
        
    def switchMode2(self, mode:int) -> None:
        self.mode[1] = mode
    
    def step(self, events) -> None:
        self.screen.fill((0))
        if self.game.state==None:
            variables.running = False
            return self.screen
        for event in events:
            if event.type == pygame.QUIT:
                variables.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                mousePos = remapMouse(mousePos)
                for button in self.buttons:
                    if button[0].collidepoint(mousePos):
                        if not button[1]: pass
                        elif button[3]:
                            self.chat.pop()
                            for msg in button[1](button[2]):
                                self.chatPerson.append(1)
                                self.chat.append(msg)
                            self.chat.append(""); self.chatPerson.append(0); self.chat.append("")
                        else: button[1](button[2])
            if event.type == pygame.KEYDOWN:
                if self.mode[0]=="chat" and self.enabled[1]:
                    if event.key == pygame.K_RETURN:
                        _input = self.chat[-1]
                        response = self.game.takeInput(_input)
                        self.chatPerson.append(0)
                        [self.chat.append(msg[3:]) for msg in response if msg and msg[:3]=="!!!"]
                        [self.chat.append(msg) for msg in response if msg and msg[:3]!="!!!"]
                        [self.chatPerson.append(2) for msg in response if msg and msg[:3]=="!!!"]
                        [self.chatPerson.append(1) for msg in response if msg and msg[:3]!="!!!"]
                        self.chat.append(""); self.chatPerson.append(1)
                        self.chat.append("")
                    elif event.key == pygame.K_BACKSPACE:
                        self.chat[-1] = self.chat[-1][:-1]
                    else:
                        self.chat[-1] += event.unicode
        self.buttons = []
        self.chat = self.chat[-12:]
        self.chatPerson = self.chatPerson[-11:]
        pygame.draw.line(self.screen, self.defaultColour, (0,30), (1200,30), 5)
        pygame.draw.line(self.screen, self.defaultColour, (0,130), (1200,130), 5)
        pygame.draw.line(self.screen, self.defaultColour, (0,500), (1200,500), 5)
        pygame.draw.line(self.screen, self.defaultColour, (200,130), (200,500), 5)
        pygame.draw.line(self.screen, self.defaultColour, (1000,130), (1000,500), 5)
        self.text(f"state: {self.game.state}",20,(50,0),anchor="tl")
        self.text(f"mode: {self.mode[0]}",20,(250,0),anchor="tl")
        self.text(f"fps: {int(self.clock.get_fps()*100)/100}",20,(450,0),anchor="tl")
        self.text(f"seedInfo: {settings.seed.split()[0]}",20,(600,0),anchor="tl")
        self.text(f"time: {self.time}ms",20,(850,0),anchor="tl")
        if self.game.state=="normal": option = ["player","items","room","actions","map","compass","chat"]
        if self.game.state=="fighting": option = ["player","items","friends","enemies","chat"]
        for i in range(len(option)):
            if option[i]==self.mode[0]: self.rect((140*i+600-(len(option)*70-70),80),(120,50),colour=(0,60,0))
            self.rect((140*i+600-(len(option)*70-70),80),(120,50),width=5)
            self.text(option[i],20,(140*i+600-(len(option)*70-70),80),colour=None)
            self.button((140*i+600-(len(option)*70-70),80),(120,50),self.switchMode1,option[i],False)
            self.button((140*i+600-(len(option)*70-70),80),(120,50),self.switchMode2,-1,False)
        if self.game.state=="normal":
            for i in range(5):
                if self.game.player.inv[i]:
                    self.rect((i*125+100,700),(100,100),colour=self.game.player.inv[i].type.rarity.colour)
                    self.image(self.game.player.inv[i].type.img,(i*125+100,700),(64,64))
                    self.text(str(i),16,(i*125+57,653),colour=(0,0,0),anchor="tl")
                    self.button((i*125+100,700),(100,100),self.switchMode1,"items",False)
                    self.button((i*125+100,700),(100,100),self.switchMode2,i,False)
                else:
                    self.text(str(i),16,(i*125+57,653),anchor="tl")
                self.rect((i*125+100,700),(100,100),width=5)
            for i in range(4):
                if self.game.player.armour[i]:
                    self.rect((i*125+100,575),(100,100),colour=self.game.player.armour[i].type.rarity.colour)
                    self.image(self.game.player.armour[i].type.img,(i*125+100,575),(64,64))
                    self.text(f"a{i}",16,(i*125+57,528),colour=(0,0,0),anchor="tl")
                    self.button((i*125+100,575),(100,100),self.switchMode1,"items",False)
                    self.button((i*125+100,575),(100,100),self.switchMode2,i+5,False)
                else:
                    self.text(f"a{i}",16,(i*125+57,528),anchor="tl")
                self.rect((i*125+100,575),(100,100),width=5)
            self.rect((i*125+225,575),(100,100),width=5)
            self.image("c0.png",(i*125+225,575),(64,64))
            self.image("c1.png",(i*125+225,575),(64,64))
            self.text("c",16,(i*125+182,528),anchor="tl")
            self.button((i*125+225,575),(100,100),self.switchMode1,"compass",False)
            self.button((i*125+225,575),(100,100),self.switchMode2,-1,False)
            for i in range(3):
                skills = ["constitution","dexterity","strength"]
                colours = [(220,0,0),(0,0,220),(220,220,0)]
                n = int(self.game.player.skills[skills[i]]*sum([100]+[e.level for e in self.game.player.effects if e.effect==skills[i]])/100)-100
                self.text(skills[i],20,(700,i*75+530),anchor="tl")
                self.text(f"+{n}%",20,(1150,i*75+530),colour=colours[i],anchor="tr")
                self.rect((700,i*75+560),(n*450/100,35)if n<=100 else (450,35),colour=colours[i],anchor="tl")
                self.rect((700,i*75+560),(450,35),anchor="tl",width=5)
            if self.mode[0]=="player":
                maxHp = int(self.game.player.type.data["health"]*(self.game.player.skills["constitution"]/100)*(sum([100]+[e.level for e in self.game.player.effects if e.effect=="constitution"])/100))
                self.rect((250,190),((self.game.player.hp/maxHp)*700,50),colour=(220,0,0),anchor="l")
                self.rect((600,190),(700,50),width=5)
                self.text("health",20,(250,220),colour=(220,0,0),anchor="tl")
                self.text(f"{self.game.player.hp}HP / {maxHp}HP",20,(950,220),colour=(220,0,0),anchor="tr")
                for i in range(7):
                    text1 = ["balance","constitution","dexterity","strength","effects","",""]
                    text2 = [f"{self.game.player.balance}{settings.currencySym}",
                                str(int(self.game.player.skills["constitution"]*sum([100]+[e.level for e in self.game.player.effects if e.effect=="constitution"])/100)),
                                str(int(self.game.player.skills["dexterity"]*sum([100]+[e.level for e in self.game.player.effects if e.effect=="dexterity"])/100)),
                                str(int(self.game.player.skills["strength"]*sum([100]+[e.level for e in self.game.player.effects if e.effect=="strength"])/100)),
                                f"{self.game.player.effects[0].name} ({self.game.player.effects[0].time//6}:{self.game.player.effects[0].time%6}0)" if len(self.game.player.effects)>0 else "None",
                                f"{self.game.player.effects[1].name} ({self.game.player.effects[1].time//6}:{self.game.player.effects[1].time%6}0)" if len(self.game.player.effects)>1 else "",
                                f"{self.game.player.effects[2].name} ({self.game.player.effects[2].time//6}:{self.game.player.effects[2].time%6}0)" if len(self.game.player.effects)>2 else "",]
                    col = [settings.currencyCol,(220,0,0),(0,0,220),(220,220,0),settings.effectCol,settings.effectCol,settings.effectCol]
                    self.text(text1[i],20,(250,i*30+250),colour=col[i],anchor="tl")
                    self.text(text2[i],20,(950,i*30+250),colour=col[i],anchor="tr")
            if self.mode[0]=="items":
                if self.mode[1]==-1:
                    self.text("Select an Item",20,(600,315))
                else: 
                    if self.mode[1]<5: item = self.game.player.inv[self.mode[1]]
                    if self.mode[1]>4: item = self.game.player.armour[self.mode[1]-5]
                    if not item:
                        self.text("Select an Item",20,(600,315))
                    else:
                        self.rect((800,315),(300,300),colour=item.type.rarity.colour)
                        self.image(item.type.img,(800,315),(256,256))
                        self.rect((800,315),(300,300),width=5)
                        text = []
                        text.append(f"{item.type.name} (x{item.uses})" if "uses" in item.type.data else str(item.type.name))
                        text.append(f"     [{item.type.rarity.name}]")
                        text.append(f"     [{item.type.use}]")
                        if "attack" in item.type.data: text.append(f"     [attack: {item.type.data['attack']}]")
                        if "hitRate" in item.type.data: text.append(f"     [hitRate: {item.type.data['hitRate']}]")
                        if "stamina" in item.type.data: text.append(f"     [stamina: {item.type.data['stamina']}]")
                        if "healing" in item.type.data: text.append(f"     [healing: {item.type.data['healing']}]")
                        if "protection" in item.type.data: text.append(f"     [protection: {item.type.data['protection']}]")
                        if "constitution" in item.type.data: text.append(f"     [constitution: {item.type.data['constitution']}]")
                        if "dexterity" in item.type.data: text.append(f"     [dexterity: {item.type.data['dexterity']}]")
                        if "strength" in item.type.data: text.append(f"     [strength: {item.type.data['strength']}]")
                        if len(item.type.data["enchantments"])>0: text.append(f"ench: {item.type.data['enchantments'][0].name}")
                        if len(item.type.data["enchantments"])>1: text.append(f"ench: {item.type.data['enchantments'][1].name}")
                        if len(item.type.data['effects'])>0: text.append(f"eff: {item.type.data['effects'][0].name}")
                        if len(item.type.data['effects'])>1: text.append(f"eff: {item.type.data['effects'][1].name}")
                        for i in range(len(text)):
                            if i==0: col = item.type.rarity.colour
                            elif text[i][:4]=="ench": col = settings.enchantmentCol
                            elif text[i][:3]=="eff": col = settings.effectCol
                            else: col = None
                            self.text(text[i],20,(250,i*25+165),colour=col,anchor="tl")
                        if self.enabled[0]:
                            for i in range(2):
                                text = ["use","drop"]
                                func = [self.game.use if (self.mode[1]<5 and item.type.use not in ["weapon","secret"]) else None,self.game.drop]
                                args = [self.mode[1],self.mode[1]]
                                self.rect((i*200+325,440),(150,50),width=5)
                                self.text(text[i],20,(i*200+325,440),colour=(0,60,0) if not func[i] else None)
                                self.button((i*200+325,440),(150,50),func[i],args[i],True)
            if self.mode[0]=="room":
                room = self.game.map.rooms[self.game.player.loc[0]][self.game.player.loc[1]]
                for i in range(3):
                    text1 = ["biome","room","shop availible"]
                    text2 = [settings.biomeNames[room.biome],settings.roomNames[room.type],str(room.type in settings.rooms["shop"])]
                    col = [None,None,settings.currencyCol]
                    self.text(text1[i],20,(250,i*30+165),colour=col[i],anchor="tl")
                    self.text(text2[i],20,(950,i*30+165),colour=col[i],anchor="tr")
                for i in range(5):
                    if len(room.contents)>i:
                        self.rect((i*125+300,415),(100,100),colour=room.contents[i].type.rarity.colour)
                        self.image(room.contents[i].type.img,(i*125+300,415),(64,64))
                        self.text(f"r{i}",16,(i*125+257,368),colour=(0,0,0),anchor="tl")
                        if self.enabled[0]: self.button((i*125+300,415),(100,100),self.game.pickup,i,True)
                        self.rect((i*125+300,415),(100,100),width=5)
                if len(room.contents)==0:
                    self.text("There are no items in the room",20,(600,415))
            if self.mode[0]=="actions":
                room = self.game.map.rooms[self.game.player.loc[0]][self.game.player.loc[1]]
                for i in range(3):
                    text = ["buy","sell","library"]
                    if self.mode[1]==i: self.rect((i*190+410,190),(150,50),colour=(0,60,0))
                    self.rect((i*190+410,190),(150,50),width=5)
                    self.text(text[i],20,(i*190+410,190))
                    self.button((i*190+410,190),(150,50),self.switchMode2,i,False)
                if self.mode[1]==-1:
                    self.text("Select an option",20,(600,315))
                if self.mode[1]==0:
                    self.text(f"balance: {self.game.player.balance}{settings.currencySym}",20,(600,220),colour=settings.currencyCol,anchor="t")
                    if room.type in settings.rooms["shop"]:
                        for i in range(len(room.shopStuff)):
                            value = room.shopStuff[i].value
                            self.text(f"{i}. {room.shopStuff[i].name}",20,(250,i*30+250),colour=room.shopStuff[i].rarity.colour,anchor="tl")
                            self.text(f"{value}{settings.currencySym}",20,(800,i*30+250),colour=room.shopStuff[i].rarity.colour,anchor="tr")
                            self.rect((900,i*30+265),(100,20),colour=room.shopStuff[i].rarity.colour)
                            if self.enabled[0]: self.button((900,i*30+265),(100,20),self.game.shopbuy,i,True)
                    else: self.text("You are not currently in a shop",20,(600,315))
                if self.mode[1]==1:
                    self.text(f"balance: {self.game.player.balance}{settings.currencySym}",20,(600,220),colour=settings.currencyCol,anchor="t")
                    if room.type in settings.rooms["shop"]:
                        for i in range(5):
                            item = self.game.player.inv[i]
                            if item:
                                if "uses" in item.type.data: value = int(item.type.value*item.uses/item.type.data["uses"])
                                else: value = item.type.value
                                self.text(f"{i}. {item.type.name}",20,(250,i*30+250),colour=item.type.rarity.colour,anchor="tl")
                                self.text(f"{value}{settings.currencySym}",20,(800,i*30+250),colour=item.type.rarity.colour,anchor="tr")
                                self.rect((900,i*30+265),(100,20),colour=item.type.rarity.colour)
                                if self.enabled[0]: self.button((900,i*30+265),(100,20),self.game.shopsell,i,True)
                            else:
                                self.text(f"{i}. None",20,(250,i*30+250),colour=(0,60,0),anchor="tl")
                                self.text(f"--{settings.currencySym}",20,(800,i*30+250),colour=(0,60,0),anchor="tr")
                    else: self.text("You are not currently in a shop",20,(600,315))
                if self.mode[1]==2:
                    if room.type in settings.rooms["library"]:
                        if len(room.entries)==0: self.text("There is nothing found in this library",20,(600,315))
                        else:
                            for i in range(10):
                                prompt(room.entries[0])
                    else: self.text("You are not currently in a libary",20,(600,315))
            if self.mode[0]=="map":
                self.screen.blit(pygame.transform.scale_by(self.guiMap.render(),2.3),(300,160))
                pos = (495,280)
                if self.time%1000>500:
                    self.screen.blit(self.anim_move1,pos)
                else:
                    self.screen.blit(self.anim_move2,pos)
            if self.mode[0]=="compass":
                x,y = self.game.getCompass()
                rot = math.degrees(math.atan2(-y,x))-90
                self.image("c0.png",(600,315),(300,300))
                self.image("c1.png",(600,315),(300,300),rot)
            if self.mode[0]=="chat":
                for i in range(len(self.chat)-1):
                    colours = [(0,200,0),(0,200,200),(200,200,0)]
                    if self.chat[i]:
                        if self.chatPerson[i]==0: self.text(f">>> {self.chat[i]}",16,(250,i*24+165),colour=colours[0],anchor="tl")
                        elif self.chatPerson[i]==1: self.text(f"{self.chat[i]}",16,(250,i*24+165),colour=colours[1],anchor="tl")
                        elif self.chatPerson[i]==2: self.text(f"{self.chat[i]}",16,(250,i*24+165),colour=colours[2],anchor="tl")
                self.text(f">>> {self.chat[-1]}{'|' if self.time%1000>=500 and self.enabled[1] else ''}",20,(250,465),anchor="bl")
        if self.game.state=="fighting":
                maxHp = int(self.game.player.type.data["health"]*(self.game.player.skills["constitution"]/100)*(sum([100]+[e.level for e in self.game.player.effects if e.effect=="constitution"])/100))
                self.rect((300,550),((self.game.player.hp/maxHp)*600,50),colour=(220,0,0),anchor="l")
                for i in range(10):
                    maxStam = max([item.type.data["stamina"] for item in self.game.player.inv if item and "stamina" in item.type.data],default=0)
                    if maxStam==0: maxStam=0.001
                    self.rect((i*62.5+300,560),(37.5,10),colour=(220,0,220) if (self.game.player.stamina/maxStam)>=(i+1)/10 else (0,0,0),anchor="tl")
                self.rect((600,550),(600,50),width=5)
                self.text(f"Health: {self.game.player.hp}",20,(300,580),colour=(220,0,0),anchor="tl")
                self.text(f"Stamina: {self.game.player.stamina}",20,(900,580),colour=(220,0,220),anchor="tr")
                for i in range(5):
                    if self.game.player.inv[i]:
                        self.rect((i*125+350,675),(100,100),colour=self.game.player.inv[i].type.rarity.colour)
                        self.image(self.game.player.inv[i].type.img,(i*125+350,675),(64,64))
                        self.text(str(i),16,(i*125+307,628),colour=(0,0,0),anchor="tl")
                        self.text(f"{self.game.player.stamina}/{self.game.player.inv[i].type.data['stamina'] if 'stamina' in self.game.player.inv[i].type.data else 0}",20,(i*125+350,730),colour=(220,0,220),anchor="t")
                        self.button((i*125+350,675),(100,100),self.switchMode1,"items",False)
                        self.button((i*125+350,675),(100,100),self.switchMode2,i,False)
                    else:
                        self.text(str(i),16,(i*125+307,628),anchor="tl")
                    self.rect((i*125+350,675),(100,100),width=5)
                if self.mode[0]=="player":
                    maxHp = int(self.game.player.type.data["health"]*(self.game.player.skills["constitution"]/100)*(sum([100]+[e.level for e in self.game.player.effects if e.effect=="constitution"])/100))
                    self.rect((250,190),((self.game.player.hp/maxHp)*700,50),colour=(220,0,0),anchor="l")
                    self.rect((600,190),(700,50),width=5)
                    self.text("health",20,(250,220),colour=(220,0,0),anchor="tl")
                    self.text(f"{self.game.player.hp}HP / {maxHp}HP",20,(950,220),colour=(220,0,0),anchor="tr")
                    for i in range(7):
                        text1 = ["balance","constitution","dexterity","strength","effects","",""]
                        text2 = [f"{self.game.player.balance}{settings.currencySym}",
                                 str(self.game.player.skills["constitution"]),
                                 str(self.game.player.skills["dexterity"]),
                                 str(self.game.player.skills["strength"]),
                                 f"{self.game.player.effects[0].name} ({self.game.player.effects[0].time//6}:{self.game.player.effects[0].time%6}0)" if len(self.game.player.effects)>0 else "None",
                                 f"{self.game.player.effects[1].name} ({self.game.player.effects[1].time//6}:{self.game.player.effects[1].time%6}0)" if len(self.game.player.effects)>1 else "",
                                 f"{self.game.player.effects[2].name} ({self.game.player.effects[2].time//6}:{self.game.player.effects[2].time%6}0)" if len(self.game.player.effects)>2 else "",]
                        col = [settings.currencyCol,(220,0,0),(0,0,220),(220,220,0),settings.effectCol,settings.effectCol,settings.effectCol]
                        self.text(text1[i],20,(250,i*30+250),colour=col[i],anchor="tl")
                        self.text(text2[i],20,(950,i*30+250),colour=col[i],anchor="tr")
                if self.mode[0]=="items":
                    if self.mode[1]==-1:
                        self.text("Select an Item",20,(600,315))
                    else: 
                        if self.mode[1]<5: item = self.game.player.inv[self.mode[1]]
                        if self.mode[1]>4: item = self.game.player.armour[self.mode[1]-5]
                        if not item:
                            self.text("Select an Item",20,(600,315))
                        else:
                            self.rect((800,315),(300,300),colour=item.type.rarity.colour)
                            self.image(item.type.img,(800,315),(256,256))
                            self.rect((800,315),(300,300),width=5)
                            text = []
                            text.append(f"{item.type.name} (x{item.uses})" if "uses" in item.type.data else str(item.type.name))
                            text.append(f"     [{item.type.rarity.name}]")
                            text.append(f"     [{item.type.use}]")
                            if "attack" in item.type.data: text.append(f"     [attack: {item.type.data['attack']}]")
                            if "hitRate" in item.type.data: text.append(f"     [hitRate: {item.type.data['hitRate']}]")
                            if "stamina" in item.type.data: text.append(f"     [stamina: {item.type.data['stamina']}]")
                            if "healing" in item.type.data: text.append(f"     [healing: {item.type.data['healing']}]")
                            if "protection" in item.type.data: text.append(f"     [protection: {item.type.data['protection']}]")
                            if len(item.type.data["enchantments"])>0: text.append(f"ench: {item.type.data['enchantments'][0].name}")
                            if len(item.type.data["enchantments"])>1: text.append(f"ench: {item.type.data['enchantments'][1].name}")
                            if len(item.type.data['effects'])>0: text.append(f"eff: {item.type.data['effects'][0].name}")
                            if len(item.type.data['effects'])>1: text.append(f"eff: {item.type.data['effects'][1].name}")
                            for i in range(len(text)):
                                if i==0: col = item.type.rarity.colour
                                elif text[i][:4]=="ench": col = settings.enchantmentCol
                                elif text[i][:3]=="eff": col = settings.effectCol
                                else: col = None
                                self.text(text[i],20,(250,i*25+165),colour=col,anchor="tl")
                            if self.enabled[0] and not self.game.encounter.winner and "armour" not in item.type.use:
                                self.rect((325,440),(150,50),width=5)
                                self.text("use",20,(325,440))
                                self.button((325,440),(150,50),self.game.encounter.update,["use",str(self.mode[1])],True)
                if self.mode[0]=="friends":
                    for i in range(4):
                        if len(self.game.encounter.playerTeam)>i:
                            char = self.game.encounter.playerTeam[i]
                            if char.hp>0:
                                self.image(char.type.img,(282,75*i+202.5),(64,64))
                                self.text(f"{char.name} ({char.type.name}) [{i}]",20,(330,75*i+175),anchor="tl")
                                maxHp = int(char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100))
                                self.rect((330,75*i+210),((char.hp/maxHp)*150,15),colour=(220,0,0),anchor="tl")
                                self.text(str(char.hp),16,(490,75*i+217.5),colour=(220,0,0),anchor="l")
                                self.rect((550,75*i+210),((char.stamina/100)*150 if char.stamina<100 else 150,15),colour=(220,0,220),anchor="tl")
                                self.text(str(char.stamina),16,(710,75*i+217.5),colour=(220,0,220),anchor="l")
                                if len(char.effects)==0: self.text("No effects",16,(770,75*i+217.5),colour=settings.effectCol,anchor="l")
                                elif len(char.effects)==1: self.text(f"{char.effects[0].name}",16,(770,75*i+217.5),colour=settings.effectCol,anchor="l")
                                else: self.text(f"{len(char.effects)} effects",16,(770,75*i+217.5),colour=settings.effectCol,anchor="l")
                            else:
                                self.rect((282,75*i+202.5),(64,64),colour=(0,60,0))
                                self.text(f"Character Died",20,(330,75*i+175),colour=(0,60,0),anchor="tl")
                        pygame.draw.line(self.screen,self.defaultColour,(200,75*i+165),(1000,75*i+165),width=5)
                    pygame.draw.line(self.screen,self.defaultColour,(200,75*i+240),(1000,75*i+240),width=5)
                if self.mode[0]=="enemies":
                    for i in range(4):
                        if len(self.game.encounter.enemyTeam)>i:
                            enemy = self.game.encounter.enemyTeam[i]
                            if enemy.hp>0:
                                self.image(enemy.type.img,(282,75*i+202.5),(64,64))
                                self.text(f"{enemy.type.name} [{i}]",20,(330,75*i+175),anchor="tl")
                                maxHp = int(enemy.type.data["health"]*(enemy.skills["constitution"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="constitution"])/100))
                                self.rect((330,75*i+210),((enemy.hp/maxHp)*150,15),colour=(220,0,0),anchor="tl")
                                self.text(str(enemy.hp),16,(490,75*i+217.5),colour=(220,0,0),anchor="l")
                            else:
                                self.rect((282,75*i+202.5),(64,64),colour=(0,60,0))
                                self.text(f"Enemy Died",20,(330,75*i+175),colour=(0,60,0),anchor="tl")
                        if len(self.game.encounter.enemyTeam)>i+4:
                            enemy = self.game.encounter.enemyTeam[i+4]
                            if enemy.hp>0:
                                self.image(enemy.type.img,(682,75*i+202.5),(64,64))
                                self.text(f"{enemy.type.name} [{i+4}]",20,(730,75*i+175),anchor="tl")
                                maxHp = int(enemy.type.data["health"]*(enemy.skills["constitution"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="constitution"])/100))
                                self.rect((730,75*i+210),((enemy.hp/maxHp)*150,15),colour=(220,0,0),anchor="tl")
                                self.text(str(enemy.hp),16,(890,75*i+217.5),colour=(220,0,0),anchor="l")
                            else:
                                self.text(f"Enemy Died",20,(330,75*i+175),colour=(0,60,0),anchor="tl")
                        pygame.draw.line(self.screen,self.defaultColour,(200,75*i+165),(1000,75*i+165),width=5)
                    pygame.draw.line(self.screen,self.defaultColour,(200,75*i+240),(1000,75*i+240),width=5)
                if self.mode[0]=="chat":
                    for i in range(len(self.chat)-1):
                        colours = [(0,200,0),(0,200,200),(200,200,0)]
                        if self.chat[i]:
                            if self.chatPerson[i]==0: self.text(f">>> {self.chat[i]}",16,(250,i*24+165),colour=colours[0],anchor="tl")
                            elif self.chatPerson[i]==1: self.text(f"{self.chat[i]}",16,(250,i*24+165),colour=colours[1],anchor="tl")
                            elif self.chatPerson[i]==2: self.text(f"{self.chat[i]}",16,(250,i*24+165),colour=colours[2],anchor="tl")
                    self.text(f">>> {self.chat[-1]}{'|' if self.time%1000>=500 and self.enabled[1] else ''}",20,(250,465),anchor="bl")
        
        self.time += self.clock.get_time()
        self.clock.tick()
        
        return self.screen
