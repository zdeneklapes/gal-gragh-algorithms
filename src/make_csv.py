import os
import subprocess
import csv

input_folder = "./csv_data/raw"
output_file = "./csv_data/data.csv"

csv_header = ["Name", "Exact algorithm time", "Approximation algorithm time", "Accuracy", "Tolerance", "Iteration modifier"]

with open(output_file, mode='w', newline='') as output_csv:
	writer = csv.writer(output_csv)
	writer.writerow(csv_header)

	for filename in os.listdir(input_folder):
		if filename.endswith(".csv"):
			file_path = os.path.join(input_folder, filename)

			with open(file_path, mode='r', newline='') as input_csv:
				reader = csv.reader(input_csv)
				for row in reader:
					writer.writerow(row)