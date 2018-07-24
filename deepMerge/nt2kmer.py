from tqdm import tqdm
from deepMerge import parse


class IndexGenome(object):
    def __init__(self, doc_list='', kmer=15, model_file=""):
        self.doc_list = doc_list
        self.k = kmer
        self.index_file = model_file+".h5"
    #

    def __iter__(self):
        for doc in open(self.doc_list):
            fasta_file, label = doc.split()
            # print(label)
            words = parse.genome_to_doc(input_file=fasta_file, kmer=self.k, label=label, index_file=self.index_file)
            yield dict(words=words, tags=[label])


def index(genome_list='', model_filename='', kmer=31):
    ''' Split sequences into consecutive kmers and store it as hdf5 objects.'''
    index_genome = IndexGenome(doc_list=genome_list, kmer=kmer, model_file=model_filename)
    for i in index_genome:
        assert(1)