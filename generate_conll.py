import json
import classla
import os
import stanza
from stanza.utils.conll import CoNLL


def load_candidates(filepath):
    return json.load(open(filepath, "r"))


def generate_conll(nlp, candidates):
    doc = nlp("\n".join(candidates[0]))
    return doc.to_conll()


def generate_conll_stanza(nlp, candidates):
    doc = nlp("\n".join(candidates[0]))
    return doc


def write_rsdo(candidate_file, nlp):
    conll = generate_conll(nlp, load_candidates(f"candidates/rsdo/{candidate_file}"))
    with open(f"conll/rsdo{candidate_file}", "w") as f:
        f.write(conll)


def write_acter(candidate_file, nlp, lang):
    candidates = load_candidates(f"candidates/acter/{lang}/{candidate_file}")
    print(len(candidates[0]))
    # doc = generate_conll_stanza(
    #    nlp, load_candidates(f"candidates/acter/{lang}/{candidate_file}")
    # )

    # CoNLL.write_doc2conll(doc, f"conll/acter/{lang}/{candidate_file}")


def process_rsdo():
    nlp = classla.Pipeline("sl", processors="tokenize,pos", tokenize_pretokenized=True)
    for file in os.listdir("candidates/rsdo"):
        print(file)
        write_rsdo(file, nlp)


def process_acter():
    lang = "en"
    # nlp = stanza.Pipeline(lang, processors="tokenize,pos", tokenize_pretokenized=True)
    nlp = False
    for file in os.listdir(f"candidates/acter/{lang}"):
        print(file)
        write_acter(file, nlp, lang)


process_acter()
