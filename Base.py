class Player:
    def __init__(self, Name, Class, Level,x,y):
        self.Name = Name
        self.Class = Class
        self.Level = Level
        self.Enemy = None
        self.AC=0
        self.Weapon=[]
        self.x=x
        self.y=y
        debug(f'Created {self.Name}, a Level {self.Level} {self.Class}')
    def Weaponize(self, weapon,):
        self.Weapon.append(weapon)
    def Damage(self, amount, DC, enemy):
        if self.Health<=0:
            self.Health=0
            print(f'{self.Name} the {self.Class} is dead, ')
        elif DC > self.AC-1:
            damage=round(amount-amount/20*self.held.Block) # type: ignore
            self.Health-=damage
            print(f'{enemy.Name} the {enemy.Class} attacks {self.Name} with their {enemy.held.Name}, they deal, {damage} damage')
        else:
            print(f'{enemy.Name} the {enemy.Class} tries to attack {self.Name} with their {enemy.held.Name}, they miss')
        if self.Health<=0:
            self.Health=0
            print(f'{self.Name} the {self.Class} is dead, ')
        
        
        

#debugging functions
def debug(debugging):
    #print(f'DEBUG: {debugging}')
    pass
    
#quick math functions in a class
class maths:
    '''To find the Lowest Common Multiple of a pair'''
        #Goes up by one to find an integer number both inputs are divisible by without a remainder
    def LCM(self, Num1, Num2):
        if Num1 >= Num2:
            Greater = Num1
        else:
            Greater = Num2
        
        while True:
            if((Greater % Num1 == 0) and (Greater % Num2 == 0)):
                LCM = Greater
                debug(f'The LCM is: {LCM}')
                break
            Greater += 1
        return LCM