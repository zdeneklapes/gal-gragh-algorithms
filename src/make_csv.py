# RUN:
"""
python3 src/make_csv.py --batches batch1 batch3
"""

import os
import subprocess
import csv
from argparse import ArgumentParser

args = ArgumentParser()
args.add_argument("--batches", type=str, nargs="+", help="Specifies the name of the batches to be processed")

batches = args.parse_args().batches

input_folder = "./csv_data/raw"
output_file = "./csv_data/data.csv"

csv_header = ["Name", "Exact algorithm time", "Approximation algorithm time", "Accuracy", "Tolerance", "Iteration modifier"]

with open(output_file, mode='w', newline='') as output_csv:
	writer = csv.writer(output_csv)
	writer.writerow(csv_header)

	for batch in batches:
		for filename in os.listdir(os.path.join(input_folder, batch)):
			if filename.endswith(".csv"):
				file_path = os.path.join(input_folder, batch, filename)

				with open(file_path, mode='r', newline='') as input_csv:
					reader = csv.reader(input_csv)
					for row in reader:
						writer.writerow(row)
