from deepMerge import nt2vec
from deepMerge.nt2kmer import NToKmer
import click

@click.command()
@click.option('--input-file', default='', help='tabular file where the first field is the fasta file and the second field the label of the fasta file')
@click.option('--output-file', default='', help='output file to write the model')
# @click.option('--training-chunk', default=1000, help='Number of genomes used to train the model iteratively (default 1000).')
@click.option('--kmer-size', default=31, help='Decompose the genomes into k length mers (31 default)')
# @click.option('--embedding-size', default=100, help='Length of embedding vector size (100 default)')
# @click.option('--epochs', default=10, help='Number of training epochs (10 default)')
def index(input_file, output_file, kmer_size):
    '''
        Transform sequences to kmers.

        This program splits the input sequences into "sentences" of kmers and store them into a hdf5 file. This input is used later to get the word vectors.
     '''
    if not input_file:
        print('\nUsage: No input file, type --help\n')
        exit()

    nt2kmer = NToKmer(
        genome_list=input_file,
        model_filename=output_file,
        kmer=kmer_size
    )

    nt2kmer.index()
