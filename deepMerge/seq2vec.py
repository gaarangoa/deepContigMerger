from deepMerge import parse
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import h5py
from tqdm import tqdm
from Bio import SeqIO
from multiprocessing import Pool
import numpy as np
import time


class Quant():
    def __init__(self, input_file='', model_file='', output_dir='', compress='', kmer=31, proc=1, chunk=10):
        self.input_file = input_file
        self.model_file = model_file
        self.output_dir = output_dir
        self.compress = compress
        self.kmer = kmer
        self.proc = proc
        self.chunk = chunk

    def fetch_wv(self, sentence):
        data = []
        for i in sentence:
            try:
                data.append(self.model.wv[i])
            except Exception as e:
                pass
        return data

    def genome_to_doc(self, record):

        matrix = []
        for i in range(0, len(record.seq)-self.kmer, self.kmer):
            _fragment = [record.seq[i:i + self.kmer].upper()]

            try:
                matrix.append(self.model.wv[_fragment])
            except Exception as e:
                print(e)

        matrix = np.array(matrix)

        f5 = h5py.File(self.output_dir + '/' + record.id + '.h5')
        f5.create_dataset(record.id, data=matrix)

        return True

    def index(self):

        fasta_file = SeqIO.parse(self.input_file, 'fasta')

        print('loading model ...')
        self.model = Doc2Vec.load(self.model_file)

        print('processing input file ...')

        x = [self.genome_to_doc(i) for i in fasta_file]

        # pool = Pool(processes=self.proc)

        # for i in pool.imap_unordered(self.genome_to_doc, fasta_file, chunksize=self.chunk):
        #     assert(i)

        # pool.close()
