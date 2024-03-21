import pygame as py
import advanceddungeon as m
import jsonpickle, json
import sys
class drawable:
    class door:
        def __init__(self, door:m.dungeongraphgen.dungeon.door) -> None:
            self.door=door
        def draw(self, app) -> None:

            if self.door.type=='door':
                py.draw.line(app.screen, (255,0,0), (self.door.r1.coords.x*app.scrollmeter+app.scrollmeter/4+app.x, self.door.r1.coords.y*app.scrollmeter+app.scrollmeter/4+app.y), (self.door.r2.coords.x*app.scrollmeter+app.scrollmeter/4+app.x, self.door.r2.coords.y*app.scrollmeter+app.scrollmeter/4+app.y), 2)
            else:
                py.draw.line(app.screen, (0,0,255), (self.door.r1.coords.x*app.scrollmeter+7+app.x, self.door.r1.coords.y*app.scrollmeter+7+app.y), (self.door.r2.coords.x*app.scrollmeter+7+app.x, self.door.r2.coords.y*app.scrollmeter+7+app.y), 2)

    class room:
        def __init__(self, room:m.dungeon.room) -> None:
            self.room=room.node
            self.c= room.rt.guic
        def draw(self, app) -> None:

            if py.draw.rect(app.screen, self.c, py.rect.Rect(self.room.coords.x*app.scrollmeter+app.x, self.room.coords.y*app.scrollmeter+app.y, app.scrollmeter/2, app.scrollmeter/2)).collidepoint(py.mouse.get_pos()):
                print(self.room.truroom.rt)
                py.draw.rect(app.screen, 'black', py.rect.Rect(self.room.coords.x*app.scrollmeter+app.x, self.room.coords.y*app.scrollmeter+app.y, app.scrollmeter/2, app.scrollmeter/2), 3)


        

class app:
    def __init__(self, dungeon:m.dungeon.newdungeon)->None:
        self.screen=py.display.set_mode((500,500))
        self.dungeon=dungeon
        self.rooms=[drawable.room(i)for i in dungeon.rooms]
        self.doors=[drawable.door(i) for i in dungeon.graph.doors]
        self.scrollmeter=1000/50
        self.d=50
        self.x,self.y=0,0




    def run(self) -> None:
        running=True
        while running:
            for event in py.event.get():  
                if event.type == py.QUIT:  
                    running = False 
                
            self.screen.fill('white') 
            keys=py.key.get_pressed()

            if keys[py.K_o]:    self.d+=0.1
            if keys[py.K_i]:    self.d-=0.1
            if keys[py.K_w]:    self.y+=1
            if keys[py.K_a]:    self.x+=1
            if keys[py.K_d]:    self.x-=1
            if keys[py.K_s]:    self.y-=1
            self.scrollmeter=1000/self.d

            [i.draw(self) for i in self.doors]
            [i.draw(self) for i in self.rooms]



            py.display.flip()

def save_object(obj, filename):
    sys.setrecursionlimit(30000)
    fr=jsonpickle.encode(obj)
    with open(filename, 'w') as outp:
        json.dump(fr, outp)
    outp.close()


a=m.dungeon.newdungeon((30,30), 0.25, 10)
t=app(a)
t.run()