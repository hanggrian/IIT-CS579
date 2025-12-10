import re
from glob import glob
from json import load

from colorama import Fore, Style
from matplotlib import pyplot
from numpy import float64, arange, array
from pandas import concat, read_csv, DataFrame

from _lib import DECENNIAL_DIR, ACS_DIR, REGION_KEY, YEAR_KEY, POPULATION_KEY, \
    create_tract_lookup_table

CITY_VEHICLES = 'City vehicles'
WORKING_POPULATION_KEY = 'Working population'
WORKING_POPULATION_PER_VEHICLES_KEY = 'Working population @10k vehicles'


def load_vehicles() -> DataFrame:
    with open('vehicles.json', 'r', encoding='UTF-8') as file:
        data = load(file)
    frame = DataFrame(data)
    frame.rename(columns={'vehicles': CITY_VEHICLES}, inplace=True)
    frame.rename(columns={'year': YEAR_KEY}, inplace=True)
    return frame.set_index(YEAR_KEY)


def load_decennial() -> list[DataFrame]:
    file_list = glob(f'{DECENNIAL_DIR}/*.csv')
    frames = []
    pattern = re.compile(r'(.+)_(\d{4})\.csv')

    for file_path in file_list:
        match = pattern.search(file_path)
        year = int(match.group(2))

        frame = read_csv(file_path)
        frame.rename(
            columns={
                next((col for col in frame.columns if f'population {year}' in col.lower()), None):
                    POPULATION_KEY,
            },
            inplace=True,
        )
        frame[YEAR_KEY] = year

        frame['tract'] = frame['tract'].astype(str).str.zfill(6)
        merged_frame = frame.merge(create_tract_lookup_table(), on='tract', how='left')

        merged_frame = merged_frame.dropna(subset=[REGION_KEY, POPULATION_KEY])
        merged_frame[POPULATION_KEY] = merged_frame[POPULATION_KEY].astype(float64)

        frames.append(merged_frame)
    return frames


def load_acs() -> list[DataFrame]:
    file_list = glob(f'{ACS_DIR}/*.csv')
    frames = []
    pattern = re.compile(r'.*?(\d{4})\.csv')

    for file_path in file_list:
        frame = read_csv(file_path)
        frame[YEAR_KEY] = int(pattern.search(file_path).group(1))
        frame['tract'] = frame['tract'].astype(str).str.zfill(6)

        frame.rename(columns={'Population with personal vehicle': POPULATION_KEY}, inplace=True)

        merged_frame = frame.merge(create_tract_lookup_table(), on='tract', how='left')
        merged_frame = merged_frame.dropna(subset=[REGION_KEY, POPULATION_KEY])
        merged_frame[POPULATION_KEY] = merged_frame[POPULATION_KEY].astype(float64)

        frames.append(merged_frame)
    return frames


def print_title(title):
    print(f'Plotting {title}...')
    return title


if __name__ == '__main__':
    acs_combined_frame = concat(load_acs(), ignore_index=True)

    regional_working_pop = \
        acs_combined_frame.groupby([REGION_KEY, YEAR_KEY])[POPULATION_KEY].sum().reset_index()

    vehicle_frame = load_vehicles()
    regional_working_pop.rename(
        columns={POPULATION_KEY: WORKING_POPULATION_KEY},
        inplace=True,
    )

    combined_analysis_frame = \
        regional_working_pop.merge(
            vehicle_frame,
            on=YEAR_KEY,
            how='left',
        )

    combined_analysis_frame[WORKING_POPULATION_PER_VEHICLES_KEY] = \
        (combined_analysis_frame[WORKING_POPULATION_KEY] / combined_analysis_frame[
            CITY_VEHICLES]) * 10000

    heatmap_matrix = \
        combined_analysis_frame.pivot(
            index=REGION_KEY,
            columns=YEAR_KEY,
            values=WORKING_POPULATION_PER_VEHICLES_KEY,
        )

    heatmap_matrix.sort_values(by=2023, ascending=False, inplace=True)

    plot_data = heatmap_matrix.values
    region_labels = heatmap_matrix.index.tolist()
    year_labels = heatmap_matrix.columns.tolist()

    annot_data = \
        array(
            [
                [f'{val:,.0f}' for val in row] for row in plot_data
            ],
        )

    txt = 'Regional working population density trend (2009–2023)'
    print(f'Plotting {txt}...')

    pyplot.figure(figsize=(10, 8))

    im = pyplot.imshow(plot_data, cmap='viridis', aspect='auto')

    pyplot.title(txt, fontweight='bold')
    pyplot.ylabel(REGION_KEY)

    pyplot.yticks(arange(len(region_labels)), labels=region_labels, fontsize=10)
    pyplot.xticks(arange(len(year_labels)), labels=year_labels, fontsize=10)

    for i in range(plot_data.shape[0]):
        for j in range(plot_data.shape[1]):
            pyplot.text(
                j,
                i,
                annot_data[i, j],
                ha='center',
                va='center',
                color='white',
                fontsize=10,
            )

    cbar = \
        pyplot.colorbar(
            im,
            label='Working population per 10,000 vehicles',
            orientation='vertical',
            pad=0.04,
        )
    cbar.ax.tick_params(labelsize=9)

    pyplot.tight_layout()

    pyplot.show()
    pyplot.close()

    print(f'{Fore.GREEN}Done.{Style.RESET_ALL}')
