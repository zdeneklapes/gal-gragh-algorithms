# Makefile for Docker Nginx PHP Composer MySQL

install:
	rm -rf .venv
	python3.11 -m venv .venv
	bash -c "source .venv/bin/activate && pip install -r requirements.txt"

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

pack:
	rm -f xlapes02_xdvora3r.zip
	zip -r xlapes02_xdvora3r.zip src/ Makefile README.md requirements.txt .python-version dokumentace.pdf

run_test:
	python3 src/run_test.py --iteration_modifier 0.5 --tolerance 5 --batch_name "batch13"

auto_gen:
	python3 src/auto_gen.py --nodes 100 100 --probability 0.7 --max_weight 100 --seeds 1000 1007 --batch_name "batch13"

run_algo:
	python3 ./src/gal.py --graph_path ./autogen_datasets/batch13/graph-nodes100-seed1000-prob0.7-weight100.txt --csv_output csv_data/raw/batch13 --iteration_modifier 0.5 --tolerance 5

