import rarity

class ObjectType:
    def __init__(self, name:str, rarity:rarity.Rarity, use:str, data:dict) -> None:
        self.name = name
        self.rarity = rarity
        self.use = use
        self.data = data
    def __str__(self) -> str:
        return f"ObjectType({self.name}, {self.rarity}, {self.data})"

class Object:
    def __init__(self, _type:ObjectType) -> None:
        self.type = _type
    def __str__(self) -> str:
        x = ""
        if self.type.rarity.colour != None:
            x += f"\033{self.type.rarity.colour}  - {self.type.name} [{self.type.rarity}] \033[0m"
        else:
            x += f"  - {self.type.name} [{self.type.rarity}]"
        for enchant in self.type.data["enchantments"]:
            x += f"\n\033[1;36m      - {enchant} \033[0m"
        for effect in self.type.data["effects"]:
            x += f"\n\033[1;32m      - {effect} \033[0m"
        return x

basicSword = ObjectType("Basic Sword", rarity.common, "weapon", {"attack":25,"durability":100,"speed":4,"enchantments":[],"effects":[]})
basicHelmet = ObjectType("Basic Helmet", rarity.uncommon, "armour0", {"protection":10,"durability":200,"enchantments":[],"effects":[]})
coolChestplate = ObjectType("Cool Chestplate", rarity.special, "armour1", {"protection":100,"durability":400,"enchantments":["Protection II"],"effects":[]})
cocaine = ObjectType("Cocaine", rarity.rare, "effectPosi", {"uses":5,"enchantments":[],"effects":["Heightened Reflexes I"]})