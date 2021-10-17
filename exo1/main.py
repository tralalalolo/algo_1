import math
import numpy
import sys

rng = numpy.random.default_rng()

def cost_function(state):
    cost = abs(state[0])
    last_index = 0
    for index in range(1, len(state)):
        cost = cost + abs(state[last_index] - state[index])
        last_index = index
    return cost
        
        
def nearest(state):
    ''' Compute Nearest Neighbor '''
    actual_index = -1
    new_state = []
    actual_state = state
    while actual_state:
        value_to_beat = sys.maxsize
        best_index = None
        for index_to_test in range(len(actual_state)):
            if actual_index == -1 and abs(0 - actual_state[index_to_test]) < value_to_beat: # on part de zero, contrairement à l'algo normal qui part d'un noeud choisis au hasard
                value_to_beat = abs(0 - actual_state[index_to_test])
                best_index = index_to_test
            elif actual_index != -1 and abs(new_state[-1] - actual_state[index_to_test]) < value_to_beat:
                value_to_beat = abs(new_state[-1] - actual_state[index_to_test])
                best_index = index_to_test
        new_state.append(actual_state[best_index])
        actual_state.pop(best_index)
        actual_index = best_index
    return new_state


def parcours(initial_state):
    print('Initial cost of random: ', cost_function(initial_state))
    g = nearest(initial_state)
    print('cost of nearest :', cost_function(g))
    print('Resulting array:', g)


if __name__ == '__main__':
    parcours(numpy.random.normal(0, 1000, 1000).tolist())
