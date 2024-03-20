import items.settings as settings

class Rarity:
    def __init__(self, name:str, colour:str|None=None) -> None:
        self.name = name
        self.colour = colour
    def __str__(self) -> str:
        return self.name

common = Rarity("Common")
uncommon = Rarity("Uncommon")
rare = Rarity("Rare")
sub_mythic = Rarity("Sub-Mythic",settings.subMythicCol)
mythic = Rarity("Mythic",settings.mythicCol)
special = Rarity("Special",settings.specialCol)