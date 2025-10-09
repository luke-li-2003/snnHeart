# By ChatGPT

#!/usr/bin/env python3
"""
scan_headers.py

Scan all MIT-BIH .hea files and report distributions of key attributes:
- number of channels
- sampling frequency
- signal gains
- baselines
- lead names
"""

import os
import wfdb
import numpy as np
from collections import Counter

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
DATA_DIR = "raw_data"   # folder containing .hea files (e.g., downloaded by wfdb.dl_database)

# ------------------------------------------------------------
# COLLECT STATS
# ------------------------------------------------------------
fs_list = []
n_sig_list = []
gain_list = []
base_list = []
leads_list = []

for fname in sorted(os.listdir(DATA_DIR)):
    if not fname.endswith(".hea"):
        continue
    path = os.path.join(DATA_DIR, fname)
    rec_no_ext = os.path.splitext(path)[0]  # strip the ".hea"

    try:
        h = wfdb.rdheader(rec_no_ext)           # correct: wfdb will open rec_no_ext + ".hea"
    except Exception as e:
        print(f"Skipping {fname}: {e}")
        continue

    fs_list.append(h.fs)
    n_sig_list.append(h.n_sig)
    for s in h.sig_name:
        leads_list.append(s)

    # per-signal parameters
    for g, b in zip(h.adc_gain, h.baseline):
        gain_list.append(g)
        base_list.append(b)

# ------------------------------------------------------------
# SUMMARIZE RESULTS
# ------------------------------------------------------------
def summarize(name, values):
    if not values:
        return
    values = np.array(values)
    unique, counts = np.unique(values, return_counts=True)
    print(f"\n{name}:")
    for u, c in zip(unique, counts):
        print(f"  {u}: {c} files")
    print(f"  mean={values.mean():.2f}, std={values.std():.2f}, min={values.min()}, max={values.max()}")

print("📊 MIT-BIH Header Summary")
print("=========================")
summarize("Sampling frequency (Hz)", fs_list)
summarize("Number of signals (channels)", n_sig_list)
summarize("ADC gain (counts/mV)", gain_list)
summarize("Baseline (ADC offset)", base_list)

lead_counts = Counter(leads_list)
print("\nLead names:")
for lead, cnt in lead_counts.items():
    print(f"  {lead}: {cnt} occurrences")

print("\n✅ Done.")

