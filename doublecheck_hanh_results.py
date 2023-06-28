import csv, ast


def find_sequence_indices(lst):
    sequences = []
    sequence = []

    for i, item in enumerate(lst):
        if item == "B-T":
            # Start of a new sequence
            if sequence:  # Check if sequence is not empty
                sequences.append(sequence)
            sequence = [i]
        elif item == "T" and sequence:  # Check if we're inside a sequence
            # Continuation of a sequence
            sequence.append(i)
        else:  # End of a sequence or 'n'
            if sequence:  # Check if sequence is not empty
                sequences.append(sequence)
                sequence = []

    # Append the last sequence if it ended with 'T' or 'B-T'
    if sequence:
        sequences.append(sequence)

    return sequences


def load_gs(filepath):
    gs = []
    with open(filepath, "r") as f:
        for line in f:
            gs.append(line.strip().split("\t")[0])
    return gs


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


def evaluate_candidates(candidates, gs_path):
    c = 0

    gs = load_gs(gs_path)

    true_positives = 0
    false_positives = 0

    for candidate in candidates:
        if candidate in gs:
            true_positives += 1
        else:
            false_positives += 1

    print(true_positives, false_positives, len(gs), len(candidates))

    precision, recall, fscore = compute_metrics(true_positives, false_positives, gs)
    print(f"Precision: {round(precision,2)}")
    print(f"Recall: {round(recall,2)}")
    print(f"F-score: {round(fscore,2)}")


candidates_path = "corpora/repar_features/rsdo_16/test_bim/kem_vet_jez.csv"
gs_path = "/Users/andrazrepar/Koda/terminologija/hanh_paper_eval/gs/ling.terms"
candidates = []
# load csv in pandas
with open(candidates_path, "r") as f:
    reader = csv.reader(f)
    next(reader)
    data = list(reader)

    for line in data:
        try:
            labels = ast.literal_eval(line[1])
            words = ast.literal_eval(line[0])
            indices = find_sequence_indices(labels)
            for sequence in indices:
                if len(sequence) == 1:
                    print(words[sequence[0]])
                    candidates.append(words[sequence[0]].lower())
                else:
                    print(words[sequence[0] : sequence[-1] + 1])
                    candidates.append(
                        " ".join(words[sequence[0] : sequence[-1] + 1]).lower()
                    )
        except:
            print(line)


candidates = list(set(candidates))
evaluate_candidates(candidates, gs_path)
