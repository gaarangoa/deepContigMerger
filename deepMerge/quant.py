from deepMerge.seq2vec import Quant
import click
import os


@click.command()
@click.option('--input-file', default='', help='fasta input file')
@click.option('--model-file', default='', help='model generated by train')
@click.option('--output-dir', default='', help='output directory to write the model')
@click.option('--compress', default=1, help='merge columns in the word vector matrix to reduce its size, by default there is no reduction (default: 1)')
@click.option('--kmer', default=31, help='kmer size (default: 31)')
@click.option('--proc', default=8, help='number of cores to use (default: all)')
@click.option('--chunk', default=10, help='chunk processed entries (default: 10)')
def quant(input_file, output_dir, model_file, compress, kmer, proc, chunk):
    '''

    Represent a sequence as word vectors.

    It takes as input a fasta file (contigs) and produces one hdf5 file as output for each entry in the fasta file.


    '''
    if not input_file:
        os.system('nuc2vec quant --help')
        exit()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    _quant = Quant(
        input_file=input_file,
        model_file=model_file,
        output_dir=output_dir,
        compress=compress,
        kmer=kmer,
        proc=proc,
        chunk=chunk
    )

    _quant.index()
