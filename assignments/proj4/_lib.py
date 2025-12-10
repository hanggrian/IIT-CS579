import re
from glob import glob
from json import load
from os import getenv
from sys import stdout, stderr, exit as sysexit
from types import SimpleNamespace
from typing import Any

from census import Census
from colorama import Fore, Style
from dotenv import load_dotenv
from pandas import read_csv, DataFrame

AREA_KEY: str = 'Area'
REGION_KEY: str = 'Region'
YEAR_KEY: str = 'Year'
POPULATION_KEY: str = 'Population'

FRAME_COLUMNS = ['state', 'county', 'tract']
CTA_COLORS = [
    '#fca7f2',  # Central
    '#73b932',  # Far North Side
    '#5da665',  # Far Southwest Side
    '#b7dccb',  # Far Southeast Side
    '#eff547',  # South Side
    '#fd8e16',  # Southwest Side
    '#7174da',  # Northwest Side
    '#68efe5',  # North Side
    '#ff5e70',  # West Side
]

DECENNIAL_DIR: str = 'data_decennial/'
ACS_DIR: str = 'data_acs/'


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


def load_areas() -> Any:
    with open('areas.json', 'r', encoding='UTF-8') as file:
        return load(file, object_hook=lambda d: SimpleNamespace(d))


def create_tract_lookup_table() -> DataFrame:
    tract_list = []

    for area in load_areas():
        [
            tract_list.append({
                'tract': str(tract_id),
                AREA_KEY: area.area,
                REGION_KEY: area.region,
            }) for tract_id in area.tracts
        ]
    return DataFrame(tract_list).set_index('tract')
