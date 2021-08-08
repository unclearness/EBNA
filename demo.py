from bic_metric import *
from setup_maxproblem import *
from individual import *
from bayesian_network import *
from ebna import *
"""set = Setup()
samp = []
for i in range(5):
    samp.append(Individual(set))

samp[0].gene = [0,1,1,1,1]
samp[1].gene = [1,0,1,0,1]
samp[2].gene = [0,1,1,0,1]
samp[3].gene = [0,0,0,0,1]
samp[4].gene = [1,1,0,0,0]

bic = BICMetric()
bic.set_samples(samp, set)
bn = BayesianNetwork(5, samp, set)
#bn.network[0][1] = 1
#bn.network[2][3] = 1
#bn.network[2][4] = 1

bn.network[0][2] = 1
bn.network[0][3] = 1
bn.network[0][4] = 1
bn.network[1][3] = 1
bn.network[1][4] = 1
bn.network[2][4] = 1
bn.network[3][4] = 1
print bic.scoe(bn)
"""

"""
set = SetupEda()
samp = []
for i in range(6):
    samp.append(Individual(set))
samp[0].gene = [0,1,0,0,0]
samp[1].gene = [1,0,1,0,1]
samp[2].gene = [0,1,1,1,1]
samp[3].gene = [1,0,1,1,0]
samp[4].gene = [0,1,0,0,1]
samp[5].gene = [0,1,0,1,1]
bic = BICMetric()
bic.set_samples(samp, set)
bn = BayesianNetwork(samp, set)
set.gene_length=5
set.pop_size=100
bn.estimate_edges()
#bn.add_edge(1,2)
print 
for row in bn.get_network():
    print row
print bic.score(bn)
#print bic.score(bn)
bn.estimate_params()
print "univarate"
for k,v in bn.prior_table.items():
    print k,v
print "conditional"
for k,v in bn.cond_table.items():
    print k,v
print
print bn.get_children(1)
print bn.sampling()
"""

s = SetupEda()
b = Ebna(s)
b.run()

