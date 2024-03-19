import random
import sys
import weapons
from Base import *
import time



        
class AI(Player):
    def __init__(self,Name,Class,Level,x,y,timeToMove=2):
        super().__init__(Name, Class, Level,x,y)
        self.time=0
        self.timeToMove=timeToMove
        
    def Turn(self):
        
        for move, cooldown in self.moves.items():# type: ignore
            if cooldown != 0:
                self.moves[move]=cooldown-1# type: ignore
        possible=False
        for _ in self.moves:# type: ignore
            if self.moves[_]==0:# type: ignore
                possible=True
            if possible == True:
                while True:
                    move, cooldown = random.choice(list(self.moves.items()))# type: ignore
        
                    if cooldown == 0:
                        move()
                        time.sleep(1)
                        return
    def Move(self,grid):
        x=random.randint(1,4)
        if self.time == self.timeToMove:
            self.time=0
            if x==1 and len(grid)-1 > self.y:
                self.y+=1
                return
            if x==2 and 0 != self.y:
                self.y-=1
                return
            if x==3 and len(grid[0])-1 > self.x:
                self.x+=1
                return
            if x==4 and 0 != self.x:
                self.x-=1
                return
        else:
            self.time+=1
            return
class Goblin(AI):
    def __init__(self,name,x,y):
        super().__init__(name, 'Goblin', 1,x,y)
        self.moves={
            self.Scimitar:1,
            self.Shortbow:1
            }
        self.AC=15
        self.Maxhealth=7
        self.Health=self.Maxhealth
        self.shield=False
        self.key='G'
        Player.Weaponize(self,weapons.scimitar())
        Player.Weaponize(self,weapons.shortbow())
        self.held=self.Weapon[0]
        
    def Scimitar(self):
        weapon=self.Weapon[0]
        self.held=self.Weapon[0]
        random.shuffle(self.enemies)# type: ignore
        self.enemies[0].Damage(random.randint(0, self.held.Damage)+self.held.Modifier,random.randint(0,21)+self.held.Proficiency,self)# type: ignore
        
    def Shortbow(self):
        weapon=self.Weapon[1]
        random.shuffle(self.enemies)# type: ignore
        self.held=self.Weapon[1]
        self.enemies[0].Damage(random.randint(0, self.held.Damage)+self.held.Modifier,random.randint(0,21)+self.held.Proficiency,self)# type: ignore

class Person(AI):
    def __init__(self,name,x,y):
        super().__init__(name, 'Person', 1,x,y)
        self.key=name[0]
        self.moves={
            self.longsword:1,
            }
        self.AC=10
        self.Maxhealth=10
        self.Health=self.Maxhealth
        self.shield=False
        Player.Weaponize(self,weapons.longsword())
        self.held=self.Weapon[0]
        
    def longsword(self):
        weapon=self.Weapon[0]
        self.held=self.Weapon[0]
        random.shuffle(self.enemies)# type: ignore
        self.enemies[0].Damage(random.randint(0, self.held.Damage)+self.held.Modifier,random.randint(0,21)+self.held.Proficiency,self)# type: ignore



#debugging
'''gobley=Goblin('Gobley')
boblin=Goblin('Boblin')
gobley.Enemy=boblin
gobley.Turn()'''