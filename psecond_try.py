from util import *
import sys
from math import ceil
from numpy import inf
from copy import deepcopy

struct = NotImplemented
imers = NotImplemented
min_allowed = NotImplemented #number of occurrences necessary to not be p-absent, = ceil((1 - p) * |S|)
size_S = NotImplemented #numer of sequences
pmaws = NotImplemented
# a c-like structure in python
class Struct: 
    def __init__(self, **entries): self.__dict__.update(entries)
    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k,v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)


def initialization(k, nb_sequences, sequences, p):
    global struct
    global pmaws
    global size_S 
    global min_allowed 
    struct = [ 
            {}
        for _ in range(k+1)
    ]
    size_S = nb_sequences
    min_allowed = ceil ((1-p) * nb_sequences)
    pmaws = [[] for i in range(k+1)]
    for l in "ACGNT": #treating the base case of single-letter words
        occurrences = []
        for i in range(len(sequences)):
            if l in sequences[i]:
                occurrences.append(i)
        if len(occurrences) >= min_allowed:
            struct[0][l] = Struct(occurrences = occurrences)
        else: 
            pmaws[1].append(l)
    pmaws[1] = sorted(pmaws[1])



def filling_structure(stage): 
    #constructs the structure of the not p absent words of size stage, 
    # and stores the one that get ejected, the pmaws of size stage. 
    global struct 
    global imers 
    global pmaws
    dic = struct[stage - 1]
   
    for x in dic:
        for l in "ACGNT":     
            x_r = x[1:] + l      
            if x_r in dic:
                struct1 = dic[x]              
                struct2 = dic[x_r]               
                occurrences = []
                for i in struct1.occurrences:
                    if i in struct2.occurrences:                       
                        if x + l in imers[i][stage + 1]:
                            occurrences.append(i)
                if len(occurrences) >= min_allowed:
                    struct[stage][x+l] = Struct(occurrences = occurrences)
                else:
                    pmaws[stage].append(x+l)
    pmaws[stage] = sorted(set(pmaws[stage]))


def filling_imer(seq, k):
    global imers
    imers.append([set() for _ in range(k+2)]) # all kmers of size <= k
    imers[-1][0] = {""}# the kmer of size 0 is the empty string
    for i in range(1,k+2):
        for j in range(len(seq) - i):
            imers[-1][i].update([seq[j: j + i].upper()]) # we build the collections of kmers of s of size i for i in range k

    


def main(): 
    global pmaws
    global size_S
    global imers
    
    args = read_args(5, 4, "Usage: python psecond_try.py <output file path (will add the .tsv at the end)> <sequences file path> <kmax> <p> <optional: maximum number of sequences>") 
    counter = 0
    nb_iter = 0
    if len(args) >= 5:
        nb_iter = int(args[4])
    else:
        nb_iter = inf
    sequences = []
    imers = []
    k = int(args[2])
    p = float(args[3])
    with xopen(args[1]) as file:
        for seqname,seq,_ in readfq(file):
            sequences.append(seq)
            filling_imer(seq, k)
            counter += 1
            if counter >= nb_iter:
                break
    size_S = counter
    initialization(k, size_S, sequences, p)
    
    for i in range(k):
        filling_structure(i + 1)   
    
    tsv_print_array_version(args[1] + f" for p = {p} and k = ", pmaws, k, args[0] + "0.tsv")            


if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
        
