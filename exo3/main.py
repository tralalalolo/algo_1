import numpy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, nodes, edges):
        if edges < 0 or nodes <= 0:
            raise 'Wrong number'
        self.nodes = nodes
        self.edges = edges
        self.rng = numpy.random.default_rng()
        self.matrix = self.__generate_matrix()
        self.line_matrix = self.__line_graph__from_matrix()

    def __generate_matrix(self):
        matrix = [[0 for _ in range(0, self.nodes)] for _ in range(0, self.nodes)]
        done = 0
        while done < self.edges:
            x, y = self.rng.integers(0, self.nodes), self.rng.integers(0, self.nodes)
            if x != y and matrix[x][y] == 0:  # x != y : no loop
                done += 1
                matrix[x][y] = 1
                matrix[y][x] = 1
        return matrix

    def __check_if_exist(self, line_graph_label, e, other_e):
        try:
            return line_graph_label.index((e, other_e))
        except ValueError:
            pass
        try:
            return line_graph_label.index((other_e, e))
        except ValueError:
            pass
        return None

    def __line_graph__from_matrix(self):
        for lines in self.matrix:
            print(lines)
        graph_line_matrix = [[0 for _ in range(self.edges)] for _ in range(self.edges)]
        graph_label_matrix = []
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] == 1 and (y, x) not in graph_label_matrix and (x, y) not in graph_label_matrix:
                    graph_label_matrix.append((y, x))
        i = 0
        print(graph_label_matrix)
        for (e1, e2) in graph_label_matrix:
            for j in self.matrix[e1]:
                if j != e2 and self.matrix[e1][j] == 1:  # j != e2 sinon boucle !
                    # regarde position e1 jndex dans label
                    position = self.__check_if_exist(graph_label_matrix, e1, j)
                    if not position:
                        continue
                    # attache index actuelle + position
                    graph_line_matrix[i][position] = 1
                    graph_line_matrix[position][i] = 1
            for j in self.matrix[e2]:
                if j != e1 and self.matrix[e2][j] == 1:  # j != e1 sinon boucle !
                    # regarde position e1 jndex dans label
                    position = self.__check_if_exist(graph_label_matrix, e2, j)
                    if not position:
                        continue
                    # attache index actuelle + position
                    graph_line_matrix[i][position] = 1
                    graph_line_matrix[position][i] = 1
            i += 1
        print(graph_line_matrix)
        return graph_line_matrix

    def get_matrix(self):
        return pd.DataFrame(self.matrix)

    def get_matrix_parameters(self):
        return self.nodes, self.edges

    def get_line_matrix(self):
        return pd.DataFrame(self.line_matrix)


def display_matrix(g: Graph):
    G = nx.from_pandas_adjacency(g.get_matrix())
    nodes, edges = g.get_matrix_parameters()
    G.name = "Graph from pandas adjacency matrix"
    options = {
        'node_color': 'black',
        'node_size': nodes,
        'width': 3,
        'font_size': 8,
    }
    plt.figure(f"Graph with {nodes} nodes and {edges} edges", figsize=(12, 12))
    nx.draw(G, **options)


def display_line_graph(g: Graph):
    G = nx.from_pandas_adjacency(g.get_line_matrix())
    nodes, edges = g.get_matrix_parameters()
    G.name = "Graph from pandas adjacency line matrix"
    options = {
        'node_color': 'black',
        'node_size': edges,
        'width': 3,
        'font_size': 8,
    }
    plt.figure(f"Line Graph with {edges} nodes", figsize=(12, 12))
    nx.draw(G, **options)


if __name__ == '__main__':
    g = Graph(edges=30, nodes=10)
    display_matrix(g)
    display_line_graph(g)
    plt.show()