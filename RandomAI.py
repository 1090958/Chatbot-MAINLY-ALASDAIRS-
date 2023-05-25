import random
import sys
import Weapons
from Base import *




        
class AI(Player):
    def __init__(self,Name,Class,Level):
        super().__init__(Name, Class, Level)
        
    def Turn(self):
        
        for move, cooldown in self.moves.items():
            if cooldown != 0:
                self.moves[move]=cooldown-1
        possible=False
        for _ in self.moves:
            if self.moves[_]==0:
                possible=True
                break
        if possible == True:
            while True:
                move, cooldown = random.choice(list(self.moves.items()))
        
                if cooldown == 0:
                    move()
                    break
        
class Goblin(AI):
    def __init__(self,name):
        super().__init__(name, 'Goblin', 1)
        self.moves={
            self.Scimitar:1,
            self.Shortbow:1
            }
        self.AC=15
        self.Maxhealth=7
        self.Health=self.Maxhealth
        self.shield=False
        Player.Weaponize(self,Weapons.scimitar())
        Player.Weaponize(self,Weapons.shortbow())
        self.held=self.Weapon[0]
        
    def Scimitar(self):
        weapon=self.Weapon[0]
        self.held=self.Weapon[0]
        random.shuffle(self.enemies)
        self.enemies[0].Damage(random.randint(0, self.held.Damage)+self.held.Modifier,random.randint(0,21)+self.held.Proficiency,self)
        
    def Shortbow(self):
        weapon=self.Weapon[1]
        random.shuffle(self.enemies)
        self.held=self.Weapon[1]
        self.enemies[0].Damage(random.randint(0, self.held.Damage)+self.held.Modifier,random.randint(0,21)+self.held.Proficiency,self)
#debugging
'''gobley=Goblin('Gobley')
boblin=Goblin('Boblin')
gobley.Enemy=boblin
gobley.Turn()'''