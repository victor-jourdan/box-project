from readfa import readfq
from xopen import xopen
import matplotlib.pyplot as plt
import sys 


def read_args(expected_args, num_mandatory_args, presentation_str): #and also flushes the output file 
    args = sys.argv[1:]
    if len(args) >= 1:
        with open(args[0]) as _: #flush the output file
            pass 
    if len(args) < num_mandatory_args: #lack of mandatory args
        print(presentation_str)
        sys.exit(1)
    return read_args

def fileconcat(filename):
    with xopen(filename) as fasta:
        sum = []
        for _,seq,_ in readfq(fasta):
            sum += seq.upper().split("[^ATCGN]")
            print(sum)
        return sum


RC_TABLE = str.maketrans("ACTGNactgn", "TGACNtgacn")

def reverse_complement(seq: str) -> str:
    complement = seq.translate(RC_TABLE)
    return complement[::-1]


def canonical(kmer):
    return min(kmer, reverse_complement(kmer))


def tsv_print_array_version(seqname, kmaws, kmax, output_file):
    with open(output_file, "a") as output_file_s:
        for i in range(kmax + 1):
            if kmaws[i] != []:
                out_file_s.write(seqname + "\t" + k + "\t")
                for kmer in kmaws[i]:
                    output_file_s.write(kmer + ";")
                output_file_s.write("\n")


                
            


    
