#!/usr/bin/env python3

import re
import click
from Bio import SeqIO
import os
import random

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
# @click.option('--output-file', help="Output file to write")
def main(input_file, length, reads):
    ''' This script generates n random reads of length l from the input FASTA file '''
    records = []
    for record in SeqIO.parse(input_file, 'fasta'):
        _seq = str(record.seq).upper()
        if len(_seq) < length: continue
        random_intervals = [random.randint(0, len(_seq)-length) for i in range(reads)]

        records+=[ [_seq[ix:ix+length], input_file] for ix in random_intervals ]

    # print(records)
    fo = open(input_file+'.reads', 'w')
    for ix,i in enumerate(records):
        fo.write('>'+i[1]+'|'+str(ix)+'\n'+i[0]+'\n')

if __name__ == '__main__':
    main()
