from deepMerge import nt2vec
import click

@click.command()
@click.option('--input-file', default='', help='tabular file where the first field is the fasta file and the second field the label of the fasta file')
@click.option('--output-file', default='', help='output file to write the model')
@click.option('--training-chunk', default=1000, help='Number of genomes used to train the model iteratively (default 1000).')
@click.option('--kmer-size', default=31, help='Decompose the genomes into k length mers (31 default)')
@click.option('--embedding-size', default=100, help='Length of embedding vector size (100 default)')
@click.option('--epochs', default=10, help='Number of training epochs (10 default)')
def train(input_file, output_file, training_chunk, kmer_size, embedding_size, epochs):
    '''
        Train a word vector model.

        This script generates iteratively word vectors for an input corupus of full size genomes (or any sequences).
        It decomposes the sequences into kmers and repeats using an sliding window of 1. Thus, there will be k versions of
        the same genome shifted by one nucleotide.

        Because large corpus would take long to compute the word vectors, we implemented a training-chunk of the input files. This means that the
        model will be created and updated iteratively. This approach can be risky as it can vanish the already computed weights. need more exploration.

        The output is the gensim model that can be used to compute the word vectors of any input sequence.
     '''
    if not input_file:
        print('\nUsage: No input file, type --help\n')
        exit()

    nt2vec.build(
        genome_list=input_file,
        model_filename=output_file,
        max_epochs=epochs,
        kmer=kmer_size,
        vec_size=embedding_size,
    )
