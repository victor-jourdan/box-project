from readfa import readfq
from util import *
import sys 

def brute_force_neighbors(kmer):
    neighbors = []
    for l in "ATCG":
        neighbors.append(kmer + l) 
        neighbors.append(l + kmer)
    return neighbors

def brute_force(seqname, seq, k = 0, output_file = "output.tsv"):
    kmers = [{} for _ in range(k+1)] # all kmers of size <= k
    kmers[0][""] = 1 # the kmer of size 0 is the empty string
    kmaws = [[] for _ in range(k+1)] # to avoid offset of 1 errors, we add a kmaw for substrings of size 0
    for i in range(k):
        for j in range(len(seq) - k + 1):
            kmers[i][canonical(seq[j: j + k])] = 1 # we build the collections of kmers of s of size i for i in range k
    
    for i in range(k): 
        for kmer in kmers[i]:
            neighbors = brute_force_neighbors(kmer)  
            # we select all substrings that are kmer + 1 letter at the beginning or at the end, reverse_complement included, because we then select the canonical form of the neighbor
            for neighbor in neighbors:
                can_neighbor = canonical
                if neighbor not in kmers[i+1]:
                    kmaws[i+1].append(neighbor)
    for i in range(k+1):
        kmaws[i].sort()
    tsv_print_array_version(seqname, kmaws, k, output_file)

def main():
    args = read_args(3, 3, "Usage: python first_try.py <output file> <sequence file> <kmax>") 
    for seqname,seq,_ in readfq(args[1]):
        brute_force(seqname, seq, int(args[2]), args[3])

if __name__ == "__main__":
    main()

