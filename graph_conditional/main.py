from anytree import Node
from anytree.exporter import DotExporter


def nodeattrfunc(node):
    # We're using here an ugly hack from the official graphviz forum:
    # https://forum.graphviz.org/t/how-to-create-node-with-image-and-label-outside/907/3
    # Unfortunately, I haven't found any good alternatives for controlling a node's label position
    # while keeping it _outside_ of the node.
    # xlabel attribute doesn't work, since it places the label almost arbitrary.
    return 'penwidth=0;label=<<TABLE CELLSPACING="2" CELLPADDING="2" BORDER="0"><TR><TD><IMG SRC="pics/math-{0}.png" /></TD></TR><tr><td>{0}</td></tr></TABLE>>'.format(node.name)


if __name__ == '__main__':
    root = Node('root')
    child1 = Node('geometry', parent=root)
    child2 = Node('info', parent=root)

    DotExporter(root, nodeattrfunc=nodeattrfunc).to_picture('pics/output.png')
