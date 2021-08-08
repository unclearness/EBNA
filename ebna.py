#!/usr/bin/python
# coding: UTF-8
#from setup import *
from individual import *
from bayesian_network import *
import random, time

class Ebna:
    def __init__(self, setup):
        self.setup = setup

    def run(self):
        self.init_population()
        self.generation = 0
        self.eval_population()
        self.sort_population()
        suc = self.setup.terminate(self.population)
        print self.generation, self.population[0].fitness
        while(not suc[0]):
            self.generation += 1
            self.breed()
            self.eval_population()
            self.sort_population()
            print self.generation, self.population[0].fitness
            suc = self.setup.terminate(self.population)
        if suc[1]:
            print self.generation, "success!"
        else:
            print self.generation, "failed"

    def init_population(self):
        self.population = []
        bn = BayesianNetwork([], self.setup)
        bn.initialize_network()
        for i in range(self.setup.pop_size):
            tmp = Individual()
            tmp.gene = bn.sampling()
            self.population.append(tmp)
        """"result = []
        for i in range(self.setup.pop_size):
            indiv = Individual()
            indiv.init_gene(self.setup)
            result.append(indiv)
        self.population = result"""
    
    def eval_population(self):
        for i in self.population:
            self.setup.evaluate(i)

    def sort_population(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        #self.population = sorted(self.population, key=(lambda x: x.fitness))

    def breed(self):
        samples = self.setup.selection(self.population)
        bn = BayesianNetwork(samples, self.setup)
        time0 = time.clock()
        bn.estimate_edges()
        time1 = time.clock()
        print "calc edges:", time1 - time0
        print "edges ", bn.get_num_of_edges()
        bn.estimate_params()
        time2 = time.clock()
        print "calc params:", time2 - time1
        new_pop = self.setup.get_elites(self.population)
        elite_size = int (self.setup.elite_rate * len(self.population))
        for i in range(self.setup.pop_size-elite_size):
            tmp = Individual()
            tmp.gene = bn.sampling()
            new_pop.append(tmp)
        time3 = time.clock()
        print "calc samp:", time3 - time2
        self.population = new_pop
