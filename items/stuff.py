import random,settings

class Effect:
    def __init__(self, name:str, effect:str, level:int, time:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level
        self.time = time
    def copy(self):
        return Effect(self.name, self.effect, self.level, self.time)

str20 = Effect("Strength I", "strength", 20, 3)
str100 = Effect("Strength V", "strength", 100, 3)
dex20 = Effect("Dexterity I", "dexterity", 20, 3)
dex100 = Effect("Dexterity V", "dexterity", 100, 3)
pro10 = Effect("Protection I", "protection", 10, 3)
pro50 = Effect("Protection V", "protection", 50, 3)
potion00 = Effect("Strength III", "strength", 50, 3)
potion01 = Effect("Slowness I", "dexterity", -10, 3)
potion10 = Effect("Protection III", "protection", 30, 3)
potion11 = Effect("Weakness II", "strength", -50, 3)
potion20 = Effect("Invisibility", "dexterity", 100, 3)
burningEff = Effect("Burning", "health", -10, 10)
bleedingEff = Effect("Bleeding", "health", -5, 10)
blindingEff = Effect("Blinding", "dexterity", -40, 5)




class Enchantment:
    def __init__(self, name:str, effect:str, level:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level

burning = Enchantment("Curse of Burning", burningEff, 1)
bleeding = Enchantment("Curse of Bleeding", bleedingEff, 1)
blinding = Enchantment("Curse of Blinding", blindingEff, 1)





class Rarity:
    def __init__(self, name:str, colour:tuple) -> None:
        self.name = name
        self.colour = colour
    def __str__(self) -> str:
        return self.name

common = Rarity("common",(110,110,110))
uncommon = Rarity("uncommon",(0,150,0))
rare = Rarity("rare",(0,50,220))
epic = Rarity("epic",(100,0,220))
legendary = Rarity("legendary",(220,100,0))
mythic = Rarity("mythic",(150,150,0))





class ObjectType:
    def __init__(self, name:str, image:str, rarity:Rarity, use:str, value:int|float, data:dict) -> None:
        self.name = name
        self.img = image
        self.rarity = rarity
        self.use = use
        self.value = value
        self.data = data

class Object:
    def __init__(self, _type:ObjectType) -> None:
        self.type = _type
        if "uses" in self.type.data:
            self.uses = self.type.data["uses"]
    
potionHeal1 = ObjectType("Basic Healing Potion", "test.jpg", rare, "instant", 20, {"uses":1,"healing":30,"enchamntments":[],"effects":[]})
potionHeal2 = ObjectType("Basic Healing Potion", "test.jpg", rare, "instant", 50, {"uses":3,"healing":30,"enchamntments":[],"effects":[]})
potionHeal3 = ObjectType("Basic Healing Potion", "test.jpg", epic, "instant", 90, {"uses":5,"healing":30,"enchamntments":[],"effects":[]})
potionHeal4 = ObjectType("Full Healing Potion", "test.jpg", legendary, "instant", 175, {"uses":1,"healing":500,"enchamntments":[],"effects":[]})
potionHeal5 = ObjectType("True Healing Potion", "test.jpg", mythic, "instant", 150, {"uses":1,"constitution":25,"enchamntments":[],"effects":[]})
potionDamage1 = ObjectType("Basic Rage Potion", "test.jpg", rare, "effect", 20, {"uses":1,"enchamntments":[],"effects":[str20]})
potionDamage2 = ObjectType("Basic Rage Potion", "test.jpg", rare, "effect", 50, {"uses":3,"enchamntments":[],"effects":[str20]})
potionDamage3 = ObjectType("Basic Rage Potion", "test.jpg", epic, "effect", 90, {"uses":5,"enchamntments":[],"effects":[str20]})
potionDamage4 = ObjectType("Full Rage Potion", "test.jpg", legendary, "effect", 175, {"uses":1,"enchamntments":[],"effects":[str100]})
potionDamage5 = ObjectType("True Rage Potion", "test.jpg", mythic, "instant", 150, {"uses":1,"strength":25,"enchamntments":[],"effects":[]})
potionSpeed1 = ObjectType("Basic Speed Potion", "test.jpg", rare, "effect", 20, {"uses":1,"enchamntments":[],"effects":[dex20]})
potionSpeed2 = ObjectType("Basic Speed Potion", "test.jpg", rare, "effect", 50, {"uses":3,"enchamntments":[],"effects":[dex20]})
potionSpeed3 = ObjectType("Basic Speed Potion", "test.jpg", epic, "effect", 90, {"uses":5,"enchamntments":[],"effects":[dex20]})
potionSpeed4 = ObjectType("Full Speed Potion", "test.jpg", legendary, "effect", 175, {"uses":1,"enchamntments":[],"effects":[dex100]})
potionSpeed5 = ObjectType("True Flight Potion", "test.jpg", mythic, "instant", 150, {"uses":1,"dexterity":25,"enchamntments":[],"effects":[]})
potionCrystal1 = ObjectType("Basic Crystal Skin Potion", "test.jpg", rare, "effect", 20, {"uses":1,"enchamntments":[],"effects":[pro10]})
potionCrystal2 = ObjectType("Basic Crystal Skin Potion", "test.jpg", rare, "effect", 50, {"uses":3,"enchamntments":[],"effects":[pro10]})
potionCrystal3 = ObjectType("Basic Crystal Skin Potion", "test.jpg", epic, "effect", 90, {"uses":5,"enchamntments":[],"effects":[pro10]})
potionCrystal4 = ObjectType("Full Crystal Skin Potion", "test.jpg", legendary, "effect", 175, {"uses":1,"enchamntments":[],"effects":[pro50]})
#potionCrystal5 = ObjectType("True Crystal Skin Potion", "test.jpg", mythic, "instant", 150, {"uses":1,"enchamntments":[],"effects":[]})
potionStrength = ObjectType("Strength Potion", "test.jpg", epic, "effect", 100, {"uses":5,"enchamntments":[],"effects":[potion00,potion01]})
potionScalene = ObjectType("Scalene Skin Potion", "test.jpg", epic, "effect", 100, {"uses":5,"enchamntments":[],"effects":[potion10,potion11]})
potionInvisibility = ObjectType("Invisibility Potion", "test.jpg", legendary, "effect", 150, {"uses":1,"enchamntments":[],"effects":[potion20]})






class CharacterType:
    def __init__(self, name:str, image:str, data:dict) -> None:
        self.name = name
        self.img = image
        self.data = data
    def __str__(self) -> str:
        return f"CharacterType({self.name}, {self.data})"

class Character:
    def __init__(self, _type:CharacterType, name:str|None=None) -> None:
        self.type = _type
        if name==None: self.name=self.type.name
        else: self.name=name
        self.inv = []
        if "inventory" in self.type.data:
            for i in range(self.type.data["invSize"]):
                if random.random()<self.type.data["invChance"]: self.inv.append(Object(self.type.data["inventory"][i]))
        self.hp = self.type.data["health"]
        self.stamina = 0
        self.armour = [None,None,None,None]
        self.effects = []
        self.skills = {"constitution":100,"dexterity":100,"strength":100}

player = CharacterType("Player", "c0.jpg", {"health":200,"attack":20,"defense":15,"staminaRate":20})
##





class Encounter:
    def __init__(self, team1:list[Character], team2:list[Character]) -> None:
        self.playerTeam = team1
        for char in self.playerTeam:
            char.team = 1
        self.enemyTeam = team2
        for char in self.enemyTeam:
            char.team = 2
        self.people = team1+team2
        random.shuffle(self.people)
        self.playerSelected = 0
        self.time = -1
        self.winner = None
    def update(self, _input:list[str]) -> str:
        output = []
        validInput = True
        if not _input:
            pass
        elif _input[0]=="use":
            if -3<int(_input[1])<5: self.playerSelected = int(_input[1])
            else: validInput = False
        elif _input[0] in ["wait","skip"]:
            self.playerSelected = -2
        else:
            validInput = False
        if not validInput:
            output += [f"Invalid Input, automatically using slot {self.playerSelected}"]
        if self.time==-1:
            output += ["You get caught in a fight!"]
            output += ["Enter to continue"]
            self.time += 1
        else:
            while True:
                self.time += 1
                for char in self.people:
                    if char.type.name=="Player": slot = self.playerSelected
                    elif char.inv==[]: slot = -1
                    else: slot = random.randint(0,len(char.inv)-1)
                    char.hp += sum([e.level for e in char.effects if e.effect=="health"])
                    maxHp = int(char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100))
                    if char.hp>maxHp: char.hp = maxHp
                    for eff in char.effects[:]:
                        eff.time -= 1
                        if eff.time <= 0:
                            char.effects.remove(eff)
                    if (slot==-1 or char.inv[slot]==None) and slot!=-2:
                        if char.stamina>char.type.data["staminaRate"]*3:
                            for enemy in self.people:
                                if char.team != enemy.team:
                                    if random.random()<(enemy.skills["dexterity"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="dexterity"])/100)*(enemy.type.data["defense"]/100):
                                        output += [f"{char.name} tries to attack but {enemy.name} dodges!"]
                                    else:
                                        damage = char.type.data["attack"]
                                        prot = sum(sum(e.level for e in a.type.data["enchantments"] if e.effect=="protect")+a.type.data["protection"] for a in enemy.armour if a)
                                        if prot>40: prot=40
                                        damage -= int((prot/100)*damage)
                                        damage = int(damage*char.skills["strength"]/100)
                                        output += [f"{char.name} attacks {enemy.name}! (-{damage}HP)"]
                                        enemy.hp -= damage
                                        char.stamina -= char.type.data["staminaRate"]*3
                    elif slot!=-2 and ("stamina" not in char.inv[slot].type.data or char.stamina>char.inv[slot].type.data["stamina"]):
                        if char.inv[slot].type.use=="weapon":
                            for enemy in self.people:
                                if char.team != enemy.team:
                                    if random.random()<char.inv[slot].type.data["hitRate"]/100:
                                        if random.random()<(enemy.skills["dexterity"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="dexterity"])/100)*(enemy.type.data["defense"]/100):
                                            output += [f"{char.name} tries to attack but {enemy.name} dodges!"]
                                        else:
                                            damage = char.inv[slot].type.data["attack"]
                                            prot = sum(sum(e.level for e in a.type.data["enchantments"] if e.effect=="protect")+a.type.data["protection"] for a in enemy.armour if a)
                                            if prot>40: prot=40
                                            damage -= int((prot/100)*damage)
                                            damage = int(damage*char.skills["strength"]/100)
                                            output += [f"{char.name} attacks {enemy.name} with a {char.inv[slot].type.name}! (-{damage}HP)"]
                                            if any([ench.effect=="steal" for ench in char.inv[slot].type.data["enchantments"]]):
                                                x = [ench for ench in char.inv[slot].type.data["enchantments"] if ench.effect=="steal"]
                                                output += [f"{char.name} uses {x[0].name} to steal health!"]
                                                char.hp += int((x[0].level/100)*damage)
                                            enemy.hp -= damage
                                            char.stamina -= char.inv[slot].type.data["stamina"]
                                            for ench in char.inv[slot].type.data["enchantments"]:
                                                if isinstance(ench.effect, Effect):
                                                    enemy.effects.append(ench.effect)
                                            if "uses" in char.inv[slot].type.data:
                                                char.inv[slot].uses -= 1
                                    else:
                                        output += [f"{char.name} tries to attack {enemy.name} but misses!"]
                        elif char.inv[slot].type.use=="instant":
                            output += [f"{char.name} uses {char.inv[slot].type.name}"]
                            if "healing" in char.inv[slot].type.data:
                                char.hp += char.inv[slot].type.data["healing"]
                                maxHp = int(char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100))
                                if char.hp>maxHp: char.hp = maxHp
                            if "stamina" in char.inv[slot].type.data:
                                char.stamina += char.inv[slot].type.data["stamina"]
                            for skill in char.skills:
                                if skill in char.inv[slot].type.data:
                                    char.skills[skill] += char.inv[slot].type.data[skill]
                            char.inv[slot].uses -= 1
                        elif char.inv[slot].type.use=="effect":
                            output += [f"{char.name} uses {char.inv[slot].type.name}"]
                            for eff in char.inv[slot].type.data["effects"]:
                                char.effects.append(eff.copy())
                            char.inv[slot].uses -= 1
                    char.stamina += char.type.data["staminaRate"]
                    for eff in char.effects[:]:
                            if any([e!=eff and e.effect==eff.effect and e.time>=eff.time for e in char.effects]): char.effects.remove(eff)
                    for item in char.inv:
                        if item and "uses" in item.type.data and item.uses<1:
                            char.inv[char.inv.index(item)] = None
                leave = False
                for char in self.people:
                    if char.hp <= 0:
                        output += [f"{char.name} has fallen!"]
                        if char.type.name=="Player":
                            output += ["You lost the battle!"]
                            self.winner = 2
                            leave = True
                        self.people.remove(char)
                if sum([1 for c in self.people if c.team==2])==0 and not self.winner:
                    output += ["You have won the battle!"]
                    output += ["Enter to continue"]
                    self.winner = 1
                    leave = True
                p = next(iter([c for c in self.people if c.type.name=="Player"]),None)
                if p and any([p.stamina>item.type.data["stamina"] for item in p.inv if (item!=None and item.type.use=="weapon")]):
                    leave = True
                if leave:
                    if not self.winner:
                        output += ["Your Turn"]
                    break
        return output
    def endUpdate(self) -> tuple[str|Character|list]:
        for char in self.people:
            if char.type.name=="Player":
                x = char
                self.people.remove(char)
        return x, self.people





class Room:
    def __init__(self, place:tuple[int], biome:int, _type:int, connections:tuple[int]) -> None:
        self.place = place
        self.biome = biome
        self.type = _type
        self.connections = connections
        self.seen = False
        self.contents = []
        self.characters = []
        self.shopStuff = []
    def copy(self):
        return Room(self.place, self.biome, self.type, self.connections)
    def __str__(self) -> str:
        return f"Room({self.place},{self.biome},{self.type},{self.connections})"

class Map:
    def __init__(self, size:int, spawn:tuple[int]) -> None:
        self.size = size
        self.spawn = spawn
        self.rooms = [[None for x in range(size)] for y in range(size)]
    def update(self, loc:tuple[int], info:tuple[int]):
        self.rooms[loc[0]][loc[1]] = Room(loc,info[0],info[1],info[2])
    def print(self) -> str:
        for i in self.rooms:
            for j in i:
                print(j)

def generateMap(x:str) -> Map:
    stuff,seed = x.split()
    size,biomes,types,sx,sy = [int(i) for i in stuff.split(".")]
    output = Map(size,(sx,sy))
    for i in range(size**2):
        n = ord(seed[i])
        if n>126: n-=68
        else: n-=34
        if n>-1:
            con = [int(j) for j in bin(n//(biomes*types))[2:]]
            if len(con)<4: con = tuple([0]*(4-len(con))+con)
            else: con = tuple(con)
            room = updateRoom(Room((i//size,i%size),(n//types%biomes),(n%types),con))
            output.rooms[i//size][i%size] = room
    return output

def updateRoom(room:Room) -> Room:
    if room.type==1:
        characters = random.choice([[],[]])
        #room.characters = [Character(i) for i in random.choices(characters, weights=(), k=random.randint())]
    elif room.type==2:
        characters = random.choice([[],[]])
        #room.characters = [Character(i) for i in random.choices(characters, weights=(), k=random.randint())]
    elif room.type==3:
        characters = random.choice([[],[]])
        #room.characters = [Character(i) for i in random.choices(characters, weights=(), k=random.randint())]
    elif room.type==4:
        objects = []
        #room.shopStuff = [i for i in random.choices(objects, k=random.randint())]
        #room.shopStuff = list(dict.fromkeys(room.shopStuff))
    elif room.type==5:
        objects = []
        #room.shopStuff = [i for i in random.choices(objects, k=random.randint())]
        #room.shopStuff = list(dict.fromkeys(room.shopStuff))
    elif room.type==6:
        objects = []
        #room.shopStuff = [i for i in random.choices(objects, k=random.randint())]
        #room.shopStuff = list(dict.fromkeys(room.shopStuff))
    return room