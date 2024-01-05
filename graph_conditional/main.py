from anytree import Node
from anytree.exporter import DotExporter

from graph_conditional.graphviz import attr_string


def nodeattrfunc(node):
    attr_dict = {
        'penwidth': '0'
    }
    # We're using here an ugly hack from the official graphviz forum:
    # https://forum.graphviz.org/t/how-to-create-node-with-image-and-label-outside/907/3
    # Unfortunately, I haven't found any good alternatives for controlling a node's label position
    # while keeping it _outside_ of the node.
    # xlabel attribute doesn't work, since it places the label almost arbitrary.
    attr_dict['label'] = '''<<TABLE CELLSPACING="2" CELLPADDING="2" BORDER="0">
    <TR><TD><IMG SRC="pics/math-{0}.png" /></TD></TR>
    <tr><td>{1}</td></tr></TABLE>>'''.format(node.name, node.label)
    return attr_string(attr_dict)


if __name__ == '__main__':
    root = Node('root', label='Архипелаг "Математика"')
    child1 = Node('geometry', parent=root, label='Остров геометрии')
    child2 = Node('info', parent=root, label='Остров математической информации')

    DotExporter(root, nodeattrfunc=nodeattrfunc).to_picture('pics/output.png')
