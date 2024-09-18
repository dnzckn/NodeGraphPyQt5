import signal
from PyQt5 import QtCore, QtWidgets
from pathlib import Path
from NodeGraphQt import BaseNode, NodeGraph
from NodeGraphQt.constants import PipeLayoutEnum  
BASE_PATH = Path(__file__).parent.resolve()

class CustomPortNode(BaseNode):
    """
    A custom node with four inputs and four outputs.
    """

    __identifier__ = 'custom.ports'
    NODE_NAME = 'Custom Port Node'

    def __init__(self):
        super(CustomPortNode, self).__init__()
        
        for i in range(2):
            self.add_input(f'trace{i}', color=(255, 0, 0), display_name=True)
        for i in range(3):
            self.add_input(f'input{i}', color=(0, 0, 255), display_name=True)
        for i in range(4):
            self.add_output(f'output{i}', color=(0, 255, 0), display_name=True)


# Recursive function to create nodes dynamically
def create_descendants(graph, parent_node, name_prefix, depth, max_depth, child_counts, pos, spacing, branch_num):
    """
    Helper function to recursively create children for the given parent node.

    Args:
        graph (NodeGraph): The graph to add nodes to.
        parent_node (CustomPortNode): The parent node.
        name_prefix (str): Prefix for naming nodes.
        depth (int): Current depth in the hierarchy.
        max_depth (int): Maximum depth to recurse.
        child_counts (dict): A dictionary mapping node names to number of children.
        pos (list): Position [x, y] for the next node.
        spacing (int): Spacing between nodes.
        branch_num (int): Current branch number.
    """
    if depth >= max_depth:
        return

    # Determine how many children the current parent should have
    num_children = child_counts.get(name_prefix, 0)

    for i in range(num_children):
        # For the first level under root, assign branch numbers starting from 0
        if depth == 0:
            child_branch_num = i  # Assign branch numbers starting from 0
            child_name = f'{name_prefix}_branch{child_branch_num}'
        else:
            child_branch_num = branch_num  # Use the same branch number as parent
            child_name = f'{name_prefix}_{i}'  # Start child index from 0

        # Create the child node
        child_node = graph.create_node('custom.ports.CustomPortNode', name=child_name)

        # Set position for the child node
        new_pos = [pos[0] + (i - num_children / 2) * spacing, pos[1] + spacing]
        child_node.set_pos(*new_pos)

        # Connect the parent to the child using 'output0' and 'input0'
        parent_node.set_output(0, child_node.input(1))  # Connect 'output0' to 'input0'

        # Recursively create children for the current child node
        create_descendants(graph, child_node, child_name, depth + 1, max_depth, child_counts, new_pos, spacing, child_branch_num)


def build_graph():
    """
    Build a hierarchical graph with the root at the top and children descending vertically.
    """
    app = QtWidgets.QApplication([])

    # Create the graph.
    graph = NodeGraph()

    # Set the pipe style to angled
    graph.set_pipe_style(PipeLayoutEnum.ANGLE.value)

    # Register the custom node.
    graph.register_node(CustomPortNode)

    # Create root node at the top center.
    root_node = graph.create_node('custom.ports.CustomPortNode', name='root0')
    root_node.set_pos(0, 0)

    # Define the number of children for each node in the hierarchy
    child_counts = {
        'root0': 2,                # root0 has 2 branches starting from branch0
        'root0_branch0': 1,        # Branch 0 continues with one child
        'root0_branch0_0': 1,      # Next level in branch 0
        'root0_branch1': 2,        # Branch 1 splits into two children
        'root0_branch1_0': 1,      # One of Branch 1's children continues
    }

    # Create descendants from the root
    create_descendants(graph, root_node, 'root0', 0, 4, child_counts, [0, 0], 200, branch_num=0)

    graph.auto_layout_nodes()
    graph.clear_selection()
    graph.fit_to_selection()

    hotkey_path = Path(BASE_PATH, 'hotkeys', 'hotkeys.json')
    graph.set_context_menu_from_file(hotkey_path, 'graph')

    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    app.exec_()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    build_graph()
