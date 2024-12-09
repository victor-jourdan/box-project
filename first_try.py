from readfa import readfq
from util import *
import sys 

def semi_brute_force_neighbors(kmer):
    neighbors = []
    for l in "ATCG":
        neighbors.append(kmer + l) 
        neighbors.append(l + kmer)
    return neighbors

def semi_brute_force(seqname, seq, k = 0, output_file = "output.tsv"):
    kmers = [{} for _ in range(k+1)] # all kmers of size <= k
    kmers[0][""] = 1 # the kmer of size 0 is the empty string
    kmaws = [[] for _ in range(k+1)] # to avoid offset of 1 errors, we add a kmaw for substrings of size 0
    for i in range(1,k+1):
        for j in range(len(seq) - k):
            kmers[i][canonical(seq[j: j + i])] = 1 # we build the collections of kmers of s of size i for i in range k
    
    for i in range(k): 
        for kmer in kmers[i]:
            neighbors = semi_brute_force_neighbors(kmer)  
            # we select all substrings that are kmer + 1 letter at the beginning or at the end, reverse_complement included, because we then select the canonical form of the neighbor
            for neighbor in neighbors:
                can_neighbor = canonical(neighbor)
                if can_neighbor not in kmers[i+1]:
                    kmaws[i+1].append(can_neighbor)
    for i in range(k+1):
        kmaws[i].sort()
    tsv_print_array_version(seqname, kmaws, k, output_file)

def main():
    args = read_args(3, 3, "Usage: python first_try.py <output file> <sequence file> <kmax>") 
    with xopen(args[1]) as filename:
        for seqname,seq,_ in readfq(filename):
            semi_brute_force(seqname, seq, int(args[2]), args[0])

if __name__ == "__main__":
    main()

