import random

class Room:
    def __init__(self, place:tuple[int], _type:tuple[int]) -> None:
        self.place = place
        self.type = _type
        self.contents = []
        if self.type==6:
            self.shop = []
    def __str__(self) -> str:
        return f"Room({self.place},{self.type})"

def generateRooms():
    rooms = []
    for a in range(50):
        x = []
        for b in range(50):
            biome = random.randint(0,3)
            _type = random.randint(0,6)
            r = Room((a,b),(biome,_type))
            x.append(r)
        rooms.append(x)
    return rooms