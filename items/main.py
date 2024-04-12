from stuff import Object,Character,Encounter
import stuff, settings



class Game:
    def __init__(self):
        self.state = "normal"
        self.map = stuff.generateMap(settings.seed)
        self.player = Character(stuff.player, "Jeff")
        self.player.loc = list(self.map.spawn)
        self.player.balance = 100
        self.player.friends = []
        self.encounter = None
        
        self.player.inv = [Object(stuff.basicSword),Object(stuff.coolChestplate),None,None,None]
        self.player.armour = [Object(stuff.basicHelmet),None,None,None]
        self.map.rooms[self.player.loc[0]-1][self.player.loc[1]].characters = [Character(stuff.goblin),Character(stuff.goblin),Character(stuff.goblin)]
    
    def update(self, time):
        for eff in self.player.effects:
            eff.time -= time
            if eff.time <= 0:
                self.player.effects.remove(eff)
        if self.map.rooms[self.player.loc[0]][self.player.loc[1]].type in [1,4,5] and self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters!=[]:
            self.state = "fighting"
            self.encounter = Encounter([self.player]+self.player.friends, self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters)
            return self.encounter.update("")
    
    def view(self, input1):
        output = ""
        if input1=="self":
            n = int((30*self.player.hp)/(self.player.type.data["health"]*(self.player.skills["constitution"]/100)))
            string = f"{self.player.hp}HP"
            output += (string + (" "*(30-len(string))) + "[" + ("="*n) + (" "*(30-n)) + "]" + "\n")
            for skill,value in self.player.skills.items():
                n = int((30*(value-100))/(100))
                string = f"{skill[0:1].upper()+skill[1:]} +{value-100}%"
                output += (string + (" "*(30-len(string))) + "[" + ("="*n) + (" "*(30-n)) + "]" + "\n")
            output += (f"{self.player.balance}{settings.currencySym} \n")
            output += ("Inventory: \n")
            for item in self.player.inv:
                if item: output += (str(item) + "\n")
                else: output += ("  - No Item \n")
            output += ("Armour Equipped: \n")
            for item in self.player.armour:
                if item: output += (str(item) + "\n")
                else:
                    output += ("  - No Armour \n")
            if len(self.player.effects)>0:
                output += ("Effects: \n")
                for effect in self.player.effects:
                    output += (f"\033[1;32m  - {effect.name} \033[0m \n")
        if input1=="room":
            currentRoom = self.map.rooms[self.player.loc[0]][self.player.loc[1]]
            biomes = ["Normal","Fire","Water","Mines"]
            output += (f"  - {biomes[currentRoom.biome]} Biome \n")
            types = ["Normal Room","Dungon","Library","Shop","Mini-Boss Fight","Boss Fight"]
            output += (f"  - {types[currentRoom.type]} \n") 
            if len(currentRoom.contents)>0:
                output += ("In the room: \n")
                for item in currentRoom.contents:
                    output += (str(item) + "\n")
        if input1=="shop":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].shop:
                for item in self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff:
                    if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3:
                        if item.rarity.colour: output += (f"\033{item.rarity.colour}{item.name} \033[0m{int(0.9*item.value)}{settings.currencySym} \n")
                        else: output += (f"{item.name} {int(0.9*item.value)}{settings.currencySym} \n")
                    else:
                        if item.rarity.colour: output += (f"\033{item.rarity.colour}{item.name} \033[0m{item.value}{settings.currencySym} \n")
                        else: output += (f"{item.name} {item.value}{settings.currencySym} \n")
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3: output += (f"10% discount (Mines Biome) \n")
            else:
                output += ("You aren't currently in a shop. \n")
        return output
    
    def move(self,input1):
        output = ""
        if input1.lower()=="up":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[0]:
                self.player.loc[1] -= 1
                output += (f"Moved {input1.lower()} \n")
            else:
                output += (f"No Pathway \n")
        elif input1.lower()=="down":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[1]:
                self.player.loc[1] += 1
                output += (f"Moved {input1.lower()} \n")
            else:
                output += (f"No Pathway \n")
        elif input1.lower()=="left":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[2]:
                self.player.loc[0] -= 1
                output += (f"Moved {input1.lower()} \n")
            else:
                output += (f"No Pathway \n")
        elif input1.lower()=="right":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].connections[3]:
                self.player.loc[0] += 1
                output += (f"Moved {input1.lower()} \n")
            else:
                output += (f"No Pathway \n")
        else:
            output += (f"Invalid Input \n")
        x = self.update(4)
        if x: output += x
        return output

    def pickup(self,input1):
        output = ""
        if int(input1) >= len(self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents):
            output += ("Invalid Input \n")
        elif None not in self.player.inv:
            output += ("Inventory Full \n")
        else:
            for i in range(len(self.player.inv)):
                if self.player.inv[i]==None:
                    self.player.inv[i] = self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents[int(input1)]
                    self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.pop(int(input1))
                    item = self.player.inv[i]
                    if item.type.rarity.colour:
                        output += (f"Picked up \033{item.type.rarity.colour}{item.type.name} \033[0m \n")
                    else:
                        output += (f"Picked up {item.type.name} \n")
                    break
        x = self.update(1)
        if x: output += x
        return output
    
    def drop(self,input1):
        output = ""
        if int(input1) >= len(self.player.inv+self.player.armour):
            output += ("Invalid Input \n")
        else:
            if int(input1)<5:
                item = self.player.inv[int(input1)]
                self.player.inv[int(input1)] = None
            elif int(input1)>4:
                item = self.player.armour[int(input1)-5]
                self.player.armour[int(input1)-5] = None
            if item:
                self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents.append(item)
                if item.type.rarity.colour:
                    output += (f"Dropped \033{item.type.rarity.colour}{item.type.name} \033[0m \n")
                else:
                    output += (f"Dropped {item.type.name} \n")
        x = self.update(1)
        if x: output += x
        return output

    def switch(self,input1,input2):
        output = ""
        if int(input1)>=len(self.player.inv) or int(input2)>=len(self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents):
            output += ("Invalid Input \n")
        elif self.player.inv[int(input1)]==None:
            output += ("Nothing Selected, Use Pickup Command \n")
        else:
            item1 = self.player.inv[int(input1)]
            item2 = self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents[int(input2)]
            self.player.inv[int(input1)] = item2
            self.map.rooms[self.player.loc[0]][self.player.loc[1]].contents[int(input2)] = item1
            if item1.type.rarity.colour: output += (f"Dropped \033{item1.type.rarity.colour}{item1.type.name} \033[0m \n")
            else: output += (f"Dropped {item1.type.name} \n")
            if item2.type.rarity.colour: output += (f"Picked up \033{item2.type.rarity.colour}{item2.type.name} \033[0m \n")
            else: output += (f"Picked up {item2.type.name} \n")
        x = self.update(1)
        if x: output += x
        return output

    def use(self,input1):
        output = ""
        if int(input1) >= len(self.player.inv):
            output += ("Invalid Input \n")
        else:
            item = self.player.inv[int(input1)]
            if item.type.use=="weapon":
                output += ("You aren't currently in combat, use fight command to fight someone \n")
            if item.type.use[:6]=="armour":
                item2 = self.player.armour[int(item.type.use[6:7])]
                self.player.armour[int(item.type.use[6:7])] = item
                if item.type.rarity.colour: output += (f"Equipped \033{item.type.rarity.colour}{item.type.name} \033[0m \n")
                else: output += (f"Equipped {item.type.name} \n")
                self.player.inv[int(input1)] = item2
                if item2:
                    if item2.type.rarity.colour: output += (f"Unequipped \033{item2.type.rarity.colour}{item2.type.name} \033[0m \n")
                    else: output += (f"Unequipped {item2.type.name} \n")
            if item.type.use=="effectPosi":
                [self.player.effects.append(i) for i in item.type.data["effects"]]
                self.player.inv[int(input1)] = None
                if item.type.rarity.colour: output += (f"Used \033{item.type.rarity.colour}{item.type.name} \033[0m \n")
                else: output += (f"Used {item.type.name} \n")
        x = self.update(1)
        if x: output += x
        return output
    
    def shop(self, input1, input2):
        output = ""
        if self.map.rooms[self.player.loc[0]][self.player.loc[1]].shop:
            if input1=="view":
                for item in self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff:
                    if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3:
                        if item.rarity.colour: output += (f"\033{item.rarity.colour}{item.name} \033[0m{int(0.9*item.value)}{settings.currencySym} \n")
                        else: output += (f"{item.name} {int(0.9*item.value)}{settings.currencySym} \n")
                    else:
                        if item.rarity.colour: output += (f"\033{item.rarity.colour}{item.name} \033[0m{item.value}{settings.currencySym} \n")
                        else: output += (f"{item.name} {item.value}{settings.currencySym} \n")
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3: output += (f"10% discount (Mines Biome) \n")
            if input1=="buy":
                if int(input2)>=len(self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff):
                    output += ("Invalid Input \n")
                elif self.player.balance<self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff[int(input2)].value:
                    output += ("Insufficient Funds \n")
                elif None not in self.player.inv:
                    output += ("Inventory Full \n")
                else:
                    for i in range(len(self.player.inv)):
                        if self.player.inv[i]==None:
                            self.player.inv[i] = Object(self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff[int(input2)])
                            item = self.player.inv[i]
                            value = item.type.value
                            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3: value = int(value*0.9)
                            self.player.balance -= value
                            if item.type.rarity.colour: output += (f"Bought \033{item.type.rarity.colour}{item.type.name}\033[0m for {value}{settings.currencySym} \n")
                            else: output += (f"Bought {item.type.name} for {value}{settings.currencySym} \n")
                            x = self.update(1)
                            if x: output += x
                            break
            if input1=="sell":
                if int(input2)>=len(self.player.inv):
                    output += ("Invalid Input \n")
                elif self.player.inv[int(input2)]==None:
                    output += ("Nothing Selected \n")
                else:
                    item = self.player.inv[int(input2)]
                    if "durability" in item.type.data: value = int(item.type.value*item.durability/item.type.data["durability"])
                    elif "uses" in item.type.data: value = int(item.type.value*item.uses/item.type.data["uses"])
                    if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3: value = int(value*0.9)
                    self.player.inv[int(input2)] = None
                    self.player.balance += value
                    self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff.append(item.type)
                    if item.type.rarity.colour: output += (f"Sold \033{item.type.rarity.colour}{item.type.name}\033[0m for {value}{settings.currencySym} \n")
                    else: output += (f"Sold {item.type.name} for {value}{settings.currencySym} \n")
                    x = self.update(1)
                    if x: output += x
        else:
            output += ("You aren't currently in a shop. \n")
        return output
    
    def wait(self):
        x = self.update(1)
        if x: return x
    
    def help(self):
        return """Functions:
  view [self|inventory|room|shop] - Give information about the thing asked for
  move [direction] - Move player in direction given
  pickup [obj_index] - Pick up object at given index (room)
  drop [obj_index] - Drop object at given index (inventory and armour)
  switch [inv_index] [room_index] - Switch objects at given indexes
  fight - Under development
  use [obj_index] - Use object at given index (inventory)
  shop [view|buy|sell] [obj_index] - Interact with shop
  help | ? - List functions
  quit - Quit the game \n"""

    def takeInput(self):
        if self.state=="normal":
            _input = input(">>> ").split()
            if not _input: _input=[""]
            if _input[0]=="view":
                return self.view(_input[1])
            elif _input[0]=="move":
                return self.move(_input[1])
            elif _input[0]=="pickup":
                return self.pickup(_input[1])
            elif _input[0]=="drop":
                return self.drop(_input[1])
            elif _input[0]=="switch":
                return self.switch(_input[1],_input[2])
            elif _input[0]=="use":
                return self.use(_input[1])
            elif _input[0]=="shop":
                if len(_input)==2: return self.shop(_input[1],None)
                elif len(_input)==3: return self.shop(_input[1],_input[2])
                else: return "Invalid Input \n"
            elif _input[0]=="wait":
                return self.wait()
            elif _input[0] in ["help","?"]:
                return self.help()
            elif _input[0]=="quit":
                self.state = None
                return "Exited Successfully"
            else:
                return "Invalid Input \n"
        if self.state=="fighting":
            if self.encounter.winner:
                self.state = "normal"
                x = self.encounter.endUpdate()
                self.player = x[1]
                self.player.friends = x[2]
                self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters = []
                return x[0]
            else: return self.encounter.update(input())



if __name__ == "__main__":
    game = Game()
    while game.state:
        print(game.takeInput())