import glob
import pandas as pd
import numpy as np


def computeTermEvalMetrics(extracted_terms, gold_df):
    extracted_terms = set([item.lower() for item in extracted_terms])
    gold_set = set(gold_df)
    true_pos = extracted_terms.intersection(gold_set)
    print(len(true_pos))
    print(len(extracted_terms))
    recall = round(len(true_pos) * 100 / len(gold_set), 1) if len(gold_set) > 0 else 0
    precision = (
        round(len(true_pos) * 100 / len(extracted_terms), 1)
        if len(extracted_terms) > 0
        else 0
    )
    fscore = (
        round(2 * (precision * recall) / (precision + recall), 1)
        if precision > 0 or recall > 0
        else 0
    )
    print(
        str(len(extracted_terms))
        + " & "
        + str(len(gold_set))
        + " & "
        + str(len(true_pos))
    )
    print(str(precision) + " & " + str(recall) + " & " + str(fscore))


if __name__ == "__main__":
    preds = [
        eval(x)
        for x in pd.read_csv("candidates/ann_bim_kem.txt", sep="\t", header=None)[0]
    ][0][0]
    gts = pd.read_csv(
        "gs/kem.terms", header=None, delimiter="\t", names=["Term", "Label"]
    )["Term"]
    computeTermEvalMetrics(preds, gts)
