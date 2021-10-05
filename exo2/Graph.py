import numpy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

a=[# 1  2  3  4
    [0, 0, 0, 0], # node 1
    [0, 0, 1, 0], # node 2
    [0, 1, 0, 1], # node 3
    [0, 0, 1, 0], # node 4
]


class Graph:
    def __init__(self, nodes, edges):
        if edges < 0 or nodes <= 0:
            raise 'Wrong number'
        self.nodes = nodes
        self.edges = edges
        self.rng = numpy.random.default_rng()
        self.matrix = self.__generate_matrix()
        self.color_space = []

    def __generate_matrix(self):
        matrix = [[0 for _ in range(0, self.nodes)] for _ in range(0, self.nodes)]
        done = 0
        while done < self.edges:
            x, y = self.rng.integers(0, self.nodes), self.rng.integers(0, self.nodes)
            if x != y and matrix[x][y] == 0: # x != y : no loop
                done += 1
                matrix[x][y] = 1
                matrix[y][x] = 1
        return matrix

    def __manage_color_space(self, new=False, unwanted_color=None):
        if new:
            while True:
                n = self.rng.integers(0, 1000000)
                if n not in self.color_space:
                    self.color_space.append(n)
                    return self.color_space[-1]
        else:
            if unwanted_color:
                for color in self.color_space:
                    if color not in unwanted_color:
                        return color
                return self.__manage_color_space(new=True)
            else:
                if self.color_space:
                    return self.color_space[self.rng.integers(0, len(self.color_space))]
                else:
                    return self.__manage_color_space(new=True)

    def __reset_color_space(self):
        self.color_space = []

    def __get_degree_from_matrix(self):
        vertices_degree = []
        for vertex in self.matrix:
            deg = 0
            for edge in vertex:
                if edge >= 1:
                    deg += 1
            vertices_degree.append(deg)
        return vertices_degree

    def __welsh_powell(self):
        vertices_degree = self.__get_degree_from_matrix()
        print(vertices_degree)
        matrix_color_space = [-1 for _ in range(0, self.nodes)]
        self.__reset_color_space()
        current_degree = max(vertices_degree)
        while current_degree > 0:
            try:
                unwanted_colors = []
                index = vertices_degree.index(current_degree)
                # check if no neighbor has a color:
                for i in range(0, len(self.matrix[index])):
                    if self.matrix[index][i] == 1 and matrix_color_space[i] != -1:
                        unwanted_colors.append(matrix_color_space[i])
                if unwanted_colors:
                    # if found a color, ask a color available, or create a new one
                    matrix_color_space[index] = self.__manage_color_space(unwanted_color=unwanted_colors)
                else:
                    # if not found a color, just ask an existing color or create a new one
                    matrix_color_space[index] = self.__manage_color_space()
                vertices_degree[index] = -1
            except ValueError:
                # in case vertices_degree.index(current_degree) fail
                current_degree -= 1
        # finishing touch with unconnected edges
        for i in range(0, len(matrix_color_space)):
            if matrix_color_space[i] == -1:
                matrix_color_space[i] = self.__manage_color_space()
        print(matrix_color_space)
        print(self.color_space)
        return matrix_color_space

    def get_matrix(self):
        return pd.DataFrame(self.matrix)

    def get_color_matrix(self):
        return self.__welsh_powell(), self.color_space


if __name__ == '__main__':
    a = Graph(edges=130, nodes=60)
    a.get_color_matrix()
    G = nx.from_pandas_adjacency(a.get_matrix())
    G.name = "Graph from pandas adjacency matrix"
    print(nx.info(G))
    options = {
        'node_color': 'black',
        'node_size': 60,
        'width': 3,
        'font_size': 8,
    }
    # subax1 = plt.subplot(221)
    plt.figure(3, figsize=(12, 12))
    nx.draw(G, **options)
    plt.show()

