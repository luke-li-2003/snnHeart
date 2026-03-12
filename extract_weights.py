import torch
import csv
import math

pth_path = "./cps/net_premier.pth"
output_csv = "model_weights_1024.csv"

state_dict = torch.load(pth_path, map_location="cpu")

with open(output_csv, "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerow(["layer", "input_index", "output_index", "weight"])

	for name, tensor in state_dict.items():

		# Only process linear layer weights
		if tensor.ndim == 2 and "weight" in name:
			
			out_features, in_features = tensor.shape

			print("processing %s %dx%d" % (name, out_features, in_features))

			for j in range(out_features):	  # output neuron
				for i in range(in_features):   # input neuron

					weight = tensor[j, i].item()
					weight = weight * 1024
					weight = round(weight)

					writer.writerow([
						name,
						i,
						j,
						weight
					])

print("Export complete.")
