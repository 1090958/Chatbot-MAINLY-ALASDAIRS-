from weapons import weapon
import dice, attack_Types, random
d20 = dice.generic_Die(20)

class character:
    """The parent class for all player characters and non-player characters
    in the game.\n
    max_Health
        the character's maximum health
    base_Speed
        the character's base speed
    """
    def __init__(self, max_Health:int, base_Speed:int, AC:int, name:str = 'Joe'):
        self.name = name
        self.max_Health = max_Health
        self.health = max_Health
        self.base_Speed = base_Speed
        self.AC=AC
        self.faction = 1
        
        self.weapon = weapon('Longsword', 5, dice.generic_Dice(3,6), 3, 4, attack_Types.Slashing, 'Sword')
        self.coordinates = (0, 0)
    def __str__(self):
        return self.name
    def take_Hit(self, DC, damage) -> bool: 
        """function used to determine if a character can be hit and applies the damage
        DC
            The roll (of a d20 plus proficiency)
        damage
            The damage to be done to the character on a hit
            
        returns a True on hit and a False on a miss
        """
            
        
        if self.AC >= DC:
            return False
        else:
            self.health -= damage
            self.health = max(0,self.health)
            return True
        
        
    def take_Turn(self, enemies:list, allies:list):
        if self.health == 0:
            return
        x = random.choice(enemies)
        print(x.health)
        self.attack(x)
    def attack(self, target, weapon:weapon):
        DC = 20 #d20.roll()
        damage = self.weapon.damage_Dice.roll()+self.weapon.damage_Modifier
        damage *= 2 if DC == 20 else 1
        DC += self.weapon.proficiency
        target.take_Hit(damage=damage)
        
     
    
    
class player_Character(character):
    """The player controlled character."""
    def __init__(self, constitution, strength, dexterity, charisma):
        self.constitution = constitution
        self.strength = strength
        self.dexterity = dexterity
        self.charisma = charisma
        super().__init__(5 + constitution/4, 15, 10+self.dexterity)
        self.faction = 0
        
    def take_Turn(self, enemies:list[character], allies:list[character]):
        """Lets the player make a turn during combat
        enemies
            A list of all enemies, including those that are dead.
        """
        input_ = input('>>> ').lower()
        if 'attack' in input_:
            self.attack(enemies[-1])

