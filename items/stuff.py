import pygame,random,variables

lore = ["""Entry 1: Whilst I doubt anyone will ever read this anyway more and more surface dwellers are appearing here with no recollection of who they are. I believe the dungeons strip you of your past life (some believe the dungeon is even alive). I was born here and with nothing better to do so I am writing a diary about history. Before the tunnels existed and the dungeons were found we lived on the surface. No one really remembers what it looked like but is was probably nicer than this place. The world was bent to 4 immortal beings, Fayre, Lilith, Gabriel and Lux. They were winged and beautiful, as far as we know they were always there.""",
        """Entry 2: Some worshipped them as gods some didn't really care about them but all was pretty much fine. Sometimes the immortals would fight. Their small brawls lasted years. At some point the immortals had a big fight and the great war started. The worshippers divided each to one immortal and war waged. Unlike the small fights of the past their war was violent their worshippers were savage, the world filled with death. Anyone who didn't choose a side was slaughtered anyway and they searched for asylum. That was why the tunnels were created and why the dungeons were found.""",
        """Entry 3: Something strange is going on. People of my clan are going missing; father says its nothing to worry about. My aunt says it's the goblins fault she says they are going savage. We aren't supposed to talk to the other clans but I have a friend named Arit in the peace cult. Or at least my aunt calls it the peace cult; they call themselves equalists.  Arit says people in his clan are going missing aswell. I'm worried.""",
        """Entry 4: The non-worshippers began to dig down creating a web of tunnels. The tunnels were not deep and the worshipers still managed to find them. The non-worshippers kept digging until they reached an unbreakable wall. They followed it for a long time until they found a breach.  At least they thought it was a breach, but it was a door. What they entered was the dungeon an incredible underground structure that stretched far and wide. The dungeon was devoid of any noticeable life but there were signs of creation. The non-believers had found their asylum.""",
        """Entry 5: After exploration a device was discovered capable of destroying even the thought unbreakable walls of the dungeon and tunnels were built connecting the dungeons to the surface. The device was named the breaker.  The breaker was able to not only destroy but build dungeon stone. Arit and I have been meeting in secret more often to talk about the disappearances. His clan came across a monster. He said it looked like a goblin but also like Fayre. It was savage and was quickly killed and examined. His clan thinks the monster was one of fayres worshippers, somehow so devout they tried to host her body.""",
        """Entry 6: As we left off the dungeons were found, and the non-worshippers began to live there. But as you can tell the dungeons weren't necessarily that nice. Leavers were slaughtered or came running back. Eventually a group called to peace, lead by a goblin named Catam (the peace cult). But his idea of peace revolved around murdering the immortals and many feared that the worshippers would hunt them down if they found their gods dead, or even worse they would reveal the dungeons to the immortals.""",
        """Entry 7: Catams cult grew and eventually set out to kill the immortals. they stole the breaker and used it to tunnel underground into each immortal's territory. They decided to trap the immortals as they could not kill them and created a prison out of the dungeon's rubble (using the breaker) . They created a letters pretending to be immortals asking to create alliances. They said the meeting place would be found by following a tunnel. The immortals got given letters and all fell for the trick, following the tunnels to the indestructible cage where they were locked in. This solution seemed permanent but it was short lived.""",
        """Entry 8: Our tribe has come across a great discovery! The immortal essence (I haven't told you about it yet) has come with great power! There are still people going missing and more monsters have been discovered.  After inspection it has been found that the monsters can also be extracted using the breaker just like the immortals (I will explain this soon reader). Anyway their essence is similar to the immortals but is impermanent weird right? Perhaps with this new power we will be able to come back to the surface.""",
        """Entry 9: The immortals were beginning to alert worshippers to their locations just as many had feared. The peace cult had a solution though, they used the breaker to create indestructible bottles and then used the breaker on the immortals. The immortals became an essence, which was then trapped in the jars. (arit tells me that the jars were necessary as when to much essence was held together it would begin to build back into the immortals).The jars were split across the dungeon. After this the non-worshippers began to split into more and more tribes, some even staying as nomads.""",
        """Entry 10: There is us the believers of freedom (that one day we should live on the surface alongside the worshippers). The peace cult / equalists (they believe the worshippers should be murdered). The goblins (they are split racially, they believe they are above the other tribes and steal a lot). And there are the grounded clan (believes the dungeon is alive and their only home, that the surface is a wasteland). There are more but they mostly keep to themselves, their ideologies unknown."""]

def loadImages(filename:str) -> None:
    names = [["p04","p03","p02","p01","p05","m0","b0"],
             ["p14","p13","p12","p11","p15","m1","b1"],
             ["p24","p23","p22","p21","p25","m2","b2"],
             ["p34","p33","p32","p31","p35","m3","b3"],
             ["p43","p42","p41","e0","e2","e3","x0"],
             ["s1","s0","s2","s3","e1","s4","s5"],
             ["a11","a21","a31","a41","a01","x51"],
             ["a12","a22","a32","a42","a02","x52"],
             ["a13","a23","a33","a43","a03","x53"],
             ["a14","a24","a34","a44","a04","x54"],
             ["al0","al1","al2","al3","al4","xx"]]
    img = pygame.image.load(filename+"main.png")
    for y in range(len(names)):
        for x in range(len(names[y])):
            new = img.subsurface((x*16,y*17),(16,16))
            pygame.image.save(new,filename+names[y][x]+".png")
    for i in range(2):
        new = img.subsurface((i*23,(y+1)*17),(23,23))
        pygame.image.save(new,filename+("c0" if i>0 else "c1")+".png")





class Effect:
    def __init__(self, name:str, effect:str, level:int, time:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level
        self.time = time
    def copy(self):
        return Effect(self.name, self.effect, self.level, self.time)

antiHealEff = Effect("Fayre's Curse", "health", -10, 5)
str20 = Effect("Strength I", "strength", 20, 3)
str100 = Effect("Strength V", "strength", 100, 3)
antiStrEff = Effect("Alexander's Curse", "strength", -20, 5)
dex20 = Effect("Dexterity I", "dexterity", 20, 3)
dex100 = Effect("Dexterity V", "dexterity", 100, 3)
antiDexEff = Effect("Gabriel's Curse", "dexterity", -20, 5)
pro10 = Effect("Protection I", "protection", 10, 3)
pro50 = Effect("Protection V", "protection", 50, 3)
pro50x = Effect("Protection V", "protection", 50, 15)
antiProEff = Effect("Lux's Curse", "protection", -20, 5)
potion41eff1 = Effect("Strength III", "strength", 50, 3)
potion41eff2 = Effect("Slowness I", "dexterity", -10, 3)
potion42eff1 = Effect("Protection III", "protection", 30, 3)
potion42eff2 = Effect("Weakness II", "strength", -50, 3)
potion43eff = Effect("Invisibility", "dexterity", 100, 3)
burningEff = Effect("Burning", "health", -10, 10)
bleedingEff = Effect("Bleeding", "health", -5, 10)
blindingEff = Effect("Blinding", "dexterity", -40, 5)




class Enchantment:
    def __init__(self, name:str, effect:str, level:int) -> None:
        self.name = name
        self.effect = effect
        self.level = level

burning = Enchantment("Curse of Burning", burningEff, 1)
bleeding = Enchantment("Curse of Bleeding", bleedingEff, 1)
blinding = Enchantment("Curse of Blinding", blindingEff, 1)
armourNeg = Enchantment("Armour Piecing", "armourNeg", 1)
healCurse = Enchantment("Fayre's Curse", antiHealEff, 1)
rageCurse = Enchantment("Alexander's Curse", antiStrEff, 1)
speedCurse = Enchantment("Gabriel's Curse", antiDexEff, 1)
crystalCurse = Enchantment("Lux's Curse", antiProEff, 1)





class Rarity:
    def __init__(self, name:str, colour:tuple) -> None:
        self.name = name
        self.colour = colour
    def __str__(self) -> str:
        return self.name

common = Rarity("common",(110,110,110))
uncommon = Rarity("uncommon",(0,150,0))
rare = Rarity("rare",(0,50,220))
epic = Rarity("epic",(100,0,220))
legendary = Rarity("legendary",(220,100,0))
mythic = Rarity("mythic",(120,120,0))
special = Rarity("special",(180,0,0))





class ObjectType:
    def __init__(self, name:str, image:str, rarity:Rarity, use:str, value:int|float, data:dict) -> None:
        self.name = name
        self.img = image
        self.rarity = rarity
        self.use = use
        self.value = value
        self.data = data

class Object:
    def __init__(self, _type:ObjectType) -> None:
        self.type = _type
        if "uses" in self.type.data:
            self.uses = self.type.data["uses"]
    
potion01 = ObjectType("Basic Healing Potion", "p01.png", rare, "instant", 20, {"uses":1,"healing":30,"enchantments":[],"effects":[]})
potion02 = ObjectType("Basic Healing Potion", "p02.png", rare, "instant", 50, {"uses":3,"healing":30,"enchantments":[],"effects":[]})
potion03 = ObjectType("Basic Healing Potion", "p03.png", epic, "instant", 90, {"uses":5,"healing":30,"enchantments":[],"effects":[]})
potion04 = ObjectType("Full Healing Potion", "p04.png", legendary, "instant", 90, {"uses":1,"healing":500,"enchantments":[],"effects":[]})
potion05 = ObjectType("True Healing Potion", "p05.png", mythic, "instant", 0, {"uses":1,"constitution":25,"enchantments":[],"effects":[]})
potion11 = ObjectType("Basic Rage Potion", "p11.png", rare, "effect", 20, {"uses":1,"enchantments":[],"effects":[str20]})
potion12 = ObjectType("Basic Rage Potion", "p12.png", rare, "effect", 50, {"uses":3,"enchantments":[],"effects":[str20]})
potion13 = ObjectType("Basic Rage Potion", "p13.png", epic, "effect", 90, {"uses":5,"enchantments":[],"effects":[str20]})
potion14 = ObjectType("Full Rage Potion", "p14.png", legendary, "effect", 90, {"uses":1,"enchantments":[],"effects":[str100]})
potion15 = ObjectType("True Rage Potion", "p15.png", mythic, "instant", 0, {"uses":1,"strength":25,"enchantments":[],"effects":[]})
potion21 = ObjectType("Basic Speed Potion", "p21.png", rare, "effect", 20, {"uses":1,"enchantments":[],"effects":[dex20]})
potion22 = ObjectType("Basic Speed Potion", "p22.png", rare, "effect", 50, {"uses":3,"enchantments":[],"effects":[dex20]})
potion23 = ObjectType("Basic Speed Potion", "p23.png", epic, "effect", 90, {"uses":5,"enchantments":[],"effects":[dex20]})
potion24 = ObjectType("Full Speed Potion", "p24.png", legendary, "effect", 90, {"uses":1,"enchantments":[],"effects":[dex100]})
potion25 = ObjectType("True Speed Potion", "p25.png", mythic, "instant", 0, {"uses":1,"dexterity":25,"enchantments":[],"effects":[]})
potion31 = ObjectType("Basic Crystal Skin Potion", "p31.png", rare, "effect", 20, {"uses":1,"enchantments":[],"effects":[pro10]})
potion32 = ObjectType("Basic Crystal Skin Potion", "p32.png", rare, "effect", 50, {"uses":3,"enchantments":[],"effects":[pro10]})
potion33 = ObjectType("Basic Crystal Skin Potion", "p33.png", epic, "effect", 90, {"uses":5,"enchantments":[],"effects":[pro10]})
potion34 = ObjectType("Full Crystal Skin Potion", "p34.png", legendary, "effect", 90, {"uses":1,"enchantments":[],"effects":[pro50]})
potion35 = ObjectType("True Crystal Skin Potion", "p35.png", mythic, "effect", 0, {"uses":1,"enchantments":[],"effects":[pro50x]})
potion41 = ObjectType("Strength Potion", "p41.png", epic, "effect", 100, {"uses":5,"enchantments":[],"effects":[potion41eff1,potion41eff2]})
potion42 = ObjectType("Scalene Skin Potion", "p42.png", epic, "effect", 100, {"uses":5,"enchantments":[],"effects":[potion42eff1,potion42eff2]})
potion43 = ObjectType("Invisibility Potion", "p43.png", legendary, "effect", 90, {"uses":1,"enchantments":[],"effects":[potion43eff]})
sword01 = ObjectType("Basic Sword", "s0.png", common, "weapon", 30, {"attack":15,"stamina":20,"hitRate":80,"enchantments":[],"effects":[]})
sword02 = ObjectType("Dull Basic Sword", "s0.png", common, "weapon", 30, {"attack":12,"stamina":20,"hitRate":80,"enchantments":[],"effects":[]})
sword03 = ObjectType("Sharp Basic Sword", "s0.png", common, "weapon", 30, {"attack":18,"stamina":20,"hitRate":80,"enchantments":[],"effects":[]})
sword04 = ObjectType("Light Basic Sword", "s0.png", common, "weapon", 30, {"attack":15,"stamina":20,"hitRate":92,"enchantments":[],"effects":[]})
sword05 = ObjectType("Heavy Basic Sword", "s0.png", common, "weapon", 30, {"attack":15,"stamina":20,"hitRate":72,"enchantments":[],"effects":[]})
sword11 = ObjectType("Flame Sword", "s1.png", epic, "weapon", 75, {"attack":20,"stamina":30,"hitRate":80,"enchantments":[burning],"effects":[]})
sword12 = ObjectType("Dull Flame Sword", "s1.png", epic, "weapon", 75, {"attack":15,"stamina":30,"hitRate":80,"enchantments":[burning],"effects":[]})
sword13 = ObjectType("Sharp Flame Sword", "s1.png", epic, "weapon", 75, {"attack":25,"stamina":30,"hitRate":80,"enchantments":[burning],"effects":[]})
sword14 = ObjectType("Light Flame Sword", "s1.png", epic, "weapon", 75, {"attack":20,"stamina":30,"hitRate":87,"enchantments":[burning],"effects":[]})
sword15 = ObjectType("Heavy Flame Sword", "s1.png", epic, "weapon", 75, {"attack":20,"stamina":30,"hitRate":75,"enchantments":[burning],"effects":[]})
sword21 = ObjectType("Point Destroyer", "s2.png", uncommon, "weapon", 45, {"attack":18,"stamina":15,"hitRate":95,"enchantments":[],"effects":[]})
sword22 = ObjectType("Dull Point Destroyer", "s2.png", uncommon, "weapon", 45, {"attack":15,"stamina":15,"hitRate":95,"enchantments":[],"effects":[]})
sword23 = ObjectType("Sharp Point Destroyer", "s2.png", uncommon, "weapon", 45, {"attack":22,"stamina":15,"hitRate":95,"enchantments":[],"effects":[]})
sword31 = ObjectType("Gold Arm", "s3.png", rare, "weapon", 60, {"attack":50,"stamina":35,"hitRate":85,"enchantments":[],"effects":[]})
sword32 = ObjectType("Dull Gold Arm", "s3.png", rare, "weapon", 60, {"attack":42,"stamina":35,"hitRate":85,"enchantments":[],"effects":[]})
sword33 = ObjectType("Sharp Gold Arm", "s3.png", rare, "weapon", 60, {"attack":55,"stamina":35,"hitRate":85,"enchantments":[],"effects":[]})
sword34 = ObjectType("Light Gold Arm", "s3.png", rare, "weapon", 60, {"attack":50,"stamina":35,"hitRate":90,"enchantments":[],"effects":[]})
sword35 = ObjectType("Heavy Gold Arm", "s3.png", rare, "weapon", 60, {"attack":50,"stamina":35,"hitRate":80,"enchantments":[],"effects":[]})
sword41 = ObjectType("King's Blade", "s4.png", legendary, "weapon", 120, {"attack":60,"stamina":35,"hitRate":75,"enchantments":[bleeding],"effects":[]})
sword42 = ObjectType("Dull King's Blade", "s4.png", legendary, "weapon", 120, {"attack":55,"stamina":35,"hitRate":75,"enchantments":[bleeding],"effects":[]})
sword43 = ObjectType("Sharp King's Blade", "s4.png", legendary, "weapon", 120, {"attack":70,"stamina":35,"hitRate":75,"enchantments":[bleeding],"effects":[]})
sword44 = ObjectType("Light King's Blade", "s4.png", legendary, "weapon", 120, {"attack":60,"stamina":35,"hitRate":70,"enchantments":[bleeding],"effects":[]})
sword45 = ObjectType("Heavy King's Blade", "s4.png", legendary, "weapon", 120, {"attack":60,"stamina":35,"hitRate":82,"enchantments":[bleeding],"effects":[]})
sword51 = ObjectType("King's Staff", "s5.png", legendary, "weapon", 120, {"attack":40,"stamina":35,"hitRate":95,"enchantments":[bleeding],"effects":[]})
sword52 = ObjectType("Dull King's Staff", "s5.png", legendary, "weapon", 120, {"attack":30,"stamina":25,"hitRate":90,"enchantments":[bleeding],"effects":[]})
sword53 = ObjectType("Sharp King's Staff", "s5.png", legendary, "weapon", 120, {"attack":42,"stamina":25,"hitRate":90,"enchantments":[bleeding],"effects":[]})
sword54 = ObjectType("Light King's Staff", "s5.png", legendary, "weapon", 120, {"attack":40,"stamina":25,"hitRate":85,"enchantments":[bleeding],"effects":[]})
sword55 = ObjectType("Heavy King's Staff", "s5.png", legendary, "weapon", 120, {"attack":40,"stamina":25,"hitRate":95,"enchantments":[bleeding],"effects":[]})
extra0 = ObjectType("Gun", "e0.png", rare, "weapon", 60, {"attack":60,"stamina":25,"hitRate":60,"enchantments":[],"effects":[]})
extra1 = ObjectType("Wrecking Ball", "e1.png", rare, "weapon", 90, {"attack":75,"stamina":40,"hitRate":60,"enchantments":[armourNeg],"effects":[]})
extra2 = ObjectType("Grappling Hook", "e2.png", uncommon, "weapon", 40, {"attack":12,"stamina":10,"hitRate":100,"enchantments":[armourNeg],"effects":[]})
extra3 = ObjectType("Mirror", "e3.png", rare, "weapon", 40, {"attack":5,"stamina":30,"hitRate":95,"enchantments":[blinding],"effects":[]})
mythic0 = ObjectType("Fayre's Bow of Healing", "m0.png", mythic, "weapon", 0, {"attack":80,"stamina":30,"hitrate":85,"enchantments":[healCurse],"effects":[]})
mythic1 = ObjectType("Alexander's Sword of Rage", "m1.png", mythic, "weapon", 0, {"attack":100,"stamina":40,"hitrate":90,"enchantments":[rageCurse],"effects":[]})
mythic2 = ObjectType("Gabriel's Feathers of Speed", "m2.png", mythic, "weapon", 0, {"attack":70,"stamina":25,"hitrate":95,"enchantments":[speedCurse],"effects":[]})
mythic3 = ObjectType("Lux's Hammer of Crystals", "m3.png", mythic, "weapon", 0, {"attack":110,"stamina":45,"hitrate":85,"enchantments":[crystalCurse],"effects":[]})
album0 = ObjectType("TV Girl's Album", "al0.png", special, "secret", 200, {"enchantments":[],"effects":[]})
album1 = ObjectType("MGMT's Album", "al1.png", special, "secret", 200, {"enchantments":[],"effects":[]})
album2 = ObjectType("Pink Floyd's Album", "al2.png", special, "secret", 200, {"enchantments":[],"effects":[]})
album3 = ObjectType("The Living Tombstone's Album", "al3.png", special, "secret", 200, {"enchantments":[],"effects":[]})
album4 = ObjectType("The Neighbourhood's Album", "al4.png", special, "secret", 200, {"enchantments":[],"effects":[]})
armour01 = ObjectType("Tin Helmet", "a01.png", uncommon, "armour0", 40, {"protection":5,"enchantments":[],"effects":[]})
armour02 = ObjectType("Tin Chestplate", "a02.png", uncommon, "armour1", 40, {"protection":5,"enchantments":[],"effects":[]})
armour03 = ObjectType("Tin Leggings", "a03.png", uncommon, "armour2", 40, {"protection":5,"enchantments":[],"effects":[]})
armour04 = ObjectType("Tin Boots", "a04.png", uncommon, "armour3", 40, {"protection":5,"enchantments":[],"effects":[]})
armour11 = ObjectType("Iron Helmet", "a11.png", rare, "armour0", 55, {"protection":7,"enchantments":[],"effects":[]})
armour12 = ObjectType("Iron Chestplate", "a12.png", rare, "armour1", 55, {"protection":7,"enchantments":[],"effects":[]})
armour13 = ObjectType("Iron Leggings", "a13.png", rare, "armour2", 55, {"protection":7,"enchantments":[],"effects":[]})
armour14 = ObjectType("Iron Boots", "a14.png", rare, "armour3", 55, {"protection":7,"enchantments":[],"effects":[]})
armour21 = ObjectType("Crystal Helmet", "a21.png", epic, "armour0", 40, {"protection":10,"enchantments":[],"effects":[]})
armour22 = ObjectType("Crystal Chestplate", "a22.png", epic, "armour1", 40, {"protection":10,"enchantments":[],"effects":[]})
armour23 = ObjectType("Crystal Leggings", "a23.png", epic, "armour2", 40, {"protection":10,"enchantments":[],"effects":[]})
armour24 = ObjectType("Crystal Boots", "a24.png", epic, "armour3", 40, {"protection":10,"enchantments":[],"effects":[]})
armour31 = ObjectType("Gold Helmet", "a31.png", epic, "armour0", 55, {"protection":10,"enchantments":[],"effects":[]})
armour32 = ObjectType("Gold Chestplate", "a32.png", epic, "armour1", 55, {"protection":10,"enchantments":[],"effects":[]})
armour33 = ObjectType("Gold Leggings", "a33.png", epic, "armour2", 55, {"protection":10,"enchantments":[],"effects":[]})
armour34 = ObjectType("Gold Boots", "a34.png", epic, "armour3", 55, {"protection":10,"enchantments":[],"effects":[]})
armour41 = ObjectType("King's Helmet", "a41.png", legendary, "armour0", 55, {"protection":17,"enchantments":[],"effects":[]})
armour42 = ObjectType("King's Chestplate", "a42.png", legendary, "armour1", 55, {"protection":17,"enchantments":[],"effects":[]})
armour43 = ObjectType("King's Leggings", "a43.png", legendary, "armour2", 55, {"protection":17,"enchantments":[],"effects":[]})
armour44 = ObjectType("King's Boots", "a44.png", legendary, "armour3", 55, {"protection":17,"enchantments":[],"effects":[]})





class CharacterType:
    def __init__(self, name:str, image:str, data:dict) -> None:
        self.name = name
        self.img = image
        self.data = data
    def __str__(self) -> str:
        return f"CharacterType({self.name}, {self.data})"

class Character:
    def __init__(self, _type:CharacterType, name:str|None=None) -> None:
        self.type = _type
        if name==None: self.name=self.type.name
        else: self.name=name
        self.inv = []
        if "inventory" in self.type.data:
            for i in range(self.type.data["invSize"]):
                if random.random()<self.type.data["invChance"]: self.inv.append(Object(self.type.data["inventory"][i]))
        self.hp = self.type.data["health"]
        self.stamina = 0
        self.armour = [None,None,None,None]
        self.effects = []
        self.skills = {"constitution":100,"dexterity":100,"strength":100}

player = CharacterType("Player", "xx.png", {"health":200,"attack":20,"defense":15,"staminaRate":20})
example = CharacterType("John", "xx.png", {"health":10,"attack":0,"defense":0,"staminaRate":1,"invSize":1,"inventory":[armour34],"invChance":1})
char01 = CharacterType("Small Goblin", "xx.png", {"health":30,"attack":15,"defense":5,"staminaRate":30,"invSize":1,"inventory":[sword02],"invChance":0.5})
char02 = CharacterType("Goblin", "xx.png", {"health":50,"attack":20,"defense":5,"staminaRate":30,"invSize":1,"inventory":[sword03],"invChance":0.5})
char03 = CharacterType("Fast Goblin", "xx.png", {"health":40,"attack":15,"defense":25,"staminaRate":30,"invSize":1,"inventory":[sword21],"invChance":0.4})
char04 = CharacterType("Big Goblin", "xx.png", {"health":60,"attack":25,"defense":0,"staminaRate":30,"invSize":1,"inventory":[sword23],"invChance":0.7})
char11 = CharacterType("King's Dwarfs", "xx.png", {"health":40,"attack":20,"defense":20,"staminaRate":12,"invSize":1,"inventory":[sword52],"invChance":0.6})
char12 = CharacterType("King's Soldiers", "xx.png", {"health":100,"attack":50,"defense":10,"staminaRate":12,"invSize":1,"inventory":[sword53],"invChance":0.9})
boss0 = CharacterType("Fayre (God of Healing)", "b0.png", {"health":500,"attack":0,"defense":40,"staminaRate":50,"invSize":5,"inventory":[mythic0,potion05,potion05,potion04,potion04],"invChance":1})
boss1 = CharacterType("Alexander (God of Rage)", "b1.png", {"health":500,"attack":0,"defense":40,"staminaRate":50,"invSize":5,"inventory":[mythic1,potion15,potion15,potion14,potion14],"invChance":1})
boss2 = CharacterType("Gabriel (God of Speed)", "b2.png", {"health":500,"attack":0,"defense":40,"staminaRate":50,"invSize":5,"inventory":[mythic2,potion25,potion25,potion24,potion24],"invChance":1})
boss3 = CharacterType("Lux (God of Crystal)", "b3.png", {"health":500,"attack":0,"defense":40,"staminaRate":50,"invSize":5,"inventory":[mythic3,potion35,potion35,potion34,potion34],"invChance":1})





class Encounter:
    def __init__(self, team1:list[Character], team2:list[Character]) -> None:
        self.playerTeam = team1
        for char in self.playerTeam:
            char.team = 1
        self.enemyTeam = team2
        for char in self.enemyTeam:
            char.team = 2
        self.people = team1+team2
        random.shuffle(self.people)
        self.playerSelected = 0
        self.time = -1
        self.winner = None
        self.items = []
    def update(self, _input:list[str]) -> str:
        output = []
        validInput = True
        if not _input:
            pass
        elif _input[0]=="use":
            if -3<int(_input[1])<5: self.playerSelected = int(_input[1])
            else: validInput = False
        elif _input[0] in ["wait","skip"]:
            self.playerSelected = -2
        else:
            validInput = False
        if not validInput:
            output += [f"Invalid Input, automatically using slot {self.playerSelected}"]
        if self.time==-1:
            output += ["You get caught in a fight!"]
            output += ["Enter to continue"]
            self.time += 1
        else:
            while True:
                self.time += 1
                for char in self.people:
                    if char.type.name=="Player": slot = self.playerSelected
                    elif char.inv==[]: slot = -1
                    else: slot = random.randint(0,len(char.inv)-1)
                    char.hp += sum([e.level for e in char.effects if e.effect=="health"])
                    maxHp = int(char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100))
                    if char.hp>maxHp: char.hp = maxHp
                    for eff in char.effects[:]:
                        eff.time -= 1
                        if eff.time <= 0:
                            char.effects.remove(eff)
                    if (slot==-1 or char.inv[slot]==None) and slot!=-2:
                        if char.stamina>char.type.data["staminaRate"]*3:
                            for enemy in self.people:
                                
                                if char.team != enemy.team:
                                    if random.random()<(enemy.skills["dexterity"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="dexterity"])/100)*(enemy.type.data["defense"]/100):
                                        output += [f"{char.name} tries to attack but {enemy.name} dodges!"]
                                    else:
                                        damage = char.type.data["attack"]
                                        prot = sum(sum(e.level for e in a.type.data["enchantments"] if e.effect=="protect")+a.type.data["protection"] for a in enemy.armour if a)
                                        if prot>40: prot=40
                                        damage -= int((prot/100)*damage)
                                        damage = int(damage*char.skills["strength"]/100)
                                        output += [f"{char.name} attacks {enemy.name}! (-{damage}HP)"]
                                        enemy.hp -= damage
                                        char.stamina -= char.type.data["staminaRate"]*3
                    elif slot!=-2 and ("stamina" not in char.inv[slot].type.data or char.stamina>char.inv[slot].type.data["stamina"]):
                        if char.inv[slot].type.use=="weapon":
                            for enemy in self.people:
                                if char.team != enemy.team:
                                    try:
                                        if random.random()<char.inv[slot].type.data["hitRate"]/100:
                                            if random.random()<(enemy.skills["dexterity"]/100)*(sum([100]+[e.level for e in enemy.effects if e.effect=="dexterity"])/100)*(enemy.type.data["defense"]/100):
                                                output += [f"{char.name} tries to attack but {enemy.name} dodges!"]
                                            else:
                                                damage = char.inv[slot].type.data["attack"]
                                                prot = sum(sum(e.level for e in a.type.data["enchantments"] if e.effect=="protect")+a.type.data["protection"] for a in enemy.armour if a)
                                                if prot>40: prot=40
                                                if not any([e.effect=="armourNeg" for e in char.inv[slot].type.data["enchantments"]]): damage -= int((prot/100)*damage)
                                                damage = int(damage*char.skills["strength"]/100)
                                                output += [f"{char.name} attacks {enemy.name} with a {char.inv[slot].type.name}! (-{damage}HP)"]
                                                if any([ench.effect=="steal" for ench in char.inv[slot].type.data["enchantments"]]):
                                                    x = [ench for ench in char.inv[slot].type.data["enchantments"] if ench.effect=="steal"]
                                                    output += [f"{char.name} uses {x[0].name} to steal health!"]
                                                    char.hp += int((x[0].level/100)*damage)
                                                enemy.hp -= damage
                                                char.stamina -= char.inv[slot].type.data["stamina"]
                                                for ench in char.inv[slot].type.data["enchantments"]:
                                                    if isinstance(ench.effect, Effect):
                                                        enemy.effects.append(ench.effect)
                                                if "uses" in char.inv[slot].type.data:
                                                    char.inv[slot].uses -= 1
                                    
                                        else:
                                            output += [f"{char.name} tries to attack {enemy.name} but misses!"]
                                    except:
                                        variables.game.quit()
                        elif char.inv[slot].type.use=="instant":
                            output += [f"{char.name} uses {char.inv[slot].type.name}"]
                            if "healing" in char.inv[slot].type.data:
                                char.hp += char.inv[slot].type.data["healing"]
                                maxHp = int(char.type.data["health"]*(char.skills["constitution"]/100)*(sum([100]+[e.level for e in char.effects if e.effect=="constitution"])/100))
                                if char.hp>maxHp: char.hp = maxHp
                            if "stamina" in char.inv[slot].type.data:
                                char.stamina += char.inv[slot].type.data["stamina"]
                            for skill in char.skills:
                                if skill in char.inv[slot].type.data:
                                    char.skills[skill] += char.inv[slot].type.data[skill]
                            char.inv[slot].uses -= 1
                        elif char.inv[slot].type.use=="effect":
                            output += [f"{char.name} uses {char.inv[slot].type.name}"]
                            for eff in char.inv[slot].type.data["effects"]:
                                char.effects.append(eff.copy())
                            char.inv[slot].uses -= 1
                    char.stamina += char.type.data["staminaRate"]
                    for eff in char.effects[:]:
                            if any([e!=eff and e.effect==eff.effect and e.time>=eff.time for e in char.effects]): char.effects.remove(eff)
                    for item in char.inv:
                        if item and "uses" in item.type.data and item.uses<1:
                            char.inv[char.inv.index(item)] = None
                leave = False
                for char in self.people:
                    if char.hp <= 0:
                        output += [f"{char.name} has fallen!"]
                        [self.items.append(item) for item in char.inv]
                        if char.type.name=="Player":
                            output += ["You lost the battle!"]
                            self.winner = 2
                            leave = True
                        self.people.remove(char)
                if sum([1 for c in self.people if c.team==2])==0 and not self.winner:
                    output += ["You have won the battle!"]
                    output += ["Enter to continue"]
                    self.winner = 1
                    leave = True
                p = next(iter([c for c in self.people if c.type.name=="Player"]),None)
                if p and any([p.stamina>item.type.data["stamina"] for item in p.inv if (item!=None and item.type.use=="weapon")]):
                    leave = True
                if leave:
                    if not self.winner:
                        output += ["Your Turn"]
                    break
        return output
    def endUpdate(self) -> tuple[Character|list]:
        for char in self.people:
            if char.type.name=="Player":
                x = char
                self.people.remove(char)
        return x, self.people,self.items





class Room:
    def __init__(self, place:tuple[int], biome:int, _type:int, connections:tuple[int]) -> None:
        self.place = place
        self.biome = biome
        self.type = _type
        self.connections = connections
        self.seen = False
        self.contents = []
        self.characters = []
        self.shopStuff = []
        self.entries = []
    def copy(self):
        return Room(self.place, self.biome, self.type, self.connections)
    def __str__(self) -> str:
        return f"Room({self.place},{self.biome},{self.type},{self.connections})"

class Map:
    def __init__(self, size:int, spawn:tuple[int]) -> None:
        self.size = size
        self.spawn = spawn
        self.rooms = [[None for x in range(size)] for y in range(size)]
    def update(self, loc:tuple[int], info:tuple[int]):
        self.rooms[loc[0]][loc[1]] = Room(loc,info[0],info[1],info[2])
    def print(self) -> str:
        for i in self.rooms:
            for j in i:
                print(j)

def generateMap(x:str) -> Map:
    stuff,seed = x.split()
    size,biomes,types,sx,sy = [int(i) for i in stuff.split(".")]
    output = Map(size,(sx,sy))
    for i in range(size**2):
        n = ord(seed[i])
        if n>126: n-=68
        else: n-=34
        if n>-1:
            con = [int(j) for j in bin(n//(biomes*types))[2:]]
            if len(con)<4: con = tuple([0]*(4-len(con))+con)
            else: con = tuple(con)
            room = updateRoom(Room((i//size,i%size),(n//types%biomes),(n%types),con))
            output.rooms[i//size][i%size] = room
    return output

def updateRoom(room:Room) -> Room:
    if room.type==1:
        characters = [char01,char02,char03]
        room.characters = [Character(i) for i in random.choices(characters, weights=(3,2,1), k=random.randint(2,4))]
    elif room.type==2:
        characters = [char02,char03,char04,char11]
        room.characters = [Character(i) for i in random.choices(characters, weights=(2,3,4,1), k=random.randint(3,6))]
    elif room.type==3:
        characters = [char03,char04,char11,char12]
        room.characters = [Character(i) for i in random.choices(characters, weights=(2,2,4,3), k=random.randint(5,8))]
    elif room.type==4:
        room.entries = [lore[random.randint(0,len(lore)-1)]]
    elif room.type==5:
        objects = [sword01,sword02,sword03,sword04,sword05,sword11,sword12,sword13,sword14,sword15,
                   sword21,sword22,sword23,sword31,sword32,sword33,sword34,sword35,
                   sword41,sword42,sword43,sword44,sword45,sword31,sword32,sword33,sword34,sword35,
                   armour01,armour02,armour03,armour04,armour11,armour12,armour13,armour14,
                   armour21,armour22,armour23,armour24,armour31,armour32,armour33,armour34,
                   armour41,armour42,armour43,armour44,]
        room.shopStuff = [i for i in random.choices(objects, k=random.randint(4,5))]
        room.shopStuff = list(dict.fromkeys(room.shopStuff))
    elif room.type==6:
        objects = [extra0,extra1,extra2,extra3,
                   album0,album1,album2,album3,album4,
                   potion01,potion02,potion03,potion04,potion11,potion12,potion13,potion14,
                   potion21,potion22,potion23,potion24,potion31,potion32,potion33,potion34]
        room.shopStuff = [i for i in random.choices(objects, k=random.randint(4,5))]
        room.shopStuff = list(dict.fromkeys(room.shopStuff))
    elif room.type==7:
        objects = [potion03,potion04,potion05,potion13,potion14,potion15,
                   potion23,potion24,potion25,potion33,potion34,potion35,
                   potion41,potion42,potion43]
        room.shopStuff = [i for i in random.choices(objects, k=random.randint(2,5))]
        room.shopStuff = list(dict.fromkeys(room.shopStuff))
    elif room.type==8:
        characters = [[boss0,char11,char11,char11,char12,char12],
                      [boss1,char11,char11,char11,char12,char12],
                      [boss2,char11,char11,char11,char12,char12],
                      [boss3,char11,char11,char11,char12,char12],]
        room.characters = [Character(i) for i in characters[room.biome]]
    return room

if __name__=="__main__":
    pass