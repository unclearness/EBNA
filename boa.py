#!/usr/bin/python
# coding: UTF-8
from setup import *
import random

class Boa:
    def __init__(self, setup):
        self.setup = setup

    def run(self):
        self.population = init_population()
        self.generation = 0
        eval_population()
        sort_population()
        suc = setup.terminate(self.population)
        while(not suc[0]):
            self.generation += 1
            breed()
            eval_population()
            sort_population()
            suc = setup.terminate(self.population)
        if suc[1]:
            pass
        else:
            pass

    def init_population(self):
        result = []
        for i in range(self.setup.pop_size):
            result.append(Individual(self.setup))
        return result
    
    def eval_population(self):
        for i in self.population:
            self.setup.evaluate(i)

    def sort_population(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        #self.population = sorted(self.population, key=(lambda x: x.fitness))

    def breed(self):
        bn = BayesianNetwork()
        bn.estimate_edges()
        bn.estimate_params()
        new_pop = []
        for i in range(self.setup.pop_size):
            new_pop.append(bn.sample())
        self.population = new_pop
         
s = SetupEda()
b = Boa(s)
b.population = b.init_population()
for i in b.population:
    print i.fitness, i.gene
print
print
b.eval_population()
b.sort_population()
for i in b.population:
    print i.fitness, i.gene

