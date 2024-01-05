"""Tools related to graphviz."""
from typing import Optional

from anytree.exporter import DotExporter
from anytree.importer import DictImporter


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


def _filtered_tree_data(node_data: dict, controls: dict) -> Optional[dict]:
    # Check whether we'd like to output this node
    control_data = controls.get(node_data.get('name'))
    control_var = control_data.get('var')
    if not control_var or not control_var.get():
        return None

    attrs = node_data.copy()
    children = attrs.pop('children', [])
    filtered_children = []

    for child in children:
        child_data = _filtered_tree_data(child, controls)
        if child_data:
            filtered_children.append(child_data)
    if filtered_children:
        attrs['children'] = filtered_children

    return attrs


def plot_graph(root: dict, controls: dict) -> None:
    """Plot the graph with only the selected nodes."""
    filtered_root = _filtered_tree_data(root, controls)
    importer = DictImporter()
    root_node = importer.import_(filtered_root)

    DotExporter(root_node, nodeattrfunc=_nodeattrfunc).to_picture('pics/output.png')
