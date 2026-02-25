import torch
import csv
import numpy as np

# -------- CONFIG --------
pth_path = "./cps/net_premier.pth"   # change to your file
output_csv = "model_weights.csv"
# ------------------------

# Load state_dict (CPU-safe)
state_dict = torch.load(pth_path, map_location="cpu")

print(f"Loaded {len(state_dict)} layers")

with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)

    # Header
    writer.writerow(["layer_name", "weight_index", "value"])

    # Iterate through layers
    for layer_name, tensor in state_dict.items():
        print(f"Processing: {layer_name}  shape={tuple(tensor.shape)}")

        # Convert tensor → numpy → flatten
        values = tensor.detach().cpu().numpy().flatten()
        values = values * 16
        values = np.round(values)

        # Write each weight
        for idx, val in enumerate(values):
            writer.writerow([layer_name, idx, float(val)])

print(f"\nWeights exported to: {output_csv}")
