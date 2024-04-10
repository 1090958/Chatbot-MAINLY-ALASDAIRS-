import random,settings

class Effect:
    def __init__(self, name:str, effect:str, level:int, time:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level
        self.time = time

con1 = Effect("Health Boost I","constitution",10,10)
dex1 = Effect("Heightened Reflexes I","dexterity",10,10)





class Enchantment:
    def __init__(self, name:str, effect:str, level:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level

prot1 = Enchantment("Protection I","protect",6)
prot2 = Enchantment("Protection II","protect",10)





class Rarity:
    def __init__(self, name:str, colour:str|None=None) -> None:
        self.name = name
        self.colour = colour
    def __str__(self) -> str:
        return self.name

common = Rarity("Common")
uncommon = Rarity("Uncommon")
rare = Rarity("Rare")
sub_mythic = Rarity("Sub-Mythic",settings.subMythicCol)
mythic = Rarity("Mythic",settings.mythicCol)
special = Rarity("Special",settings.specialCol)





class ObjectType:
    def __init__(self, name:str, rarity:Rarity, use:str, value:int|float, data:dict) -> None:
        self.name = name
        self.rarity = rarity
        self.use = use
        self.value = value
        self.data = data
    def __str__(self) -> str:
        return f"ObjectType({self.name}, {self.rarity}, {self.data})"

class Object:
    def __init__(self, _type:ObjectType) -> None:
        self.type = _type
        if "uses" in self.type.data:
            self.uses = self.type.data["uses"]
    def __str__(self) -> str:
        x = ""
        if self.type.rarity.colour != None:
            x += f"\033{self.type.rarity.colour}  - {self.type.name} [{self.type.rarity}] \033[0m"
        else:
            x += f"  - {self.type.name} [{self.type.rarity}]"
        for enchant in self.type.data["enchantments"]:
            x += f"\n\033{settings.enchantmentCol}      - {enchant} \033[0m"
        for effect in self.type.data["effects"]:
            x += f"\n\033{settings.effectCol}      - {effect} \033[0m"
        return x

basicSword = ObjectType("Basic Sword", common, "weapon", 20, {"attack":25,"speed":3,"hitRate":90,"enchantments":[],"effects":[]})
basicHelmet = ObjectType("Basic Helmet", uncommon, "armour0", 30, {"protection":10,"enchantments":[],"effects":[]})
enchIronLeggings = ObjectType("Enchanted Iron Chestplate", rare, "armour2", 140, {"protection":80,"enchantments":[prot1],"effects":[]})
coolChestplate = ObjectType("Cool Chestplate", special, "armour1", 140, {"protection":100,"enchantments":[prot2],"effects":[]})
cocaine = ObjectType("Cocaine", rare, "effectPosi", 75, {"uses":5,"enchantments":[],"effects":[dex1]})





class CharacterType:
    def __init__(self, name:str, data:dict) -> None:
        self.name = name
        self.data = data
    def __str__(self) -> str:
        return f"CharacterType({self.name}, {self.data})"

class Character:
    def __init__(self, _type:CharacterType, name:str|None=None, inventory:list[Object|None]=[None,None,None,None,None]) -> None:
        self.type = _type
        if name==None: self.name=self.type.name
        else: self.name=name
        self.inv = inventory
        self.hp = self.type.data["health"]
        self.armour = [None,None,None,None]
        self.effects = []
        self.skills = {"constitution":100,"dexterity":100,"strength":100,"intelligence":100}
    def __str__(self) -> str:
        pass

player = CharacterType("Player", {"health":200,"attack":20,"defense":10,"speed":3})
npc = CharacterType("Default NPC", {"health":150,"attack":10,"defense":10,"speed":3})
goblin = CharacterType("Goblin", {"health":30,"attack":7,"defense":10,"speed":2})





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
        self.playerselected = 0
        self.time = -1
        self.winner = None
    def update(self, input1:str) -> str:
        output = ""
        if self.time==-1:
            output += ("You get caught in a fight! \n")
            output += ("Enemies: \n")
            for enemy in self.enemyTeam:
                output += (f"  - {enemy.name} ({enemy.type.name}) \n")
            output += ("Your Team: \n")
            for char in self.playerTeam:
                output += (f"  - {char.name} ({char.type.name}) \n")
            output += ("Enter commands any time in the battle: ")
            self.time += 1
        else:
            event = False
            while not event:
                self.time += 1
                for char in self.people:
                    if char.type.name=="Player": slot = self.playerselected
                    else: slot = 0
                    for eff in char.effects:
                        eff.time -= 1
                        if eff.time <= 0:
                            char.effects.remove(eff)
                    if char.hp <= 0:
                        event = True
                        output += (f"{char.name} has fallen! \n")
                        if char.type.name=="Player":
                            output += ("You lost the battle! \n")
                            self.winner = 2
                        self.people.remove(char)
                    elif char.inv[slot]==None:
                        if self.time%char.type.data["speed"]==0:
                            event = True
                            for enemy in self.people:
                                if char.team != enemy.team:
                                    if random.random()<(enemy.skills["dexterity"]/100)*(enemy.type.data["defense"]/100):
                                        output += (f"{char.name} tries to attack but {enemy.name} dodges! \n")
                                    else:
                                        damage = char.type.data["attack"]
                                        output += (f"{char.name} attacks {enemy.name}! (-{damage}HP) \n")
                                        enemy.hp -= damage
                    elif self.time%char.inv[slot].type.data["speed"]==0:
                        event = True
                        for enemy in self.people:
                            if char.team != enemy.team:
                                if random.random()<char.inv[slot].type.data["hitRate"]/100:
                                    if random.random()<(enemy.skills["dexterity"]/100)*(enemy.type.data["defense"]/100):
                                        output += (f"{char.name} tries to attack but {enemy.name} dodges! \n")
                                    else:
                                        damage = char.inv[slot].type.data["attack"]
                                        if char.inv[slot].type.rarity.colour: output += (f"{char.name} attacks {enemy.name} with a \033{char.inv[slot].type.rarity.colour}{char.inv[slot].type.name}\033[0m! (-{damage}HP) \n")
                                        else: output += (f"{char.name} attacks {enemy.name} with a {char.inv[slot].type.name}! (-{damage}HP) \n")
                                        if not random.random()<(char.inv[slot].type.data["hitRate"]/100):
                                            new = int(damage*char.skills["strength"]/100)
                                            damage += new
                                            output += (f"{char.name} got a double hit! (-{new-damage}HP) \n")
                                        enemy.hp -= damage
                                else:
                                    output += (f"{char.name} tries to attack {enemy.name} but misses! \n")
                count = 0
                for char in self.people:
                    if char.team==2: count+=1
                if count==0:
                    event = True
                    output += ("You have won the battle! \n")
                    self.winner = 1
        return output
    def endUpdate(self) -> tuple[Character|list]:
        for char in self.people:
            if char.type.name=="Player":
                x = char
                self.people.remove(char)
        return ("The battle is over! \n"), x, self.people





class Room:
    def __init__(self, place:tuple[int], biome:int, _type:int, connections:tuple[int]) -> None:
        self.place = place
        self.biome = biome
        self.type = _type
        self.connections = connections
        self.contents = []
        self.characters = []
        if self.type==3:
            self.shop = True
            self.shopStuff = []
        else: self.shop = False
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

# ["Normal","Fire","Water","Mines"]
# ["Normal Room","Dungon","Guardian Room","Shop","Mini-Boss Fight","Boss Fight"]

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
            output.update((i//size,i%size),(n//types%biomes,n%types,con))
    return output