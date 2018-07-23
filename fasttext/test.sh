kmer=16
embedding_dim=100

for rep in `seq 1 10`;
do
    echo $rep
    for file in `ls ./PATRIC_Export_plasmids/`;
    do
        python ../../src/parse.py --input_file ./PATRIC_Export_plasmids/$file/$file.fna --kmer $kmer --output_file test.txt
    done
done

fasttext skipgram -input test.txt -output ../model/model-50e-500d -minn 11 -maxn 13 -thread 60 -epoch 50 -dim 500 -loss hs -lr 0.1 -minCount 1

fasttext skipgram -input test.txt -output ../model/model-10 -minn 11 -maxn 13 -thread 60 -epoch 10 -dim 100 -loss hs  -lr 0.1 -minCount 1
fasttext skipgram -input test.txt -output ../model/model-50 -minn 11 -maxn 13 -thread 60 -epoch 50 -dim 300 -loss hs  -lr 0.1 -minCount 1
fasttext skipgram -input test.txt -output ../model/model-100 -minn 11 -maxn 13 -thread 60 -epoch 100 -dim 300 -loss hs -lr 0.1 -minCount 1


# generate test reads
for file in `ls ./PATRIC_Export_plasmids/`;
do
    echo $file
    python ../../src/random_reads.py --input-file ./PATRIC_Export_plasmids/$file/$file.fna --length 1000 --reads 500 --mutate 10
done

# make one big file
cat ./PATRIC_Export_plasmids/*/*.fna.reads > reads.fasta

# now get wordvectors from sequences
rm vectors.h5
python ../../src/seq2vec.py --input-file reads.fasta --model-file ../model/model-100.bin --kmer $kmer --output-file vectors.h5 --embedding-size 100

# plot
python ../../src/vec2dist.py


