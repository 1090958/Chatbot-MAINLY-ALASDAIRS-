import time
import random
import keyboard

class character:
    def __init__(self, locationx, locationy, key, speed, health, damage):
        self.y=locationy
        self.x=locationx
        self.k=key
        self.speed=speed
        self.health=health
        self.damage=damage
    quests=[]
    items={}
    def checkitems(self):
        a=len(self.items)
        print("Items:", end="")
        if a ==0:
            print("nothing")
        else:
            for i in self.items:
                print(i, self.items.get(i))
    def check_quests(self):
        if len(self.quests)==0:
            print("no quests are currently active")
        else:
            for i in self.quests:
                print("goal:",i.goal, "reward:", i.reward)
    def get_new_quest(character, quest):
        print(quest)
        character.quests.append(quest)
        print(f"""you got a new quest!
        Goal: {quest.quest_type} {quest.amount} {quest.entity} 
        Reward: {quest.reward[0]}, {quest.reward[1]}""")
    def get_items(self, item, amount):
        try:
            self.items[item]=amount+self.items.get(item)
        except:
            self.items[item]=amount

class biome:
    def __init__(self, x, y, key, looks):
        self.x=x
        self.key=key
        self.y=y
        self.looks=looks
    def enter(biome):
        print(biome.looks)
    
class village(biome):
    def __init__(self, x, y, key, looks):
        super.__init__(self, x, y, key, looks)
    def enter(village):
        print(village.looks)
    def quests(village):
        print()

class quests:
    def __init__(self, difficulty, reward, ):
        self.difficulty = difficulty
        self.reward=reward

class kill_quest():
    def __init__(self, difficulty, reward, entity, amount, identity):
        self.difficulty=difficulty
        self.reward=reward
        self.entity=entity
        self.amount=amount
        self.identity=identity
        self.quest_type="kill"
        self.goal=(f"{self.quest_type} {entity} {amount}")
    def add_to_quest(self, entity):
        if entity==self.entity:
            self.amount=self.amount-1
    def check_quest(self):
        if self.amount<1:
            print("quest complete")
        else:
            print(f"you have {self.amount} more {self.entity} to kill")
    def give_reward(self, character):
        character.get_items(self.reward[0], self.items[1] )
        
        


    
a={}
m=kill_quest(2, [10, "gold"], "cow", 2, "m")
player=character(0, 0, "k",  0, 1, 1)

player.get_new_quest(m)
player.checkitems()
player.get_items("gold", 20)
player.checkitems()
player.check_quests()

player.get_items("gold", 20)
player.checkitems()