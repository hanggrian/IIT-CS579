from colorama import Fore, Style
from pandas import DataFrame
from us.states import IL

from _lib import MONTCLARE_TRACTS, TRACTS_FILE, Type, Subject, Table, Sequence, get_census

FRAME_COLUMNS = ['state', 'county', 'tract']


def fetch_tracts(title, call_client, year, columns):
    print(f'Fetching {title}... ', end='')
    print('100%')
    frame = \
        DataFrame(
            call_client(get_census()).get(
                list(columns.keys()),
                geo={'for': 'tract:*', 'in': f'state:{IL.fips} county:031'},
                year=year,
            ),
        ).rename(columns=columns)
    return frame[frame['tract'].isin(MONTCLARE_TRACTS)] \
        [FRAME_COLUMNS + list(columns.values())].copy()


if __name__ == '__main__':
    frame_decennial1 = \
        fetch_tracts(
            '2010 Decennial',
            lambda census: census.sf1,
            2010,
            {
                Type.POPULATION + '001001': 'Population 2010',
                Type.HOUSING + '001001': 'Housing 2010',
            },
        )
    frame_decennial2 = \
        fetch_tracts(
            '2020 Decennial',
            lambda census: census.pl,
            2020,
            {
                Type.POPULATION + '1_001N': 'Population 2020',
                Type.HOUSING + '1_001N': 'Housing 2020',
            },
        )
    frame_acs = \
        fetch_tracts(
            '2019\u20132023 ACS 5-Year Estimates',
            lambda census: census.acs5,
            2023,
            {
                Type.DETAILED +
                Subject.INCOME +
                Table.HOUSEHOLD_INCOME +
                Sequence.TOTAL: 'Median household income',
                Type.DETAILED +
                Subject.POVERTY +
                Table.POVERTY_STATUS +
                Sequence.BELOW_POVERTY: 'Population below poverty level',
                Type.DETAILED +
                Subject.HISPANIC +
                Table.HISPANIC_ORIGIN +
                Sequence.HISPANIC_OR_LATINO: 'Hispanic or Latino population',
                Type.DETAILED +
                Subject.HOUSING +
                Table.TENURE +
                Sequence.OWNER_OCCUPIED: 'Owner-occupied housing units',
                Type.DETAILED +
                Subject.COMMUTING +
                Table.COMMUTE_ABILITY +
                Sequence.TOTAL: 'Workers 16+ with transportation',
                Type.DETAILED +
                Subject.EDUCATION +
                Table.EDUCATIONAL_TITLE +
                Sequence.BACHELORS_DEGREE: "Population 25+ with Bachelor's degree",
            },
        )

    print('Writing...')
    frame_decennial1 \
        .merge(frame_decennial2, on=FRAME_COLUMNS, how='outer') \
        .merge(frame_acs, on=FRAME_COLUMNS, how='outer') \
        .to_csv(TRACTS_FILE, index=False)
    print(f'{Fore.GREEN}Done.{Style.RESET_ALL}')

    print()
    print('Goodbye!')
