from json import load
from types import SimpleNamespace

from colorama import Style

MAP_FILE = 'map_2020.json'

if __name__ == '__main__':
    with open(MAP_FILE, 'r', encoding='UTF-8') as file:
        areas = load(file, object_hook=lambda d: SimpleNamespace(**d))

    print(
        f'L coverage: {Style.BRIGHT}' +
        str(
            round(
                len([area.stations for area in areas if len(area.stations) > 0]) /
                len(areas) *
                100,
            ),
        ) +
        '%' +
        Style.RESET_ALL,
    )

    print()
    print('Goodbye!')
