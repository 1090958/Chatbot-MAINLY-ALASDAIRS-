import pygame as py
import movment as m

a=m.dungeon.new_dungeon((15,15),0.25)

class drawable:
    class door:
        def __init__(self, door:m.dungeon.door) -> None:
            self.door=door
        def draw(self, app) -> None:

            py.draw.line(app.screen, (255,0,0), (self.door.r1.coords.x*20+5, self.door.r1.coords.y*20+5), (self.door.r2.coords.x*20+5, self.door.r2.coords.y*20+5), 2)

    class room:
        def __init__(self, room:m.dungeon.room) -> None:
            self.room=room
            self.rect=py.rect.Rect(self.room.coords.x*20, self.room.coords.y*20, 10, 10)
        def draw(self, app) -> None:

            py.draw.rect(app.screen, (0, 0, 0), self.rect)
        

class app:
    def __init__(self, dungeon:m.dungeon.new_dungeon)->None:
        self.screen=py.display.set_mode((500,500))
        self.dungeon=dungeon
        self.rooms=[drawable.room(i)for i in dungeon.rooms]
        self.doors=[drawable.door(i) for i in dungeon.doors]



    def run(self) -> None:
        running=True
        while running:
            for event in py.event.get():  
                if event.type == py.QUIT:  
                    running = False 
            self.screen.fill('white') 
            [i.draw(self) for i in self.doors]
            [i.draw(self) for i in self.rooms]



            py.display.flip()

            


            
            



a=app(a)
a.run()
