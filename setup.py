class Setup:
    def __init__(self, gene_type="binary", sl_method="tournament",\
                     gene_length=50, pop_size=5, t_size=5):
        self.gene_type = gene_type
        self.gene_length = gene_length
        self.pop_size = pop_size
        #self.optimum = optimum
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

    def selection(self):
        if sl_method=="truncate":
            return self.population[:(int) (self.setup.sl_rate * len(self.population))]
        elif sl_method=="tournament":
            return self.tournament_selection()
        else:
            raise Exception('selection method: 'sl_method+' is not supported')

    def tournament_selection(self):
        
class SetupEda(Setup):
    def __init__(self, gene_type="binary", sl_method="tournament", \
                     gene_length=20, pop_size=100, t_size=5, alpha=1):
        Setup.__init__(self, gene_type, sl_method, gene_length, pop_size, t_size)
        self.alpha = alpha
