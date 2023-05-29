import os
from Base import *
import keyboard
import time
import random
import RandomAI as AI
from colorama import Fore, Back, Style
from colorama import init as colorama_init
from Combat import *
colorama_init(autoreset=True)
class biome():
    def __init__(self, key, name, fore=Fore.RESET, back=Back.RESET, style=Style.NORMAL):
        self.key = key
        self.name = name
        self.fore,self.back,self.style=fore,back,style

    def pkey(self):
        print(self.fore + self.back +self.style + self.key +' ', end='')
class field(biome):
    def __init__(self):
        super().__init__('F','Field',fore=Fore.WHITE,back=Back.GREEN)

class desert(biome):
    def __init__(self):
        super().__init__('D','Desert',fore=Fore.RED,back=Back.YELLOW,style=Style.DIM)
biomes=[field(),desert()]
biomeweights=[5,2]


def generate_grid(size):
    grid ={}
    for i in range(size):
        list=[]
        for _ in range(size):
            list.extend(random.choices(biomes, weights=biomeweights))
        #print(list)
        grid[i]=list
    return grid

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
                print(biome.back +Style.BRIGHT + player.key + ' ', end='')
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
        fight=(printgrid(grid, entities,[player,AI.Niresh('Kieran Tan',0,1)]))
        if fight[0]:
            
            #for i in range(150):
                #print('s')
                #keyboard.unblock_key(i)
            result=Fightloop(fight[1],fight[2])
            if result== 'win':
                for enemy in fight[2]:
                    ai.remove(enemy)
            
        time.sleep(0.05)
        if timing % 2 ==0:
            
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
map(player,generate_grid(40),[AI.Niresh('Niresh',random.randint(0,20),random.randint(0,20)),AI.Niresh('Niresh',random.randint(0,20),random.randint(0,20)),AI.Niresh('Niresh',random.randint(0,20),random.randint(0,20)),AI.Niresh('Niresh',random.randint(0,20),random.randint(0,20))])
#print(generate_grid(2))
    
    
