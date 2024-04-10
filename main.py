from items.main import Game
import items.characters
import variables
game = Game()
variables.player:items.characters.Character = game.player
#while game.playing:
max_step = 20
print((variables.player.hp/variables.player.max_hp)*max_step)
print((variables.player.skills["constitution"]-100)/100*max_step)
