import re
from glob import glob
from json import load
from os import getenv
from sys import stdout, stderr, exit as sysexit
from types import SimpleNamespace

from census import Census
from colorama import Fore, Style
from dotenv import load_dotenv
from pandas import read_csv

COMMUNITY_AREA_KEY = 'Community area'
YEAR_KEY = 'Year'
POPULATION_KEY = 'Population'


def warn(message: str) -> None:
    print(f'{Fore.YELLOW}{message}{Style.RESET_ALL}', file=stdout)


def die(message: str) -> None:
    print(f'\n{Fore.RED}{message}{Style.RESET_ALL}\n', file=stderr)
    sysexit(1)


class _Internals:
    census: Census | None = None


def get_census() -> Census:
    census: Census | None = _Internals.census
    if census is not None:
        return census
    load_dotenv()
    census = Census(getenv('CENSUS_API_KEY') or die('Census API key is not found.'))
    _Internals.census = census
    return census


def load_areas():
    with open('areas.json', 'r', encoding='UTF-8') as file:
        return load(file, object_hook=lambda d: SimpleNamespace(**d))


def load_csvs():
    file_list = glob('*.csv')
    frames = []
    pattern = re.compile(r'(.+)_(\d{4})\.csv')

    for file_name in file_list:
        match = pattern.match(file_name)
        if not match:
            continue
        area_name = match.group(1).replace('_', ' ').title()
        year = int(match.group(2))
        frame = read_csv(file_name)
        frame[COMMUNITY_AREA_KEY] = area_name
        frame[YEAR_KEY] = year
        frames.append(frame)
    return frames
