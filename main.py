from items.main import Game
import variables
game = Game()
variables.player = game.player
#while game.playing:
print(dir(game.player))
    