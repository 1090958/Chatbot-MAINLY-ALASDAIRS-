import os
from Base import *
import keyboard
class biome():
    def __init__(self, key, name):
        self.key = key
        self.name = name
class field(biome):
    def __init__(self):
        super().__init__('F','Field')

class rake(biome):
    def __init__(self):
        super().__init__('R','Rake')
grid ={
    0:[field(),field(),field(),field(),field()],
    1:[field(),field(),field(),field(),field()],
    2:[field(),field(),field(),field(),field()],
    3:[field(),field(),field(),field(),field()],
    4:[field(),field(),field(),field(),rake()]
}
x=0
y=0
p1=Player('P1','Person',1)
p2=Player('P2','Person',1)
p2.x,p2.y=2,3
def printgrid(grid,players):
    for ys in range(len(grid)):
        line=grid[ys]
        
        for xs in range(len(line)):
            biome=line[xs]
            p=False
            for ps in players:
                x=ps.x
                y=ps.y
                if xs==x and ys==len(line)-y-1:
                    p=True
                    #print(ps.Name)
            if p==True:
                print('#', end=' ')
                
            else:
                print(biome.key, end=' ')
        print()
def map(player):
    while True:
        os.system('CLS')
        printgrid(grid, [p1,p2])
        while True:
            if keyboard.is_pressed("w"):
                p1.y+=1
                break
            if keyboard.is_pressed("s"):
                p1.y-=1
                break
            if keyboard.is_pressed("d"):
                p1.x+=1
                break
            if keyboard.is_pressed("a"):
                p1.x-=1
                break
map(p1)
        
    
    
    
