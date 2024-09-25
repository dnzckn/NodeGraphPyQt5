import signal
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsItem
from pathlib import Path
from NodeGraphQt import BaseNode, NodeGraph, BackdropNode
from NodeGraphQt.constants import PipeLayoutEnum  

# from NodeGraphQt.qgraphics import node_backdrop 
BASE_PATH = Path(__file__).parent.resolve()


from PyQt5.QtWidgets import QGraphicsItem
from NodeGraphQt import BaseNode

from NodeGraphQt import BackdropNode, BaseNode

class CustomBackdropNode(BackdropNode):
    """
    A custom backdrop node that serializes the IDs of the nodes it contains.
    """

    __identifier__ = 'custom.ports'
    NODE_NAME = 'Custom Backdrop Node'

    def __init__(self):
        super(CustomBackdropNode, self).__init__()
        # Initialize properties to store contained node IDs and nodes
        self._contained_node_ids = []
        self._contained_nodes = []
        # Create a custom property 'contained_node_ids' in the node model
        self.create_property('contained_node_ids', self._contained_node_ids)

    def get_nodes(self, inc_intersects=False):
        """
        Returns the list of nodes within the backdrop.

        Args:
            inc_intersects (bool): If True, includes nodes that intersect with the backdrop.

        Returns:
            list[NodeObject]: list of nodes within the backdrop.
        """
        # Access the get_nodes method from the BackdropNodeItem via self.view
        node_items = self.view.get_nodes(inc_intersects)
        # Convert the node items to node objects
        nodes = [self.graph.get_node_by_id(item.id) for item in node_items]
        return nodes

    def update_contained_nodes(self):
        """
        Updates the list of nodes contained within the backdrop.
        """
        nodes = self.get_nodes()  # Use the newly defined get_nodes method
        self._contained_nodes = nodes
        self._contained_node_ids = [node.id for node in nodes if node]
        # Update the property in the model
        self.set_property('contained_node_ids', self._contained_node_ids)

    def update_model(self):
        """
        Update the node model from view.
        """
        # Update contained nodes before updating the model
        self.update_contained_nodes()
        super(CustomBackdropNode, self).update_model()

    def to_dict(self):
        """
        Serialize the backdrop node to a dictionary, including contained node IDs.

        Returns:
            dict: Serialized node data.
        """
        node_dict = super(CustomBackdropNode, self).to_dict()
        # Include the contained node IDs under the 'custom' field
        if 'custom' not in node_dict:
            node_dict['custom'] = {}
        node_dict['custom']['contained_node_ids'] = self.get_property('contained_node_ids')
        return node_dict

    def from_dict(self, node_dict):
        """
        Deserialize the backdrop node from a dictionary.

        Args:
            node_dict (dict): Serialized node data.
        """
        super(CustomBackdropNode, self).from_dict(node_dict)
        # Retrieve the contained node IDs from the 'custom' field
        self._contained_node_ids = node_dict.get('custom', {}).get('contained_node_ids', [])
        self._contained_nodes = []

    def restore_contained_nodes(self, graph):
        """
        After loading the session, restore the contained nodes based on IDs.

        Args:
            graph (NodeGraph): The node graph.
        """
        self.graph = graph  # Store a reference to the graph
        for node_id in self._contained_node_ids:
            node = graph.get_node_by_id(node_id)
            if node and node not in self._contained_nodes:
                self._contained_nodes.append(node)





class CustomPortNode(BaseNode):
    """
    A custom node with dynamic inputs and outputs.
    """

    __identifier__ = 'custom.ports'
    NODE_NAME = 'Custom Port Node'

    def __init__(self):
        super(CustomPortNode, self).__init__()

        # Allow port deletion
        self.set_port_deletion_allowed(True)

        # Initialize with default inputs and outputs
        for i in range(3):
            self.add_input(f'input{i}', color=(0, 0, 255), display_name=True)
        for i in range(4):
            self.add_output(f'output{i}', color=(0, 255, 0), display_name=True)
        for i in range(2):
            self.add_input(f'trace{i}', color=(255, 0, 0), display_name=True)

    def add_input_port(self, name=None):
        """
        Adds an input port to the node.

        Args:
            name (str): Optional. Name of the port.
        """
        if not name:
            name = f'input{len(self.input_ports())}'
        self.add_input(name, color=(0, 0, 255), display_name=True)

    def add_output_port(self, name=None):
        """
        Adds an output port to the node.

        Args:
            name (str): Optional. Name of the port.
        """
        if not name:
            name = f'output{len(self.output_ports())}'
        self.add_output(name, color=(0, 255, 0), display_name=True)

    def remove_port_by_name(self, port_name):
        """
        Removes a port from the node.

        Args:
            port_name (str): Name of the port to remove.
        """
        if port_name in self.inputs():
            self.delete_input(port_name)
        elif port_name in self.outputs():
            self.delete_output(port_name)
        else:
            print(f'Port "{port_name}" not found in node "{self.name()}".')



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
    graph.register_node(CustomBackdropNode)
    # Create root node at the top center.
    root_node = graph.create_node('custom.ports.CustomPortNode', name='root0')
    bd_node = graph.create_node('custom.ports.CustomBackdropNode', name='test')

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
