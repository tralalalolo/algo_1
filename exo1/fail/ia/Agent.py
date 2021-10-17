import math
import random
from numpy import random as rnd


class Agent:
    def __init__(self, genetics, mutation_level=0, index_genetics=None):
        self.chromosomes = genetics
        self.fit_value = -1
        self.mutationLevel = mutation_level
        self.modifiedSinceLastFitnessTest = True
        self.indexGenetics = index_genetics if index_genetics else random.sample([i for i in range(0, len(genetics))], len(genetics))

    def crossover(self, other, method='CX2') -> ([], []):
        """
            Produce two beautiful logical correct offspring. Mummy and daddy have to be proud ! Even if some might
            be like the pharaohs of the old, a little special.
        """
        if not self.genetics or not self.indexGenetics:
            return self, self
        offspring_1, offspring_2 = [], []
        number_barrier = math.floor(math.sqrt(len(self.genetics()))) >> 1
        position_barrier = []
        for index in range(0, number_barrier):
            position_barrier.append(random.randint(0, len(self.genetics())))

        # Default method
        if method == 'CX2':
            while len(offspring_1) < len(self.indexGenetics):
                new_starting_position_for_parent_1_to_terminate = None
                # step 2
                if not offspring_1:
                    bit_1 = other.get_indexes()[0]
                    offspring_1.append(bit_1)
                else:
                    # step 6
                    # when breaking due to cycle start a new cycle again at the last position possible
                    # we look for next index available in parent 1 never used
                    new_starting_position = 0
                    all_index_already_used = []
                    for index in offspring_1:
                        all_index_already_used.append(other.get_indexes().index(index))
                    all_index_already_used.sort()
                    for i, j in enumerate(all_index_already_used, all_index_already_used[0]):
                        if i != j:
                            new_starting_position = i
                            break
                    if not new_starting_position:
                        new_starting_position = all_index_already_used[-1] + 1
                    bit_1 = other.get_indexes()[new_starting_position]
                    offspring_1.append(bit_1)
                    # Now that we know how to start again for parent 2, we need to find the first bit that will
                    # fill the condition to break in the main loop when comparing with parent 1
                    all_index_already_used = []
                    for index in offspring_2:
                        all_index_already_used.append(self.get_indexes().index(index))
                    all_index_already_used.sort()
                    for i, j in enumerate(all_index_already_used, all_index_already_used[0]):
                        if i != j:
                            new_starting_position_for_parent_1_to_terminate = i
                            break
                    if not new_starting_position_for_parent_1_to_terminate:
                        new_starting_position_for_parent_1_to_terminate = all_index_already_used[-1] + 1
                while True:
                    if len(offspring_1) > len(self.indexGenetics):
                        raise 'error'
                    # step 3
                    position_index_in_parent_1 = self.indexGenetics.index(bit_1)
                    position_index_in_parent_2 = self.indexGenetics.index(other.get_indexes()[position_index_in_parent_1])
                    bit_2 = other.get_indexes()[position_index_in_parent_2]
                    offspring_2.append(bit_2)
                    # When we go back to the first bit of the first parent, we stop
                    if self.indexGenetics.index(bit_2) == 0 or \
                        new_starting_position_for_parent_1_to_terminate and self.indexGenetics.index(bit_2) == new_starting_position_for_parent_1_to_terminate:
                        break
                    # step 4
                    position_index2_in_parent_1 = self.indexGenetics.index(bit_2)
                    bit_3 = other.get_indexes()[position_index2_in_parent_1]
                    offspring_1.append(bit_3)
                    # to start again
                    bit_1 = bit_3
            if len(offspring_1) != len(set(offspring_1)) or len(offspring_2) != len(set(offspring_2)):
                raise 'BAD'
            return Agent(genetics=self.genetics(), index_genetics=offspring_1), Agent(genetics=self.genetics(), index_genetics=offspring_2)

    def __crossover_ord(self, other):
        # TODO TEST
        a, b = int(rnd.random() * len(self.chromosomes)), int(rnd.random() * len(self.chromosomes))
        boy, girl = [], []
        for i in range(min(a, b), max(a, b)):
            boy.append(other.get_index()[i])
            girl.append(self.get_indexes()[i])

        boy += [item for item in self.indexGenetics if item not in boy]
        girl += [item for item in other.get_index() if item not in girl]
        return Agent(genetics=self.genetics(), index_genetics=boy), Agent(genetics=self.genetics(), index_genetics=girl)

    def __crossover_pmx(self, other):
        #TODO TEST
        a, b = int(rnd.random() * len(self.get_indexes())), int(rnd.random() * len(self.get_indexes()))
        boy, girl = [-1 for i in range(0, len(self.indexGenetics))], [-1 for i in range(0, len(self.indexGenetics))]
        for i in range(min(a, b), max(a, b)):
            boy[i] = other.get_indexes()[i]
            girl = self.get_indexes()[i]
        bboy = list(dict.fromkeys([self.get_indexes()[index] if self.get_indexes()[index] not in boy else -1 for index in range(0, len(self.get_indexes()))]))
        ggirl = list(dict.fromkeys([other.get_indexes()[index] if other.get_indexes()[index] not in boy else -1 for index in range(0, len(other.get_indexes()))]))
        bboy.remove(-1)
        ggirl.remove(-1)
        while -1 in boy:
            boy[boy.index(-1)] = bboy[0]
            bboy.remove(bboy[0])
        while -1 in girl:
            girl[boy.index(-1)] = ggirl[0]
            ggirl.remove(bboy[0])
        return Agent(genetics=self.chromosomes, index_genetics=boy), Agent(genetics=self.chromosomes, index_genetics=girl)

    def __crossover_cx(self, other):
        # TODO TEST
        pass

    def mutate(self, mutation_rate):
        for swapped in range(0, len(self.chromosomes)):
            if random.random() < mutation_rate:
                swap_with = random.randint(0, len(self.chromosomes) - 1)
                x = self.chromosomes[swapped]
                self.chromosomes[swapped] = self.chromosomes[swap_with]
                self.chromosomes[swap_with] = x
        self.modifiedSinceLastFitnessTest = True

    def probability(self, number):
        return self.fitness() / number

    def fitness(self):
        """
        Produce or estimate (if not already calculated, and not modified) the score of the individual
        :return: A number representing the score of this individual. The lower, the better.
        """
        if not self.modifiedSinceLastFitnessTest:
            if self.fit_value <= 0:
                raise 'WHAT'
            return 1 / self.fit_value
        self.fit_value = 0
        last_index = -1
        for index in self.indexGenetics:
            if last_index == -1:
                self.fit_value = abs(self.genetics()[index])
                last_index = index
            else:
                self.fit_value = self.fit_value + abs(self.genetics()[last_index] - self.genetics()[index])
                last_index = index
        # for index in self.chromosomes:
        #     self.fit_value += self.fit_value + abs(last_index - index)
        self.modifiedSinceLastFitnessTest = False
        return 1 / self.fit_value

    def get_int_fitness(self):
        self.fitness()
        return self.fit_value

    def get_indexes(self):
        return self.indexGenetics

    def genetics(self):
        return self.chromosomes

    def __add__(self, other):
        return self.crossover(other)

    def __gt__(self, other):
        return self.fitness() > other.fitness()

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def __ge__(self, other):
        return self.fitness() >= other.fitness()

    def __le__(self, other):
        return self.fitness() <= other.fitness()


if __name__ == '__main__':
    # a = Agent(genetics=[], index_genetics=[3, 4, 8, 2, 7, 1, 6, 5])
    # b = Agent(genetics=[], index_genetics=[4, 2, 5, 1, 6, 8, 3, 7])
    # a = Agent(genetics=[], index_genetics=[1, 2, 3, 4, 5, 6, 7, 8])
    # b = Agent(genetics=[], index_genetics=[2, 7, 5, 8, 4, 1, 6, 3])
    a = Agent(genetics=[random.randint(0, 4) for _ in range(0, 5)], index_genetics=[4, 1, 3, 2])
    b = Agent(genetics=[], index_genetics=[2, 4, 3, 1])
    boy, girl = a + b
    print(boy)
    print(girl)
    boy = Agent(genetics=[3, 2, 0, 1, 3], index_genetics=[2, 4, 3, 1])
    print('indexes : ', boy.get_indexes())
    print('genetics : ', boy.genetics())
    print(boy.fitness())
