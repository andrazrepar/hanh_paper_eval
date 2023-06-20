from conllu import parse_incr
import os


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


def compute_metrics(true_positives, false_positives, gs):
    # Compute the precision, recall, and F-score
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / len(gs)  # assuming all gs forms should be recognized
    fscore = (
        2 * (precision * recall) / (precision + recall)
        if precision + recall != 0
        else 0
    )

    return precision, recall, fscore


c = 0

gs = load_gs("gs/jez.terms")

true_positives = 0
false_positives = 0

true_positives_after_filtering = 0
false_positives_after_filtering = 0

candidate_count = 0
with open("conll/ann_bim_ling.txt", "r") as f:
    for sent in parse_incr(f):
        candidate_count += 1
        form = " ".join([word["form"] for word in sent])

        if form in gs:
            true_positives += 1
        else:
            false_positives += 1

        if filter_ngrams(sent):
            if form in gs:
                true_positives_after_filtering += 1

            else:
                false_positives_after_filtering += 1


precision, recall, fscore = compute_metrics(true_positives, false_positives, gs)

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F-score: {fscore}")

precision, recall, fscore = compute_metrics(
    true_positives_after_filtering, false_positives_after_filtering, gs
)

print(f"Precision after filtering: {precision}")
print(f"Recall after filtering: {recall}")
print(f"F-score after filtering: {fscore}")
