from anytree import Node
from anytree.exporter import DotExporter


def nodeattrfunc(node):
    return 'image="pics/math-{}.png"'.format(node.name)


if __name__ == '__main__':
    root = Node('root')
    child1 = Node('geometry', parent=root)
    child2 = Node('info', parent=root)

    DotExporter(root, nodeattrfunc=nodeattrfunc).to_picture('pics/output.png')
