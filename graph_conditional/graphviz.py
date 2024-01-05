"""Tools related to graphviz."""
from typing import Optional

from anytree import Node
from anytree.exporter import DotExporter


def attr_string(attrs: dict) -> str:
    """Convert an attribute dictionary to the respective dot-file attribute string."""
    return ';'.join(
        '{}={}'.format(attr, attr_value) for attr, attr_value in attrs.items()
    )


def _nodeattrfunc(node):
    attrs = {
        'penwidth': '0'
    }
    # We're using here an ugly hack from the official graphviz forum:
    # https://forum.graphviz.org/t/how-to-create-node-with-image-and-label-outside/907/3
    # Unfortunately, I haven't found any good alternatives for controlling a node's label position
    # while keeping it _outside_ of the node.
    # xlabel attribute doesn't work, since it places the label almost arbitrary.
    attrs['label'] = '''<<TABLE CELLSPACING="2" CELLPADDING="2" BORDER="0">
    <TR><TD><IMG SRC="pics/math-{0}.png" /></TD></TR>
    <tr><td>{1}</td></tr></TABLE>>'''.format(node.name, node.label)
    return attr_string(attrs)


def _new_tree_node(node_data: dict, controls: dict, parent=None) -> Optional[Node]:
    # Check whether we'd like to output this node
    control_data = controls.get(node_data.get('name'))
    control_var = control_data.get('var')
    if not control_var or not control_var.get():
        return None

    attrs = node_data.copy()
    attrs.pop('children', [])
    if parent:
        attrs['parent'] = parent

    node = Node(**attrs)
    if 'children' in node_data:
        for child in node_data['children']:
            _new_tree_node(child, controls, node)
    return node


def plot_graph(root: dict, controls: dict) -> None:
    """Plot the graph with only the selected nodes."""
    root = _new_tree_node(root, controls)
    DotExporter(root, nodeattrfunc=_nodeattrfunc).to_picture('pics/output.png')
