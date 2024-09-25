#!/usr/bin/python

# ------------------------------------------------------------------------------
# menu command functions
# ------------------------------------------------------------------------------


from PyQt5.QtWidgets import QInputDialog, QMessageBox

def zoom_in(graph):
    """
    Set the node graph to zoom in by 0.1
    """
    zoom = graph.get_zoom() + 0.1
    graph.set_zoom(zoom)


def zoom_out(graph):
    """
    Set the node graph to zoom out by 0.2
    """
    zoom = graph.get_zoom() - 0.2
    graph.set_zoom(zoom)


def reset_zoom(graph):
    """
    Reset zoom level.
    """
    graph.reset_zoom()


def layout_h_mode(graph):
    """
    Set node graph layout direction to horizontal.
    """
    graph.set_layout_direction(0)


def layout_v_mode(graph):
    """
    Set node graph layout direction to vertical.
    """
    graph.set_layout_direction(1)


def open_session(graph):
    """
    Prompts a file open dialog to load a session.
    """
    current = graph.current_session()
    file_path = graph.load_dialog(current)
    if file_path:
        graph.load_session(file_path)


def import_session(graph):
    """
    Prompts a file open dialog to import a session.
    """
    current = graph.current_session()
    file_path = graph.load_dialog(current)
    if file_path:
        graph.import_session(file_path)


def save_session(graph):
    """
    Prompts a file save dialog to serialize a session if required.
    """
    current = graph.current_session()
    if current:
        graph.save_session(current)
        msg = 'Session layout saved:\n{}'.format(current)
        viewer = graph.viewer()
        viewer.message_dialog(msg, title='Session Saved')
    else:
        save_session_as(graph)


def save_session_as(graph):
    """
    Prompts a file save dialog to serialize a session.
    """
    current = graph.current_session()
    file_path = graph.save_dialog(current)
    if file_path:
        graph.save_session(file_path)


def clear_session(graph):
    """
    Prompts a warning dialog to clear the current node graph session.
    """
    if graph.question_dialog('Clear Current Session?', 'Clear Session'):
        graph.clear_session()


def quit_qt(graph):
    """
    Quit the Qt application.
    """
    from PyQt5 import QtCore
    QtCore.QCoreApplication.quit()


def clear_undo(graph):
    """
    Prompts a warning dialog to clear the undo stack.
    """
    viewer = graph.viewer()
    msg = 'Clear all undo history, Are you sure?'
    if viewer.question_dialog('Clear Undo History', msg):
        graph.clear_undo_stack()


def copy_nodes(graph):
    """
    Copy selected nodes to the clipboard.
    """
    graph.copy_nodes()


def cut_nodes(graph):
    """
    Cut selected nodes to the clipboard.
    """
    graph.cut_nodes()


def paste_nodes(graph):
    """
    Paste nodes from the clipboard.
    """
    graph.paste_nodes()


def delete_nodes(graph):
    """
    Delete selected nodes.
    """
    graph.delete_nodes(graph.selected_nodes())


def extract_nodes(graph):
    """
    Extract selected nodes from a group.
    """
    graph.extract_nodes(graph.selected_nodes())


def clear_node_connections(graph):
    """
    Clear port connections on selected nodes.
    """
    graph.undo_stack().beginMacro('clear selected node connections')
    for node in graph.selected_nodes():
        for port in node.input_ports() + node.output_ports():
            port.clear_connections()
    graph.undo_stack().endMacro()


def select_all_nodes(graph):
    """
    Select all nodes in the graph.
    """
    graph.select_all()


def clear_node_selection(graph):
    """
    Clear node selection.
    """
    graph.clear_selection()


def invert_node_selection(graph):
    """
    Invert the current node selection.
    """
    graph.invert_selection()


def disable_nodes(graph):
    """
    Toggle disable on selected nodes.
    """
    graph.disable_nodes(graph.selected_nodes())


def duplicate_nodes(graph):
    """
    Duplicate selected nodes.
    """
    graph.duplicate_nodes(graph.selected_nodes())


def expand_group_node(graph):
    """
    Expand selected group node.
    """
    selected_nodes = graph.selected_nodes()
    if not selected_nodes:
        graph.message_dialog('Please select a "GroupNode" to expand.')
        return
    graph.expand_group_node(selected_nodes[0])


def fit_to_selection(graph):
    """
    Sets the zoom level to fit selected nodes.
    """
    graph.fit_to_selection()


def show_undo_view(graph):
    """
    Show the undo list widget.
    """
    graph.undo_view.show()


def curved_pipe(graph):
    """
    Set node graph pipes layout as curved.
    """
    from NodeGraphQt.constants import PipeLayoutEnum
    graph.set_pipe_style(PipeLayoutEnum.CURVED.value)


def straight_pipe(graph):
    """
    Set node graph pipes layout as straight.
    """
    from NodeGraphQt.constants import PipeLayoutEnum
    graph.set_pipe_style(PipeLayoutEnum.STRAIGHT.value)


def angle_pipe(graph):
    """
    Set node graph pipes layout as angled.
    """
    from NodeGraphQt.constants import PipeLayoutEnum
    graph.set_pipe_style(PipeLayoutEnum.ANGLE.value)


def bg_grid_none(graph):
    """
    Turn off the background grid patterns.
    """
    from NodeGraphQt.constants import ViewerEnum
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_NONE.value)


def bg_grid_dots(graph):
    """
    Set the node graph background with grid dots.
    """
    from NodeGraphQt.constants import ViewerEnum
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_DOTS.value)


def bg_grid_lines(graph):
    """
    Set the node graph background with grid lines.
    """
    from NodeGraphQt.constants import ViewerEnum
    graph.set_grid_mode(ViewerEnum.GRID_DISPLAY_LINES.value)


def layout_graph_down(graph):
    """
    Auto layout the nodes downstream.
    """
    nodes = graph.selected_nodes() or graph.all_nodes()
    graph.auto_layout_nodes(nodes=nodes, down_stream=True)


def layout_graph_up(graph):
    """
    Auto layout the nodes upstream.
    """
    nodes = graph.selected_nodes() or graph.all_nodes()
    graph.auto_layout_nodes(nodes=nodes, down_stream=False)


def toggle_node_search(graph):
    """
    Show/hide the node search widget.
    """
    graph.toggle_node_search()


def search_nodes(graph):
    """
    Opens a search dialog to find nodes by name.
    """
    from PyQt5.QtWidgets import QInputDialog

    # Prompt the user for a search query
    query, ok = QInputDialog.getText(graph.viewer(), 'Search Nodes', 'Enter node name:')

    if ok and query:
        # Search for nodes with names matching the query
        matching_nodes = []
        for node in graph.all_nodes():
            node_name = node.name()
            if query.lower() in node_name.lower():
                matching_nodes.append(node)

        if matching_nodes:
            # Clear current selection
            graph.clear_selection()
            # Select matching nodes
            for node in matching_nodes:
                node.set_selected(True)
            # Fit the view to the selection
            graph.fit_to_selection()
        else:
            # Show a message that no nodes were found
            graph.message_dialog(f'No nodes found matching "{query}".', title='Search Nodes')


def undo_action(graph):
    """
    Undo the last action.
    """
    graph.undo_stack().undo()

def redo_action(graph):
    """
    Redo the last undone action.
    """
    graph.undo_stack().redo()




def add_input_port(graph):
    """
    Adds an input port to the selected nodes.
    """
    selected_nodes = graph.selected_nodes()
    if not selected_nodes:
        graph.message_dialog('No nodes selected.', title='Add Input Port')
        return

    # Prompt for the port name
    port_name, ok = QInputDialog.getText(graph.viewer(), 'Add Input Port', 'Enter port name:')
    if not ok:
        return  # User cancelled the dialog

    # Collect results
    nodes_successful = []
    nodes_with_existing_port = []
    unsupported_nodes = []
    nodes_with_errors = []

    # Loop over all selected nodes
    for node in selected_nodes:
        if not hasattr(node, 'add_input_port'):
            unsupported_nodes.append(node.name())
            continue

        if port_name in node.inputs():
            nodes_with_existing_port.append(node.name())
            continue

        try:
            node.add_input_port(port_name if port_name else None)
            nodes_successful.append(node.name())
        except Exception as e:
            nodes_with_errors.append(f"{node.name()}: {e}")

    # Build the message
    messages = []
    if nodes_successful:
        messages.append(f"Input port '{port_name}' added to nodes: {', '.join(nodes_successful)}.")
    if nodes_with_existing_port:
        messages.append(f"Nodes already have an input port named '{port_name}': {', '.join(nodes_with_existing_port)}.")
    if unsupported_nodes:
        messages.append(f"Nodes do not support dynamic ports: {', '.join(unsupported_nodes)}.")
    if nodes_with_errors:
        messages.append(f"Errors occurred on nodes: {'; '.join(nodes_with_errors)}")

    # Show the message
    if messages:
        graph.message_dialog('\n'.join(messages), title='Add Input Port')


def add_output_port(graph):
    """
    Adds an output port to the selected nodes.
    """
    selected_nodes = graph.selected_nodes()
    if not selected_nodes:
        graph.message_dialog('No nodes selected.', title='Add Output Port')
        return

    # Prompt for the port name
    port_name, ok = QInputDialog.getText(graph.viewer(), 'Add Output Port', 'Enter port name:')
    if not ok:
        return  # User cancelled the dialog

    # Collect results
    nodes_successful = []
    nodes_with_existing_port = []
    unsupported_nodes = []
    nodes_with_errors = []

    # Loop over all selected nodes
    for node in selected_nodes:
        if not hasattr(node, 'add_output_port'):
            unsupported_nodes.append(node.name())
            continue

        if port_name in node.outputs():
            nodes_with_existing_port.append(node.name())
            continue

        try:
            node.add_output_port(port_name if port_name else None)
            nodes_successful.append(node.name())
        except Exception as e:
            nodes_with_errors.append(f"{node.name()}: {e}")

    # Build the message
    messages = []
    if nodes_successful:
        messages.append(f"Output port '{port_name}' added to nodes: {', '.join(nodes_successful)}.")
    if nodes_with_existing_port:
        messages.append(f"Nodes already have an output port named '{port_name}': {', '.join(nodes_with_existing_port)}.")
    if unsupported_nodes:
        messages.append(f"Nodes do not support dynamic ports: {', '.join(unsupported_nodes)}.")
    if nodes_with_errors:
        messages.append(f"Errors occurred on nodes: {'; '.join(nodes_with_errors)}")

    # Show the message
    if messages:
        graph.message_dialog('\n'.join(messages), title='Add Output Port')

def remove_port(graph):
    """
    Removes a port from the selected nodes.
    """
    selected_nodes = graph.selected_nodes()
    if not selected_nodes:
        graph.message_dialog('No nodes selected.', title='Remove Port')
        return

    # Get a set of all port names across selected nodes
    port_names_set = set()
    for node in selected_nodes:
        if hasattr(node, 'inputs') and hasattr(node, 'outputs'):
            port_names_set.update(node.inputs().keys())
            port_names_set.update(node.outputs().keys())
    port_names = sorted(port_names_set)

    if not port_names:
        graph.message_dialog('No ports available to remove.', title='Remove Port')
        return

    # Prompt the user to select a port to remove
    port_name, ok = QInputDialog.getItem(graph.viewer(), 'Remove Port', 'Select port to remove:', port_names, editable=False)
    if not ok:
        return  # User cancelled the dialog

    # Confirm the removal
    reply = QMessageBox.question(graph.viewer(), 'Confirm Remove Port',
                                f'Are you sure you want to remove port "{port_name}" from all selected nodes?',
                                QMessageBox.Yes | QMessageBox.No)
    if reply != QMessageBox.Yes:
        return

    # Collect results
    nodes_successful = []
    nodes_port_not_found = []
    unsupported_nodes = []
    nodes_with_errors = []

    # Loop over all selected nodes
    for node in selected_nodes:
        if not hasattr(node, 'remove_port_by_name'):
            unsupported_nodes.append(node.name())
            continue

        try:
            if port_name in node.inputs() or port_name in node.outputs():
                node.remove_port_by_name(port_name)
                nodes_successful.append(node.name())
            else:
                nodes_port_not_found.append(node.name())
        except Exception as e:
            nodes_with_errors.append(f"{node.name()}: {e}")

    # Build the message
    messages = []
    if nodes_successful:
        messages.append(f"Port '{port_name}' removed from nodes: {', '.join(nodes_successful)}.")
    if nodes_port_not_found:
        messages.append(f"Port '{port_name}' not found in nodes: {', '.join(nodes_port_not_found)}.")
    if unsupported_nodes:
        messages.append(f"Nodes do not support dynamic port removal: {', '.join(unsupported_nodes)}.")
    if nodes_with_errors:
        messages.append(f"Errors occurred on nodes: {'; '.join(nodes_with_errors)}")

    # Show the message
    if messages:
        graph.message_dialog('\n'.join(messages), title='Remove Port')
