#import random
import csv

def g_0(n):
    return ("?",) * n

def s_0(n):
    return ('$',)*n
#true if h1 more general than h2
def more_general(h1, h2):#h1-hypothesis h2-example
    more_general_parts = []
    for x, y in zip(h1, h2):#x-hyp y-ex
        mg = x == "?" or (x != "$" and (x == y or y == "$"))
        more_general_parts.append(mg)
        #print(more_general_parts)
    return all(more_general_parts)

def fulfills(example, hypothesis):
    #print('hyp:',hypothesis)
    return more_general(hypothesis, example)

def min_generalizations(h, x):#checks each attribute and replaces with ? or the value like finds
    h_new = list(h)
    for i in range(len(h)):
        if not fulfills(x[i:i+1], h[i:i+1]):
            h_new[i] = '?' if h[i] != '$' else x[i]
    return [tuple(h_new)]

def min_specializations(h, domains, x):
    results = []
    for i in range(len(h)):
        if h[i] == "?":
            for val in domains[i]:
                if x[i] != val:
                    h_new = h[ : i] + (val, ) + h[i + 1: ]
                    results.append(h_new)
        #elif h[i] != "$":
           # h_new = h[ : i] + ('$', ) + h[i + 1: ]
           # results.append(h_new)
    return results

with open('Training_examples.csv') as csvFile:
    examples = [tuple(line) for line in csv.reader(csvFile)]

def get_domains(examples):
    d = [set() for i in examples[0]]
    for x in examples:
        for i, xi in enumerate(x):
            d[i].add(xi)
    return [list(sorted(x)) for x in d]
#get_domains(examples)

def candidate_elimination(examples):
    domains = get_domains(examples)[: -1]#all except last one
    print(domains)
    G = set([g_0(len(domains))])
    S = set([s_0(len(domains))])
    i = 0
    print("\n G[{0}]:".format(i), G)
    print("\n S[{0}]:".format(i), S)
    for xcx in examples:
        i = i + 1
        x, cx = xcx[:-1], xcx[-1]
        if cx == 'Y':
            G = {g for g in G if fulfills(x, g)}#check if each g fulfills x
            S = generalize_S(x, G, S)#make S more general
        else:
            S = {s for s in S if not fulfills(x, s)}#hypothesis s is not more general than x
            G = specialize_G(x, domains, G, S)
        print("\nG[{0}]:".format(i), G)
        print("\nS[{0}]:".format(i), S)
    return

def generalize_S(x, G, S):
    S_prev = list(S)
    #print('S prev:',S_prev)
    for s in S_prev:
        #print('s: ',s)
        #if s not in S:
         #   continue
        if not fulfills(x, s):#if s is not more general than x
            S.remove(s)
            Splus = min_generalizations(s, x)#generalise s
            S.update([h for h in Splus if any([more_general(g, h) for g in G])])#make sure g is more general than s
            S.difference_update([h for h in S if any([more_general(h, h1) for h1 in S if h != h1])])#remove more general hypothesis
    return S

def specialize_G(x, domains, G, S):
    G_prev = list(G)
    for g in G_prev:
        #if g not in G:
        #    continue
        if fulfills(x, g):
            G.remove(g)
            Gminus = min_specializations(g, domains, x)#specialize g
            G.update([h for h in Gminus if any([more_general(h, s) for s in S])])#make sure h is more general than s
            G.difference_update([h for h in G if any([more_general(g1, h) for g1 in G if h != g1])])#rermove less general hypothesis
    return G

candidate_elimination(examples)
