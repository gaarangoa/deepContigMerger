import click
from deepMerge.train import train
from deepMerge.quant import quant

@click.group()
def cli():
    '''

        DeepMerge builds word vector representations for genomic sequences (nucleotides). It consists of two main
        executable files:
            deepMerge train: to build the word vector representation.
            deepMerge quant: to represent a sequence into its word vectors.

    '''
    pass


cli.add_command(train)
cli.add_command(quant)