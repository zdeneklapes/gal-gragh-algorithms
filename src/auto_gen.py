# RUN:
"""
python3 src/auto_gen.py --nodes 200 221 --probability 0.4 --max_weight 100 --seeds 100 107 --batch_name "batch1"; \
python3 src/auto_gen.py --nodes 300 321 --probability 0.3 --max_weight 200 --seeds 200 207 --batch_name "batch5"; \

# python3 src/auto_gen.py --nodes 300 321 --probability 0.5 --max_weight 200 --seeds 200 207 --batch_name "batch3"; \
# python3 src/auto_gen.py --nodes 300 321 --probability 0.7 --max_weight 200 --seeds 200 207 --batch_name "batch4"

python3 src/auto_gen.py --nodes 1000 1003 --probability 0.4 --max_weight 100 --seeds 500 502 --batch_name "batch7"
"""

import glob
import os
import subprocess
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

parser = ArgumentParser()
parser.add_argument("--nodes", type=int, nargs="+", help="Specifies the amount of nodes in graph to be generated")
parser.add_argument("--probability", type=float, help="Specifies the probability of an edge being created")
parser.add_argument("--max_weight", type=int, help="Specifies the maximum weight of an edge")
parser.add_argument("--seeds", type=int, nargs="+", help="Specifies the range of seeds to be used")
parser.add_argument("--batch_name", type=str, help="Specifies the name of the batch")
args = parser.parse_args()

nodes = args.nodes
probability = args.probability
max_weight = args.max_weight
seeds = args.seeds
batch_name = args.batch_name

# Folder parameters
output_folder = os.path.join("./autogen_datasets",batch_name)
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

print(f"Generating datasets with the following parameters:")
print(f"Nodes: {nodes}")
print(f"Probability: {probability}")
print(f"Max weight: {max_weight}")
print(f"Seeds: {seeds}")

# Try to delete preexisting files
txt_files = glob.glob(os.path.join(output_folder, "*.txt"))
if txt_files:
	for txt_file in txt_files:
		os.remove(txt_file)

def generate_graph(nodes, seed, probability, max_weight, output_folder):
	# Define output paths
	output_txt = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-prob{probability}-weight{max_weight}.txt")
	# output_png = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-weight{max_weight}.png")

	# Command to be run
	command = [
		"python3", "src/dataset_generator.py",
		"--nodes", str(nodes),
		"--probability", str(probability),
		"--max_weight", str(max_weight),
		"--seed", str(seed),
		"--output_txt", output_txt,
		# "--output_png", output_png,
	]

	# Run the command
	print(f"\nRunning: {' '.join(command)}\n")
	subprocess.run(command, check=True)

MAX_WORKERS = os.cpu_count()

# Use ThreadPoolExecutor for parallelism
with ThreadPoolExecutor(MAX_WORKERS) as executor:
	futures = [
		executor.submit(generate_graph, nodes, seed, probability, max_weight, output_folder)
		for nodes in range(nodes[0], nodes[1])
		for seed in range(seeds[0], seeds[1])
	]

	# Wait for all futures to complete
	for future in futures:
		try:
			future.result()  # This will raise an exception if the task failed
		except Exception as e:
			print(f"Error occurred: {e}")
			# abort
			break


# for nodes in range(nodes[0], nodes[1]):
# 	for seed in range(seeds[0], seeds[1]):
# 		# output_txt = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-weight{max_weight}.txt")
# 		# output_png = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-weight{max_weight}.png")
# 		output_txt = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-prob{probability}-weight{max_weight}.txt")
# 		# output_png = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-{probability}-weight{max_weight}.png")
#
#
# 		# Command to be run
# 		command = [
# 			"python3", "src/dataset_generator.py",
# 			"--nodes", str(nodes),
# 			"--probability", str(probability),
# 			"--max_weight", str(max_weight),
# 			"--seed", str(seed),
# 			"--output_txt", output_txt,
# 			# "--output_png", output_png,
# 		]
#
# 		# Run the gen
# 		print(f"\nRunning: {' '.join(command)}\n")
# 		subprocess.run(command, check=True)
#

print(f"\nAll datasets were generated into {output_folder}")
