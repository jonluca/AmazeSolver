import json

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from termcolor import colored


def add_tuples(a, b):
    return tuple(p + q for p, q in zip(a, b))


def AGL_to_str(agl):
    return str(agl.index)


# this function is used to convert networkx to Cytoscape.js JSON format
# returns string of JSON
def convert2cytoscapeJSON(G):
    # load all nodes into nodes array
    final = {}
    final["nodes"] = []
    final["edges"] = []
    for node in G.nodes():
        nx = {}
        nx["data"] = {}
        nx["data"]["id"] = str(node)
        nx["data"]["label"] = str(node)
        final["nodes"].append(nx.copy())
    # load all edges to edges array
    for edge in G.edges():
        nx = {}
        nx["data"] = {}
        nx["data"]["id"] = str(edge[0]) + str(edge[1])
        nx["data"]["source"] = str(edge[0])
        nx["data"]["target"] = str(edge[1])
        final["edges"].append(nx)
    return json.dumps(final)


class AmazeGameLocation:

    def __init__(self, index):
        self.index = index
        self.dirs = {'U': None, 'D': None, 'L': None, 'R': None, }

    def __str__(self):
        return str(self.index)


class AmazeGame:

    def __init__(self, board_size):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.nodes = np.empty((board_size, board_size), dtype=object)
        self.traversed = np.full((board_size, board_size), False)
        self.paths = nx.DiGraph()
        self.ball = (0, 0)

    def generate_graph(self):
        ind = (12, 0)
        self.ball = ind
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
                    weight = 1
                    while self.is_move_possible(next_attempt):
                        next_move_loc = next_attempt
                        next_attempt = add_tuples(move[1], next_move_loc)
                        weight += 1
                    if not self.nodes[next_move_loc]:
                        self.nodes[next_move_loc] = AmazeGameLocation(next_move_loc)
                        self.paths.add_node(self.nodes[next_move_loc])
                        locs.append(next_move_loc)
                    self.paths.add_edge(self.nodes[next_loc], self.nodes[next_move_loc], weight=weight)
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
                elif j == 2:
                    color = 'blue'
                    letter = 'O'
                elif j == 3:
                    color = 'green'
                    letter = 'Y'
                printed += colored(letter, color)
            printed += '\n'
        print(printed)
        fig_size = plt.rcParams["figure.figsize"]
        fig_size[0] = 12
        fig_size[1] = 9
        plt.rcParams["figure.figsize"] = fig_size
        nx.draw_networkx(self.paths, pos=nx.spectral_layout(self.paths), with_labels=True)
        plt.show()
        cyto = convert2cytoscapeJSON(self.paths)
        with open('cyto.json', 'w') as out:
            out.write(cyto)

    def is_move_possible(self, move):
        return all(0 <= v < self.board_size for v in move) and self.board[move] != 0

    def make_move(self, letter):
        move = (0, 0)
        if letter == 'U':
            move = (-1, 0)
        elif letter == 'D':
            move = (1, 0)
        elif letter == 'L':
            move = (0, -1)
        elif letter == 'R':
            move = (0, 1)

        self.board[self.ball] = 3
        next_move_loc = add_tuples(self.ball, move)
        if self.is_move_possible(next_move_loc):
            self.ball = next_move_loc
            self.board[self.ball] = 3
            next_attempt = add_tuples(move, next_move_loc)
            while self.is_move_possible(next_attempt):
                self.ball = next_attempt
                self.board[self.ball] = 3
                next_attempt = add_tuples(move, next_attempt)
        else:
            print('error')

    def solve(self):
        solution = nx.edge_dfs(self.paths, self.nodes[12][0])
        return list(solution)


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
    amaze.print_board()  # solution = amaze.solve()  # moveNum = 0  # for move in solution:  #     for letter in ('U', 'D', 'L', 'R'):  #         if move[0].dirs[letter] == move[1]:  #             print(f'Move number {moveNum}, move {letter}')  #             moveNum += 1  #             amaze.make_move(letter)  #             amaze.print_board()  #             break


if __name__ == "__main__":
    main()
