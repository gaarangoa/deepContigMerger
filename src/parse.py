#!/usr/bin/env python3

import re
import click
from Bio import SeqIO
import os

def split_genome(genome="ATCGATATACCA", k=3):
    return re.findall('.'*k, genome)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def genearte_genomes(genome='ATCGATATACCA', k=3):
    sentences=[]
    for index in range( 0, k ):
        _sentences = split_genome(genome=genome[index:], k=k)
        sentences += chunks(_sentences, 20)
    return sentences

@click.command()
@click.option('--input_file', help='Input file in FASTA format')
@click.option('--kmer', default=100, help='kmer length')
@click.option('--output_file', help="Output file to write")
def main(input_file, kmer, output_file):
    ''' This script converts a FASTA file sequence into consecutive set of kmers '''
    records = []
    for record in SeqIO.parse(input_file, 'fasta'):
        records += genearte_genomes(genome=str(record.seq).upper(), k=kmer)
        break

    fo = open(output_file, 'a')

    for i in records:
        fo.write(' '.join(i)+'\n')


if __name__ == '__main__':
    main()
