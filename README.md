# GAL - Gragh Algorithms Course project

## Topic: Comparison - exact and approximation algorithm for the Floyd-Warshall algorithm


## Instalation

```bash
make install
source venv/bin/activate
```

## Generate data

```bash
python3 src/auto_gen.py --nodes 1000 1002 --probability 0.45 --max_weight 300 --seeds 500 502 --batch_name "batch7"
```

## Run

```bash
python3 src/run_test.py --iteration_modifier 0.5 --tolerance 15 --batch_name batch7
```




