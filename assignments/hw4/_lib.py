from dataclasses import dataclass
from os import getenv
from sys import stdout, stderr, exit as sysexit

from census import Census
from colorama import Fore, Style
from dotenv import load_dotenv


def warn(message: str) -> None:
    print(f'{Fore.YELLOW}{message}{Style.RESET_ALL}', file=stdout)


def die(message: str) -> None:
    print(f'\n{Fore.RED}{message}{Style.RESET_ALL}\n', file=stderr)
    sysexit(1)


MONTCLARE_TRACTS: list[str] = ['180100', '831600']

TRACTS_FILE = 'montclare_tracts.csv'
BLOCKGROUPS_FILE = 'montclare_blockgroups.csv'


class Type:
    POPULATION: str = 'P'
    HOUSING: str = 'H'
    DETAILED: str = 'B'


class Subject:
    POPULATION: str = '01'
    RACE: str = '02'
    HISPANIC: str = '03'
    COMMUTING: str = '08'
    HOUSEHOLD: str = '11'
    EDUCATION: str = '15'
    LANGUAGE: str = '16'
    POVERTY: str = '17'
    INCOME: str = '19'
    EMPLOYMENT: str = '23'
    HOUSING: str = '25'


class Table:
    TOTAL_POPULATION: str = '003'
    SEX_AGE: str = '001'
    MEDIAN_AGE: str = '002'

    RACE: str = '001'
    HISPANIC_ORIGIN: str = '002'

    HOUSING_UNITS: str = '001'
    OCCUPANCY: str = '002'
    TENURE: str = '003'
    HOME_VALUE: str = '077'
    GROSS_RENT: str = '064'

    HOUSEHOLD_INCOME: str = '013'
    PER_CAPITA_INCOME: str = '301'
    POVERTY_STATUS: str = '001'

    EDUCATIONAL_TITLE: str = '003'

    COMMUTE_ABILITY: str = '301'

    LANGUAGE_SPOKEN: str = '001'

    EMPLOYMENT_STATUS: str = '025'


class Sequence:
    TOTAL: str = '_001E'

    # poverty
    BELOW_POVERTY: str = '_002E'

    # race
    WHITE_ALONE: str = '_003E'
    BLACK_ALONE: str = '_004E'
    HISPANIC_OR_LATINO: str = '_012E'

    # household
    OWNER_OCCUPIED: str = '_002E'
    RENTER_OCCUPIED: str = '_003E'

    # education
    BACHELORS_DEGREE: str = '_022E'

    # employment
    IN_LABOR_FORCE: str = '_002E'

    # language
    ENGLISH_ONLY: str = '_002E'
    SPANISH: str = '_003E'


@dataclass
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
