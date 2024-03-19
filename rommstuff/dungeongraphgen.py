import random
class d2:
    def __init__(self,x:int,y:int):
        self.x=x
        self.y=y
        self.xy=(x,y)
    def __str__(self)->str:
        return f'{self.x}, {self.y}'

class dungeon:

    class room:
        def __init__(self, location:tuple) -> None:
            self.doors=[]
            self.sp=[]
            self.connectrooms=[]
            self.secretconnectrooms=[]
            self.truroom=''
            self.coords=d2(location[0], location[1])

        def moveops(self)->dict:
            '''returns all movment options from self.to other rooms.'''
            t=lambda x: ['north','south'] if self.coords.y!=x.coords.y else ['east','west']
            m=lambda x: t(x)[0] if  x.coords.y>self.coords.y or x.coords.x>self.coords.x else t(x)[1]

            i={i:m(i) for i in self.connectrooms}
            [i.update({j:f'passageway {self.secretconnectrooms.index(j)+1}'}) for j in self.secretconnectrooms]

            return i
            
        def __str__(self) -> str:
            return f'room({self.coords.x, self.coords.y})'
        
    class door:
        def __init__(self, r1, r2, 
                     tpe:str='door') -> None:
            self.r1,self.r2=r1,r2
            if type(self.r1)!= dungeon.room:
                raise TypeError(f'{str(self.r1)} is {type(self.r1)}, {str(self.r1)} must be a room')
            if type(self.r2)!=dungeon.room:
                raise TypeError(f'{str(self.r2)} is {type(self.r2)}, {str(self.r2)} must be a room')

            self.r1.doors.append(self)
                
            self.r2.doors.append(self)
            self.type=tpe
            if tpe=='door':
                self.r1.connectrooms.append(self.r2)
                self.r2.connectrooms.append(self.r1)

            else:
                self.r1.secretconnectrooms.append(self.r2)
                self.r2.secretconnectrooms.append(self.r1)
                

            

        def delete(self) -> None:
            self.r1.connectrooms.remove(self.r2)
            self.r2.connectrooms.remove(self.r1)
            self.r1.doors.remove(self)
            self.r2.doors.remove(self)
            

        def __str__(self) -> str:
            return f'(door({self.r1}, {self.r2}))' if self.type=='door' else f'(door({self.r1}, {self.r2}) but secret)'

    class new_dungeon:    
        def __init__(self, size:tuple,
                     rds:float=0.0,
                     spa:int=10) -> None:

            self.size=d2(size[0], size[1])
            self.rooms=[ dungeon.room((x, y)) for x in range(self.size.x) for y in range(self.size.y)]
            self.doors=[]
            
            for i in self.rooms:
                if random.random() < rds:
                    self.rooms.pop(self.rooms.index(i))



            for i in self.rooms:
                    for j in self.rooms:
                            if (i.coords.x==j.coords.x and i.coords.y==j.coords.y+1) or (i.coords.y==j.coords.y and i.coords.x==j.coords.x+1):  
                                self.doors.append(dungeon.door(i,j))
            
            for i in self.doors:
                if random.random() < rds:
                    i.delete()
                    self.doors.pop(self.doors.index(i))
            for i in self.rooms:
                if len(i.doors)==0:
                    self.rooms.pop(self.rooms.index(i))


            for i in range(spa):
                    self.doors.append(dungeon.door(self.rooms[random.randint(0,len(self.rooms)-1)],self.rooms[random.randint(0,len(self.rooms)-1)], 'secret'))





if __name__=='__main__':
    a=dungeon.new_dungeon((10,10, 0.25))
    print('dpajsgklandgk;')
    [print(str(i)) for i in a.doors]



    rm=a.rooms[1]
    while True:
        print('you enter a dimlit room')
        print(f'your coordinates are ({rm.coords})')

        print('you see ')
        [print(f'a door heading {i[1]} to ({str(i[0].coords)})') if i[1]!='secret' else print('omg there is a secret passage 0:') for i in rm.moveops().items()]


        a=input('move?')

        unexpectedinput=True

        for i in rm.moveops().items():
            if a==i[1]:
                rm=i[0]
                unexpectedinput=False
        
        if unexpectedinput: 
            print('that is not an option')
        else:
            print(f'u walk in a {a} like way')




