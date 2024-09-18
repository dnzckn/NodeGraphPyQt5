import json
import networkx as nx

def build_simple_hierarchy_with_networkx(nodes, connections):
    """
    Build a simplified structure showing direct connections (N+1 neighbors)
    using NetworkX for efficient graph traversal and metadata assignment.

    Args:
        nodes (dict): Dictionary of nodes with their attributes.
        connections (list): List of connections between nodes.

    Returns:
        dict: A dictionary where each node has its immediate connections and metadata.
    """
    # Create a lookup for node IDs to names.
    node_lookup = {node_id: node_data['name'] for node_id, node_data in nodes.items()}

    # Initialize the directed graph.
    G = nx.DiGraph()

    # Add nodes to the graph with initial metadata.
    for node_id, node_data in nodes.items():
        node_name = node_data['name']
        G.add_node(node_name, metadata={'root': None})

    # Add edges to the graph based on connections.
    for conn in connections:
        output_node_id, output_port = conn['out']
        input_node_id, input_port = conn['in']

        output_node_name = node_lookup[output_node_id]
        input_node_name = node_lookup[input_node_id]

        # Add edge with port information.
        G.add_edge(
            output_node_name,
            input_node_name,
            output_port=output_port,
            input_port=input_port
        )

    # Identify root nodes (nodes with no incoming edges).
    root_nodes = [node for node, degree in G.in_degree() if degree == 0]

    # Assign root metadata using BFS traversal.
    for root_name in root_nodes:
        # BFS traversal from the root node.
        for node in nx.bfs_tree(G, source=root_name):
            # Assign the root metadata.
            G.nodes[node]['metadata']['root'] = root_name

    # Build the simplified hierarchy.
    simple_hierarchy = {}

    for node_name in G.nodes():
        node_data = G.nodes[node_name]
        inputs = []
        outputs = []

        # For inputs, look at incoming edges.
        for pred in G.predecessors(node_name):
            edge_data = G.get_edge_data(pred, node_name)
            inputs.append({
                'connected_from': pred,
                'input_port': edge_data.get('input_port'),
                'output_port': edge_data.get('output_port')
            })

        # For outputs, look at outgoing edges.
        for succ in G.successors(node_name):
            edge_data = G.get_edge_data(node_name, succ)
            outputs.append({
                'connected_to': succ,
                'output_port': edge_data.get('output_port'),
                'input_port': edge_data.get('input_port')
            })

        # Build the node's simplified representation.
        simple_hierarchy[node_name] = {
            'name': node_name,
            'inputs': inputs,
            'outputs': outputs,
            'metadata': node_data['metadata']
        }

    return simple_hierarchy

def convert_json_structure(json_data):
    """
    Convert the graph JSON structure into a simplified N+1 neighbor structure using NetworkX.

    Args:
        json_data (dict): The input graph data in JSON format.

    Returns:
        dict: The simplified structure showing direct relationships (N+1 neighbors).
    """
    nodes = json_data['nodes']
    connections = json_data['connections']

    # Build the simplified structure using NetworkX.
    return build_simple_hierarchy_with_networkx(nodes, connections)

def save_hierarchy_to_json(hierarchy, file_path):
    """
    Save the simplified structure to a JSON file.

    Args:
        hierarchy (dict): The simplified graph structure (N+1 neighbor model).
        file_path (str): Path to save the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(hierarchy, f, indent=4)
    print(f"Simplified structure saved to {file_path}")

# Example usage:
if __name__ == "__main__":
    # Load the saved graph JSON (replace 'demo.json' with your actual file).
    with open('demo.json', 'r') as f:
        graph_json = json.load(f)

    # Convert the JSON to the simplified N+1 neighbor structure.
    simple_hierarchy = convert_json_structure(graph_json)

    # Save the simplified structure to a new JSON file.
    save_hierarchy_to_json(simple_hierarchy, 'nw_struct.json')
