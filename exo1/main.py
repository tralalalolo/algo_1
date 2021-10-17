import math
import numpy
import sys

rng = numpy.random.default_rng()


def probability(state, new_state, time):
    if time <= 0:
        return 0, 0
    cost_actual_state = cost_function(state)
    cost_new_state = cost_function(new_state)
    if cost_new_state < cost_actual_state:
        return time - 0.01, 1
    return time - 0.01, math.exp(-(cost_new_state - cost_actual_state) / time)


def cost_function(state):
    cost = abs(state[0])
    last_index = 0
    for index in range(1, len(state)):
        cost = cost + abs(state[last_index] - state[index])
        last_index = index
    return cost


def __test__cost_function():
    state = [-8, 1, 2, -1, 50]
    if cost_function(state) != 72:  # somme cumulative
        raise Exception('Bad sum')


def two_opt(state, minimum, maximum):
    """Take [min, max] to inverse"""
    if not minimum < maximum or minimum < 0 or maximum == len(state):
        raise Exception('min < max')
    new_state = state[:minimum]
    for i in range(maximum, minimum - 1, -1):
        new_state.append(state[i])
    new_state.extend(state[maximum + 1:])
    return new_state


def __test__two_opt():
    s = [chr(i) for i in range(65, 91)]
    print(s)
    section = rng.integers(low=0, high=len(s), size=2).tolist()
    print(section)
    ss = two_opt(s, min(section), max(section))
    print(ss)
    if len(s) != len(ss) or len(ss) != len(set(ss)) or len(s) != len(set(s)):
        raise Exception('Replication or omission')

def run(beginning_state, time=1000):
    state = beginning_state
    new_state = None
    while time >= 0:
        section = rng.integers(low=0, high=len(state), size=2).tolist()
        if section[0] == section[1]:
            continue
        new_state = two_opt(state, min(section), max(section))
        time, prob = probability(state, new_state, time)
        if prob == 1:
            state = new_state
        else:
            if prob > rng.random():
                state = new_state
    return new_state, cost_function(new_state)


def parcours(initial_state):
    print('Initial cost of random: ', cost_function(initial_state))
    # print(initial_state)
    new_state, cost = run(initial_state)
    print('Final Cost of annealing: ', cost)
    print(new_state)


if __name__ == '__main__':
    parcours(numpy.random.normal(0, 1000, 1000).tolist())
