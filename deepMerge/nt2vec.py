from deepMerge import parse
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import h5py
from tqdm import tqdm

class LabeledFastaGenome(object):
    def __init__(self, doc_list='', doc_dir=''):
        self.doc_list = doc_list
        self.doc_dir = doc_dir
    #

    def __iter__(self):
        for doc in self.doc_list:

            f5 = h5py.File(self.doc_dir + '/' + doc)

            fasta_header = [i for i in f5.keys()][0]
            words = f5[fasta_header]['sequences']
            labels = f5[fasta_header]['labels']

            for ix, i in enumerate(words):
                try:
                    assert (i.shape)
                    yield TaggedDocument(words=i, tags=[labels[ix]])
                except:
                    print('Error in: ', doc)

def build(genome_list={}, max_epochs=10, vec_size=300, alpha=0.025, model_filename="./genome.model", cores=1):
    '''

    genome_list is a list where each entry corresponds to an *.h5 file.

    '''

    # iterator class
    it = LabeledFastaGenome(
        doc_list=genome_list['doc_list'],
        doc_dir=genome_list['doc_dir'],
    )


    # check if the model exists
    if os.path.isfile(model_filename):
        print('Model exists, it will retrain the model with the new entries!')
        print("Loading model ...")
        model = Doc2Vec.load(model_filename)
        print("Building.. \nUpdating model with new entries ...")
        model.build_vocab(it, update=True)
    else:
        print("Building model ...")
        model = Doc2Vec(vector_size=vec_size,
                        alpha=alpha,
                        min_alpha=0.025,
                        min_count=1,
                        dm=1,
                        epochs=max_epochs,
                        cores=cores
        )
        model.build_vocab(it)
    #

    print("Training model ...")
    for epoch in tqdm(range(max_epochs)):
        # print('iteration {0}'.format(epoch))
        model.train(
            it,
            total_examples=model.corpus_count,
            epochs=model.epochs
        )
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha
    #

    print('total kmers %s' % (len(model.wv.vocab.items())))

    model.save(model_filename)
    print("Model Saved")
