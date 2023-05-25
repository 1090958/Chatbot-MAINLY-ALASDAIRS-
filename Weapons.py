import sys
from Base import *
class weapon:
    def __init__(self, rarity, Range, Damage, Weight_Pounds, Block, Type, Modifier,Proficiency, Name):
        
        if rarity==1:
            #finding given our values how to allocate them evenly based on rarity
            per=15/(Damage - Weight_Pounds + Block + Modifier+Range/10)
            NDamage, NBlock,NRange=[round(i*per) for i in [Damage, Block, Range]]
               
        self.Range = NRange
        self.Damage = NDamage
        self.Base_Speed = Weight_Pounds * 1#base speed modifier, 4 is middlish number
        self.Block = NBlock
        self.Type = Type
        self.Modifier= Modifier
        self.Proficiency=Proficiency
        self.Name=Name
        
#Example

class battleaxe(weapon):
    def __init__(self, rarity=1):
        Range, Damage, Weight_Pounds, Block, Modifier, Proficiency=5,8,4,2,0,2#sets proportions to values
        super().__init__( rarity, Range, Damage, Weight_Pounds, Block, 'slashing', Modifier, Proficiency, 'battleaxe')
        debug(f'{self.Range},{self.Damage},{self.Base_Speed},{self.Block},{self.Type}')
class longsword(weapon):
    def __init__(self, rarity=1):
        Range, Damage, Weight_Pounds, Block, Modifier, Proficiency=5,8,3,5,0,3#sets proportions to values
        super().__init__(rarity, Range, Damage, Weight_Pounds, Block, 'slashing', Modifier, Proficiency, 'longsword')
        
        debug(f'{self.Range},{self.Damage},{self.Base_Speed},{self.Block}, {self.Type}')
class banana(weapon):
    def __init__(self, rarity=1):
        Range, Damage, Weight_Pounds, Block, Modifier, Proficiency=5,10,10,2,0,5#sets proportions to values
        super().__init__(rarity, Range, Damage, Weight_Pounds, Block, 'slashing', Modifier, Proficiency, 'longsword')
class scimitar(weapon):
    def __init__(self, rarity=1):
        Range, Damage, Weight_Pounds, Block, Modifier, Proficiency=5,6,3,5,2,4#sets proportions to values
        super().__init__(rarity, Range, Damage, Weight_Pounds, Block, 'slashing', Modifier, Proficiency, 'scimitar')
        
        debug(f'{self.Range},{self.Damage},{self.Base_Speed},{self.Block}, {self.Type}')
        
class shortbow(weapon):
    def __init__(self, rarity=1):
        Range, Damage, Weight_Pounds, Block, Modifier, Proficiency=100,6,2,0,2,4#sets proportions to values
        super().__init__(rarity, Range, Damage, Weight_Pounds, Block, 'piercing', Modifier, Proficiency, 'shortbow')
        
        debug(f'{self.Range},{self.Damage},{self.Base_Speed},{self.Block}, {self.Type}')
        


'''
shorty=battleaxe()
#shorty.init(shorty)
print(shorty.Base_Speed)'''
