import items.objects as objects
import items.rooms as rooms

class CharacterType:
    def __init__(self, name:str, defaultAttack:objects.ObjectType, data:dict) -> None:
        self.name = name
        self.default = defaultAttack
        self.data = data
    def __str__(self) -> str:
        return f"ObjectType({self.name}, {self.default}, {self.data})"

class Character:
    def __init__(self, _type:CharacterType, location:list[int], name:str, inventory:list[objects.Object|None]=[None]*6) -> None:
        self.type = _type
        self.loc = location
        self.name = name
        self.inv = inventory
        self.hp = self.type.data["health"]
        self.armour = [None,None,None,None]
        self.effects = []
    def __str__(self) -> str:
        pass

player = CharacterType("Player", objects.basicSword, {"health":200,"defense":10,"speed":3})
npc = CharacterType("Default NPC", objects.basicSword, {"health":150,"defense":10,"speed":1})