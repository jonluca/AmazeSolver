import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from termcolor import colored


def add_tuples(a, b):
    return tuple(p + q for p, q in zip(a, b))


class AmazeGameLocation:

    def __init__(self, index):
        self.index = index
        self.dirs = {'U': None, 'D': None, 'L': None, 'R': None, }

    def __hash__(self):
        return hash(tuple(np.array(self.index)))

    def __str__(self):
        return str(self.index)


class AmazeGame:

    def __init__(self, board_size):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.nodes = np.empty((board_size, board_size), dtype=object)
        self.traversed = np.full((board_size, board_size), False)
        self.paths = nx.DiGraph()

    def generate_graph(self):
        ind = (12, 0)
        locs = [ind]
        while len(locs):
            next_loc = locs.pop()
            if not self.nodes[next_loc]:
                self.nodes[next_loc] = AmazeGameLocation(next_loc)
                self.paths.add_node(self.nodes[next_loc])

            moves = [("U", (-1, 0)), ("D", (1, 0)), ("L", (0, -1)), ("R", (0, 1))]
            for move in moves:
                next_move_loc = add_tuples(move[1], next_loc)
                if self.is_move_possible(next_move_loc):
                    next_attempt = add_tuples(move[1], next_move_loc)
                    while self.is_move_possible(next_attempt):
                        next_move_loc = next_attempt
                        next_attempt = add_tuples(move[1], next_move_loc)
                    if not self.nodes[next_move_loc]:
                        self.nodes[next_move_loc] = AmazeGameLocation(next_move_loc)
                        self.paths.add_node(self.nodes[next_move_loc])
                        locs.append(next_move_loc)
                    self.paths.add_edge(self.nodes[next_loc], self.nodes[next_move_loc])
                    self.nodes[next_loc].dirs[move[0]] = self.nodes[next_move_loc]

    def print_board(self):
        printed = ''
        for i in self.board:
            for j in i:
                letter = 'X'
                color = 'white'
                if j == 1:
                    color = 'red'
                    letter = '.'
                if j == 2:
                    color = 'blue'
                    letter = 'O'
                printed += colored(letter, color)
            printed += '\n'
        print(printed)
        nx.draw_networkx(self.paths, with_labels=True, font_weight='bold')
        plt.show()

    def is_move_possible(self, move):
        return all(0 <= v < self.board_size for v in move) and self.board[move] == 1


def main():
    amaze = AmazeGame(13)
    ### 0 = wall, 1 = path, 2 = ball
    amaze.board = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1], [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                            [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1], [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                            [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                            [2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0]])
    amaze.generate_graph()
    amaze.print_board()


if __name__ == "__main__":
    main()
