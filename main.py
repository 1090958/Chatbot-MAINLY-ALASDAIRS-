import random
import time
import keyboard
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
    def __init__(self, locationx, locationy, key, money, speed, health, damage, items):
        self.y=locationy
        self.x=locationx
        self.k=key
        self.money=money
        self.speed=speed
        self.health=health
        self.damage=damage
        self.items=items
    def checkitems(self):
        a=len(self.items)
        print("Items:", end="")
        if a ==0:
            print("nothing")
        else:
            for i in self.items:
                print(i, end=" ")

        
player=character(0, 0, "@", 0, 10, 10, 1, ["cocian", "silly child"])

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
            print_grid(xl, yl, you)
        if keyboard.is_pressed("s"):
            you.y=you.y+1
            print_grid(xl, yl, you)
        if keyboard.is_pressed("d"):
            you.x=you.x+1
            print_grid(xl, yl, you)
        if keyboard.is_pressed("a"):
            you.x=you.x-1
            print_grid(xl, yl, you)
        time.sleep(0.1)
        if keyboard.is_pressed("m"):
            return()
class biome:
    def __init__(self, x, y, key, looks, ents):
        self.x=x
        self.key=key
        self.y=y
        self.looks=looks
        self.ents=ents
    def enter(biome):
        print(biome.looks)
    def search(biome):
        l=len(biome.ents)
        vowels=["a", "e", "i", "o", "u"]

        print("you see")

        for i in biome.ents:
            if biome.ents.index(i)==(l-2):
                if i[0] in vowels:
                    print(f"an {i} and ")
                else:
                    print(f"a {i} and ")
            elif biome.ents.index(i)==(l-1):
                if i[0] in vowels:
                    print(f"an {i}")
                else:
                    print(f"a {i}")
            else:
                if i[0] in vowels:
                    print(f"an {i}, ")
                else:
                    print(f"a {i}, ")
new_land=biome(3, 4, "k", "a barren wasteland, grey clouds covering the sky and the sun, the smell of rotting flesh and stagnant air seeping into your cloths and nose", ["corrupted man", "Beast", "mongrelic parasite", "amathion"])

new_land.enter()
new_land.search()
    


        











