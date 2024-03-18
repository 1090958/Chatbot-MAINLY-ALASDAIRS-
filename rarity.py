class Rarity:
    def __init__(self, name:str, colour:str|None=None) -> None:
        self.name = name
        self.colour = colour
    def __str__(self) -> str:
        return self.name

common = Rarity("Common")
uncommon = Rarity("Uncommon")
rare = Rarity("Rare")
sub_mythic = Rarity("Sub-Mythic", "[1;35m")
mythic = Rarity("Mythic", "[1;33m")
special = Rarity("Special", "[1;31m")