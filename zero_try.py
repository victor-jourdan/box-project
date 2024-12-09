from readfa import readfq
from util import * 
import itertools as itt

def is_maw(seq, kmer):
    return (kmer[1:len(kmer)] in seq and \
    kmer not in seq and \
    kmer[0:len(kmer)-1] in seq) or\
    (reverse_complement(kmer[0:len(kmer)-1]) in seq and\
    reverse_complement(kmer[1:len(kmer)]) in seq and \
    reverse_complement(kmer) not in seq)

def brute_force(seqname, seq, k, output_file):
    maws = [[] for _ in range(k+1)]
    all_kmers = [""]
    for i in range(k):
        all_kmers = itt.product( ["A", "C", "G", "T"], repeat=i+1)
        for elt in all_kmers:
            if is_maw(seq, "".join(elt)):
                maws[i+1].append("".join(elt))
    tsv_print_array_version(seqname, maws, k, output_file)


def main():
    args = read_args(3, 3, "Usage: python zero_try.py <output file> <sequence file> <kmax>") 
    with xopen(args[1]) as filename:
        for seqname,seq,_ in readfq(filename):
            brute_force(seqname, seq, int(args[2]), args[0])

main()

    



