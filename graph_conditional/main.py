from graph_conditional._tcltk import run_tkinter


if __name__ == '__main__':
    tree = {
        'name': 'root',
        'label': 'Архипелаг "Математика"',
        'children': [
            dict(name='geometry', label='Остров геометрии'),
            dict(name='info', label='Остров математической информации'),
        ]
    }

    run_tkinter(tree)
