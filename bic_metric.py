# coding: UTF-8
import math
import itertools

class BICMetric():
    def __init__(self):
        pass
        
    def set_samples(self, samples, setup):
        self.samples = samples
        self.setup = setup
        self.prev_likeli_table = {}
        self.prev_cpt_size_table = {}

    def score(self, bn):
        self.bn = bn
        return self.get_likelihood() - \
            0.5 * self.get_CPT_size()  * math.log(len(self.samples), 2)

    def get_likelihood(self):
        res = 0.0
        for i in range(self.bn.num_of_var):
            if self.prev_likeli_table.has_key((i,tuple(self.bn.get_parents(i)))):
                res += self.prev_likeli_table[(i,tuple(self.bn.get_parents(i)))]
                continue
            pi_size = len(self.bn.pi_table[i])
            res_j = 0.0
            for j in range(pi_size):
                n_ij = self.count_samples(i, j, None)
                for k in range(len(self.setup.get_cardinality(i))):
                    n_ijk = self.count_samples(i, j, k)
                    if n_ijk < 1:
                        continue
                    res_j += n_ijk * math.log(float(n_ijk)/float(n_ij), 2)
            res += res_j
            self.prev_likeli_table[(i,tuple(self.bn.get_parents(i)))] = res_j
        return res

    def count_samples(self, i, j, k):
        res = 0
        candidate = self.bn.pi_table[i][j]
        for s in self.samples:
            if k is not None and s.gene[i] != self.setup.get_cardinality(i)[k]:
                continue
            flag = True
            for p,c in zip(self.bn.get_parents(i),candidate):
                if s.gene[p] != c:
                    flag = False
                    break
            if flag:
                res += 1
        return res
        
    def get_CPT_size(self):
        #条件付き確率表のサイズを求める
        K = 0
        for i in range(self.bn.num_of_var):
            if self.prev_cpt_size_table.has_key((i,tuple(self.bn.get_parents(i)))):
                K += self.prev_cpt_size_table[(i,tuple(self.bn.get_parents(i)))]
                continue
            #r,x_iがとれるシンボル数
            r = len(self.setup.get_cardinality(i)) 
            #q,x_iの親ノードがとれる状態数
            q = len(self.bn.pi_table[i])
            """r-1なのは最後のシンボルの確率は他の確率の合計値を1から引けば求まるので
            シンボル1つ分の確率を保持する必要がないから"""
            K += q * (r-1)
            self.prev_cpt_size_table[(i,tuple(self.bn.get_parents(i)))] = q * (r-1)
        return K
