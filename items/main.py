import items.rooms as rooms
import items.characters as characters
import items.objects as objects
import items.settings as settings


class Game:
    def __init__(self):
        self.playing = True
        self.map = rooms.generateRooms()
        self.player = characters.Character(characters.player, [25,25], "name")
        self.player.skills = {"constitution":100,"dexterity":100,"otherstuff":100}
        self.player.balance = 100
        self.inFight = False
        
        self.player.inv = [objects.Object(objects.basicSword),objects.Object(objects.coolChestplate),None,None,None]
        self.player.armour = [objects.Object(objects.basicHelmet),None,None,None]
        self.map[self.player.loc[0]][self.player.loc[1]].shop = [objects.cocaine,objects.enchIronLeggings]
    
    def update(self):
        for i in range(len(self.player.effects)):
            self.player.effects[i].time -= 1
            if self.player.effects[i].time <= 0:
                self.player.effects.pop(i)
    
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
            currentRoom = self.map[self.player.loc[0]][self.player.loc[1]]
            biomes = ["Default","Lava","Water","Mines"]
            output += (f"  - {biomes[currentRoom.type[0]]} Biome \n")
            types = ["Normal Room","Skeleton Dungon","Goblin Dungon","Guardian Room","Shop","Mini-Boss Fight","Boss Fight"]
            output += (f"  - {types[currentRoom.type[1]]} \n") 
            if len(currentRoom.contents)>0:
                output += ("In the room: \n")
                for item in currentRoom.contents:
                    output += (str(item) + "\n")
        return output
    
    def move(self,input1):
        output = ""
        if input1.lower()=="up":
            self.player.loc[1] += 1
            output += (f"Moved {input1.lower()} \n")
        elif input1.lower()=="down":
            self.player.loc[1] -= 1
            output += (f"Moved {input1.lower()} \n")
        elif input1.lower()=="left":
            self.player.loc[0] -= 1
            output += (f"Moved {input1.lower()} \n")
        elif input1.lower()=="right":
            self.player.loc[0] += 1
            output += (f"Moved {input1.lower()} \n")
        else:
            output += (f"Invalid Input \n")
        return output
        

    def pickup(self,input1):
        output = ""
        if int(input1) >= len(self.map[self.player.loc[0]][self.player.loc[1]].contents):
            output += ("Invalid Input \n")
        elif None not in self.player.inv:
            output += ("Inventory Full \n")
        else:
            for i in range(len(self.player.inv)):
                if self.player.inv[i]==None:
                    self.player.inv[i] = self.map[self.player.loc[0]][self.player.loc[1]].contents[int(input1)]
                    self.map[self.player.loc[0]][self.player.loc[1]].contents.pop(int(input1))
                    item = self.player.inv[i]
                    if item.type.rarity.colour:
                        output += (f"Picked up \033{item.type.rarity.colour}{item.type.name} \033[0m \n")
                    else:
                        output += (f"Picked up {item.type.name} \n")
                    break
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
            self.map[self.player.loc[0]][self.player.loc[1]].contents.append(item)
            if item.type.rarity.colour:
                output += (f"Dropped \033{item.type.rarity.colour}{item.type.name} \033[0m \n")
            else:
                output += (f"Dropped {item.type.name} \n")
        return output

    def switch(self,input1,input2):
        output = ""
        if int(input1)>=len(self.player.inv) or int(input2)>=len(self.map[self.player.loc[0]][self.player.loc[1]].contents):
            output += ("Invalid Input \n")
        else:
            item1 = self.player.inv[int(input1)]
            item2 = self.map[self.player.loc[0]][self.player.loc[1]].contents[int(input2)]
            self.player.inv[int(input1)] = item2
            self.map[self.player.loc[0]][self.player.loc[1]].contents[int(input2)] = item1
            if item1.type.rarity.colour: output += (f"Dropped \033{item1.type.rarity.colour}{item1.type.name} \033[0m \n")
            else: output += (f"Dropped {item1.type.name} \n")
            if item2.type.rarity.colour: output += (f"Picked up \033{item2.type.rarity.colour}{item2.type.name} \033[0m \n")
            else: output += (f"Picked up {item2.type.name} \n")
        return output

    def fight(self):
        return "\n"

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
        return output
    
    def shop(self, input1, input2):
        output = ""
        if self.map[self.player.loc[0]][self.player.loc[1]].type[1]<10:
            if input1=="view":
                for item in self.map[self.player.loc[0]][self.player.loc[1]].shop:
                    if item.rarity.colour: output += (f"\033{item.rarity.colour}{item.name} \033[0m{item.value}{settings.currencySym} \n")
                    else: output += (f"{item.name} {item.value}{settings.currencySym} \n")
        else:
            output += ("You aren't currently in a shop. \n")
            output += (self.map[self.player.loc[0]][self.player.loc[1]].type + "\n")
        return output
    
    def help(self):
        return """Functions:
  view [self|inventory|room] - Give information about the thing asked for
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
        _input = input().split()
        #try:
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
        elif _input[0]=="fight":
            return self.fight(_input[1])
        elif _input[0]=="use":
            return self.use(_input[1])
        elif _input[0]=="shop":
            if len(_input)==2: return self.shop(_input[1],None)
            elif len(_input)==3: return self.shop(_input[1],_input[2])
            else: return "Invalid Input \n"
        elif _input[0] in ["help","?"]:
            return self.help()
        elif _input[0]=="quit":
            self.playing = False
        else:
            return "Invalid Input \n"
            self.update()
        #except:
            #return "Something Went Wrong \n"



if __name__ == "__main__":
    game = Game()
    while game.playing:
        print(game.takeInput())