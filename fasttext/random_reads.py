#!/usr/bin/env python3

import re
import click
from Bio import SeqIO
import os
import random
import numpy as np

def split_genome(genome="ATCGATATACCA", k=3):
    return re.findall('.'*k, genome)


def genearte_genomes(genome='ATCGATATACCA', k=3):
    sentences = []
    for index in range(0, k):
        sentences.append(split_genome(genome=genome[index:], k=k))
    return sentences


@click.command()
@click.option('--input-file', help='Input file in FASTA format')
@click.option('--length', default=10000, help='read length')
@click.option('--reads', default=100, help='number of random reads to produce')
@click.option('--mutate', default=0, help='% of mutation of total number of nucleotides')
# @click.option('--output-file', help="Output file to write")
def main(input_file, length, reads, mutate):
    ''' This script generates n random reads of length l from the input FASTA file '''
    records = []
    for record in SeqIO.parse(input_file, 'fasta'):
        _seq = str(record.seq).upper()
        if len(_seq) < length: continue
        random_intervals = [random.randint(0, len(_seq)-length) for i in range(reads)]

        records+=[ [_seq[ix:ix+length], input_file] for ix in random_intervals ]

    # print(records)
    nucleotides = ['A', 'C', 'T', 'G']
    if mutate > 0:
        for item in records:
            print(item[0])
            _mutation_counts = int(len(item[0])*mutate/100)
            _choises = range(0, len(item[0]))
            random.shuffle(_choises)
            _bp_to_mutate = _choises[:_mutation_counts]
            for _bp in _bp_to_mutate:
                item[0][_bp] = nucleotides[ random.randint(0,3) ]
            print(item[0])
            exit()


    fo = open(input_file+'.reads', 'w')
    for ix,i in enumerate(records):
        fo.write('>'+i[1]+'|'+str(ix)+'\n'+i[0]+'\n')

if __name__ == '__main__':
    main()
