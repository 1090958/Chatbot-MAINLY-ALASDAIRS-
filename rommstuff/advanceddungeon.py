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
def RGB(red=None, green=None, blue=None,bg=False):
    if(bg==False and red!=None and green!=None and blue!=None):
        return f'\u001b[38;2;{red};{green};{blue}m'
    elif(bg==True and red!=None and green!=None and blue!=None):
        return f'\u001b[48;2;{red};{green};{blue}m'
    elif(red==None and green==None and blue==None):
        return '\u001b[0m'
 
if __name__=='__main__':




    
    d=dungeon.newdungeon((5,5), 0.25)
    global r
    r:dungeon.room=d.rooms[0]

    def search(r):
        print('\033[1;4m'+'items:'+'\033[m'+'\n')
        x='\n'.join(     [          f' -\033[34m\033[1m {str(i[0])} {str(i[1])}\033[m'               for i in r.get_items().items()]            )+'\n'+'\033[m'
        print(x)
        print('\033[1;4m'+'doors:'+'\033[m'+'\n')
        l='\n'.join([f' -\033[32;1m{str(i[1])} -> {i[0].node.coords} \033[m' for i in r.get_doors().items()])
        print(l)





    def move(r):
        print('\033[1;4m'+'doors:'+'\033[m'+'\n')
        l='\n'.join([f' -\033[32;1m{str(i[1])} -> {i[0].node.coords} \033[m' for i in r.get_doors().items()])
        print(l)
        a=input('>>>')
        op=False
        while not op:
            for i in r.get_doors().items():
                if i[1] in a.lower():
                    r=i[0]
                    op=True
            if not op:
                print('\033[93invalid option')
                a=input('where?: ')
            print('you walk into a room')
            print(r.description)

    def check_coords(r):
        print(f'your coords - ({r.node.coords})')

    options={'coords':check_coords, 'search':search, 'move':move}

    print('you wake up in a room')
    while True:
        op=False

        a=input('>>>')
        for i in options.items():
                if i[0] in a.lower():
                    print('\n')
                    i[1](r)
                    op=True
        if not op:
            print('\n')
            print('not an option')
        


        
            







