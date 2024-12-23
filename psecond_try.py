from util import *
import sys

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
        [
            [] 
            for _ in range(nb_sequences)
        ] 
        for _ in range(k)
    ]
    size_S = nb_sequences
    min_allowed = ceil ((1-p) * nb_sequences)
    pmaws = [set() for i in range(k+1)]
    for l in "ACGNT": #treating the base case of single-letter words
        occurrences = []
        for i in range(len(sequences)):
            if l in sequences[i]:
                occurrences.append(i)
        if occurrences >= min_allowed:
            struct[0][l] = Struct(occurrences = occurrences)
        else: 
            pmaws[1].update(l)
    pmaws[1] = sorted(pmaws[1])



def filling_structure(stage):
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
                        if x + l in imers[i][stage]:
                            occurrences.append(i)
                if occurrences >= min_allowed:
                    struct[stage][x+l] = Struct(occurrences = occurrences)
                else:
                    pmaws[i].update([x+l])
    pmaws[i] = sorted(pmaws[i])


def filling_imer(sequence, sequence_number):
    imers.append([[] for _ in range(k)])
    


def main(): 
    global pmaws
    #initializtion() setup args retrieval
    for i in range(k):
        filling_structure(i + 1)   
    tsv_print_array_version(seqname=seqname)
            

        
