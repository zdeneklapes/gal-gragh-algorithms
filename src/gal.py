import argparse
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tqdm import tqdm


@dataclass
class AlgorithmResult:
    graph: np.ndarray
    elapsed_time: float


def floyd_warshall_exact(graph: np.ndarray) -> AlgorithmResult:
    """
    Performs the exact Floyd-Warshall algorithm to find the shortest paths between all pairs of nodes.

    Parameters:
        graph (np.ndarray): The adjacency matrix of the graph.

    Returns:
        AlgorithmResult: The distance matrix and the time taken to compute it.
    """
    n = len(graph)
    dist = np.array(graph)
    start_time = time.time()  # Start measuring time

    # Diagonal elements are always 0
    np.fill_diagonal(dist, 0)

    for k in tqdm(range(n), desc="Running Exact Floyd-Warshall"):
        for i in range(n):
            for j in range(n):
                dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])

    elapsed_time = time.time() - start_time  # End measuring time
    return AlgorithmResult(graph=dist, elapsed_time=elapsed_time)


def floyd_warshall_approx(graph: np.ndarray, iteration_modifier:float) -> AlgorithmResult:
    """
    Performs an approximate version of the Floyd-Warshall algorithm using Monte Carlo sampling.

    Parameters:
        graph (np.ndarray): The adjacency matrix of the graph.
        num_samples (int): The number of samples to use for the approximation.

    Returns:
        AlgorithmResult: The approximated distance matrix and the time taken to compute it.
    """
    n = len(graph)
    dist = np.array(graph)
    start_time = time.time()  # Start measuring time

    # Diagonal elements are always 0
    np.fill_diagonal(dist, 0)

    for _ in tqdm(range(int(n*iteration_modifier)), desc="Running Approximate Floyd-Warshall"):
        # Randomly sample a node as the "intermediate" node
        k = np.random.randint(0, n)
        for i in range(n):
            for j in range(n):
                dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])

    elapsed_time = time.time() - start_time  # End measuring time
    return AlgorithmResult(graph=dist, elapsed_time=elapsed_time)


def load_graph_from_file(file_path: str) -> np.ndarray:
    """
    Loads a graph from a file.

    Parameters:
        file_path (str): The path to the file containing the adjacency matrix.

    Returns:
        np.ndarray: The loaded adjacency matrix.
    """
    return np.loadtxt(file_path)


def compare_results(exact_result: AlgorithmResult, approx_result: AlgorithmResult, tolerance:float):
    """
    Compares the results of the exact and approximate Floyd-Warshall algorithms.

    Parameters:
        exact_result (AlgorithmResult): The result of the exact algorithm.
        approx_result (AlgorithmResult): The result of the approximate algorithm.
        tolerance (float): The maximum allowed difference between corresponding elements.

    Prints:
        - The accuracy of the approximation based on the number of elements within the tolerance.
        - The time performance comparison between the two algorithms.
    """
    exact_graph = exact_result.graph
    approx_graph = approx_result.graph
    num_elements = exact_graph.size

    # Calculate accuracy based on the number of elements within the tolerance
    within_tolerance = np.sum(np.abs(exact_graph - approx_graph) <= tolerance)
    accuracy = within_tolerance / num_elements * 100

    print(f"Approximation Accuracy: {accuracy:.2f}% of elements are within the tolerance of {tolerance}.")
    print(f"Time Comparison: Exact: {exact_result.elapsed_time:.6f} seconds, Approximate: {approx_result.elapsed_time:.6f} seconds. Faster by {exact_result.elapsed_time / approx_result.elapsed_time:.2f}x")


def save_result_to_file(result: AlgorithmResult, file_path: str):
    """
    Saves the algorithm result to a file.

    Parameters:
        result (AlgorithmResult): The algorithm result to save.
        file_path (str): The path to the output file.
    """
    np.savetxt(file_path, result.graph, fmt="%.2f")
    print(f"Result saved to {file_path}")


def run_program(args):
    # Load the graph from the specified file
    graph = load_graph_from_file(args.graph_path)

    # Run the exact Floyd-Warshall algorithm
    exact_result = floyd_warshall_exact(graph)
    print(f"Exact Floyd-Warshall completed in {exact_result.elapsed_time:.6f} seconds")

    # Run the approximate Floyd-Warshall algorithm
    approx_result = floyd_warshall_approx(graph, args.iteration_modifier)
    print(f"Approximate Floyd-Warshall completed in {approx_result.elapsed_time:.6f} seconds")

    # Compare the results of the exact and approximate algorithms
    compare_results(exact_result, approx_result, args.tolerance)

    # Save results to the specified output files
    if args.output_exact:
        Path(args.output_exact).parent.mkdir(parents=True, exist_ok=True)
        save_result_to_file(exact_result, args.output_exact)
    if args.output_approx:
        Path(args.output_approx).parent.mkdir(parents=True, exist_ok=True)
        save_result_to_file(approx_result, args.output_approx)


def parse_args():
    parser = argparse.ArgumentParser(description="Run Floyd-Warshall algorithms on a graph dataset.")
    parser.add_argument(
        '--graph_path',
        type=str,
        help='File path to the graph dataset'
    )
    parser.add_argument(
        '--output_exact',
        type=str,
        nargs='?',
        help='File path to the output file for the exact algorithm'
    )
    parser.add_argument(
        '--iteration_modifier',
        type=float,
        default=2,
        nargs='?',
        help='File path to the output file for the approximate algorithm'
    )
    parser.add_argument(
        '--output_approx',
        type=str,
        nargs='?',
        help='File path to the output file for the approximate algorithm'
    )
    parser.add_argument(
        '--tolerance',
        type=float,
        default=1e-3,
        nargs='?',
        help='File path to the output file for the approximate algorithm'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    run_program(args)


if __name__ == '__main__':
    main()
