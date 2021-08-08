import random
import individual

class Setup:
    def __init__(self, gene_size, gene_type="binary", sl_method="roulette",\
                     gene_length=50, pop_size=5, elite_rate=0.01, t_size=5):
        self.gene_type = gene_type
        self.sl_method=sl_method
        self.gene_length = gene_length
        self.pop_size = pop_size
        if pop_size < 100:
            self.elite_rate=1.0 / pop_size
        else:
            self.elite_rate=elite_rate
        self.t_size = t_size
        self.gene_size = gene_size
        self.current_max = -100000
        self.unchanged = 0
        self.optimum = gene_length

    def get_cardinality(self, index):
        return [0,1]

    def evaluate(self, indiv):
        indiv.fitness = sum(indiv.gene)

    def terminate(self, population):
        if population[0].fitness > self.current_max:
            self.unchanged = 0
            self.current_max = population[0].fitness
        else:
            self.unchanged += 1  
        if population[0].fitness >= self.optimum:
            return True, True
        elif self.unchanged > 10:
            return True, False
        else:
            return False, None

    def get_elites(self,population):
        res = []
        for i in range(int (self.pop_size*self.elite_rate)):
            res.append(population[i].clone())
        return res

    def selection(self, population):
        if self.sl_method=="truncate":
            return population[:(int) (self.setup.tr_rate * len(self.population))]
        elif self.sl_method=="tournament":
            return self.tournament_selection(population)
        elif self.sl_method=="roulette":
            return self.roulette_selection(population)
        else:
            raise Exception('selection method: '+self.sl_method+' is not supported')

    def tournament_selection(self, population):
        raise Exception('selection method: '+self.sl_method+' is not supported')

    def roulette_selection(self, population):
        res = []
        fitness_sum = sum(map(lambda x: x.fitness, population))
        for i in range(self.gene_size):
            r = random.random()
            tmp_low = tmp_high = 0
            for indiv in population:
                tmp_high += (indiv.fitness / float (fitness_sum))
                if tmp_low < r and r < tmp_high:
                    res.append(indiv.clone())
                    break
                else:
                    tmp_low = tmp_high
        return res
    
class SetupEda(Setup):
    def __init__(self, gene_type="binary", sl_method="roulette", \
                     gene_length=20, pop_size=100, elite_rate=0.01, \
                     t_size=5, alpha=1, sample_rate=0.1):
        Setup.__init__(self,int(sample_rate*pop_size), gene_type, sl_method, gene_length, pop_size, elite_rate, t_size)
        self.alpha = alpha
        self.sample_rate = sample_rate
