import nt2vec
genome_list = [
    {
        "fasta_file": "../../data/dataset/PATRIC_Export_plasmids/1280.15015/1280.15015.fna",
        "document_label": 1280.15015,
    },
    {
        "fasta_file": "../../data/dataset/PATRIC_Export_plasmids/562.24630/562.24630.fna",
        "document_label": 562.24630,
    }
]

nt2vec.build(genome_list=genome_list, model_filename="../../test/plasmids.bin")
