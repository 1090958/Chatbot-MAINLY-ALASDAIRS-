import random
import sys
import Weapons
import RandomAI as AI
from Base import *



maths = maths()

#todo, working on player interface, prototype is as follows
#During battle
'''
It is your turn, you are currently on x of your max of x health, your enemies are x, x and x.
what do you want to do(remember you can ask for help to learn what you can do)
'''
#if you won and are on more than 50% health
'''
You won, it was trivial, you could still probably take a short rest 
'''
#if you won and are on less than 50% healty
'''
You won although not without some losses, it is best you rest and patch up your wounds for some time.
'''
class Fighter(Player):
    def __init__(self):
        super().__init__('Brunor Battlehammer', 'Fighter', 1)
        Player.Weaponize(self,Weapons.longsword())
        self.AC=15
        
        self.Maxhealth=10
        self.Health=self.Maxhealth
        self.held=self.Weapon[0]
        self.options={'Change'}
    def Turn(self):
        
        print()
    def Change(self):
        joined='\n'.join([str(i.Name).title() for i in self.Weapon])
        print(f'You have the following weapons that you can change into;\n{joined}')
        #todo, implement my autoinput program into weapon changing
        weapon = input('What weapon do you chose?')
        a=[str(i.Name).title() for i in self.Weapon]
        while True:
            if weapon in a:
                for i in range(len(a)):
                    if a[i]= str(self.Weapon.Name) str
        
    def Attack(self):
        self.Enemy.Damage(random.randint(0, self.held.Damage)+self.held.Modifier,random.randint(0,21)+self.held.Proficiency,self)
    
    
            
    
def Fightloop(P1, P2):
    P1speed=round(sum([i.Base_Speed for i in P1.Weapon])/len(P1.Weapon))
    P1.Enemy=P2
    P2speed=round(sum([i.Base_Speed for i in P2.Weapon])/len(P2.Weapon))
    P2.Enemy=P1
    
    clock_max= maths.LCM(P1speed,P2speed)
    clock_cur= 0
    clock_cur
    while True:
        
        clock_cur += 1
        print(clock_cur)
        if clock_cur % P1speed==0:
            debug('P1 turn')
            P1.Turn()
            
        if clock_cur % P2speed==0:
            debug('P2 turn')
            P2.Turn()
        
        if clock_cur == clock_max:
            clock_cur = 0
        
        
Player = Fighter()
Player.Change()
Enemy = AI.Goblin('Gobbley')


Fightloop(Player,Enemy)