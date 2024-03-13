'''import random
import Weapons
def hit():
    print('get hit')
def heal():
    print('get healed')
x
moves={
    hit:['attack','kill','hurt','murder','strike','hit','bash','smash','smack','wallop','assassinate','slay','dispatch', 'eradicate','annihilate','exterminate','finish','massacre','behead','hang','shoot','fire'],
    heal:['heal']#todo, add more words for healing
    }
parameters={#options are a player(enemy or ally, name or class), a weapon or an item
    hit:['enemy','weapon']
    }
x='bash'
held=Weapons.longsword()
def return_move(inputs,allies=[], enemies=[]):
    inputs=inputs.lower().split()
    for move, keywords in moves.items():
        for keyword in keywords:
            if keyword in inputs:
                function=move
    params
    for requirement in parameters[function]:
        
        if requirement == 'ally':
            for p in [i.Name for i in allies]:
                if p in inputs:
                    target=p
        elif requirement == 'enemy':
            for p in [i.Name for i in enemies]:
                if p in inputs:
                    target=p
        elif requirement == 'weapon' and held.Name.lower() !=

    
    
class random_guy():
    def __init__(self,name):
        self.Name=name#+str(random.randint(0,99))
        
ally1,ally2,enemy1,enemy2=random_guy('Johnson'),random_guy('Jerome'),random_guy('Jeffery'),random_guy('Jake')
allies=[ally1,ally2]
enemies=[enemy1,enemy2]
return_move(x,allies=allies,enemies=enemies)'''
import random
from Base import *
import weapons

def hit():
    print('get hit')

def heal():
    print('get healed')

moves = {
    hit: ['attack', 'kill', 'hurt', 'murder', 'strike', 'hit', 'bash', 'smash', 'smack', 'wallop', 'assassinate', 'slay', 'dispatch', 'eradicate', 'annihilate', 'exterminate', 'finish', 'massacre', 'behead', 'hang', 'shoot', 'fire'],
    heal: ['heal'] # todo, add more words for healing
}

parameters = {
    hit: ['enemy', 'weapon']
}

held = weapons.longsword()

def return_move(inputs, user,allies=[], enemies=[]):
    inputs = inputs.lower().split()
    for move, keywords in moves.items():
        for keyword in keywords:
            if keyword in inputs:
                function = move
                break

    for requirement in parameters[function]:
        if requirement == 'ally':
            for p in [i.Name.lower() for i in allies]:
                if p in inputs:
                    target = p
        elif requirement == 'enemy':
            for p in [i.Name.lower() for i in enemies]:
                if p in inputs:
                    target = p
        elif requirement == 'weapon' and held.Name.lower() != inputs:
            for w in user.Weapon:
                if w.Name in inputs:
                    target = w

    if function == 'hit':
        if target:
            print('You hit {} with your {}.'.format(target, held.Name))
        else:
            print('You didn\'t specify a target.')
    elif function == 'heal':
        if target:
            print('You healed {}.'.format(target))
        else:
            print('You didn\'t specify a target.')
class random_guy(Player):
    def __init__(self,name):
        self.Name=name#+str(random.randint(0,99))
        self.Weapon=[]
        Player.Weaponize(self,weapons.longsword())
        
        
        
ally1, ally2, enemy1, enemy2 = random_guy('Johnson'), random_guy('Jerome'), random_guy('Jeffery'), random_guy('Jake')
allies = [ally1, ally2]
enemies = [enemy1, enemy2]
x='bash jake'
return_move(x, random_guy('You') ,allies=allies, enemies=enemies)

