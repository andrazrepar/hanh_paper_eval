from conllu import parse_incr
import time
from sentence_indexer import indexer


def index_corpus(
    texts_dir,
    index_folder="index_folder",
    index_name="rsdo_idx",
):
    i = 0
    errors = 0
    sentences = []
    for file in texts_dir:
        with open(file, "r") as f:
            for sent in parse_incr(f):
                # prepare sentences for index

                sentences.append(
                    {
                        "content": " ".join([token["form"].lower() for token in sent]),
                        "raw": " ".join([token["form"] for token in sent]),
                        "labels": " ".join([token["upostag"] for token in sent]),
                    }
                )
                i += 1
        print("Finished indexing file:", file, "Errors:", errors)

    idx = indexer.create_index(index_folder, index_name, schema=indexer.hanh_schema)
    indexer.add_sentences_to_index(sentences, idx)
    return i


# /Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5bim/rsdo5bimcla.conllu
if __name__ == "__main__":
    texts_vet = [
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5vet/rsdo5vetucb.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5vet/rsdo5vetdis.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5vet/rsdo5vetcla.conllu",
    ]

    texts_kem = [
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5kem/rsdo5kemcla.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5kem/rsdo5kemucb.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5kem/rsdo5kemdis.conllu",
    ]

    texts_bim = [
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5bim/rsdo5bimucb.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5bim/rsdo5bimdis.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5bim/rsdo5bimcla.conllu",
    ]

    texts_jez = [
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5jez/rsdo5jezcla.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5jez/rsdo5jezucb.conllu",
        "/Users/andrazrepar/Koda/terminologija/luscilnik/term_predictor/corpora/rsdo5/rsdo5jez/rsdo5jezdis.conllu",
    ]

    domains = ["vet", "kem", "bim", "jez"]

    if False:
        for domain in domains:
            start = time.time()

            if domain == "vet":
                texts_dir = texts_vet

            if domain == "kem":
                texts_dir = texts_kem

            if domain == "bim":
                texts_dir = texts_bim

            if domain == "jez":
                texts_dir = texts_jez
            index_corpus(texts_dir, index_name=f"{domain}_idx")
            print("Finished in", time.time() - start, "seconds")

    term = "fe3"
    idx = indexer.read_index("index_folder", "kem_idx")
    print(idx.doc_count())
    sentences = indexer.query_labels(term, idx, limit=None)

    print(sentences)
    print(len(sentences))
