import operator

from Agent import Agent
import numpy as np
import math
import pandas as pd


class Population:
    def __init__(self, genetic_template: [type(float)], demographic=1000, generation=30, crossover_method='Proportion',
                 fitness_method='CX2', crossover_probability=0.8, mutation_rate=0.1):
        if not genetic_template:
            raise 'genetic_template must be something'
        if demographic < 3:
            raise 'The population must be superior to 3'
        if generation <= 1:
            raise 'Generation number must be superior to 1'
        if crossover_probability <= 0 or crossover_probability > 1:
            raise 'crossover_probability must be between 0 and 1'
        self.demographic_number = demographic if demographic % 2 == 0 else demographic + 1
        self.population: [type(Agent)] = [Agent(genetics=genetic_template) for _ in range(0, self.demographic_number)]
        self.genetic_template: [type(float)] = genetic_template
        self.best_fit: type(Agent) = Agent(genetics=self.genetic_template, index_genetics=[i for i in range(0, len(self.genetic_template))])
        self.generation = []
        self.generation_number = generation
        print('The default fitness is : ', self.best_fit.fitness())
        print('The default int fitness is : ', self.best_fit.get_int_fitness(), '\n')
        self.crossover_method = crossover_method
        self.fitness_method = fitness_method
        self.crossover_probability = crossover_probability
        self.fitness_max = 0
        self.rng = np.random.default_rng()
        self.mutation_rate = mutation_rate

    def get_population(self):
        return self.population

    def mutate_population(self):
        for agent in self.population:
            agent.mutate(self.mutation_rate)
            agent.fitness()

    def best_of_actual_generation(self):
        g = sorted(self.population, key=lambda agent: agent.fitness(), reverse=True)
        self.fitness_max = g[-1].fitness()
        print('Best fitness for generation ', len(self.generation), ' is : ', g[0].fitness())
        print('Fitness min for this generation is', self.fitness_max)
        if g[0].fitness() > self.best_fit.fitness():
            self.best_fit = g[0]
            print('New best agent overall !\n')

    def crossover(self, option=''):
        """ Make a crossover of the population working half and half, record the best fit of the actual population and
                finally actualize the population with the children"""
        new_indexes_to_mate = []
        new_population = []
        if (option == '' and self.crossover_method == 'Proportion') or option == 'Proportion':
            new_indexes_to_mate = self.__crossover_proportion()
        elif (option == '' or self.crossover_method == 'Truncation') or option == 'Truncation':
            new_indexes_to_mate = self.__crossover_truncation()
        elif (option == '' or self.crossover_method == 'Elite') or option == 'Elite':
            new_indexes_to_mate = self.__crossover_elite(self.demographic_number // 4)
        else:
            'Unknown method'
        while len(new_population) < self.demographic_number:
            girl, boy = self.population[new_indexes_to_mate[self.rng.integers(0, len(new_indexes_to_mate))]] + \
                        self.population[new_indexes_to_mate[self.rng.integers(0, len(new_indexes_to_mate))]]
            boy.mutate(self.mutation_rate)
            girl.mutate(self.mutation_rate)
            new_population.append(boy)
            new_population.append(girl)
        self.generation.append(self.population.copy())
        self.population = new_population.copy()

    def __crossover_elite(self, elite_size):
        """The €lit€ is selection"""
        #self.population = sorted(self.population, key=lambda agent: agent.fitness(), reverse=False)
        pop = {}
        for i in range(0, len(self.population)):
            pop[i] = self.population[i].fitness()
        pop = sorted(pop.items(), key=operator.itemgetter(1), reverse=True)
        selected_mates = []
        df = pd.DataFrame(np.array(pop), columns=["Index", "Fitness"])

        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(0, elite_size):
            selected_mates.append(self.population.index(self.population[i]))
        for i in range(0, (self.demographic_number // 2) - elite_size):
            pick = 100*self.rng.random()
            for i in range(0, len(self.population)):
                if pick <= df.iat[i, 3]:
                    selected_mates.append(self.population.index(self.population[i]))
                    break
        return selected_mates

    def __crossover_proportion(self):
        """Create a mating pool based on a sotchastic approach
        https://arxiv.org/abs/1109.3627 stochastic acceptance for O(1) at best"""
        selected_indexes = []
        # selection of indexes
        crossover_probability = self.crossover_probability
        while len(selected_indexes) < (self.demographic_number // 2):
            potential = self.rng.integers(low=0, high=self.demographic_number, size=self.demographic_number).tolist()
            for i in range(0, len(potential)):
                if (self.population[potential[i]].fitness() / self.fitness_max) > crossover_probability:
                    selected_indexes.append(potential[i])
            crossover_probability -= 0.01
        if crossover_probability < self.crossover_probability:
            print('Probability of selection has been lowered to', crossover_probability * 100, '%\n')
        return selected_indexes

    def __crossover_truncation(self, k=0.5):
        """Create a mating pool by simply truncating like an idiot after ranking in order"""
        # TODO http://nitro.biosci.arizona.edu/zbook/NewVolume_2/pdf/WLChapter14.pdf
        self.population = sorted(self.population, key=lambda agent: agent.fitness(), reverse=True)
        selected_indexes = [i for i in range(0, math.floor(len(self.population) * k))]
        return selected_indexes

    def run(self):
        for i in range(0, self.generation_number):
            self.best_of_actual_generation()
            self.crossover(option='Elite')
        self.best_of_actual_generation()
        print('The best agent has this genetics : ', self.best_fit.genetics())
        print('The best agent has this index : ', self.best_fit.get_indexes())
        correct_order = []
        for i in range(0, len(self.best_fit.genetics())):
            correct_order.append(self.best_fit.genetics()[self.best_fit.get_indexes()[i]])
        print('And finally the correct order :', correct_order)
        print('The final time is : ', self.best_fit.get_int_fitness())


if __name__ == '__main__':
    np.random.seed(10)
    pop = Population(genetic_template=np.random.normal(0, 1000, 1000).tolist(), demographic=100, generation=500,
                     crossover_probability=0.8, mutation_rate=0.01)
    pop.run()
