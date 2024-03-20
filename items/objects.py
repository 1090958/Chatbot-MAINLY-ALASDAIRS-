import items.rarity as rarity
import items.stuff as stuff
import items.settings as settings

class ObjectType:
    def __init__(self, name:str, rarity:rarity.Rarity, use:str, value:int|float, data:dict) -> None:
        self.name = name
        self.rarity = rarity
        self.use = use
        self.value = value
        self.data = data
    def __str__(self) -> str:
        return f"ObjectType({self.name}, {self.rarity}, {self.data})"

class Object:
    def __init__(self, _type:ObjectType) -> None:
        self.type = _type
        if "durability" in self.type.data:
            self.durability = self.type.data["durability"]
        elif "uses" in self.type.data:
            self.uses = self.type.data["uses"]
    def __str__(self) -> str:
        x = ""
        if self.type.rarity.colour != None:
            x += f"\033{self.type.rarity.colour}  - {self.type.name} [{self.type.rarity}] \033[0m"
        else:
            x += f"  - {self.type.name} [{self.type.rarity}]"
        for enchant in self.type.data["enchantments"]:
            x += f"\n\033{settings.enchantmentCol}      - {enchant} \033[0m"
        for effect in self.type.data["effects"]:
            x += f"\n\033{settings.effectCol}      - {effect} \033[0m"
        return x

basicSword = ObjectType("Basic Sword", rarity.common, "weapon", 20, {"attack":25,"durability":100,"speed":4,"enchantments":[],"effects":[]})
basicHelmet = ObjectType("Basic Helmet", rarity.uncommon, "armour0", 30, {"protection":10,"durability":200,"enchantments":[],"effects":[]})
enchIronLeggings = ObjectType("Enchanted Iron Chestplate", rarity.rare, "armour2", 140, {"protection":80,"durability":250,"enchantments":[stuff.prot1],"effects":[]})
coolChestplate = ObjectType("Cool Chestplate", rarity.special, "armour1", 140, {"protection":100,"durability":400,"enchantments":[stuff.prot2],"effects":[]})
cocaine = ObjectType("Cocaine", rarity.rare, "effectPosi", 75, {"uses":5,"enchantments":[],"effects":[stuff.dex1]})