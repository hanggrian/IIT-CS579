import re
from glob import glob

from colorama import Fore, Style
from matplotlib import pyplot
from networkx import Graph, spring_layout, draw_networkx_nodes, draw_networkx_edges, \
    draw_networkx_labels, draw_networkx_edge_labels
from pandas import concat, read_csv, DataFrame

from _lib import CTA_COLORS, DECENNIAL_DIR, AREA_KEY, REGION_KEY, YEAR_KEY, \
    POPULATION_KEY, create_tract_lookup_table


def load_decennial() -> list[DataFrame]:
    file_list = glob(f'{DECENNIAL_DIR}/*.csv')
    frames = []
    pattern = re.compile(r'(.+)_(\d{4})\.csv')

    for file_path in file_list:
        match = pattern.search(file_path)
        area_name_raw = match.group(1).replace('_', ' ')
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
        frame[AREA_KEY] = area_name_raw.title()

        frame['tract'] = frame['tract'].astype(str).str.zfill(6)
        merged_frame = frame.merge(create_tract_lookup_table(), on='tract', how='left')
        merged_frame = merged_frame.dropna(subset=[REGION_KEY, POPULATION_KEY])
        frames.append(merged_frame)
    return frames


def print_title(title):
    print(f'Plotting {title}...')
    return title


if __name__ == '__main__':
    combined_frame = concat(load_decennial(), ignore_index=True)

    aggregated_frame = \
        combined_frame.groupby([REGION_KEY, YEAR_KEY])[POPULATION_KEY].sum().reset_index()
    aggregated_frame.sort_values(by=YEAR_KEY, inplace=True)

    unique_regions = aggregated_frame[REGION_KEY].unique()

    txt = print_title('Total population trend by region (Decennial Data)')
    pyplot.figure(figsize=(10, 6))

    for i, region in enumerate(unique_regions):
        region_data = aggregated_frame[aggregated_frame[REGION_KEY] == region]
        pyplot.plot(
            region_data[YEAR_KEY],
            region_data[POPULATION_KEY],
            marker='o',
            label=region,
            color=CTA_COLORS[i % len(CTA_COLORS)],
        )

    pyplot.suptitle(txt, fontweight='bold')
    pyplot.xlabel('Census year')
    pyplot.ylabel('Total population (sum of tracts)')
    pyplot.legend(title=REGION_KEY, loc='upper left')
    pyplot.grid(True, linestyle='--', alpha=0.6)
    pyplot.xticks(aggregated_frame[YEAR_KEY].unique())
    pyplot.show()

    txt = print_title('Regional correlation of total population (Decennial Data)')

    correlation_frame = \
        aggregated_frame.pivot(index=YEAR_KEY, columns=REGION_KEY, values=POPULATION_KEY)

    corr_matrix = correlation_frame.corr()
    regions = list(corr_matrix.columns)

    CORRELATION_THRESHOLD = 0.8

    REGION_TO_COLOR = {
        region: CTA_COLORS[i % len(CTA_COLORS)]
        for i, region in enumerate(regions)
    }
    node_colors = [REGION_TO_COLOR[region] for region in regions]

    graph = Graph()
    graph.add_nodes_from(regions)

    edge_list = []
    edge_widths = []
    edge_colors = []
    edge_labels = {}
    for i, region_a in enumerate(regions):
        for j, region_b in enumerate(regions):
            if j > i:
                original_corr = corr_matrix.loc[region_a, region_b]

                if abs(original_corr) >= CORRELATION_THRESHOLD:
                    scaled_width = (abs(original_corr) - CORRELATION_THRESHOLD) * 5 + 1

                    edge_list.append((region_a, region_b))
                    edge_widths.append(scaled_width)

                    edge_color = 'green' if original_corr > 0 else 'red'
                    edge_colors.append(edge_color)

                    edge_labels[(region_a, region_b)] = f'{original_corr:.2f}'

    pyplot.figure(figsize=(10, 8))
    pos = spring_layout(graph, seed=42)

    draw_networkx_nodes(
        graph,
        pos,
        node_size=3000,
        node_color=node_colors,
        alpha=0.9,
        nodelist=regions,
    )
    draw_networkx_edges(
        graph,
        pos,
        edgelist=edge_list,
        width=edge_widths,
        edge_color=edge_colors,
        alpha=0.7,
    )
    draw_networkx_labels(graph, pos, font_size=9, font_weight='bold')
    draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edge_labels,
        font_color='black',
        font_size=9,
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'),
    )

    pyplot.suptitle(txt, fontweight='bold')
    pyplot.figtext(
        0.5,
        0.01,
        'Edges represent strong correlation (|ρ| ≥ 0.8) of Total Population trend across 2010 ' +
        'and 2020. ' +
        'Note: Correlation is unreliable with only two time points.',
        ha='center',
        fontsize=10,
        wrap=True,
    )
    pyplot.axis('off')
    pyplot.show()

    print(f'{Fore.GREEN}Done.{Style.RESET_ALL}')
    print()
    print('Goodbye!')
