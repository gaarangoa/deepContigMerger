import re
from Bio import SeqIO
import os

def split_genome(genome="ATCGATATACCA", k=3):
    return re.findall('.'*k, genome)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def genearte_genomes(genome='ATCGATATACCA', k=3, words=50):
    sentences=[]
    for index in range( 0, k ):
        sentences += split_genome(genome=genome[index:], k=k)
        # sentences += chunks(_sentences, words) # in this case I don't need to split the genomes in small sections
    return sentences

def genome_to_doc(input_file="", kmer=16):
    records = []
    for record in SeqIO.parse(input_file, 'fasta'):
        records += genearte_genomes(genome=str(record.seq).upper(), k=kmer)
    return records