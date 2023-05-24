import random
import time
import keyboard
import os
#yay
print('yes')
def build_grid(x, y, char):
    m={}

    for i in range(x):
        at=""
        for j in range(y):
            if j==char.x and i==char.y:
                at=at+char.k
            else:
                at=at+"."
        m[i]=at
    return m

class character:
    def __init__(self, locationx, locationy, key, money):
        self.y=locationy
        self.x=locationx
        self.k=key
        self.money=money
class village:
    def __init__(self, locationx, locationy,  key, type):
        self.x=locationx
        self.y=locationy
        self.key=key
        self.type=type
    def enter_village(char):
        print("you enter a strange village")
        ar=input("cl")
        
    

def print_grid(gx, gy, character):
    a=(build_grid(gx, gy, character))
    for i in a.values():
        print(" ".join(i))
def cool_print(ste):
    a=len(ste)
    for i in ste:
        print(i, end="")
        time.sleep(2/a)

def check_grid(you, gridsize):
    xl=gridsize[0]
    yl=gridsize[1]
    print("your on the map")
    time.sleep(1)
    while True:
        if keyboard.is_pressed("w"):
            you.y=you.y-1
            os.system('cls||clear')
            print_grid(xl, yl, you)
        if keyboard.is_pressed("s"):
            you.y=you.y+1
            os.system('cls||clear')
            print_grid(xl, yl, you)
        if keyboard.is_pressed("d"):
            you.x=you.x+1
            os.system('cls||clear')
            print_grid(xl, yl, you)
            
        if keyboard.is_pressed("a"):
            you.x=you.x-1
            os.system('cls||clear')
            print_grid(xl, yl, you)
        time.sleep(0)
        if keyboard.is_pressed("m"):
            return()
grid_size=[20, 20]
a=input("""character key (this must be 1 letter) 
> """)
you=character(2, 2, a, 0)

while True:
    if keyboard.is_pressed("m"):
        check_grid(you, grid_size)
        print("you left the map")
        time.sleep(1)
    
    time.sleep(0.1)
