from util import *
import sys

struct = NotImplemented
pointers = NotImplemented
# a c-like structure in python
class Struct: 
    def __init__(self, **entries): self.__dict__.update(entries)
    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k,v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)


def initialization(k, nb_sequences):
    global struct
    global pointers
    struct = [ 
        [
            [] 
            for _ in range(nb_sequences)
        ] 
        for _ in range(k)
    ]
    pointers = [Struct(value=0) for _ in range(nb_sequences)]


def parcours(imer, curr_sequence_index): 
    i = len(imer) - 1 # at which size of i-mer we are (-1 to ease indexing)
    global struct 
    global pointers
    found = False
    for u in range(curr_sequence_index - 1):
        v = pointers[u]
        if found: 
            break
        while v < len(struct[i][u]):
            s = struct[i][u][v.value]
            if s.imer > imer:
                break
            v.value += 1
            if s.imer == imer:
                s.occurrences.append(curr_sequence_index)
                
                found = True
                break 
    if not found: 
    # the element was not found in any of the i-mers of the previously computated sequences 
        #################TODO##########################struct[i][curr_sequence_index][]Struct(occurrences=[curr_sequence_index]))
        # occurences lists the sequences in which the imer occurs, 
        # and imer stores the imer itself.
        pass

def filling_structure(sequences):
    global struct 
    global pointers
    for i in range(k):
        length = len(sequences)
        imers = [set() for _ in range(length)]
        for u in range(length):
            for v in range(len(sequences[u]) - k):
                imers[u] |= canonical(sequences[u][v: v + i])
        for u in range(k):
            imers[u] = sorted(imers[u])
            # we gathered all the imers of all sequences
        for u in range(length):
            pointers[i].value = 0
            # initialize the pointers
        for u in range(length):
            for v in range(leng(imers[u])):
                parcours(imers[u][v], u)
        

def rate_calculation():
    pass
            
            
        
        