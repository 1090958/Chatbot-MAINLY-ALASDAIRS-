class Effect:
    def __init__(self, name:str, effect:str, level:int, time:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level
        self.time = time

con1 = Effect("Health Boost I","constitution",10,10)
dex1 = Effect("Heightened Reflexes I","dexterity",10,10)

class Enchantment:
    def __init__(self, name:str, effect:str, level:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level

prot1 = Enchantment("Protection I","protect",6)
prot2 = Enchantment("Protection II","protect",10)