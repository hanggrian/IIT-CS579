import re
from glob import glob

from colorama import Style, Fore
from matplotlib import pyplot
from networkx import Graph, spring_layout, draw_networkx_nodes, draw_networkx_edges, \
    draw_networkx_labels, draw_networkx_edge_labels
from numpy import abs
from pandas import concat, DataFrame, read_csv

from _lib import warn, CTA_COLORS, ACS_DIR, REGION_KEY, YEAR_KEY, POPULATION_KEY, \
    create_tract_lookup_table


def print_title(title):
    print(f'Plotting {title}...')
    return title


def load_acs() -> list[DataFrame]:
    file_list = glob(f'{ACS_DIR}/*.csv')
    frames = []
    pattern = re.compile(r'.*?(\d{4})\.csv')

    for file_path in file_list:
        frame = read_csv(file_path)
        frame[YEAR_KEY] = int(pattern.search(file_path).group(1))
        frame['tract'] = frame['tract'].astype(str).str.zfill(6)

        merged_frame = frame.merge(create_tract_lookup_table(), on='tract', how='left')
        unmapped_count = merged_frame[REGION_KEY].isna().sum()
        if unmapped_count > 0:
            warn(f'Found {unmapped_count} rows in {file_path}.')
            merged_frame = merged_frame.dropna(subset=[REGION_KEY])
        frames.append(merged_frame)
    return frames


if __name__ == '__main__':
    acs_frames = load_acs()

    txt = print_title('Total working population (age 16+) trend by region')
    combined_frame = concat(acs_frames, ignore_index=True)
    combined_frame.rename(
        columns={'Population with personal vehicle': POPULATION_KEY},
        inplace=True,
    )

    aggregated_frame = \
        combined_frame.groupby([REGION_KEY, YEAR_KEY])[POPULATION_KEY].sum().reset_index()
    aggregated_frame.sort_values(by=YEAR_KEY, inplace=True)
    pyplot.figure(figsize=(12, 8))

    unique_regions = aggregated_frame[REGION_KEY].unique()
    for i, region in enumerate(unique_regions):
        region_data = aggregated_frame[aggregated_frame[REGION_KEY] == region]
        pyplot.plot(
            region_data[YEAR_KEY],
            region_data[POPULATION_KEY],
            marker='o',
            label=region,
            color=CTA_COLORS[i % len(CTA_COLORS)],
        )

    pyplot.suptitle('Total working population (age 16+) trend by region', fontweight='bold')
    pyplot.xlabel('ACS period end year')
    pyplot.ylabel('Total workers (sum of tracts)')
    pyplot.legend(title=REGION_KEY, loc='upper left')
    pyplot.grid(True, linestyle='--', alpha=0.6)
    pyplot.xticks(aggregated_frame[YEAR_KEY].unique())
    pyplot.show()

    txt = print_title('Network graph of population trend correlation (16+ workers) by Region')
    time_series_data = \
        aggregated_frame.pivot(
            index=YEAR_KEY,
            columns=REGION_KEY,
            values=POPULATION_KEY,
        )
    correlation_matrix = time_series_data.corr(method='pearson')
    graph = Graph()
    threshold = 0.8
    regions = correlation_matrix.columns.tolist()
    graph.add_nodes_from(regions)
    edge_list = []
    edge_widths = []
    edge_colors = []
    edge_labels = {}

    node_colors = [CTA_COLORS[i % len(CTA_COLORS)] for i in range(len(regions))]

    for i, _ in enumerate(regions):
        for j in range(i + 1, len(regions)):
            region_a = regions[i]
            region_b = regions[j]
            original_corr = correlation_matrix.loc[region_a, region_b]
            weight = abs(original_corr)
            if weight < threshold:
                continue
            scaled_width = (weight - threshold) / (1 - threshold) * 5 + 1
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
        'Edges represent strong correlation ($|\u03C1| \u2265 0.8$) of working population time ' +
        'series (2009\u20132023) grouped by Chicago Region.\nGreen = positive; Red = negative.',
        wrap=True,
        horizontalalignment='center',
        fontsize=10,
    )
    pyplot.axis('off')
    pyplot.show()

    print(f'{Fore.GREEN}Done.{Style.RESET_ALL}')
    print()
    print('Goodbye!')
