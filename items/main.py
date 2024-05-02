from items.stuff import Object,Character,Encounter
import items.stuff as stuff, items.settings as settings, pygame
import variables,math
from frontend.prompt import prompt

class Game:
    def __init__(self):
        self.state = "normal"
        self.map = stuff.generateMap(settings.seed)
        self.player = Character(stuff.player, "Jeff")
        self.player.loc = list(self.map.spawn)
        self.player.balance = 100
        self.player.friends = []
        self.player.explored = [False] * 4
        self.encounter = None
    
    def start(self):
        self.player.inv = [Object(stuff.basicSword),Object(stuff.cocaine),None,None,Object(stuff.basicHelmet)]
        self.player.armour = [None,None,None,None]
   
    def update(self, time):
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
            self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome] = True
        if self.state=="fighting":
            if self.encounter.winner:
                self.state = "normal"
                if self.encounter.winner==1:
                    x = self.encounter.endUpdate()
                    self.player = x[0]
                    self.player.friends = x[1]
                    self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters = []
                elif self.encounter.winner==2:
                    self.state = "gameOver"

    def move(self,input1):
        if input1.lower()=="up":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[0]:
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]-1].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[1] -= 1
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[1] -= 1
        elif input1.lower()=="down":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[1]:
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]+1].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[1] += 1
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[1] += 1
        elif input1.lower()=="left":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[2]:
                if self.map.rooms[self.player.loc[0]-1][self.player.loc[1]].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[0] -= 1
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[0] -= 1
        elif input1.lower()=="right":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[3]:
                if self.map.rooms[self.player.loc[0]+1][self.player.loc[1]].biome == self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome:
                    self.player.loc[0] += 1
                elif self.player.explored[self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome]:
                    self.player.loc[0] += 1
        self.update(settings.timeTo["move"])
    
    def pickup(self,input1):
        for i in range(len(self.player.inv)):
            if self.player.inv[i]==None:
                self.player.inv[i] = self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents[int(input1)]
                self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.pop(int(input1))
                break
        self.update(settings.timeTo["pickup"])
    
    def drop(self,input1):
        if int(input1)<5:
            item = self.player.inv[int(input1)]
            self.player.inv[int(input1)] = None
        elif int(input1)>4:
            item = self.player.armour[int(input1)-5]
            self.player.armour[int(input1)-5] = None
        if item:
            self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.append(item)
        self.update(settings.timeTo["drop"])

    def use(self,input1):
        item = self.player.inv[int(input1)]
        if item.type.use[:6]=="armour":
            item2 = self.player.armour[int(item.type.use[6:7])]
            self.player.armour[int(item.type.use[6:7])] = item
            self.player.inv[int(input1)] = item2
        elif item.type.use=="instant":
            if "healing" in item.type.data:
                self.player.hp += item.type.data["healing"]
                maxHp = int(self.player.type.data["health"]*(self.player.skills["constitution"]/100)*(sum([100]+[e.level for e in self.player.effects if e.effect=="constitution"])/100))
                if self.player.hp>maxHp: self.player.hp = maxHp
            if "stamina" in item.type.data:
                self.player.stamina += item.type.data["stamina"]
            self.player.inv[int(input1)].uses -= 1
        elif item.type.use=="effect":
            for eff in item.type.data["effects"]:
                self.player.effects.append(eff.copy())
            self.player.inv[int(input1)].uses -= 1
        self.update(settings.timeTo["use"])
    
    def shopbuy(self,input1):
        item = self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff[int(input1)]
        value = item.value
        if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==settings.rooms["minesBiome"]: value = int(value*0.9)
        if value<=self.player.balance:
            for i in range(len(self.player.inv)):
                if self.player.inv[i]==None:
                    self.player.inv[i] = Object(item)
                    self.player.balance -= value
                    break
        self.update(settings.timeTo["shopb"])

    def shopsell(self,input1):
        item = self.player.inv[int(input1)]
        if "uses" in item.type.data: value = int(item.type.value*item.uses/item.type.data["uses"])
        if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==settings.rooms["minesBiome"]: value = int(value*0.9)
        self.player.inv[int(input1)] = None
        self.player.balance += value
        self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff.append(item.type)
        self.update(settings.timeTo["shops"])
    
    def wait(self, n):
        self.update(int(n))

    def quit(self):
        self.state = None
    
    def get_compass(self):
        roomDis = [999,999]
        for x in self.map.rooms:
            for room in x:
                if room and (room.biome==self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome)and(room.type in settings.rooms["boss"]):
                    new = [room.place[0]-self.player.loc[0],room.place[1]-self.player.loc[1]]
                    if ((new[0]**2)+(new[1]**2))**0.5 < ((roomDis[0]**2)+(roomDis[1]**2))**0.5:
                        roomDis = new
        mag = ((roomDis[0]**2)+(roomDis[1]**2))**0.5
        roomDis[0] /= mag
        roomDis[1] /= mag
        return roomDis

class GameGUI:
    def __init__(self, game:Game, enabled:tuple[bool], filename:str|None, defaultColour:tuple, defaultFont:str) -> None:
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((1200,800),flags=pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.enabled = enabled
        self.time = 0
        self.buttons = []
        self.mode = ["",-1]
        self.filename = filename if filename else ""
        self.defaultColour = defaultColour
        self.defaultFont = defaultFont
        self.chat = [f"Buttons: {'enabled' if self.enabled[0] else 'disabled'}   Chat: {'enabled' if self.enabled[0] else 'disabled'}"] + self.game.start() + ([None]*9) + ["Chat disabled" if not self.enabled[1] else ""]
        self.chatPerson = [2]+([1]*10)
    
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
        img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(self.filename+name),size),rotation)
        pos = list(pos)
        if anchor=="c": pos[0]-=size[0]/2; pos[1]-=size[1]/2
        elif anchor=="l": pos[1]-=size[1]/2
        elif anchor=="r": pos[0]-=size[0]; pos[1]-=size[1]/2
        elif anchor=="t": pos[0]-=size[0]/2
        elif anchor=="tl": pass
        elif anchor=="tr": pos[0]-=size[0]
        self.screen.blit(img, pos)
    
    def button(self, pos:tuple, size:tuple, func, args, anchor:str="c") -> None:
        r = pygame.Rect(0,0,size[0],size[1])
        if anchor=="c": r.center=pos
        elif anchor=="l": r.midleft=pos
        elif anchor=="r": r.midright=pos
        elif anchor=="t": r.midtop=pos
        elif anchor=="tl": r.topleft=pos
        elif anchor=="tr": r.topright=pos
        self.buttons.append((r, func, args))
    
    def switchMode1(self, mode:str) -> None:
        self.mode[0] = mode
        
    def switchMode2(self, mode:int) -> None:
        self.mode[1] = mode
    
    def step(self, events) -> None:
        self.screen.fill((0,0,0))
        for event in events:
            if event.type == pygame.QUIT:
                variables.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button[0].collidepoint(mousePos):
                        if not button[1]: pass
                        elif button[3]:
                            self.chat[-1] = button[1](button[2])
                            self.chatPerson.append(1)
                            self.chat.append(""); self.chat.append("")
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
        if self.game.state=="fighting": option = ["friends","enemies","chat"]
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
            for i in range(3):
                skills = ["constitution","dexterity","strength"]
                colours = [(220,0,0),(0,0,220),(220,220,0)]
                self.text(skills[i],20,(700,i*75+530),anchor="tl")
                self.text(f"+{self.game.player.skills[skills[i]]-100}%",20,(1150,i*75+530),colour=colours[i],anchor="tr")
                self.rect((700,i*75+560),((self.game.player.skills[skills[i]]-100)*450/100,35),colour=colours[i],anchor="tl")
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
                                str(self.game.player.skills["constitution"]),
                                str(self.game.player.skills["dexterity"]),
                                str(self.game.player.skills["strength"]),
                                str(self.game.player.effects[0].name) if len(self.game.player.effects)>0 else "None",
                                str(self.game.player.effects[1].name) if len(self.game.player.effects)>1 else "",
                                str(self.game.player.effects[2].name) if len(self.game.player.effects)>2 else "",]
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
                        if self.enabled[0]:
                            for i in range(2):
                                text = ["use","drop"]
                                func = [self.game.use if (self.mode[1]<5 and item.type.use!="weapon") else None,self.game.drop]
                                args = [self.mode[1],self.mode[1]]
                                self.rect((i*200+325,440),(150,50),width=5)
                                self.text(text[i],20,(i*200+325,440),colour=(0,60,0) if not func[i] else None)
                                self.button((i*200+325,440),(150,50),func[i],args[i],True)
            if self.mode[0]=="room":
                room = self.game.map.rooms[self.game.player.loc[0]][self.game.player.loc[1]]
                for i in range(3):
                    text1 = ["biome","room","shop availible"]
                    text2 = [settings.biomeNames[room.biome],settings.roomNames[room.type],str(room.type in settings.rooms["shop"])]
                    biomeCol = [None,(200,0,0),(0,0,200),(150,150,0)]
                    col = [biomeCol[room.biome],None,settings.currencyCol]
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
                for i in range(2):
                    text = ["buy","sell"]
                    if self.mode[1]==i: self.rect((i*190+505,190),(150,50),colour=(0,60,0))
                    self.rect((i*190+505,190),(150,50),width=5)
                    self.text(text[i],20,(i*190+505,190))
                    self.button((i*190+505,190),(150,50),self.switchMode2,i,False)
                self.text(f"balance: {self.game.player.balance}{settings.currencySym}",20,(600,220),colour=settings.currencyCol,anchor="t")
                if self.mode[1]==-1:
                    self.text("Select an option",20,(600,315))
                if self.mode[1]==0:
                    if room.type in settings.rooms["shop"]:
                        for i in range(len(room.shopStuff)):
                            value = room.shopStuff[i].value
                            if room.type == settings.rooms["minesBiome"]: value = int(value*0.9)
                            self.text(f"{i}. {room.shopStuff[i].name}",20,(250,i*30+250),colour=room.shopStuff[i].rarity.colour,anchor="tl")
                            self.text(f"{value}{settings.currencySym}",20,(800,i*30+250),colour=room.shopStuff[i].rarity.colour,anchor="tr")
                            self.rect((900,i*30+265),(100,20),colour=room.shopStuff[i].rarity.colour)
                            if self.enabled[0]: self.button((900,i*30+265),(100,20),self.game.shopbuy,i,True)
                        if room.type == settings.rooms["minesBiome"]: self.text("10% discount (mines biome)",20,(600,i*30+280),anchor="t")
                    else: self.text("You are not currently in a shop",20,(600,315))
                if self.mode[1]==1:
                    if room.type in settings.rooms["shop"]:
                        for i in range(5):
                            item = self.game.player.inv[i]
                            if item:
                                if "uses" in item.type.data: value = int(item.type.value*item.uses/item.type.data["uses"])
                                else: value = item.type.value
                                if room.type == settings.rooms["minesBiome"]: value = int(value*0.9)
                                self.text(f"{i}. {item.type.name}",20,(250,i*30+250),colour=item.type.rarity.colour,anchor="tl")
                                self.text(f"{value}{settings.currencySym}",20,(800,i*30+250),colour=item.type.rarity.colour,anchor="tr")
                                self.rect((900,i*30+265),(100,20),colour=item.type.rarity.colour)
                                if self.enabled[0]: self.button((900,i*30+265),(100,20),self.game.shopsell,i,True)
                            else:
                                self.text(f"{i}. None",20,(250,i*30+250),colour=(0,60,0),anchor="tl")
                                self.text(f"--{settings.currencySym}",20,(800,i*30+250),colour=(0,60,0),anchor="tr")
                    else: self.text("You are not currently in a shop",20,(600,315))
            if self.mode[0]=="map":
                pass
            if self.mode[0]=="compass":
                x,y = self.game.getCompass()
                rot = 0
                self.image("compass.png",(600,315),(300,300),rot)
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
                else:
                    self.text(str(i),16,(i*125+307,628),anchor="tl")
                self.rect((i*125+350,675),(100,100),width=5)
                
            if self.mode[0]=="enemies":
                for i in range(4):
                    if len(self.game.encounter.enemyTeam)>i:
                        enemy = self.game.encounter.enemyTeam[i]
                        self.image(enemy.type.img,(282,75*i+202.5),(64,64))
                        self.text(f"{enemy.type.name} [{i}]",20,(330,75*i+175),anchor="tl")
                        maxHp = int(enemy.type.data["health"]*(enemy.skills["constitution"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="constitution"])/100))
                        self.rect((330,75*i+210),((enemy.hp/maxHp)*150,15),colour=(220,0,0),anchor="tl")
                        self.text(str(enemy.hp),16,(490,75*i+217.5),colour=(220,0,0),anchor="l")
                    if len(self.game.encounter.enemyTeam)>i+4:
                        enemy = self.game.encounter.enemyTeam[i+4]
                        self.image(enemy.type.img,(682,75*i+202.5),(64,64))
                        self.text(f"{enemy.type.name} [{i+4}]",20,(730,75*i+175),anchor="tl")
                        maxHp = int(enemy.type.data["health"]*(enemy.skills["constitution"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="constitution"])/100))
                        self.rect((730,75*i+210),((enemy.hp/maxHp)*150,15),colour=(220,0,0),anchor="tl")
                        self.text(str(enemy.hp),16,(890,75*i+217.5),colour=(220,0,0),anchor="l")
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
        if self.game.state==None:
           variables.running = False
        self.time += self.clock.get_time()
        self.clock.tick()
        pygame.display.flip()
        return self.screen

if __name__ == "__main__":
    game = GameGUI(Game())
    game.run()