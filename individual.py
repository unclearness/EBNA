import random

class Individual:
    def __init__(self):
        self.fitness = -100000
        self.gene = []
        #self.gene = self.init_gene(setup)
    
    def init_gene(self, setup):
        if setup.gene_type == "binary":
            self.gene = []
            for i in range(setup.gene_length):
                self.gene.append(random.randint(0, 1))
        else:
            raise AttributeError("not supported except binary")

    def clone(self):
        copy = Individual()
        copy.fitness = self.fitness
        copy.gene = self.gene
        return copy
        
        
