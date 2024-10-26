# GAL - Gragh Algorithms Course project

## Topic: Comparison - exact and approximation algorithm for the Floyd-Warshall algorithm

### Examples:

#### Go to docker

```bash
make run
```

Following commands were tested in the docker container, but should work on your local machine as well if you have `Python 3.11.9` and `uv` installed:

#### Generate data

```bash
# Generate one graph
uv run python3 src/dataset_generator.py --nodes 3 --probability 0.4 --max_weight 30 --seed 42 --output_txt datasets/graph-1.txt --output_png datasets/graph-1.png --visualize

# Generate whole dataset of graphs (fish shell)
for i in (seq 2 100); uv run python3 src/dataset_generator.py --nodes $i --probability 0.5 --max_weight 30 --seed 42 --output_txt datasets/graph-$i.txt --output_png datasets/graph-$i.png --visualize; end
```

#### Run algorithm

```bash
uv run python3 src/gal.py
```


