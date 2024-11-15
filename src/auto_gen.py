import os
import subprocess
import glob

# Folder parameters
output_folder = "./autogen_datasets"
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

# Script parameters
# Specifies the amount of nodes in graph to be generated
nodes = [150, 160]
probability = 0.4
max_weight = 30
# Specifies the amount of seeds per graph (generates different vertices)
seeds = [40, 52]

# Try to delete preexisting files
csv_files = glob.glob(os.path.join(output_folder, "*.csv"))
for csv_file in csv_files:
	try:
		os.remove(csv_file)
	except Exception as e:
		print(e)


for nodes in range(nodes[0], nodes[1]):
	for seed in range(seeds[0], seeds[1]):
		output_txt = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-weight{max_weight}.txt")
		output_png = os.path.join(output_folder, f"graph-nodes{nodes}-seed{seed}-weight{max_weight}.png")
		
		# Command to be run
		command = [
			"python3", "src/dataset_generator.py",
			"--nodes", str(nodes),
			"--probability", str(probability),
			"--max_weight", str(max_weight),
			"--seed", str(seed),
			"--output_txt", output_txt,
			"--output_png", output_png,
		]
		
		# Run the gen
		print(f"\nRunning: {' '.join(command)}\n")
		subprocess.run(command, check=True)


print(f"\nAll datasets were generated into {output_folder}")
