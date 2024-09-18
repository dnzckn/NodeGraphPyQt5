import json

def build_simple_hierarchy(nodes, connections):
    """
    Build a simplified structure showing direct connections (N+1 neighbors).

    Args:
        nodes (dict): Dictionary of nodes with their attributes.
        connections (list): List of connections between nodes.

    Returns:
        dict: A dictionary where each node has its immediate connections.
    """
    # Create a lookup for node ids to names.
    node_lookup = {node_id: node_data['name'] for node_id, node_data in nodes.items()}

    # Create a dictionary to store the simplified hierarchy.
    simple_hierarchy = {}

    # Initialize each node with empty lists for inputs and outputs.
    for node_id, node_name in node_lookup.items():
        simple_hierarchy[node_name] = {
            'name': node_name,
            'inputs': [],
            'outputs': []
        }

    # Map the connections to nodes with input/output port details.
    for conn in connections:
        output_node, output_port = conn['out']
        input_node, input_port = conn['in']

        output_node_name = node_lookup[output_node]
        input_node_name = node_lookup[input_node]

        # Add to the outputs of the output node.
        simple_hierarchy[output_node_name]['outputs'].append({
            'connected_to': input_node_name,
            'output_port': output_port,
            'input_port': input_port
        })

        # Add to the inputs of the input node.
        simple_hierarchy[input_node_name]['inputs'].append({
            'connected_from': output_node_name,
            'input_port': input_port,
            'output_port': output_port
        })

    return simple_hierarchy

def convert_json_structure(json_data):
    """
    Convert the graph JSON structure into a simplified N+1 neighbor structure.

    Args:
        json_data (dict): The input graph data in JSON format.

    Returns:
        dict: The simplified structure showing direct relationships (N+1 neighbors).
    """
    nodes = json_data['nodes']
    connections = json_data['connections']

    # Build the simplified structure
    return build_simple_hierarchy(nodes, connections)

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
    # Load the saved graph JSON
    with open('demo.json', 'r') as f:
        graph_json = json.load(f)

    # Convert the JSON to the simplified N+1 neighbor structure
    simple_hierarchy = convert_json_structure(graph_json)

    # Save the simplified structure to a new JSON file
    save_hierarchy_to_json(simple_hierarchy, 'nw_struct.json')
