import os
from Base import *
import keyboard
import time
import random
import RandomAI as AI
import WFC
from colorama import Fore, Back, Style
from colorama import init as colorama_init
from Combat import *
colorama_init(autoreset=True)
import sys
class biome():
    def __init__(self, key, name, fore=Fore.RESET, back=Back.RESET, style=Style.NORMAL):
        self.key = key
        self.name = name
        self.fore,self.back,self.style=fore,back,style

    def pkey(self):
        #print(self.fore + self.back +self.style + self.key +' ', end='')
        sys.stdout.write(self.fore + self.back +self.style + self.key +' ')

class field(biome):
    def __init__(self):
        super().__init__(' ','Field',fore=Fore.WHITE,back=Back.GREEN)

class forest(biome):
    def __init__(self):
        super().__init__('F','Forest',fore=Fore.BLACK,back=Back.GREEN)
class denseforest(biome):
    def __init__(self):
        super().__init__('E','Dense Forest',fore=Fore.BLACK,back=Back.GREEN)
class mountainbase(biome):
    def __init__(self):
        super().__init__('_','Mountain Base',fore=Fore.BLACK,back=Back.WHITE)
class mountain(biome):
    def __init__(self):
        super().__init__('|','Mountain',fore=Fore.BLACK,back=Back.WHITE)
class coast(biome):
    def __init__(self):
        super().__init__(' ','Coast',fore=Fore.YELLOW,back=Back.YELLOW)
class oceanwave(biome):
    def __init__(self):
        super().__init__('C','Ocean Waves',fore=Fore.CYAN,back=Back.BLUE)
class ocean(biome):
    def __init__(self):
        super().__init__(' ','Ocean',fore=Fore.CYAN,back=Back.BLUE)


biomes=[field(),forest(),denseforest(),mountainbase(),mountain(),coast(),oceanwave(), ocean()]
biomeweights=[10,5,2,3,4,8,20,20]
#might cause errors
keys = {
    'F' : field(),
    'T' : forest(),
    'R' : denseforest(),
    'm' :  mountainbase(),
    'M' : mountain(),
    'C' : coast(),
    'O' : ocean(),
    'W' : oceanwave()
}
#print(biomes)
def convertToGrid(path):
    grid={}
    with open(path) as f:
        l=f.read().count("\n")+1
    with open(path) as f:
        line=f.readline()
        print(line)
        while line:
            list=[]
            for character in line:
                for key, item in keys.items():
                    if character == key:
                        list.append(item)
                grid[l]=list.copy()
                l-=1

            line=f.readline()
    return grid

def generate_grid(size):
    grid ={}
    for i in range(size):
        list=[]
        for _ in range(size):
            list.extend(random.choices(biomes, weights=biomeweights))
        #print(list)
        grid[i]=list
    return grid


def generate_grid(size):
    grid =convertToGrid('Level0.txt')
    return grid
print(generate_grid(20))
def printgrid(grid,entities,allies,gridtype='mapgrid'):
    fight=False
    p1=None
    p2=[]
    for ycoord in range(len(grid)):
        line=grid[ycoord]
        
        for xcoord in range(len(line)):
            biome=line[xcoord]
            player=False
            for ent in entities:
                x=ent.x
                y=ent.y
                if xcoord==x and ycoord==len(line)-y-1:
                    for person in allies:
                        
                        if player != False:
                            if player==person and ent not in allies:
                                fight=True
                                p1=allies
                                if gridtype == 'mapgrid':
                                    p2.append(ent)
                            if person == ent and player not in allies:
                                fight=True
                                p1=allies
                                if gridtype == 'mapgrid':
                                    p2.append(player)
                    player=ent
            if player != False:
                #print(Back.BLUE +Style.BRIGHT + player.key + ' ', end='')
                sys.stdout.write(Back.BLUE +Style.BRIGHT + player.key + ' ')
                
                #print(player.key, end='')
                
            else:
                biome.pkey()
        print()
    return(fight,p1,p2)
       
def map(player,grid,ai):
    timing=0
    while True:
        timing+=1
        os.system('CLS')
        entities=ai.copy()
        entities.append(player)
        fight=(printgrid(grid, entities,[player]))
        if fight[0]:
            
            #for i in range(150):
                #print('s')
                #keyboard.unblock_key(i)
            result=Fightloop(fight[1],fight[2])
            if result== 'win':
                for enemy in fight[2]:
                    ai.remove(enemy)
            
        time.sleep(0.05)
        if timing % 1 ==0:
            
            for enemy in ai:
                enemy.Move(grid)
            
        #for i in range(150):
            #keyboard.block_key(i)
        while True:
                
            #print(len(grid),player.y)
            if keyboard.is_pressed("w") and len(grid)-1 > player.y:
                player.y+=1
                break
            if keyboard.is_pressed("s") and 0 != player.y:
                player.y-=1
                break
            if keyboard.is_pressed("d") and len(grid[0])-1 > player.x:
                player.x+=1
                break
            if keyboard.is_pressed("a") and 0 != player.x: 
                player.x-=1
                break

player=Fighter()
AIs=[]
for i in range(45):
    AIs.append(AI.Person('Niresh',random.randint(0,2),random.randint(0,2)))
map(player,generate_grid(20),AIs)
#print(generate_grid(2))
    
    
