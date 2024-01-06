"""Internal module with tcl/tk tools."""
import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd

import tomli
from graph_conditional._config import PICTURE_ROOT_KEY

from graph_conditional.graphviz import DEFAULT_EDGE_COLORS, plot_graph


def run_tkinter():
    main_window = tk.Tk()
    main_window.title('Условный граф')
    main_window.geometry('320x240')

    # Monkey-patch for showing hidden files:
    # https://stackoverflow.com/a/54068050
    # It does not work BTW: still cannot choose `.math-tree.toml`.

    # Call a dummy dialog with an impossible option to initialize the file
    # dialog without really getting a dialog window; this will throw a
    # TclError, so we need a try...except :
    try:
        main_window.tk.call('tk_getOpenFile', '-foobarbaz')
    except tk.TclError:
        pass
    # Now set the magic variables accordingly
    main_window.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    main_window.tk.call('set', '::tk::dialog::file::showHiddenVar', '1')

    def choose_config():
        filetypes = (
            ('Конфигурация', '*.toml'),
            ('Любой файл', '*.*')
        )

        filename = fd.askopenfilename(
            parent=main_window,
            title='Выбрать конфигурацию дерева',
            initialdir=Path.cwd(),
            filetypes=filetypes,
        )
        if not filename:
            return

        with open(filename, 'rb') as f:
            config = tomli.load(f)

        config_name = Path(filename)
        default_picture_root = config_name.parent
        config.setdefault(PICTURE_ROOT_KEY, default_picture_root)

        show_graph_window(main_window, config, config_name)

    b = tk.Button(main_window, text='Выбрать конфигурацию', command=choose_config)
    b.pack(expand=True)

    main_window.mainloop()


def show_graph_window(parent, config: dict, config_name: Path):
    window = tk.Toplevel(parent)
    window.title('Конфигурация дерева: {}'.format(config_name.name))
    window.geometry('640x480')

    tree_controls = {}
    tree = config['tree']
    _build_tree_controls(tree, window, tree_controls)

    def plot_graph_click():
        pict_root = Path(config[PICTURE_ROOT_KEY]).expanduser()
        edge_colors = config.get('edge-colors', DEFAULT_EDGE_COLORS)
        plot_graph(tree, tree_controls, pict_root, edge_colors)

    b = tk.Button(window, text='Вывести граф', command=plot_graph_click)
    b.pack(side=tk.BOTTOM)

    # To make window "modal".
    window.grab_set()


def _build_tree_controls(node: dict, control_window: tk.Toplevel, controls: dict, level=0) -> None:
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
