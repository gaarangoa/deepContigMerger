import deepMerge.parse
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
from tqdm import tqdm


class LabeledFastaGenome(object):
    def __init__(self, doc_list='', kmer=15):
        self.doc_list = doc_list
        self.k = kmer
    #

    def __iter__(self):
        for doc in open(self.doc_list):
            fasta_file, label = doc.split()
            # print(label)
            words = parse.genome_to_doc(input_file=fasta_file, kmer=self.k)
            yield TaggedDocument(words=words, tags=[label])


def build(genome_list="", kmer=15, max_epochs=10, vec_size=300, alpha=0.025, model_filename="./genome.model"):
    it = LabeledFastaGenome(doc_list=genome_list, kmer=kmer)
    #
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
                        iter=10)
        model.build_vocab(it)
    #

    print("Training model ...")
    for epoch in tqdm(range(max_epochs)):
        # print('iteration {0}'.format(epoch))
        model.train(
            it,
            total_examples=model.corpus_count,
            epochs=model.iter
        )
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha
    #

    model.save(model_filename)
    print("Model Saved")
