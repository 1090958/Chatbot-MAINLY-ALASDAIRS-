

class character:
    """The parent class for all player characters and non-player characters
    in the game.\n
    max_Health
        the character's maximum health
    base_Speed
        the character's base speed
    """
    def __init__(self, max_Health, base_Speed, AC):
        self.max_Health = max_Health
        self.Health = max_Health
        self.base_Speed = base_Speed
        self.AC=AC
        self.faction = 1
        
        self.weapons = []
    
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
            self.Health -= damage
            return True
            
            
     
    
    
class player_Character(character):
    """The player controlled character."""
    def __init__(self, constitution, strength, dexterity, charisma):
        self.constitution = constitution
        self.strength = strength
        self.dexterity = dexterity
        self.charisma = charisma
        super().__init__(5 + constitution/4, 5, 10+self.dexterity,)
        self.faction = 0
    def take_Turn(self, enemies:list, allies:list):
        """Lets the player make a turn during combat
        enemies
            A list of all enemies, including those that are dead.
        """
        if input('>>> ') == 'Attack':
            pass


x=player_Character(15, 15, 15, 15)