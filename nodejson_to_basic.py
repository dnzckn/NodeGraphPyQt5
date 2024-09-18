import json

def build_hierarchy(nodes, connections, root_name):
    """
    Build a hierarchical structure from nodes and connections.

    Args:
        nodes (dict): Dictionary of nodes with their attributes.
        connections (list): List of connections between nodes.
        root_name (str): The name of the root node.

    Returns:
        dict: A nested dictionary representing the hierarchy.
    """
    # Create a lookup for node ids to names and their data.
    node_lookup = {node_data['name']: node_id for node_id, node_data in nodes.items()}
    
    # Create a dictionary to hold node connections.
    hierarchy = {}

    # Initialize the structure for each node.
    def initialize_node(node_name):
        node_id = node_lookup[node_name]
        return {
            'name': node_name,
            'inputs': [],
            'outputs': [],
            'kids': []
        }

    # Build the connection mapping for inputs and outputs.
    def map_connections():
        conn_map = {node_id: {'inputs': [], 'outputs': []} for node_id in nodes}
        for conn in connections:
            output_node = conn['out'][0]
            input_node = conn['in'][0]
            conn_map[output_node]['outputs'].append(nodes[input_node]['name'])
            conn_map[input_node]['inputs'].append(nodes[output_node]['name'])
        return conn_map

    # Recursively add children nodes to the hierarchy.
    def recursive_add_children(node, conn_map):
        node_id = node_lookup[node['name']]
        node['inputs'] = conn_map[node_id]['inputs']
        node['outputs'] = conn_map[node_id]['outputs']
        
        for output_node in conn_map[node_id]['outputs']:
            child_node = initialize_node(output_node)
            node['kids'].append(recursive_add_children(child_node, conn_map))
        
        return node

    # Build the hierarchy starting from the root node.
    conn_map = map_connections()
    root_node = initialize_node(root_name)
    return recursive_add_children(root_node, conn_map)

def convert_json_structure(json_data):
    """
    Convert the graph JSON structure into a simplified hierarchical structure.

    Args:
        json_data (dict): The input graph data in JSON format.

    Returns:
        dict: The simplified hierarchical structure.
    """
    nodes = json_data['nodes']
    connections = json_data['connections']

    # Assuming root node is always 'root0'
    root_name = "root0"
    
    # Build the hierarchy starting from the root
    return build_hierarchy(nodes, connections, root_name)

def save_hierarchy_to_json(hierarchy, file_path):
    """
    Save the hierarchical structure to a JSON file.

    Args:
        hierarchy (dict): The hierarchical structure of the graph.
        file_path (str): Path to save the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(hierarchy, f, indent=4)
    print(f"Hierarchy saved to {file_path}")

# Example usage:
if __name__ == "__main__":
    # Load the saved graph JSON
    with open('demo.json', 'r') as f:
        graph_json = json.load(f)

    # Convert the JSON to the hierarchical structure
    hierarchy = convert_json_structure(graph_json)

    # Save the simplified hierarchical structure to a new JSON file
    save_hierarchy_to_json(hierarchy, 'simplified_graph_structure.json')
