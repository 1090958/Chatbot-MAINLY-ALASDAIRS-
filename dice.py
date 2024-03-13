import random

class die:
    # sides is a list(ints) of each side of the die
    # weights is a list(ints) of the weights of each corresponding side
    def __init__(self, sides:list[float|int], weights:list[int]|None=None):
        self.sides = sides
        self.weights = [1]*len(sides)
    # returns as the name implies
    def roll(self)-> int|float:
        #todo
        return random.choice(self.sides)

# just a die that has ascending sides up to the 'highest_Side'
class generic_Die(die):
    def __init__(self, highest_Side:int):
        super().__init__(list(range(1, highest_Side + 1)))

# a group of dice  
class dice:
    #takes a list(dice) for input
    def __init__(self, dice:list[die|generic_Die]):
        self.dice = dice
        
    def roll(self, method = lambda rolls: sum(rolls)):
        rolls = []
        for die in self.dice:
            rolls.append(die.roll())
        return sum(rolls)
# a group of die following dnd conventions, i.e. 3d6 is
# number_Dice = 3
# die = 6
class generic_Dice(dice):
    def __init__(self, number_Dice, die):
        self.dice = [generic_Die(die) for _ in range(number_Dice)]