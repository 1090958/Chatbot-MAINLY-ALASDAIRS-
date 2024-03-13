import random
import error, dice, attack_Types
class weapon:
    def __init__(self, name:str, range:tuple|int, damage_Dice:dice.dice|dice.generic_Dice, weight:float|int, attack_Types:tuple|attack_Types.Attack|attack_Types.Slashing|attack_Types.Bludgeoning, weapon_Class:str, falloff = lambda x:1):
        
        # range:
        # either with an int where there is not a minimum range(good for swords)
        # or with a tuple, where there is a minimum range(good for ranged weapons)
    
        if type(range) == int:
            self.max_Range = range
            self.min_Range = range
        elif type(range) == tuple:
            self.max_Range = range[1]
            self.min_Range = range[1]
        else:
            raise error.invalid_Attribute_Type(range,(tuple,int))
            
        
        # damageDice:
        # a dice class containing the dice to roll for damage
        # either a dice.dice class or a dice.genericDice class
        
        if type(damage_Dice) == dice.dice or type(damage_Dice) == dice.generic_Dice:
            self.damage_Dice = damage_Dice
        else:
            raise error.invalid_Attribute_Type(damage_Dice,(dice.dice,dice.generic_Dice))
        
        # weight:
        # a float or an int
        # determines the weapon weight.
        # this will slow down the player. 
        # in pounds
        if type(weight) == int or type(weight) == float:
            self.weight = weight
        else:
            raise error.invalid_Attribute_Type(weight,(float,int))
        
        
        
        # attack_Type:
        # a string with the attack type
        # determines the vulnerability of an enemy when attacking
        self.attack_Types = attack_Types
        
        
        
        
        
        
salmon = weapon('salmon', 10, dice.generic_Dice(2,6), 1.0, attack_Types.Attack(),"fish")
    
    