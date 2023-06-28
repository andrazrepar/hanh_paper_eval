from conllu import parse_incr
import os, json
from sentence_indexer import indexer
import re
from string import punctuation


def find_phrase(sentence, phrase):
    words = sentence.split()
    phrase_words = phrase.split()
    phrase_length = len(phrase_words)

    for i in range(len(words) - phrase_length + 1):
        if words[i : i + phrase_length] == phrase_words:
            return i

    return -1  # Phrase not found in the sentence


def load_gs(filepath):
    gs = []
    with open(filepath, "r") as f:
        for line in f:
            gs.append(line.strip().split("\t")[0])
    return gs


def filter_ngrams(lst):
    pattern = [word["upostag"] for word in lst]

    form = [word["form"].lower() for word in lst]

    if len(pattern) > 1 and pattern[-1] not in [
        "NOUN",
        "PROPN",
    ]:  # patterns longer than 1 have to end with a noun or propn to be terms
        return False
    elif pattern[0] not in [
        "ADJ",
        "NOUN",
        "ADV",
        "PROPN",
    ]:  # patterns not starting with any of these are not terms
        # elif pattern[0] not in ['ADJ', 'NOUN']: # patterns not starting with any of these are not terms
        return False
    elif any(
        el in pattern
        for el in ["VERB", "AUX", "PART", "CCONJ", "PUNCT", "SYM", "X", "DET"]
    ):  # if pattern contains any of these, it is not a term
        return False
    elif len(pattern) == 1 and pattern[0] not in [
        "NOUN",
        "PROPN",
    ]:  # only nouns can be single word terms
        return False
    elif len(" ".join(form)) < 4:  # remove terms shorter than 4 characters
        return False
    elif any("," in word for word in form):  # to remove patterns such as this "10,70"
        return False
    elif any(
        "_" in word for word in form
    ):  # to remove patterns such as this "_ osnsu1 _" which results from lemmatizing this: r_OsV1_LD
        return False
    else:
        return True


def filter_ngrams2(pattern, form):
    if len(pattern) > 1 and pattern[-1] not in [
        "NOUN",
        "PROPN",
    ]:  # patterns longer than 1 have to end with a noun or propn to be terms
        return False
    elif pattern[0] not in [
        "ADJ",
        "NOUN",
        "ADV",
        "PROPN",
    ]:  # patterns not starting with any of these are not terms
        # elif pattern[0] not in ['ADJ', 'NOUN']: # patterns not starting with any of these are not terms
        return False
    elif any(
        el in pattern
        for el in ["VERB", "AUX", "PART", "CCONJ", "PUNCT", "SYM", "X", "DET"]
    ):  # if pattern contains any of these, it is not a term
        return False
    elif len(pattern) == 1 and pattern[0] not in [
        "NOUN",
        "PROPN",
    ]:  # only nouns can be single word terms
        return False
    elif len(" ".join(form)) < 4:  # remove terms shorter than 4 characters
        return False
    elif any("," in word for word in form):  # to remove patterns such as this "10,70"
        return False
    elif any(
        "_" in word for word in form
    ):  # to remove patterns such as this "_ osnsu1 _" which results from lemmatizing this: r_OsV1_LD
        return False
    else:
        return True


def compute_metrics(true_positives, false_positives, gs):
    # Compute the precision, recall, and F-score
    precision = true_positives * 100 / (true_positives + false_positives)
    recall = (
        true_positives * 100 / len(gs)
    )  # assuming all gs forms should be recognized
    fscore = (
        2 * (precision * recall) / (precision + recall)
        if precision + recall != 0
        else 0
    )

    return precision, recall, fscore


def evaluate_candidates(candidates_path, gs_path):
    c = 0

    gs = load_gs(gs_path)

    true_positives = 0
    false_positives = 0

    true_positives_after_filtering = 0
    false_positives_after_filtering = 0

    candidate_count = 0
    candidates = []

    with open(candidates_path, "r") as f:
        for sent in parse_incr(f):
            candidate_count += 1
            form = " ".join([word["form"].lower() for word in sent])
            if form not in candidates:
                candidates.append(form)

                if form in gs:
                    print(form)
                    true_positives += 1
                else:
                    false_positives += 1

                if filter_ngrams(sent):
                    if form in gs:
                        true_positives_after_filtering += 1

                    else:
                        false_positives_after_filtering += 1

    print(true_positives, false_positives, len(gs), len(candidates))

    precision, recall, fscore = compute_metrics(true_positives, false_positives, gs)
    print(candidates_path)
    print(f"Precision: {round(precision,2)}")
    print(f"Recall: {round(recall,2)}")
    print(f"F-score: {round(fscore,2)}")

    precision, recall, fscore = compute_metrics(
        true_positives_after_filtering, false_positives_after_filtering, gs
    )

    print(f"Precision after filtering: {round(precision,2)}")
    print(f"Recall after filtering: {round(recall,2)}")
    print(f"F-score after filtering: {round(fscore,2)}")
    print("\n\n")


for file in os.listdir("conll/rsdo"):
    # get gs

    if file == "ann_vet_bim.txt":
        gs_name = file.split(".")[0].split("_")[1]
        print(file, gs_name)

        evaluate_candidates(f"conll/rsdo/{file}", f"gs/{gs_name}.terms")
