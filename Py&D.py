import random
import sys
import Weapons
import RandomAI as AI
from Base import *
import AI_input_comprehension


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
        
        self.Maxhealth=100
        self.Health=self.Maxhealth
        self.held=self.Weapon[0]
        self.options={'Change'}
    def Turn(self):
        #get user input
        userin=input('What do you want to do?')
        #check if the user wants to change weapon
        if 'change' in userin.lower():
            weapons=[str(i.Name).lower() for i in self.Weapon]
            for weapon in weapons:
                if weapon in userin.lower():
                    self.Change(weapon)
                    break
        if 'hit' in userin.lower():
            for enemy in self.enemies:
                if enemy.Name.lower() in userin.lower():
                    self.Enemy=enemy
                    break
            self.Hit(enemy)
        if 'heal' in userin.lower():
            for ally in self.allies:
                if ally.Name.lower() in userin.lower():
                    self.Ally=ally
                    break
            self.Heal(ally)
        print()
    def Change(self,Weapon):
        #joined='\n'.join([str(i.Name).title() for i in self.Weapon])
        #print(f'You have the following weapons that you can change into;\n{joined}')
        #todo, implement my autoinput program into weapon changing
        #weapon = input('What weapon do you chose?')
        #swap the current weapon for the new one
        self.held=Weapon
        '''a=[str(i.Name).title() for i in self.Weapon]
        while True:
            if weapon in a:
                for i in range(len(a)):
                    if a[i]= str(self.Weapon.Name) str'''
    
        
    def Hit(self,enemy):
        print('hitting')
        amount=random.randint(0, self.held.Damage)+self.held.Modifier
        dc=random.randint(1,20)+self.held.Proficiency
        enemy.Damage(amount,dc,self)
    def Heal(self):
        pass

    
    
            
    
def Fightloop(party1, party2):
    for ally in party1:
        ally.enemies=party2
    for enemy in party2:
        enemy.enemies=party1
    clock_cur= 0
    while True:
        
        clock_cur += 1
        totalhealth=0
        for character in party1:
            if clock_cur % character.held.Base_Speed==0:
                character.Turn()
            totalhealth+=character.Health
        if totalhealth==0:
            return('loss')
        totalhealth=0
        for character in party2:
            if clock_cur % character.held.Base_Speed==0:
                character.Turn()
            totalhealth+=character.Health
        if totalhealth==0: 
            return('win')
        
        
        
Player = Fighter()
Enemy = AI.Goblin('Gobbley')


print(Fightloop([Player],[Enemy]))