# coding: UTF-8
from numpy import *
import sys, random
from bic_metric import *

MAX_INCOMING_EDGE = 100

class BayesianNetwork:
    def __init__(self, samples, setup):
        self.num_of_var = setup.gene_length
        self.__network = zeros((self.num_of_var, self.num_of_var))
        self.prior_table = {}
        self.cond_table = {}
        self.samples = samples
        self.init_pi_table()
        self.setup = setup
        self.metric = BICMetric()

    def initialize_network(self):
        for i in range(self.num_of_var):
            for j in range(i+1,self.num_of_var):
                if 0.5 < random.random():
                    self.add_edge(i, j)
        self.initialize_params()
    
    def initialize_params(self):
        for a in self.get_node_with_no_parents():
            self.initialize_prior_table(a)
        for i in range(self.num_of_var):
            parents = self.get_parents(i)
            if parents != []:
               self.initialize_cond_table(i, parents)

    def initialize_prior_table(self, index):
        self.prior_table[index] = {}
        card = self.setup.get_cardinality(index)
        for c in card:
            self.prior_table[index][c] = 1.0 / len(card)

    def initialize_cond_table(self, child, parents):
        pi_table = self.pi_table[child]
        cardinality = self.setup.get_cardinality(child)
        for p in pi_table:
            self.cond_table[(tuple(parents), tuple(p))] = {}
            tmp = {}
            for c in cardinality:
                tmp[(child, c)] = 1.0 / len(cardinality)
            if round(sum(tmp.values())-1.0,7) != 0:
                for k,v in tmp.items():
                    print k,v
                print "sum ", sum(tmp.values())
                raise Exception("sum of conditional probability does not equal to 1")
            self.cond_table[(tuple(parents), tuple(p))] = tmp


    def ref_network(self, col, row):
        return self.__network[col][row]

    def get_network(self):
        return self.__network

    def add_edge(self, col, row):
        if self.__network[col][row] == 1:
            raise Exception("col "+str(col)+" row "+str(row)+"is already added")
        self.__network[col][row] = 1
        self.calc_pi(row)

    def remove_edge(self, col, row):
        if self.__network[col][row] == 0:
            raise Exception("col "+str(col)+" row "+str(row)+"is already removed")
        self.__network[col][row] = 0
        self.calc_pi(row)

    def estimate_edges(self):
        self.metric.set_samples(self.samples, self.setup)
        """自分よりインデックスが若いノードを親の候補とする"""
        self.parent_card = {}
        for i in range(1, self.num_of_var):
            tmp = []
            for j in range(i):
                tmp.append(j)
            self.parent_card[i] = tmp
        current_score = self.score()
        for i in range(1, self.num_of_var):
            num_of_input_edge = 0
            target_node = self.parent_card[i]     
            while(num_of_input_edge < MAX_INCOMING_EDGE and
                  len(target_node) != 0):
                current_best = -1
                current_max = -sys.maxint - 1
                for t in target_node:
                    self.add_edge(t,i)
                    tmp_score = self.score()
                    self.remove_edge(t,i)
                    if (tmp_score > current_max):
                        current_max = tmp_score
                        current_best = t
                if current_max > current_score:
                    self.add_edge(current_best,i)
                    num_of_input_edge += 1
                    current_score = current_max
                    target_node.remove(current_best)
                else:
                    break

    def estimate_params(self):
        for node in self.get_node_with_no_child():
            if len(self.get_parents(node)) != 0:
                self.learn_conditional(node)
            else:
                self.learn_univariate(node)

    def learn_univariate(self, node):
        if node in self.prior_table.keys():
            return
            #raise Exception(str(node) + " is already learned univarate")
        self.prior_table[node] = {}
        for i in self.setup.get_cardinality(node):
            self.prior_table[node][i] = float(self.count_samples(node,i)) / len(self.samples)
        if round(sum(self.prior_table[node].values())-1,7) != 0:
            for i in self.setup.get_cardinality(node):
                print i, self.prior_table[node][i]
            raise Exception("sum of prior does not equal to 1")
    
    def count_samples(self, node, instance):
        res = 0
        for s in self.samples:
            if s.gene[node] == instance:
                res += 1
        return res
    
    def count_samples_list(self, index_list, instance_list):
        res = 0
        for s in self.samples:
            flag = True
            for i,j in zip(index_list, instance_list):
                if s.gene[i] != j:
                    flag = False
                    break
            if flag:
                res += 1
        return res

    def count_samples_all(self, child, instance, parent_list, instance_list):
        res = 0
        for s in self.samples:
            if s.gene[child] != instance:
                continue
            flag = True
            for i,j in zip(parent_list, instance_list):
                if s.gene[i] != j:
                    flag = False
                    break
            if flag:
                res += 1
        return res

    def learn_conditional(self, node):
        if (node, self.setup.get_cardinality(node)[0]) in self.cond_table.keys():
            raise Exception(node + " is already learned conditional")
        parents = self.get_parents(node)
        self.set_conditional(node, parents)
        for p in parents:
            if len(self.get_parents(p)) != 0:
                self.learn_conditional(p)
            else:
                self.learn_univariate(p)

    def set_conditional(self, child, parents):
        pi_table = self.pi_table[child]
        cardinality = self.setup.get_cardinality(child)
        alpha = self.setup.alpha
        for p in pi_table:
            self.cond_table[(tuple(parents), tuple(p))] = {}
            tmp = {}
            for c in cardinality:
                #num_of_samples_child = self.count_samples(child, c)
                num_of_samples_parents = self.count_samples_list(parents, p)
                num_of_samples_all = self.count_samples_all(child, c, parents, p)
                """Laplace Smoothing"""
                tmp[(child, c)] = float(num_of_samples_all + alpha) \
                    / (num_of_samples_parents + alpha * len(cardinality))
            if round(sum(tmp.values())-1.0,7) != 0:
                for k,v in tmp.items():
                    print k,v
                print "sum ", sum(tmp.values())
                raise Exception("sum of conditional probability does not equal to 1")
            self.cond_table[(tuple(parents), tuple(p))] = tmp

    def score(self):
        return self.metric.score(self)

    def sampling(self):
        """
        
        Probabilistic Logic Sampling (PLS) 
        """
        res = [None] * self.num_of_var
        children = set([])
        for a in self.get_node_with_no_parents():
            self.prior_sampling(a, res)
            children.update(self.get_children(a))
        children = sorted(list(children))
        while(len(children) != 0):
            tmp = set([])
            for c in children:
                tmp.update(self.cond_sampling(c, res))
            children = tmp
            children = sorted(list(children))

        return res

    def prior_sampling(self, index, res):
        if index not in  self.prior_table.keys():
            raise Exception(str(index) + " does not have prior" )
        if res[index] is not None:
            return
        r = random.random()
        table = self.prior_table[index]
        tmp_low = tmp_high = 0
        for k,v in table.items():
            tmp_high += v
            if tmp_low < r and r < tmp_high:
                res[index] = k
                return
            tmp_low = tmp_high
        raise Exception("prior sampling failed" )

    def cond_sampling(self, index, res):
        if res[index] is not None:
            return self.get_children(index)
        parents = self.get_parents(index)
        parents_instance = []
        for p in parents:
            if res[p] is None:
                self.cond_sampling(p, res)
                #raise Exception(str(p) + " have not been sampled" )
            parents_instance.append(res[p])
        if (tuple(parents), tuple(parents_instance)) \
                not in self.cond_table.keys():
            raise Exception(str(index) + " does not have cond" )
        r = random.random()
        tmp_low = tmp_high = 0
        flag = True
        table = self.cond_table[(tuple(parents), tuple(parents_instance))]
        for k,v in table.items():
            tmp_high += v
            if tmp_low < r and r < tmp_high:
                res[index] = k[1]
                flag = False
                break
            tmp_low = tmp_high
        if flag:
            raise Exception("conditional sampling failed" )
        return self.get_children(index)
        #for c in self.get_children(index):
        #    self.cond_sampling(c, res)
        
    def get_children(self, index):
        result = []
        for i in range(self.num_of_var):
            if self.ref_network(index, i) == 1:
                result.append(i)
        return result

    def get_parents(self, index):
        result = []
        for i in range(self.num_of_var):
            if self.ref_network(i, index) == 1:
                result.append(i)
        return result
    
    def get_num_of_edges(self):
        res = 0
        for row in self.__network:
            res += sum(row)
        return res

    def get_node_with_no_child(self):
        res = []
        for i in range(self.num_of_var):
            if sum(self.__network[i]) == 0:
                res.append(i)
        return res

    def get_node_with_no_parents(self):
        res = []
        for i in range(self.num_of_var):
            if sum(self.__network[:,i]) == 0:
                res.append(i)
        return res

    def init_pi_table(self):
        self.pi_table = {}
        for i in range(self.num_of_var):
            self.calc_pi(i)
            
    def calc_pi(self, child):
        parents = self.get_parents(child)
        if len(parents) == 0:
            self.pi_table[child] = [[]]
            return
        elif len(parents) == 1:
            pi = map(lambda x:[x], self.setup.get_cardinality(parents[0]))
        else:
            pi = map(lambda x:[x], self.setup.get_cardinality(parents[0]))
            for p in parents[1:]:
                pi = map(lambda x: list(x),itertools.product(pi,self.setup.get_cardinality(p)))
            pi = map(lambda x:self.unfold(x), pi)
        self.pi_table[child] = pi
                
    def unfold(self, l):
        if len(l) == 1:
            return l
        else:
            return self.unfold(l[:-1][0])+[l[-1]]
