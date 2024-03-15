import character, error

#function that indexes a list of tuples
def search_List(list_:list[tuple[int,all]], value) -> all:
    keys = [list__[0] for list__ in list_]
    return [list__[-1] for list__ in list_][keys.index(value)]


class encounter:
    """A class itended to be created for combat enconters.
    characters
        a list of tuples, each tuple contains an object with 
        the parent class character and coordinates of type [x,y]
        """
    def __init__(self, characters:list[tuple[character.character,list[int,int]]]) -> None:
        # hopefully this doesn't need to be rewritten because I forgot to comment this properly
        # factions is a dictionary of groups of allies
        # this is determined by a faction value determined when creating a character
        self.factions = {}
        self.characters:list[character.character] = []
        for character_ in characters:
            self.add(character_)
    def add(self, *args) -> None:
        for character_ in args:
            if type(character_[0]) in character.character.__subclasses__()+[character.character]:
                pass
            else: raise error.invalid_character(character_)
            character_[0].coordinates = character_[-1]
            if character_[0].faction in self.factions:
                self.factions[character_[0].faction].append(character_[0])
            else:
                self.factions[character_[0].faction] = [character_[0]]
            self.characters.append(character_[0])
        
    def turn(self, subturns:int=4) -> int:
        """Initiates a turn of combat, One turn of combat involves multiple actions and just involves 4 subturns
        """
        # a list of tuples containing the faction and a list of enemies each
        options = []
        
        # 'Baking' the enemies lists
        for faction in self.factions:
            others = [i[-1] for i in self.factions.items() if i[0] != faction]
            
            enemies = []
            for other in others:
                enemies += other
            options.append((faction,enemies))
            

            
        

        for subturn in range(1, subturns+1): # 4 is not set in place just a test
            # check if anyone has won yet, if so end the turn early, returning the faction name of the winning faction
            for option in options:
                enemies = option[-1]
                win = True
                for enemy in enemies:
                    if enemy.health > 0:
                        win = False
                        break            
                if win:
                    return option[0]
            # otherwise,
            self.subturn(subturn, options)
        return -1
    def subturn(self,counter:int, options) -> None:
        
        for character_ in self.characters:
            if counter % character_.weapon.weight == 0:
                #find some needed variables
                enemies = search_List(options, character_.faction)
                allies = self.factions[character_.faction].copy()
                allies.remove(character_)
                # trigger the player's turn
                character_.take_Turn(enemies, allies)
if __name__ == "__main__":
    e=encounter([(character.player_Character(15,15,3,15),[0,0]), (character.character(15,15,15),[0,0])])
    a = -1
    while a == -1:
        a = e.turn()
        print(a)
        print(e.characters[-1].health)
    

