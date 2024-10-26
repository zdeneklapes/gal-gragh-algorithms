import argparse
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


def generate_graph(num_nodes, edge_probability, max_weight=10, seed=None)->np.ndarray:
    """
    Generates a weighted graph as an adjacency matrix.

    Parameters:
        num_nodes (int): The number of nodes in the graph.
        edge_probability (float): The probability of an edge existing between any two nodes (0 to 1).
        max_weight (int): The maximum weight of any edge.
        seed (int, optional): Random seed for reproducibility.

    Returns:
        np.ndarray: The adjacency matrix representing the graph.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Initialize the adjacency matrix with infinities (representing no connection)
    graph = np.full((num_nodes, num_nodes), float('inf'))

    # Set the diagonal to 0 (distance from a node to itself is 0)
    np.fill_diagonal(graph, 0)

    # Populate the adjacency matrix
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                weight = random.randint(1, max_weight)
                graph[i, j] = weight
                graph[j, i] = weight

    return graph

def save_graph_to_file(graph, filename):
    """
    Saves the adjacency matrix to a file.

    Parameters:
        graph (np.ndarray): The adjacency matrix to save.
        filename (str): The name of the file to save the matrix.
    """
    assert filename.endswith(".txt"), "filename must have .txt extension"
    np.savetxt(filename, graph, fmt="%.2f")

def visualize_graph(graph, filename):
    """
    Visualizes the graph using networkx and matplotlib.

    Parameters:
        graph (np.ndarray): The adjacency matrix of the graph.
        title (str): The title of the plot.
    """
    G = nx.Graph()

    num_nodes = len(graph)

    # Add edges with weights
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if graph[i, j] < float('inf'):
                G.add_edge(i, j, weight=graph[i, j])

    # Draw the graph
    pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Graph Visualization")
    assert filename.endswith(".png"), "filename must have .png extension"
    plt.savefig(filename)
    print(f"Graph visualization saved to {filename}")
    plt.show()

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Generate and visualize weighted graphs.")
    parser.add_argument("--nodes", type=int, default=10, help="Number of nodes in the graph.")
    parser.add_argument("--probability", type=float, default=0.3, help="Probability of an edge between nodes.")
    parser.add_argument("--max_weight", type=int, default=20, help="Maximum weight for edges.")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument("--output_txt", type=str, default="graph.txt", help="Output filename for the graph dataset.")
    parser.add_argument("--output_png", type=str, default="graph.png", help="Output filename for the graph dataset.")
    parser.add_argument("--visualize", action="store_true", help="Visualize the generated graph.")
    args = parser.parse_args()

    # Generate the graph
    graph = generate_graph(args.nodes, args.probability, args.max_weight, args.seed)

    # Save the graph to a file
    save_graph_to_file(graph, args.output_txt)
    print(f"Graph with {args.nodes} nodes saved to {args.output_txt}")

    # Visualize the graph if requested
    if args.visualize:
        visualize_graph(graph, filename=args.output_png)

if __name__ == "__main__":
    main()
