import re
from Bio import SeqIO
import numpy as np
import os
import h5py


def split_genome(genome="ATCGATATACCA", k=3):
    return re.findall('.'*k, genome)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def genearte_genomes(genome='ATCGATATACCA', k=3, words=50):
    sentences = []
    for index in range(0, k):
        _genome = genome[index:]
        _sentence = split_genome(genome=_genome, k=k)
        _fraction = int(len(genome) / k) - len(_sentence)

        if _fraction > 0:
            _sentence.append('')

        sentences.append(np.array(_sentence, dtype="U"))

    return np.array(sentences)

def genome_to_doc(input_file="", kmer=16, label="", index_file=""):

    f5 = h5py.File(index_file, 'a')

    records = []

    for record in SeqIO.parse(input_file, 'fasta'):
        _genome = str(record.seq).upper()
        _kmer_count = int(len(_genome) / kmer)

        # print(record.id)

        try:
            group = f5.create_group(record.id)
        except:
            group = f5[record.id]

        try:
            dt = h5py.special_dtype(vlen=str)
            dataset = group.create_dataset('sequences', (1, _kmer_count), dtype=dt, chunks=(1, _kmer_count), maxshape=(None, _kmer_count))
            labels = group.create_dataset('labels', (1, ), dtype=dt, chunks=(1, ), maxshape=(None, ))
        except:
            dataset = f5[record.id]['sequences']
            labels = f5[record.id]['labels']

        for ix, i in enumerate(genearte_genomes(genome=_genome, k=kmer)):

            if ix == 0:
                dataset[0] = i
                labels[0] = label
            else:
                dataset.resize(dataset.shape[0] + 1, axis=0)
                dataset[-1] = i
                labels.resize(labels.shape[0]+1, axis=0)
                labels[-1] = label