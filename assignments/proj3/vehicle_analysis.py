from json import load

from matplotlib import pyplot
from pandas import DataFrame, concat
from sklearn.preprocessing import minmax_scale

from _lib import load_csvs, COMMUNITY_AREA_KEY, YEAR_KEY, POPULATION_KEY

CENTRAL_AREAS = ['Loop', 'Near South Side', 'Near West Side']

CENTRAL_POPULATION_KEY = 'Central population'
TOTAL_VEHICLES_KEY = 'Total vehicles'
NORMALIZED_CENTRAL_POPULATION_KEY = 'Normalized central population'
NORMALIZED_TOTAL_VEHICLES_KEY = 'Normalized total vehicles'

if __name__ == '__main__':
    acs_frames = load_csvs()
    with open('vehicles.json', 'r', encoding='UTF-8') as file:
        vehicles = load(file)
    vehicles_frame = DataFrame(vehicles)
    vehicles_frame.rename(columns={'year': YEAR_KEY}, inplace=True)
    vehicles_frame.set_index(YEAR_KEY, inplace=True)

    combined_frame = concat(acs_frames, ignore_index=True)
    combined_frame.rename(
        columns={'Population with personal vehicle': POPULATION_KEY},
        inplace=True,
    )
    aggregated_frame = \
        combined_frame.groupby([COMMUNITY_AREA_KEY, YEAR_KEY])[POPULATION_KEY].sum().reset_index()

    time_series_data = \
        aggregated_frame.pivot(
            index=YEAR_KEY,
            columns=COMMUNITY_AREA_KEY,
            values=POPULATION_KEY,
        )

    combined_trends = \
        DataFrame({
            f'{CENTRAL_POPULATION_KEY} (workers)':
                time_series_data[CENTRAL_AREAS].sum(axis=1).rename(CENTRAL_POPULATION_KEY),
            TOTAL_VEHICLES_KEY: vehicles_frame['vehicles'],
        })
    combined_trends[NORMALIZED_CENTRAL_POPULATION_KEY] = \
        minmax_scale(combined_trends[f'{CENTRAL_POPULATION_KEY} (workers)'])
    combined_trends[NORMALIZED_TOTAL_VEHICLES_KEY] = \
        minmax_scale(combined_trends[TOTAL_VEHICLES_KEY])

    fig, ax = pyplot.subplots(figsize=(10, 6))
    pyplot.suptitle(
        'Inverse correlation: Central worker boom vs. city vehicle decline (normalized)',
        fontweight='bold',
    )
    ax.plot(
        combined_trends.index,
        combined_trends[NORMALIZED_CENTRAL_POPULATION_KEY],
        marker='o',
        linestyle='-',
        color='green',
        label=NORMALIZED_CENTRAL_POPULATION_KEY,
    )
    ax.plot(
        combined_trends.index,
        combined_trends[NORMALIZED_TOTAL_VEHICLES_KEY],
        marker='s',
        linestyle='--',
        color='red',
        label=NORMALIZED_TOTAL_VEHICLES_KEY,
    )
    ax.set_xlabel('Year')
    ax.set_ylabel('Normalized value (min-max scaling)')

    pyplot.xticks(combined_trends.index)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    pyplot.show()
