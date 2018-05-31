import numpy as np
import os
import re
import click
from fastText import load_model
from Bio import SeqIO
from tqdm import tqdm
import h5py


def split_sequence(sequence="ATCGATATACCA", k=31):
    return re.findall('.'*k, sequence)

@click.command()
@click.option('--input-file', help='Input file in FASTA format.')
@click.option('--model-file', help='File with the word vector model.')
@click.option('--kmer', default=31, help='k-mer length.')
@click.option('--embedding-size', default=100, help='length of the word embedding vectors. (default 100)')
@click.option('--output-file', help='number of random reads to produce.')
def main(input_file, model_file, kmer, output_file, embedding_size):
    ''' Convert a sequence into its word vector representation, one vector per sequence '''
    fo = h5py.File(output_file, 'a')
    data_yn = fo.create_dataset( 'y_n', (1, embedding_size), chunks=(1, embedding_size), maxshape=(None, embedding_size))
    index_yn = fo.create_dataset( 'index', (1, ), dtype='S100', chunks=(1, ), maxshape=(None, ) )

    print('loading word to vector model ...')
    f = load_model(model_file)

    print('processing input reads ...')
    _first = True
    for record in tqdm(SeqIO.parse(input_file, 'fasta')):
        _seq = str(record.seq).upper()
        _seqs = split_sequence(sequence=_seq, k=31)

        numerical_sequence = [f.get_word_vector(_seqs[0])]
        for _iseq in _seqs[1:]:
            numerical_sequence = np.append( numerical_sequence, [f.get_sentence_vector(_iseq)], axis=0)

        y_i = np.mean(numerical_sequence, axis=0)

        if _first:
            data_yn[0] = y_i
            index_yn[0] = record.id.encode('utf8')
            _first = False
        else:
            data_index = data_yn.shape[0] + 1
            data_yn.resize(data_index, axis=0)
            data_yn[-1] = y_i
            index_yn.resize(data_index, axis=0)
            index_yn[-1] = record.id.encode('utf8')

    print('there are a total of '+str(len(data_yn))+' reads in the input file.')

    # for item in y_n:
        # print(item)

if __name__ == '__main__':
    main()
