from players import *
from game import *

size = 10
num_snakes = 1
players = [RandomPlayer(0)]

game = Game(size, num_snakes, players, gui=None, display=True, max_turns=100)
game.play(True, termination=False)

