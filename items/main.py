from items.stuff import Object,Character,Encounter
import items.stuff as stuff , items.settings as settings
import variables, frontend.prompt




class Game:
    """A little dnd game which is legally under the ownership of Alasdair Marsden :)"""
    
    def __init__(self):
        self.state = "normal"
        self.map = stuff.generateMap(settings.seed)
        self.player = Character(stuff.player, "Jeff")
        self.player.loc = list(self.map.spawn)
        self.player.balance = 100
        self.player.friends = []
        self.encounter = None
        
        self.player.inv = [Object(stuff.basicSword),Object(stuff.basicSword),Object(stuff.coolChestplate),None,Object(stuff.randomPills),Object(stuff.cocaine)]
        self.player.armour = [Object(stuff.basicHelmet),None,None,None]
        self.player.skills["strength"] = 110
   
    def update(self, time):
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
            return self.encounter.update("")
    
    def view(self, input1):
        output = ""
        if input1=="self":
            n = int((30*self.player.hp)/(self.player.type.data["health"]*(self.player.skills["constitution"]/100))*(sum([100]+[e.level for e in self.player.effects if e.effect=="constitution"])/100))
            string = f"{self.player.hp}HP"
            output += (string + (" "*(30-len(string))) + "[" + ("="*n) + (" "*(30-n)) + "]" + "\n")
            for skill,value in self.player.skills.items():
                n = int((30*(value-100))/(100))
                string = f"{skill[0:1].upper()+skill[1:]} +{value-100}%"
                output += (string + (" "*(30-len(string))) + "[" + ("="*n) + (" "*(30-n)) + "]" + "\n")
            output += (f"{self.player.balance}{settings.currencySym} \n")
            output += ("Inventory: \n")
            for item in self.player.inv:
                if item: output += (item.strLong() + "\n")
                else: output += ("  - No Item \n")
            output += ("Armour Equipped: \n")
            for item in self.player.armour:
                if item: output += (item.strLong() + "\n")
                else:
                    output += ("  - No Armour \n")
            if len(self.player.effects)>0:
                output += ("Effects: \n")
                for effect in self.player.effects:
                    output += (f"\033{settings.effectCol}  - " + str(effect) + "\n")
        if input1=="room":
            currentRoom = self.map.rooms[self.player.loc[0]][self.player.loc[1]]
            biomes = ["Normal","Fire","Water","Mines"]
            output += (f"  - {biomes[currentRoom.biome]} Biome \n")
            types = ["Normal Room","Dungon","Dungon","Dungon","Blacksmith","General Shop","Dodgy Shop","Mini-Boss Fight","Boss Fight"]
            output += (f"  - {types[currentRoom.type]} \n") 
            if len(currentRoom.contents)>0:
                output += ("In the room: \n")
                for item in currentRoom.contents:
                    output += (item.strLong() + "\n")
        if input1=="shop":
            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].type in settings.rooms["shop"]:
                for item in self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff:
                    if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==settings.rooms["minesBiome"]:
                        output += (f"{item.data['uses'] if 'uses' in item.data else 1}x {item.strShort()} {int(0.9*item.value)}{settings.currencySym} \n")
                    else:
                        output += (f"{item.data['uses'] if 'uses' in item.data else 1}x {item.strShort()} {0.9*item.value}{settings.currencySym} \n")
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3: output += (f"10% discount (Mines Biome) \n")
            else:
                output += ("You aren't currently in a shop. \n")
        if input1=="compass":
            pass
        x = self.update(settings.timeTo["view"])
        if x: output += x
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
        x = self.update(settings.timeTo["move"])
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
                    output += (f"Picked up {item.uses if 'uses' in item.type.data else 1}x {item.strShort()} \n")
                    break
        x = self.update(settings.timeTo["pickup"])
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
                output += (f"Dropped {item.uses if 'uses' in item.type.data else 1}x {item.strShort()} \n")
        x = self.update(settings.timeTo["drop"])
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
            output += (f"Dropped {item1.uses if 'uses' in item1.type.data else 1}x {item1.strShort()} \n")
            output += (f"Picked up {item2.uses if 'uses' in item2.type.data else 1}x {item2.strShort()} \n")
        x = self.update(settings.timeTo["switch"])
        if x: output += x
        return output

    def use(self,input1):
        output = ""
        if int(input1) >= len(self.player.inv):
            output += ("Invalid Input \n")
        else:
            item = self.player.inv[int(input1)]
            if item==None:
                output += ("No Item Selected \n")
            elif item.type.use=="weapon":
                output += ("You aren't currently in combat, use fight command to fight someone \n")
            elif item.type.use[:6]=="armour":
                item2 = self.player.armour[int(item.type.use[6:7])]
                self.player.armour[int(item.type.use[6:7])] = item
                output += (f"Equipped {item.strShort()} \n")
                self.player.inv[int(input1)] = item2
                if item2:
                    output += (f"Unequipped {item2.strShort()} \n")
            elif item.type.use=="instant":
                if "healing" in item.type.data:
                    self.player.hp += item.type.data["healing"]
                    maxHp = int(self.player.type.data["health"]*(self.player.skills["constitution"]/100)*(sum([100]+[e.level for e in self.player.effects if e.effect=="constitution"])/100))
                    if self.player.hp>maxHp: self.player.hp = maxHp
                if "stamina" in item.type.data:
                    self.player.stamina += item.type.data["stamina"]
                self.player.inv[int(input1)].uses -= 1
                output += (f"Used {item.strShort()} \n")
            elif item.type.use=="effect":
                for eff in item.type.data["effects"]:
                    self.player.effects.append(eff.copy())
                self.player.inv[int(input1)].uses -= 1
                output += (f"Used {item.strShort()} \n")
            else: output += ("Item doesn't use a use \n")
        x = self.update(settings.timeTo["use"])
        if x: output += x
        return output
    
    def shop(self, input1, input2):
        output = ""
        if self.map.rooms[self.player.loc[0]][self.player.loc[1]].type in settings.rooms["shop"]:
            if input1=="view":
                for item in self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff:
                    if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==settings.rooms["minesBiome"]:
                        output += (f"{item.data['uses'] if 'uses' in item.data else 1}x {item.strShort()} {int(0.9*item.value)}{settings.currencySym} \n")
                    else:
                        output += (f"{item.data['uses'] if 'uses' in item.data else 1}x {item.strShort()} {item.value}{settings.currencySym} \n")
                if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==3: output += (f"10% discount (Mines Biome) \n")
                x = self.update(settings.timeTo["shopv"])
                if x: output += x
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
                            if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==settings.rooms["minesBiome"]: value = int(value*0.9)
                            self.player.balance -= value
                            output += (f"Bought {item.uses if 'uses' in item.type.data else 1}x {item.strShort()} for {value}{settings.currencySym} \n")
                            x = self.update(settings.timeTo["shopb"])
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
                    if self.map.rooms[self.player.loc[0]][self.player.loc[1]].biome==settings.rooms["minesBiome"]: value = int(value*0.9)
                    self.player.inv[int(input2)] = None
                    self.player.balance += value
                    self.map.rooms[self.player.loc[0]][self.player.loc[1]].shopStuff.append(item.type)
                    output += (f"Sold {item.uses if 'uses' in item.type.data else 1}x {item.strShort()} for {value}{settings.currencySym} \n")
                    x = self.update(settings.timeTo["shops"])
                    if x: output += x
        else:
            output += ("You aren't currently in a shop. \n")
        return output
    
    def wait(self, n):
        x = self.update(int(n))
        if x: return x
        else: return "...\n"
    
    def help(self):
        return """Normal Functions:
  view [self|inventory|room|shop] - Give information about the thing asked for
  move [direction] - Move player in direction given
  pickup [obj_index] - Pick up object at given index (room)
  drop [obj_index] - Drop object at given index (inventory and armour)
  switch [inv_index] [room_index] - Switch objects at given indexes
  use [obj_index] - Use object at given index (inventory)
  shop [view|buy|sell] [obj_index] - Interact with shop
  wait [time] - Waits for amount of time given
  help | ? - List functions
  quit - Quit the game
In Combat:
  use [obj_index] - Use object at given index (inventory), -1 means default attack
  wait|skip - Does nothing for the turn\n"""

    def quit(self):
        self.state = None
        return "\033[1;31mGAME OVER \033[0m"

    def takeInput(self, in_):
        if self.state=="normal":
            _input = in_.split()
            if not _input: _input=[""]
            if _input[0]=="view":
                
                if variables.text:
                    return self.view(_input[1])
                else:
                    self.view(_input[1])
            elif _input[0]=="move":
                return self.move(_input[1])
            elif _input[0]=="pickup":
                return self.pickup(_input[1])
            elif _input[0]=="drop":
                return self.drop(_input[1])
            elif _input[0]=="switch":
                return self.switch(_input[1],_input[2])
            elif _input[0]=="use":
                frontend.prompt.prompt( self.use(_input[1]))
                
            elif _input[0]=="shop":
                if len(_input)==2: return self.shop(_input[1],None)
                elif len(_input)==3: return self.shop(_input[1],_input[2])
                else: return "Invalid Input \n"
            elif _input[0]=="wait":
                return self.wait(_input[1])
            elif _input[0] in ["help","?"]:
                
                return self.help()
            elif _input[0]=="quit":
                return self.quit()
            elif _input[0]=="blur":
                variables.blur = True
            else:
                return "Invalid Input \n"
        if self.state=="fighting":
            if self.encounter.winner:
                self.state = "normal"
                if self.encounter.winner==1:
                    x = self.encounter.endUpdate()
                    self.player = x[1]
                    self.player.friends = x[2]
                    self.map.rooms[self.player.loc[0]][self.player.loc[1]].characters = []
                    return x[0]
                elif self.encounter.winner==2:
                    return self.quit()
            else: return self.encounter.update(in_)





if __name__ == "__main__":
    game = Game()
    while game.state:
        print(game.takeInput(input('>>> ')))