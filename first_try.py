from readfa import readfq
from util import *
from numpy import inf
import sys 

def semi_brute_force_extensions(kmer):
    neighbors = []
    for l in "ATCG":
        neighbors.append(kmer + l) 
        #neighbors.append(l + kmer) useless after analysis
    return neighbors

def semi_brute_force(seqname, seq, k = 0, output_file = "output.tsv"):
    kmers = [{} for _ in range(k+1)] # all kmers of size <= k
    kmers[0][""] = 1 # the kmer of size 0 is the empty string
    kmaws = [[] for _ in range(k+1)] # to avoid offset of 1 errors, we add a kmaw for substrings of size 0
    for i in range(1,k+1):
        for j in range(len(seq) - i):
            kmers[i][seq[j: j + i].upper()] = 1 # we build the collections of kmers of s of size i for i in range k
    
    for i in range(k): 
        for kmer in kmers[i]:
            extensions = semi_brute_force_extensions(kmer)  
            # we select all substrings that are kmer + 1 letter at the beginning or at the end, reverse_complement included, because we then select the canonical form of the neighbor
            for extension in extensions:
                if extension not in kmers[i+1] and extension[1:] in kmers[i]:
                    kmaws[i+1].append(canonical(extension))
    for i in range(k+1):
        kmaws[i].sort()
    tsv_print_array_version(seqname, kmaws, k, output_file)

def main():
    args = read_args(4, 3, "Usage: python first_try.py"\
    " <output file path (will add the number of the sequence and .tsv at the end)> "\
        "<sequence file path> <kmax> <optional: maximal number of sequences>") 
    nb_iter = 0
    if len(args) >= 4:
        nb_iter = int(args[3])
    else:
        nb_iter = inf
    with xopen(args[1]) as filename:
        counter = 0
        for seqname,seq,_ in readfq(filename): 
            semi_brute_force(seqname, seq, int(args[2]), args[0] + str(counter) + ".tsv")
            counter += 1
            if counter >= nb_iter:
                break 

if __name__ == "__main__":
    main()

