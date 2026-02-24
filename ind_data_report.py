#!/usr/bin/env python3
"""
report_mitbih_labels.py

Given a folder containing WFDB records (e.g. MIT-BIH),
report annotation labels contained in each record.
"""

import os
import argparse
import wfdb
from collections import Counter, defaultdict


# ------------------------------------------------------------
# Find records in directory
# ------------------------------------------------------------
def find_records(folder):
    records = []
    for f in os.listdir(folder):
        if f.endswith(".hea"):
            records.append(os.path.splitext(f)[0])
    return sorted(records)


# ------------------------------------------------------------
# Analyze labels
# ------------------------------------------------------------
def analyze_records(folder):
    records = find_records(folder)

    if not records:
        print("No WFDB records (.hea files) found.")
        return

    global_counts = Counter()
    per_record_labels = {}

    print(f"Found {len(records)} records\n")

    for rec in records:
        record_path = os.path.join(folder, rec)

        try:
            ann = wfdb.rdann(record_path, "atr")
        except Exception as e:
            print(f"Skipping {rec}: {e}")
            continue

        labels = ann.symbol
        counts = Counter(labels)

        per_record_labels[rec] = counts
        global_counts.update(counts)

    # --------------------------------------------------------
    # Print per-record report
    # --------------------------------------------------------
    print("=== Labels per record ===\n")

    for rec, counts in per_record_labels.items():
        label_list = ", ".join(sorted(counts.keys()))
        print(f"{rec}: {label_list}")

    # --------------------------------------------------------
    # Detailed counts
    # --------------------------------------------------------
    print("\n=== Counts per record ===\n")

    for rec, counts in per_record_labels.items():
        print(f"{rec}")
        for label, n in sorted(counts.items()):
            print(f"  {label:>3} : {n}")
        print()

    # --------------------------------------------------------
    # Global statistics
    # --------------------------------------------------------
    print("\n=== Global label distribution ===\n")

    total = sum(global_counts.values())
    for label, n in sorted(global_counts.items()):
        pct = 100 * n / total
        print(f"{label:>3} : {n:7d} ({pct:5.2f}%)")

    print(f"\nTotal annotations: {total}")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Report annotation labels in WFDB records"
    )
    parser.add_argument(
        "folder",
        help="Folder containing WFDB records (MIT-BIH files)"
    )

    args = parser.parse_args()
    analyze_records(args.folder)


if __name__ == "__main__":
    main()
