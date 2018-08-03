from deepMerge import parse
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import h5py
from tqdm import tqdm
from Bio import SeqIO
# from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
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
        #
        f5 = h5py.File(self.output_dir + '/' + self.input_file.split('/')[-1] + '.h5', 'a')

        try:
            gr = f5.create_group(record.id) # this is the fasta file header id
        except:
            return False

        matrix = []
        index = []
        document = []
        for i in range(0, len(record.seq)-self.kmer, self.kmer):
            _fragment = record.seq[i:i + self.kmer].upper()
            document.append(str(_fragment))
            try:
                index.append(i)
                matrix.append(self.model.wv[ [_fragment] ])
            except Exception as e:
                pass

        # infer the word vector for the whole document
        # TODO: need to test if using few kmers from the total is maybe a good option, so it would reduce the complexity of the computation?
        vector = self.model.infer_vector(document)

        matrix = np.array(matrix)
        index = np.array(index)

        gr.create_dataset('info', data=np.string_(record.description))

        if matrix.shape[0] > 0:
            gr.create_dataset('word_vectors', data=matrix)
            gr.create_dataset('index', data=index)

        if vector.shape[0] > 0:
            gr.create_dataset('document_vector', data=vector)

        if not f5[record.id]:
            del f5[record.id]

        return True

    def index(self):

        fasta_file = SeqIO.parse(self.input_file, 'fasta')

        print('loading model ...')
        self.model = Doc2Vec.load(self.model_file)

        print('processing input file ...')

        pool = ThreadPool(processes=self.proc)
        assert(pool.map(self.genome_to_doc, fasta_file))

        pool.close()
