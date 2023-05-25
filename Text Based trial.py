
class biome():
    def __init__(self, key, name):
        self.key = key
        self.name = name
class field(biome):
    def __init__(self):
        super.__init__('F','Field') # type: ignore
    



grid ={
    0:[field(),field(),field(),field(),field()],
    1:[field(),field(),field(),field(),field()],
    2:[field(),field(),field(),field(),field()],
    3:[field(),field(),field(),field(),field()],
    4:[field(),field(),field(),field(),field()],
    5:[field(),field(),field(),field(),field()]
}
x=0
y=0
for i in range(5):
    l=grid[i]
    for biome in l:

        print(biome.key, end=' ')