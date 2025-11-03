from colorama import Fore, Style
from pandas import DataFrame, concat
from us.states import IL

from _lib import warn, MONTCLARE_TRACTS, BLOCKGROUPS_FILE, Type, Subject, Table, Sequence, \
    get_census

FRAME_COLUMNS = ['state', 'county', 'tract', 'block group']


def fetch_block_groups(title, columns, tracts):
    print(f'Fetching {title}... ', end='')
    result = []
    for i, tract in enumerate(tracts):
        print(f'{int(i / len(tracts) * 100)}%... ', end='')
        result.extend(
            get_census().acs5.get(
                list(columns.keys()),
                geo={'for': 'block group:*', 'in': f'state:{IL.fips} county:031 tract:{tract}'},
                year=2023,
            ),
        )
    print('100%')
    return DataFrame(result).rename(columns=columns) \
        [FRAME_COLUMNS + list(columns.values())].copy()


def fetch_neighbor_block_groups(title, columns, neighbor_tracts):
    return fetch_block_groups(title, columns, neighbor_tracts)


if __name__ == '__main__':
    acs_variables = {
        f'{Type.DETAILED}{Subject.INCOME}{Table.HOUSEHOLD_INCOME}{Sequence.TOTAL}':
            'Median household income',
        f'{Type.DETAILED}{Subject.POVERTY}{Table.POVERTY_STATUS}{Sequence.BELOW_POVERTY}':
            'Population below poverty level',
        f'{Type.DETAILED}{Subject.HISPANIC}{Table.HISPANIC_ORIGIN}{Sequence.HISPANIC_OR_LATINO}':
            'Hispanic or Latino population',
        f'{Type.DETAILED}{Subject.HOUSING}{Table.TENURE}{Sequence.OWNER_OCCUPIED}':
            'Owner-occupied housing units',
        f'{Type.DETAILED}{Subject.COMMUTING}{Table.COMMUTE_ABILITY}{Sequence.TOTAL}':
            'Workers 16+ with transportation',
        f'{Type.DETAILED}{Subject.EDUCATION}{Table.EDUCATIONAL_TITLE}{Sequence.BACHELORS_DEGREE}':
            "Population 25+ with Bachelor's degree",
        f'{Type.DETAILED}{Subject.POPULATION}{Table.TOTAL_POPULATION}{Sequence.TOTAL}':
            'Total population',
        f'{Type.DETAILED}{Subject.POPULATION}{Table.MEDIAN_AGE}{Sequence.TOTAL}':
            'Median age',
        f'{Type.DETAILED}{Subject.HISPANIC}{Table.HISPANIC_ORIGIN}{Sequence.WHITE_ALONE}':
            'White alone (Non-Hispanic)',
        f'{Type.DETAILED}{Subject.HISPANIC}{Table.HISPANIC_ORIGIN}{Sequence.BLACK_ALONE}':
            'Black alone (Non-Hispanic)',
        f'{Type.DETAILED}{Subject.HOUSING}{Table.HOUSING_UNITS}{Sequence.TOTAL}':
            'Total housing units',
        f'{Type.DETAILED}{Subject.HOUSING}{Table.OCCUPANCY}{Sequence.RENTER_OCCUPIED}':
            'Vacant housing units',
        f'{Type.DETAILED}{Subject.HOUSING}{Table.HOME_VALUE}{Sequence.TOTAL}':
            'Median home value',
        f'{Type.DETAILED}{Subject.HOUSING}{Table.GROSS_RENT}{Sequence.TOTAL}':
            'Median gross rent',
        f'{Type.DETAILED}{Subject.EMPLOYMENT}{Table.EMPLOYMENT_STATUS}{Sequence.IN_LABOR_FORCE}':
            'In labor force',
        f'{Type.DETAILED}{Subject.LANGUAGE}{Table.LANGUAGE_SPOKEN}{Sequence.ENGLISH_ONLY}':
            'English only speakers',
        f'{Type.DETAILED}{Subject.LANGUAGE}{Table.LANGUAGE_SPOKEN}{Sequence.SPANISH}':
            'Spanish speakers',
    }
    frame_montclare = \
        fetch_block_groups(
            '2019\u20132023 ACS 5-Year Estimates',
            acs_variables,
            MONTCLARE_TRACTS,
        )
    frame_montclare_size = len(frame_montclare)

    if frame_montclare_size < 60:
        warn(
            'Montclare has fewer than 60 block groups: ' +
            f'{Style.BRIGHT}{frame_montclare_size}{Style.RESET_ALL}',
        )
        frame_neighbors = \
            fetch_neighbor_block_groups(
                'Neighboring community areas',
                acs_variables,
                [
                    '190100',
                    '190200',
                    '190300',
                    '170100',
                    '170200',
                    '170300',
                ],
            )
        output_frame = concat([frame_montclare, frame_neighbors], ignore_index=True)
    else:
        output_frame = frame_montclare

    print('Writing...')
    output_frame.to_csv(BLOCKGROUPS_FILE, index=False)
    print(f'{Fore.GREEN}Done.{Style.RESET_ALL}')

    print()
    print('Goodbye!')
