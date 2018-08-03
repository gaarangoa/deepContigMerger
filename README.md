# deepMerge


## Merging long contigs using sequence embeddings

<!-- In order to run this code you need to install: -->

    ls plasmids | awk -v fasta=$i '{ split($0, x, "_"); print "/Volumes/drive/projects/ARG/tmp/deepMerge/test/plasmids/"$0"\t"x[1]  }' > test.list

    nuc2vec index --input-file test.10.list --output-dir data/ --kmer-size 11 --proc 10 --batch 10
    nuc2vec train --input-dir ./data/ --output-file ./train/model --training-chunk 100 --embedding-size 512 --epochs 10 --cores 10
    nuc2vec quant --input-file ./plasmids/1001582.3_1.fasta --model-file ./train/model --output-dir ./wv --kmer 11 --proc 10




