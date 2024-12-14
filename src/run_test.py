# RUN:
"""
python3 src/run_test.py --iteration_modifier 0.3 --tolerance 5 --batch_name batch1; \
python3 src/run_test.py --iteration_modifier 0.5 --tolerance 5 --batch_name batch1; \
python3 src/run_test.py --iteration_modifier 0.7 --tolerance 5 --batch_name batch1; \
python3 src/run_test.py --iteration_modifier 0.3 --tolerance 10 --batch_name batch5; \
python3 src/run_test.py --iteration_modifier 0.5 --tolerance 10 --batch_name batch5; \
python3 src/run_test.py --iteration_modifier 0.7 --tolerance 10 --batch_name batch5;
"""

import glob
import os
import subprocess
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

args = ArgumentParser()
args.add_argument("--iteration_modifier", type=float, help="Specifies the iteration modifier for the approximate algorithm")
args.add_argument("--tolerance", type=int, help="Specifies the tolerance for the approximate algorithm")
args.add_argument("--batch_name", type=str, help="Specifies the name of the batch")

iteration_modifier = args.parse_args().iteration_modifier
tolerance = args.parse_args().tolerance
batch_name = args.parse_args().batch_name

# Folder parameters
input_folder = os.path.join("./autogen_datasets", batch_name)
output_folder = os.path.join("csv_data/raw", batch_name)

os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist
#os.makedirs(output_exact_folder, exist_ok=True)  # Create folder if it doesn't exist


# # Try to delete preexisting files
# csv_files = glob.glob(os.path.join(output_folder, "*.csv"))
# for csv_file in csv_files:
# 	try:
# 		os.remove(csv_file)
# 	except Exception as e:
# 		print(e)

def process_file(index, filename, input_folder, output_folder, iteration_modifier, tolerance):
	if filename.endswith(".txt"):
		graph_path = os.path.join(input_folder, filename)

		command = [
			"python3", "./src/gal.py",
			"--graph_path", graph_path,
			"--csv_output", output_folder,
			"--iteration_modifier", str(iteration_modifier),
			"--tolerance", str(tolerance)
		]

		print(f"\nRunning [{index}/{len(os.listdir(input_folder))}]: {' '.join(command)}\n")
		subprocess.run(command, check=True)

MAX_WORKERS = os.cpu_count()

# SINGLE-THREADING (just (un)comment)
# for index, filename in enumerate(os.listdir(input_folder)):
# 	if filename.endswith(".txt"):
# 		graph_path = os.path.join(input_folder, filename)
#
# 	process_file(index, filename, input_folder, output_folder, iteration_modifier, tolerance)


# MULTI-THREADING (just (un)comment)
with ThreadPoolExecutor(MAX_WORKERS) as executor:
	futures = [
		executor.submit(process_file, index, filename, input_folder, output_folder, iteration_modifier, tolerance)
		for index, filename in enumerate(os.listdir(input_folder)) if filename.endswith(".txt")
	]

	for future in futures:
		try:
			future.result()  # Ensures any exception in the task is raised here
		except Exception as e:
			print(f"Error occurred: {e}")
