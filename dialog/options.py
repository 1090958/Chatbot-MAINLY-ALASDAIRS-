
import random,items.objects
def get_Descriptor(word:str):
    if word[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        return "an"
    return "a"
def enter_Room(Biome, Type, Contents:list[items.objects.Object]):
    options1 = [
        f"You are in what appears to be a {Biome.lower()}, it is a {Type.lower()}",
        f"You are in a {Type.lower()}, {Biome.lower()}"
               ]
    if len(Contents) >1:
        options2 = [
            f" Inside the room there is {', '.join([get_Descriptor(str(_)) + ' ' + str(_) for _ in Contents[:-1]])} and {get_Descriptor(Contents[-1]) + ' ' + Contents[-1]}"
        ]
    elif len(Contents) == 1:
        options2 = [
            F"There is {get_Descriptor(str(Contents[0])) + ' ' + str(Contents[0])}"
        ]
    else:
        options2 = 'There is nothing on the floor'
    return random.choice(options1) + random.choice(options2)