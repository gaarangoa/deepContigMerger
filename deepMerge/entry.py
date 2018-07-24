import click
from deepMerge.train import train
from deepMerge.quant import quant
from deepMerge.index import index

@click.group()
def cli():
    '''

        DeepMerge builds word vector representations for genomic sequences (nucleotides). It consists of two main
        executable files:

            deepMerge index: to split sequences as kmers.

            deepMerge train: to build the word vector representation.

            deepMerge quant: to represent a sequence into its word vectors.

    '''
    pass


cli.add_command(index)
cli.add_command(train)
cli.add_command(quant)
