from players import *
from game import *

window_size = 7
hidden_size = 15
board_size = 15

pop_size = 100
num_generations = 1
num_trails = 1

mutation_chance = 0.1
mutation_size = 0.1
iscrossover = True


gen_player = GeneticPlayer(pop_size, num_generations, num_trails, window_size, hidden_size, board_size,
                           mutation_chance, mutation_size, iscrossover)
gen_player.evolve_pop()
