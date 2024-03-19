import dungeongraphgen
import roomtypes
import random


class dungeon:
    class room:
        def __init__(self, node:dungeongraphgen.dungeon.room, typ:roomtypes.roomtype.library|roomtypes.roomtype.regular):
            self.node=node
            self.description, self.enimies, self.items=typ.describe(), typ.getenimies(), typ.getitems()
            self.node.truroom=self
        def get_description(self)->str:
            'describes room'
            return self.description
        
        def get_doors(self)->dict[any:str]:
            'return all connecting rooms and their movment form (north east south west and secret)'

            return {i[0].truroom:i[1] for i in self.node.moveops().items()}
        def get_items(self) -> dict[int:any]:
            'will return amount of an item in the room and the item itself'
            return self.items
    class newdungeon():
        def __init__(self, size:tuple[int,int], 
                     dchance:float=0,
                     spa:int=10) -> None:
            '''generates a dungeon, dungeons size, chance of door destruction and amount of secret passages are controllable. 
            any room with no doors will be destroyed and doors with 1 or no rooms will be destroyed'''
            a=dungeongraphgen.dungeon.new_dungeon(size, dchance, spa)
            self.size=size
            self.spa=spa
            self.v=dchance
            
            self.rooms=[dungeon.room(i, [roomtypes.roomtype.library, roomtypes.roomtype.regular][random.randint(0,1)]) for i in a.rooms]
        def __len__(self) -> int:
            'amount of rooms'
            return len(self.rooms)
        def __str__(self) -> str:
            'describe dungeon'
            return f'a {self.size[0]} by {self.size[1]} dungeon. {self.v/1}% chance of variation in doors. {self.spa} secret passages'

 
if __name__=='__main__':
    
    d=dungeon.newdungeon((5,5), 0.25)
    r=d.rooms[0]
    print('you wake up in a room')
    while True:
        print(r.get_description())
        print(f'you check your coords. they are {r.node.coords}')
        x='\n'.join([f'{str(i[0])} {str(i[1])}, ' for i in r.get_items().items()])
        print(f'you see {x}')
        print('\n'.join([f'a room heading {i[1]} to {str(i[0].node.coords)}, ' for i in r.get_doors().items()]))
        a=input('where would you like to move?: ')
        
        op=False
        while not op:
            for i in r.get_doors().items():
                if i[1] in a.lower():
                    r=i[0]
                    op=True
            if not op:
                print('thats not an option')
                a=input('where would you like to move?: ')

            







