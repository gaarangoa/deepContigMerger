from tqdm import tqdm
from deepMerge import parse
from multiprocessing import Pool
import h5py
from functools import partial
import time

class NToKmer():
    def __init__(self, genome_list="", kmer=31, output_dir="", proc=8, batch=10):
        self.genome_list = genome_list
        self.kmer = kmer
        self.output_dir = output_dir
        self.proc = proc
        self.batch = batch

    def parse_input(self, line):
        fasta_file, label = line.split()
        f5 = h5py.File(self.output_dir+'/'+label + '.h5', 'a')

        genomes = parse.genome_to_doc(input_file=fasta_file, kmer=self.kmer, label=label)
        parse.store_genome_h5(records=genomes, f5=f5)

        return True


    def index(self):

        ''' Split sequences into consecutive kmers and store it as hdf5 objects.'''

        _input_file = open(self.genome_list, 'r')

        pool = Pool(processes=self.proc)
        for i in pool.imap_unordered(self.parse_input, _input_file, chunksize=self.batch):
            assert(i)

        pool.close()
