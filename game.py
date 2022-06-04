import numpy as np
import tkinter as tk
import time as time
import random as rand


#Global
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

MOVES = [UP, DOWN, LEFT, RIGHT]


EMPTY = 0
FOOD = 99


class Game:

    def __init__(self, size, num_snakes, players, gui=None, display=false, max_turns=100):
        self.size = size
        self.num_snakes
        self.players = players
        self.gui = gui
        self.display = display
        self.max_turns = max_turns

        self.num_food = 4
        self.turn = 0
        self.snake_size = 3

        self.snakes = [[((j + 1)*self.size//(2*self.num_snakes), self.size//2 + i) for i in range(self.snake_size)]
                       for j in range(self.num_snakes)]
        self.food = [(self.size//4, self.size//4), (3*self.size//4, self.size//4), (self.size//4, 3*self.size//4), (3*self.size//4, 3*self.size//4)]
        self.player_ids = [i for i in range(self.num_snakes)]

        self.board = np.zeros([self.size, self.size])
        for i in self.player_ids:
            for tup in self.snakes[i]:
                self.board[tup[0]][tup[1]] = i + 1
        for tup in self.food:
            self.board[tup[0]][tup[1]] = FOOD

        self.food_index = 0
        self.food_xy = [(1, 0), (3, 2), (9, 8), (0, 0), (4, 9), (6, 0), (9, 7), (9, 9), (8, 9), (6, 9), (7, 3), (7, 1), (6, 2), (5, 7), (5, 8), (0, 8), (0, 0), (8, 9), (8, 2), (2, 3), (6, 5), (8, 4), (5, 8), (4, 2), (2, 3), (5, 0), (3, 9), (0, 0), (5, 2), (9, 4), (5, 5), (0, 2), (9, 9), (0, 8), (0, 3), (4, 8), (7, 5), (5, 9), (8, 6), (7, 3), (1, 1), (2, 5), (4, 2), (5, 9), (6, 8), (6, 8), (5, 0), (6, 9), (8, 2), (9, 5), (4, 9), (2, 5), (0, 2), (7, 1), (7, 3), (7, 7), (9, 1), (4, 4), (0, 4), (4, 7), (3, 9), (7, 6), (7, 7), (4, 6), (8, 3), (2, 7), (9, 6), (8, 2), (8, 7), (3, 3), (6, 3), (6, 2), (3, 3), (1, 6), (8, 5), (0, 0), (8, 2), (9, 9), (2, 9), (9, 2), (0, 2), (0, 2), (0, 3), (2, 0), (1, 9), (0, 7), (5, 0), (0, 7), (4, 4), (0, 3), (2, 5), (1, 8), (1, 3), (0, 5), (1, 0), (6, 9), (3, 8), (8, 9), (4, 7), (5, 0), (1, 7), (1, 6), (7, 4), (3, 9), (8, 9), (6, 2), (2, 4), (0, 7), (7, 7), (4, 6), (9, 3), (2, 8), (8, 8), (3, 6), (4, 3), (6, 4), (5, 7), (4, 3), (3, 6), (4, 9), (2, 3), (0, 4), (8, 4), (3, 4), (2, 3), (1, 6), (8, 5), (1, 0), (1, 9), (1, 7), (0, 3), (7, 8), (8, 3), (4, 7), (8, 9), (8, 4), (0, 7), (2, 7), (9, 4), (5, 8), (8, 4), (3, 1), (9, 4), (5, 6), (5, 1), (4, 0), (0, 0), (8, 3), (8, 3), (2, 2), (8, 3), (7, 5), (5, 0), (2, 0), (5, 7), (2, 1), (0, 0), (4, 0), (6, 4), (7, 4), (7, 4), (9, 2), (1, 1), (5, 0), (6, 1), (2, 3), (5, 2), (9, 0), (9, 1), (7, 3), (3, 5), (7, 2), (2, 6), (5, 0), (0, 9), (4, 0), (5, 4), (9, 8), (6, 2), (2, 0), (8, 6), (9, 9), (8, 3), (3, 5), (7, 7), (8, 1), (5, 7), (4, 1), (9, 4), (4, 5), (4, 6), (1, 1), (8, 9), (7, 0), (5, 2), (5, 5), (9, 9), (0, 1), (9, 2), (9, 9)]

    def move(self):
        moves = []
        # moves the head up
        for i in self.player_ids:
            snake_i = self.snakes[i]
            move_i = self.players[i].get_move(self.board, snake_i)
            moves.append(move_i)
            new_square = (snake_i[-1][0] + move_i[0], snake_i[-1][1] + move_i[1])
            snake_i.append(new_square)

        # tail updateing
        for i in self.player_ids:
            head_i = self.snakes[i][-1]
            if head_i not in self.food:
                self.board[self.snakes]