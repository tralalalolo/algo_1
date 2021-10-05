import math
import numpy

rng = numpy.random.default_rng()


def probability(state, new_state, time):
    if time <= 0:
        return time, 0
    cost_actual_state = cost_function(state)
    cost_new_state = cost_function(new_state)
    if cost_new_state < cost_actual_state:
        return time - 0.1, 1
    return time - 0.1, math.exp(-(cost_new_state - cost_actual_state) / time)


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
        raise


def two_opt(state, minimum, maximum):
    """Take [min, max] to inverse"""
    if not minimum < maximum or minimum == 0 or maximum == len(state):
        raise Exception('min < max')
    new_state = state[:minimum]
    for i in range(maximum, minimum - 1, -1):
        new_state.append(state[i])
    new_state.extend(state[maximum + 1:])
    return new_state


def __test__two_opt():
    s = [chr(i) for i in range(65, 91)]
    print(s)
    section = rng.integers(low=1, high=len(s) - 2, size=2).tolist()
    print(section)
    ss = two_opt(s, min(section), max(section))
    print(ss)
    if len(s) != len(ss) or len(ss) != len(set(ss)) or len(s) != len(set(s)):
        raise


def run(beginning_state):
    print('Initial cost : ', cost_function(beginning_state))
    print(beginning_state)
    time = 100
    state = beginning_state
    new_state = None
    while time >= 0:
        section = rng.integers(low=1, high=len(state) - 2, size=2).tolist()
        if section[0] == section[1]:
            continue
        new_state = two_opt(state, min(section), max(section))
        time, prob = probability(state, new_state, time)
        if prob == 1:
            state = new_state
        else:
            if prob > rng.random():
                state = new_state
    print('Final Cost : ', cost_function(new_state))
    print(new_state)


def parcours(list):
    run(list)


if __name__ == '__main__':
    run(numpy.random.normal(0, 1000, 1000).tolist())
