"""
AuraSCM - Synthetic Training Data Generator
---------------------------------------------
Generates a labeled dataset of "merge events" with handcrafted features,
used to train the conflict-risk prediction model.

Features:
  - lines_changed        : number of lines changed in the function
  - functions_touched     : number of functions modified in the commit
  - dependency_depth      : how deep the call-graph impact ripples
  - signature_changed      : 1 if function signature changed, else 0
  - token_overlap_ratio    : similarity of old vs new function body (0-1)

Label:
  - risky_merge (1 = high conflict risk, 0 = safe merge)

NOTE: In a real product this data would come from mining actual Git
history (commit metadata + CI failure logs). For this course project we
generate a synthetic-but-realistic dataset so the ML pipeline is genuine
and reproducible.
"""

import random
import csv

random.seed(42)

ROWS = 400


def generate_row():
    lines_changed = random.randint(1, 60)
    functions_touched = random.randint(1, 6)
    dependency_depth = random.randint(0, 5)
    signature_changed = random.choice([0, 0, 0, 1])
    token_overlap_ratio = round(random.uniform(0.1, 1.0), 2)

    # Ground-truth rule used ONLY to label synthetic data (the model
    # itself never sees this rule -- it has to learn the pattern from
    # the features above).
    risk_score = (
        (lines_changed / 60) * 0.25
        + (functions_touched / 6) * 0.15
        + (dependency_depth / 5) * 0.25
        + signature_changed * 0.25
        + (1 - token_overlap_ratio) * 0.10
    )
    risky_merge = 1 if risk_score > 0.5 else 0

    return [lines_changed, functions_touched, dependency_depth,
            signature_changed, token_overlap_ratio, risky_merge]


def main():
    header = ["lines_changed", "functions_touched", "dependency_depth",
              "signature_changed", "token_overlap_ratio", "risky_merge"]
    with open("data/merge_history.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for _ in range(ROWS):
            writer.writerow(generate_row())
    print(f"Wrote {ROWS} rows to data/merge_history.csv")


if __name__ == "__main__":
    main()
