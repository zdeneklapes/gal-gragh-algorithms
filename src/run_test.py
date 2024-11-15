import os
import subprocess
import glob

# Folder parameters
input_folder = "./autogen_datasets"
output_folder = "csv_data/raw"

os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist
#os.makedirs(output_exact_folder, exist_ok=True)  # Create folder if it doesn't exist

# Try to delete preexisting files
csv_files = glob.glob(os.path.join(output_folder, "*.csv"))
for csv_file in csv_files:
	try:
		os.remove(csv_file)
	except Exception as e:
		print(e)

# Script parameters
iteration_modifier = 0.5
tolerance = 5

for filename in os.listdir(input_folder):
	if filename.endswith(".txt"):
		graph_path = os.path.join(input_folder, filename)

		command = [
			"python3", "./src/gal.py",
			"--graph_path", graph_path,
			"--csv_output", output_folder,
			"--iteration_modifier", str(iteration_modifier),
			"--tolerance", str(tolerance)
		]

		print(f"\nRunning: {' '.join(command)}\n")
		subprocess.run(command, check=True)