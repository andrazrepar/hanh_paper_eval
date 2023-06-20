import json
import classla


def load_candidates(filepath):
    return json.load(open(filepath, "r"))


def generate_conll(nlp, candidates):
    doc = nlp("\n".join(candidates[0]))
    return doc.to_conll()


CANDIDATE_FILE = "ann_bim_ling.txt"

nlp = classla.Pipeline("sl", processors="tokenize,pos", tokenize_pretokenized=True)
conll = generate_conll(nlp, load_candidates(f"candidates/{CANDIDATE_FILE}"))

with open(f"conll/{CANDIDATE_FILE}", "w") as f:
    f.write(conll)
