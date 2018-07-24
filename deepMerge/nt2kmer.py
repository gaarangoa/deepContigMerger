from tqdm import tqdm
from deepMerge import parse
from multiprocessing import Pool
import h5py
from functools import partial

class NToKmer():
    def __init__(self, genome_list="", kmer=31, model_filename=""):
        self.genome_list = genome_list
        self.kmer = kmer
        self.model_filename = model_filename

    def parse_input(self, line):
        fasta_file, label = line.split()
        genomes = parse.genome_to_doc(input_file=fasta_file, kmer=self.kmer, label=label)

        return genomes

    def index(self):

        ''' Split sequences into consecutive kmers and store it as hdf5 objects.'''

        f5 = h5py.File(self.model_filename + '.h5', 'a')
        _input_file = open(self.genome_list, 'r')

        pool = Pool(processes=2)
        for genome in pool.imap(self.parse_input, _input_file, chunksize=2):
            parse.store_genome_h5(records=genome, f5=f5)

        pool.close()
