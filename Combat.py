import character, error
class encounter:
    """A class itended to be created for combat enconters.
    characters
        a list of objects that are of a subclass of a character"""
    def __init__(self, characters:list) -> None:
        self.factions = {}
        for character_ in characters:
            if type(character_) in character.character.__subclasses__()+[character.character]:
                pass
                #print(type(character_))
            else: raise error.invalid_character(character_)
            if character_.faction in self.factions:
                self.factions[character_.faction].append(character_)
            else:
                self.factions[character_.faction] = [character_]
    
    
e=encounter([character.player_Character(15,15,15,15), character.player_Character(15,15,15,15)],)