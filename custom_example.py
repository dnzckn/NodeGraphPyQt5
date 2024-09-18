import signal
from PyQt5 import QtCore, QtWidgets
from pathlib import Path
from NodeGraphQt import BaseNode, NodeGraph
BASE_PATH = Path(__file__).parent.resolve()

# Custom Port Node Definition
class CustomPortNode(BaseNode):
    """
    A simple custom node with two inlets and one outlet.
    """

    __identifier__ = 'custom.ports'
    NODE_NAME = 'Custom Port Node'

    def __init__(self):
        super(CustomPortNode, self).__init__()
        self.add_input('trace', color=(255, 0, 0), display_name=True)  # Unused inlet
        self.add_input('inlet', color=(0, 0, 255), display_name=True)  # Connected inlet
        self.add_output('output', color=(0, 255, 0), display_name=True)  # Output connection


# Recursive function to create nodes dynamically
def create_descendants(graph, parent_node, name_prefix, depth, max_depth, child_counts, pos, spacing):
    """
    Recursively create children for the given parent node.

    Args:
        graph (NodeGraph): The graph to add nodes to.
        parent_node (CustomPortNode): The parent node.
        name_prefix (str): Prefix for naming nodes.
        depth (int): Current depth in the hierarchy.
        max_depth (int): Maximum depth to recurse.
        child_counts (dict): A dictionary mapping node names to number of children.
        pos (list): Position [x, y] for the next node.
        spacing (int): Vertical spacing between nodes.
    """
    if depth >= max_depth:
        return

    # Determine how many children the current parent should have
    num_children = child_counts.get(name_prefix, 0)

    for i in range(num_children):
        # Create the child node
        child_name = f'{name_prefix}_{i}'
        child_node = graph.create_node('custom.ports.CustomPortNode', name=child_name)

        # Set position for the child node
        new_pos = [pos[0] + i * spacing, pos[1] + spacing]
        child_node.set_pos(*new_pos)

        # Connect the parent to the child
        parent_node.set_output(0, child_node.input(1))

        # Recursively create children for the current child node
        create_descendants(graph, child_node, child_name, depth + 1, max_depth, child_counts, new_pos, spacing)


def build_graph():
    """
    Build a hierarchical graph with the root at the top and children descending vertically.
    """
    app = QtWidgets.QApplication([])

    # Create the graph.
    graph = NodeGraph()

    # Register the custom node.
    graph.register_node(CustomPortNode)

    # Create root node at the top center.
    root_node = graph.create_node('custom.ports.CustomPortNode', name='root0')
    root_node.set_pos(0, 0)

    # Define the number of children for each node in the hierarchy
    child_counts = {
        'root0': 2,         # Root has 2 children
        'root0_0': 1,       # First child of root has 1 child
        'root0_1': 2,       # Second child of root has 2 children
        'root0_1_0': 1,     # First child of root0_1 has 1 child
        # Add more entries here for further levels if needed
    }

    # Create descendants from the root
    create_descendants(graph, root_node, 'root0', 0, 4, child_counts, [0, 0], 200)

    # Automatically layout nodes for better visualization.
    graph.auto_layout_nodes()

    # Set the zoom to fit all nodes.
    graph.clear_selection()
    graph.fit_to_selection()

    # Enable hotkey support.
    hotkey_path = Path(BASE_PATH, 'hotkeys', 'hotkeys.json')
    graph.set_context_menu_from_file(hotkey_path, 'graph')

    # Show the graph widget.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    app.exec_()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    build_graph()
