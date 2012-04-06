# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
import numpy as np

def _split(counts):
    groups = ([],[])
    weights = np.zeros(2, float)

    in_order = counts.argsort()
    for s in in_order[::-1]:
        g = weights.argmin()
        groups[g].append(s)
        weights[g] += counts[s]
    return groups


class multi_tree_model(object):
    def __init__(self, labelnames, model):
        self.labelnames = labelnames
        self.model = model

    def apply(self, message):
        def ap_recursive(smodel):
            if len(smodel) == 1:
                return self.labelnames[smodel[0]]
            model,left,right = smodel
            if model.apply(message): return ap_recursive(left)
            else: return ap_recursive(right)
        return ap_recursive(self.model)

class multi_tree_learner(object):
    '''
    Implements a multi-class learner as a tree of binary decisions.

    At each level, labels are split into 2 groups in a way that attempt to
    balance the number of examples on each side (and not the number of labels
    on each side). This mean that on a 4 class problem with a distribution like
    [ 50% 25% 12.5% 12.5%], the "optimal" splits are

             o
            / \
           /   \
          [0]   o
               / \
             [1]  o
                 / \
                [2][3]

    where all comparisons are perfectly balanced.
    '''

    def __init__(self, base):
        self.base = base

    def train(self, features, labels, normalisedlabels=False, **kwargs):
        if not normalisedlabels:
            from milk.supervised.normalise import normaliselabels
            labels,names = normaliselabels(labels)
            labelset = np.arange(len(names))
        else:
            labels = np.asanyarray(labels)
            names = np.arange(labels.max()+1)
            labelset = np.arange(labels.max()+1)


        def recursive(labelset, counts):
            if len(labelset) == 1:
                return labelset
            g0,g1 = _split(counts)
            nlabels = []
            nfeatures = []
            s0 = set([labelset[g] for g in g0])
            s1 = set([labelset[g] for g in g1])
            for ell,f in zip(labels,features):
                if (ell in s0) or (ell in s1):
                    nlabels.append(int(ell in s1))
                    nfeatures.append(f)

            nlabels = np.array(nlabels)
            name = "-".join([str(labelset[e]) for e in g1])
            model = self.base.train(nfeatures, nlabels, name=name, normalisedlabels=True, **kwargs)
            m0 = recursive(labelset[g0], counts[g0])
            m1 = recursive(labelset[g1], counts[g1])
            return (model, m0, m1)
        counts = np.zeros(labels.max()+1)
        for ell in labels:
            counts[ell] += 1
        return multi_tree_model(names, recursive(np.arange(labels.max()+1), counts))

