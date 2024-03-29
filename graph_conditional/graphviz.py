"""Tools related to graphviz."""
from pathlib import Path
from typing import Optional

from anytree.exporter import DotExporter
from anytree.importer import DictImporter


# Keys are strings to be TOML-compatible:
# https://toml.io/en/v1.0.0#keys
DEFAULT_EDGE_COLORS = {
    '0': '#cc292a',
    '1': '#fb5b75',
    '2': '#eb7a42',
    '3': '#ff9734',
}
_DEFAULT_EDGE_COLOR = 'orange'


def attr_string(attrs: dict) -> str:
    """Convert an attribute dictionary to the respective dot-file attribute string."""
    return ';'.join(
        '{}={}'.format(attr, attr_value) for attr, attr_value in attrs.items()
    )


def _new_node_attr_func(pict_root: Path):
    def _nodeattrfunc(node):
        attrs = {
            'penwidth': '0'
        }
        pict_name = '{0}.png'.format(node.name)
        # We're using here an ugly hack from the official graphviz forum:
        # https://forum.graphviz.org/t/how-to-create-node-with-image-and-label-outside/907/3
        # Unfortunately, I haven't found any good alternatives for controlling a node's label position
        # while keeping it _outside_ of the node.
        # xlabel attribute doesn't work, since it places the label almost arbitrary.
        attrs['label'] = '''<<TABLE CELLSPACING="2" CELLPADDING="2" BORDER="0">
        <TR><TD><IMG SRC="{0}" /></TD></TR>
        <tr><td><font point-size="255pt">{1}</font></td></tr></TABLE>>'''.format(pict_root / pict_name, node.label)
        return attr_string(attrs)
    return _nodeattrfunc


# todo: Refactor into the `filter_` parameter of the DotExporter constructor.
#   Instead of manual traversing:
#   https://anytree.readthedocs.io/en/latest/exporter/dotexporter.html
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


def _new_edge_attr_func(edge_colors: dict):
    def edgeattrfunc(parent, child):
        # For absent depths use the root depth color or the default color if not set.
        default_color = edge_colors.get('0', _DEFAULT_EDGE_COLOR)
        attrs = {
            'minlen': 2/(parent.depth+1),
            'penwidth': 10 - parent.depth*2,
            'weight': parent.depth,
            'color': '"{}"'.format(edge_colors.get(str(parent.depth), default_color)),
        }
        return attr_string(attrs)
    return edgeattrfunc


def plot_graph(root: dict, controls: dict, pict_root: Path, edge_colors: dict) -> None:
    """Plot the graph with only the selected nodes."""
    filtered_root = _filtered_tree_data(root, controls)
    importer = DictImporter()
    root_node = importer.import_(filtered_root)

    DotExporter(
        root_node,
        graph='graph',
        nodeattrfunc=_new_node_attr_func(pict_root),
        edgeattrfunc=_new_edge_attr_func(edge_colors),
        edgetypefunc=lambda node, child: '--',
        # The graph `fontsize` setting here doesn't work for a table text under the node.
        options=(
            # 'landscape=true',
            'node [{}]'.format(attr_string(dict(
                shape='box'
            ))),
        )
    ).to_picture(str(pict_root / 'output.png'))
