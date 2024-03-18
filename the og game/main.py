import rooms,characters,objects



class Game:
    def __init__(self):
        name = input("Enter name: ")
        self.playing = True
        self.map = rooms.generateRooms()
        self.player = characters.Character(characters.player, [25,25], name)
        self.player.skills = {"constitution":118,"dexterity":110,"otherstuff":156}
        self.inFight = False
        self.player.inv = [objects.Object(objects.basicSword),objects.Object(objects.coolChestplate),None,None,None]
        self.player.armour = [objects.Object(objects.basicHelmet),None,None,None]
        self.map[self.player.loc[0]][self.player.loc[1]].contents = [objects.Object(objects.cocaine)]
        print()
    
    def view(self):
        print("Player:")
        n = int((30*self.player.hp)/(self.player.type.data["health"]*(self.player.skills["constitution"]/100)))
        string = f"{self.player.hp}HP"
        print(string + (" "*(30-len(string))) + "[" + ("="*n) + (" "*(30-n)) + "]")
        for skill,value in self.player.skills.items():
            n = int((30*(value-100))/(100))
            string = f"{skill[0:1].upper()+skill[1:]} +{value-100}%"
            print(string + (" "*(30-len(string))) + "[" + ("="*n) + (" "*(30-n)) + "]")
        print("Inventory:")
        for item in self.player.inv:
            if item: print(item)
            else: print("  - No Item")
        print("Armour Equipped:")
        for item in self.player.armour:
            if item: print(item)
            else:
                print("  - No Armour")
        print("Room:")
        currentRoom = self.map[self.player.loc[0]][self.player.loc[1]]
        biomes = ["Default","Lava","Water","Mines"]
        print(f"  - {biomes[currentRoom.type[0]]} Biome")
        types = ["Normal Room","Skeleton Dungon","Goblin Dungon","Guardian Room","Shop","Mini-Boss Fight","Boss Fight"]
        print(f"  - {types[currentRoom.type[1]]}") 
        if len(currentRoom.contents)>0:
            print("On the floor:")
            for item in currentRoom.contents:
                print(item)
        print()
    
    def move(self,input1):
        if input1.lower()=="up":
            self.player.loc[1] += 1
        if input1.lower()=="down":
            self.player.loc[1] -= 1
        if input1.lower()=="left":
            self.player.loc[0] -= 1
        if input1.lower()=="right":
            self.player.loc[0] += 1
        print()

    def pickup(self,input1):
        if int(input1) >= len(self.map[self.player.loc[0]][self.player.loc[1]].contents):
            print("Invalid Input")
        elif None not in self.player.inv:
            print("Inventory Full")
        else:
            for i in range(len(self.player.inv)):
                if self.player.inv[i]==None:
                    self.player.inv[i] = self.map[self.player.loc[0]][self.player.loc[1]].contents[int(input1)]
                    self.map[self.player.loc[0]][self.player.loc[1]].contents.pop(int(input1))
                    item = self.player.inv[i]
                    if item.type.rarity.colour:
                        print(f"Picked up \033{item.type.rarity.colour}{item.type.name} \033[0m")
                    else:
                        print(f"Picked up {item.type.name}")
                    break
        print()
    
    def drop(self,input1):
        if int(input1) >= len(self.player.inv+self.player.armour):
            print("Invalid Input")
        else:
            if int(input1)<5:
                item = self.player.inv[int(input1)]
                self.player.inv[int(input1)] = None
            elif int(input1)>4:
                item = self.player.armour[int(input1)-5]
                self.player.armour[int(input1)-5] = None
            self.map[self.player.loc[0]][self.player.loc[1]].contents.append(item)
            if item.type.rarity.colour:
                print(f"Dropped \033{item.type.rarity.colour}{item.type.name} \033[0m")
            else:
                print(f"Dropped {item.type.name}")
        print()

    def switch(self,input1,input2):
        if int(input1)>=len(self.player.inv) or int(input2)>=len(self.map[self.player.loc[0]][self.player.loc[1]].contents):
            print("Invalid Input")
        else:
            item1 = self.player.inv[int(input1)]
            item2 = self.map[self.player.loc[0]][self.player.loc[1]].contents[int(input2)]
            self.player.inv[int(input1)] = item2
            self.map[self.player.loc[0]][self.player.loc[1]].contents[int(input2)] = item1
            if item1.type.rarity.colour: print(f"Dropped \033{item1.type.rarity.colour}{item1.type.name} \033[0m")
            else: print(f"Dropped {item1.type.name}")
            if item2.type.rarity.colour: print(f"Picked up \033{item2.type.rarity.colour}{item2.type.name} \033[0m")
            else: print(f"Picked up {item2.type.name}")
        print()

    def fight(self,input1):
        print()

    def use(self,input1):
        if int(input1) >= len(self.player.inv):
            print("Invalid Input")
        else:
            item = self.player.inv[int(input1)]
            if item.type.use=="weapon":
                print("You aren't currently in combat, use fight command to fight someone")
            if item.type.use[:6]=="armour":
                item2 = self.player.armour[int(item.type.use[6:7])]
                self.player.armour[int(item.type.use[6:7])] = item
                if item.type.rarity.colour: print(f"Equipped \033{item.type.rarity.colour}{item.type.name} \033[0m")
                else: print(f"Equipped {item.type.name}")
                self.player.inv[int(input1)] = item2
                if item2:
                    if item2.type.rarity.colour: print(f"Unequipped \033{item2.type.rarity.colour}{item2.type.name} \033[0m")
                    else: print(f"Unequipped {item2.type.name}")
        print()
    
    def help(self):
        print("""Functions:
  view - Give information about player, inventory and room stats
  move [direction] - Move player in direction given
  pickup [obj_index] - Pick up object at given index (room)
  drop [obj_index] - Drop object at given index (inventory and armour)
  switch [inv_index] [room_index] - Switch objects at given indexes
  fight - Under development
  use [obj_index] - Use object at given index (inventory)
  help | ? - List functions
  quit - Quit the game \n""")
    
    def quit(self):
        self.playing = False



def takeInput(x):
    _input = input().split()
#try:
    if _input[0]=="view":
        x.view()
    elif _input[0]=="move":
        x.move(_input[1])
    elif _input[0]=="pickup":
        x.pickup(_input[1])
    elif _input[0]=="drop":
        x.drop(_input[1])
    elif _input[0]=="switch":
        x.switch(_input[1],_input[2])
    elif _input[0]=="fight":
        x.fight(_input[1])
    elif _input[0]=="use":
        x.use(_input[1])
    elif _input[0] in ["help","?"]:
        x.help()
    elif _input[0]=="quit":
        x.quit()
    else:
        print("Invalid Input \n")
#except:
    #print("Something Went Wrong \n")



if __name__ == "__main__":
    game = Game()
    while game.playing:
        takeInput(game)