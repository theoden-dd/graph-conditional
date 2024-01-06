"""Internal module with tcl/tk tools."""
import tkinter as tk
from pathlib import Path

from graph_conditional.graphviz import DEFAULT_EDGE_COLORS, plot_graph


def run_tkinter(config):
    window = tk.Tk()
    window.title('Условный граф')
    window.geometry('640x480')

    tree_controls = {}
    tree = config['tree']
    _build_tree_controls(tree, window, tree_controls)

    def plot_graph_click():
        pict_root = Path(config['picture_root']).expanduser()
        edge_colors = config.get('edge-colors', DEFAULT_EDGE_COLORS)
        plot_graph(tree, tree_controls, pict_root, edge_colors)

    b = tk.Button(window, text='Вывести граф', command=plot_graph_click)
    b.pack(side=tk.BOTTOM)

    window.mainloop()


def _build_tree_controls(node: dict, control_window: tk.Tk, controls: dict, level=0) -> None:
    node_name = node['name']

    control_var = tk.IntVar(value=1)
    control = tk.Checkbutton(
        control_window, text=node['label'], variable=control_var, onvalue=1, offvalue=0, anchor='w',
    )
    control.pack(padx=level*5, fill=tk.X)

    controls[node_name] = {
        'control': control,
        'var': control_var
    }

    if 'children' in node:
        for child in node['children']:
            _build_tree_controls(child, control_window, controls, level+1)
