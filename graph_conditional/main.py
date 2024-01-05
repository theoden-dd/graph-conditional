from pathlib import Path

import tomli

from graph_conditional._tcltk import run_tkinter


if __name__ == '__main__':
    home = Path.home()

    with open(home / '.graph-conditional.toml', 'rb') as f:
        config = tomli.load(f)

    run_tkinter(config)
