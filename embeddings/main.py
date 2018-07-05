import nt2vec
import click


@click.command()
@click.option('--input-file', default='', help='tabular file where the first field is the fasta file and the second field the label of the fasta file')
@click.option('--output-file', default='', help='output file to write the model')
def process(input_file, output_file):
    if not input_file:
        print('\nUsage: No input file, type --help\n')
        exit()
    nt2vec.build(
        genome_list=input_file,
        model_filename=output_file,
        max_epochs=1
    )
