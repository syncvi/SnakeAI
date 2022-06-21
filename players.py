import math

import numpy as np

from game import *


class RandomPlayer:

    def __init__(self, i):
        self.i = i

    def get_move(self, board, snake):
        r = rand.randint(0, 3)
        return MOVES[r]


class GeneticPlayer:

    def __init__(self, pop_size, num_generations, num_trails, window_size, hidden_size, board_size,
                 mutation_chance=0.1, mutation_size=0.1, iscrossover = False):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.num_trails = num_trails  # num of games that each brain is going to play
        self.window_size = window_size  # how much of the board each brain can see
        self.hidden_size = hidden_size  # size of the brain
        self.board_size = board_size

        self.mutation_chance = mutation_chance
        self.mutation_size = mutation_size
        self.iscrossover = iscrossover

        # DEBUG
        self.display = False

        # brain selected to play games
        self.current_brain = None
        self.pop = [self.generate_brain(self.window_size ** 2, self.hidden_size, len(MOVES)) for _ in range(self.pop_size)]

    # list of matrixes, each matrix is a layer of the neural network
    def generate_brain(self, input_size, hidden_size, output_size):
        # matrix 1 aka layer 1, all layers are randomly initialized for values between 0 and 1
        hidden_layer1 = np.array([[rand.uniform(-1, 1) for _ in range(input_size + 1)] for _ in range(hidden_size)])
        # matrix 2 aka layer 2
        hidden_layer2 = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size + 1)] for _ in range(hidden_size)])
        # matrix 3 aka layer 3
        output_layer = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size + 1)] for _ in range(output_size)])
        return [hidden_layer1, hidden_layer2, output_layer]

    def get_move(self, board, snake):
        input_vector = self.process_board(board, snake[-1][0], snake[-1][1], snake[-2][0], snake[-2][1])
        hidden_layer1 = self.current_brain[0]
        hidden_layer2 = self.current_brain[1]
        output_layer = self.current_brain[2]

        # forward prop, each layer will produce a new input vector and we send it forward thru entire network
        # hidden result is the result of multiplying the input vector with the weights of the hidden layer
        # and we do it row wise, that's why we use [i] indexing
        # np.dot is a function that multiplies the two matrices
        # math.tanh is a function that takes a number and returns a number between -1 and 1, hyperbolic tangent
        # that function helps us to make the network more robust to different inputs and not have values blow up

        hidden_result1 = np.array([math.tanh(np.dot(input_vector, hidden_layer1[i])) for i in range(hidden_layer1.shape[0])] + [1])  # [1] for bias
        hidden_result2 = np.array([math.tanh(np.dot(hidden_result1, hidden_layer2[i])) for i in range(hidden_layer2.shape[0])] + [1])  # [1] for bias
        output_result = np.array([np.dot(hidden_result2, output_layer[i]) for i in range(output_layer.shape[0])])  # [1] for bias

        # we add 1 for bias so the weights are the same

        max_index = np.argmax(output_result)
        return MOVES[max_index]

    def process_board(self, board, x1, y1, x2, y2):
        # x and y are position of the snake
        # input vector is the board around the snake with snake's head in the center
        input_vector = [[0 for _ in range(self.window_size)] for _ in range(self.window_size)]

        # i and j are gonna index the window
        # ii and jj are gonna index the board

        for i in range(self.window_size):
            for j in range(self.window_size):
                # starting point that is half of the window size away from the snake's head in both directions
                ii = x1 + i - self.window_size // 2
                jj = y1 + j - self.window_size // 2
                # if window out of bounds, snake cannot move to that position
                if ii < 0 or jj < 0 or ii >= self.board_size or jj >= self.board_size:
                    input_vector[i][j] = -1 # -1 is a wall
                elif board[ii][jj] == FOOD:
                    input_vector[i][j] = 1 # 1 is food
                elif board[ii][jj] == EMPTY:
                    input_vector[i][j] = 0 # 0 is empty or viable move
                else:  # it is another snake
                    input_vector[i][j] = -1 # -1 is another snake

        if self.display: # DEBUG, display the board that snake sees
            print(np.array(input_vector))
        input_vector = list(np.array(input_vector).flatten()) + [1] # flatten function merges all the elements of the matrix into a single list
        return np.array(input_vector)

    def reproduce(self, top_25):
        new_pop = []
        for brain in top_25:
            new_pop.append(brain) # adding a copy of the top 25 brains to the new population
        for brain in top_25:
            new_brain = self.mutate(brain)
            new_pop.append(new_brain) #adding a mutated copy of the top 25 brains to the new population
        # spawn new random brains for the remaining 50% of the population
        if(self.iscrossover):
            for _ in range(self.pop_size // 4):
                new_pop.append(self.generate_brain(self.window_size ** 2, self.hidden_size, len(MOVES))) # same as init
            #crossover leftover brains
            for _ in range(self.pop_size // 4):
                new_pop.append(self.crossover(top_25[_], top_25[rand.randint(0, len(top_25) - 1)]))
        elif(self.iscrossover == False):
            for _ in range(self.pop_size // 2):
                new_pop.append(self.generate_brain(self.window_size ** 2, self.hidden_size, len(MOVES)))


        return new_pop

    def crossover(self, brain1, brain2):
       # crossing over the brains by taking a random part of each brain and combining them
        new_brain = []
        for i in range(len(brain1)):
            new_brain.append(np.array([[rand.choice([brain1[i][j][k], brain2[i][j][k]]) for k in range(len(brain1[i][j]))] for j in range(len(brain1[i]))]))
        return new_brain

    def mutate(self, brain):
        new_brain = []
        for layer in brain:
            new_layer = np.copy(layer) # for each matrix in the brain, we make a copy of the matrix
            for i in range(new_layer.shape[0]):
                for j in range(new_layer.shape[1]): # we iterate through each element in the matrix
                    if rand.uniform(0, 1) < self.mutation_chance:
                         # with probability mutation_chance, we mutate the element
                         # if we roll a random number between 0 and 1, we mutate the element
                        new_layer[i][j] += rand.uniform(-1, 1) * self.mutation_size
                         # we add a random number between -1 and 1 scaled by (times) mutation_size
            new_brain.append(new_layer)
        return new_brain

    def one_generation(self):
        # one playthrough of the game, each brain plays one game
        scores = [0 for _ in range(self.pop_size)] # housing the scores of each brain
        # DEBUG
        max_score = 0
        for i in range(self.pop_size):
            for j in range(self.num_trails):
                self.current_brain = self.pop[i]
                game = Game(self.board_size, 1, [self])
                outcome = game.play(False, termination=True)
                # outcome is whatever happes when we play the game
                score = len(game.snakes[0])  # for single player variation
                scores[i] += score
                # DEBUG
                # if outcome == 0: # if snake made it the last turn
                    # print("Snake", i, "made it to the last turn")

                if score > max_score:
                    max_score = score
                    print(max_score, "at ID", i)
        # Testing of each brain is complete and they are all ranked
        top_25_indexes = list(np.argsort(scores))[3*(self.pop_size//4):self.pop_size]
        # DEBUG
        print(scores)
        top_25 = [self.pop[i] for i in top_25_indexes][::-1]
        # we reverse the list so the best brains are at the top
        self.pop = self.reproduce(top_25) # update the population

    def evolve_pop(self):
        for i in range(self.num_generations):
            self.one_generation()
            print("gen", i)
            # we going to go over num_generations and will call one_generation function
            # this will go over every single generation and update the population based on how well the brains did

        # DEBUG, display boards for the top brains
        key = input("enter any character to display boards")
        for brain in self.pop:
            self.display = True
            self.current_brain = brain
            game = Game(self.board_size, 1, [self], display=True)
            gui = Gui(game, 800)
            game.play(True, termination=True)
            print("Snake length", len(game.snakes[0]))

# add mating




