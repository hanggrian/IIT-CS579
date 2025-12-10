from colorama import Style, Fore
from matplotlib import pyplot
from networkx import Graph, spring_layout, draw_networkx_nodes, draw_networkx_edges, \
    draw_networkx_labels, draw_networkx_edge_labels
from numpy import arange, abs
from pandas import concat

from _lib import load_csvs, COMMUNITY_AREA_KEY, YEAR_KEY, POPULATION_KEY

CTA_COLORS = [
    # new station in Washington/Wabash is Brown/Orange/Pink extension located at Loop
    # but use Blue instead since it's the busiest
    '#00A1DE',
    # L train doesn't extend to Mount Greenwood, use arbitrary muted color Brown
    '#62361B',
    # new station in the Pink extension located at Near West Side
    '#E27EA6',
    # new station in the Green extension located at Near South Side
    '#009B3A',
]


def print_title(title):
    print(f'Plotting {title}...')
    return title


if __name__ == '__main__':
    acs_frames = load_csvs()

    txt = print_title('Total working population (age 16+) trend by community area')
    combined_frame = concat(acs_frames, ignore_index=True)
    combined_frame.rename(
        columns={'Population with personal vehicle': POPULATION_KEY},
        inplace=True,
    )
    aggregated_frame = \
        combined_frame.groupby([COMMUNITY_AREA_KEY, YEAR_KEY])[POPULATION_KEY].sum().reset_index()
    aggregated_frame.sort_values(by=YEAR_KEY, inplace=True)
    pyplot.figure(figsize=(10, 6))

    unique_areas = aggregated_frame[COMMUNITY_AREA_KEY].unique()
    for i, area in enumerate(unique_areas):
        area_data = aggregated_frame[aggregated_frame[COMMUNITY_AREA_KEY] == area]
        pyplot.plot(
            area_data[YEAR_KEY],
            area_data[POPULATION_KEY],
            marker='o',
            label=area,
            color=CTA_COLORS[i],
        )

    pyplot.suptitle('Total working population (age 16+) trend by community area', fontweight='bold')
    pyplot.xlabel('ACS period end year')
    pyplot.ylabel('Total workers (sum of tracts)')
    pyplot.legend(title=COMMUNITY_AREA_KEY, loc='upper left')
    pyplot.grid(True, linestyle='--', alpha=0.6)
    pyplot.xticks(aggregated_frame[YEAR_KEY].unique())
    pyplot.show()

    txt = print_title('Comparison of workers (age 16+) across four community areas')
    plot_data = \
        aggregated_frame.pivot(index=YEAR_KEY, columns=COMMUNITY_AREA_KEY, values=POPULATION_KEY)
    fig, ax = pyplot.subplots(figsize=(12, 7))
    bar_width = 0.2
    years = plot_data.index.values
    r = arange(len(years))
    areas = plot_data.columns

    for i, area in enumerate(areas):
        offset = (i - (len(areas) - 1) / 2) * bar_width
        bars = \
            ax.bar(
                r + offset,
                plot_data[area].values,
                width=bar_width,
                label=area,
                color=CTA_COLORS[i],
            )
        for bar in bars:
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 500,
                f'{yval / 1000:,.1f}k',
                ha='center',
                va='bottom',
                fontsize=8,
                rotation=45,
            )

    ax.set_xticks(r)
    ax.set_xticklabels(years)

    pyplot.suptitle(txt, fontweight='bold')
    ax.set_xlabel('ACS period end year')
    ax.set_ylabel(f'{POPULATION_KEY} (sum of tracts)')
    ax.legend(title=COMMUNITY_AREA_KEY, loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    pyplot.show()

    txt = 'Network graph of population trend correlation (16+ workers)'
    print(f'Printing {txt}...')
    time_series_data = \
        aggregated_frame.pivot(
            index=YEAR_KEY,
            columns=COMMUNITY_AREA_KEY,
            values=POPULATION_KEY,
        )
    correlation_matrix = time_series_data.corr(method='pearson')
    graph = Graph()
    threshold = 0.8
    areas = correlation_matrix.columns.tolist()
    graph.add_nodes_from(areas)
    edge_list = []
    edge_widths = []
    edge_colors = []
    edge_labels = {}
    for i, _ in enumerate(areas):
        for j in range(i + 1, len(areas)):
            area_a = areas[i]
            area_b = areas[j]
            original_corr = correlation_matrix.loc[area_a, area_b]
            weight = abs(original_corr)
            if weight < threshold:
                continue
            scaled_width = (weight - threshold) / (1 - threshold) * 5 + 1
            edge_list.append((area_a, area_b))
            edge_widths.append(scaled_width)
            edge_color = 'green' if original_corr > 0 else 'red'
            edge_colors.append(edge_color)
            edge_labels[(area_a, area_b)] = f'{original_corr:.2f}'
    pyplot.figure(figsize=(10, 8))
    pos = spring_layout(graph, seed=42)
    draw_networkx_nodes(
        graph,
        pos,
        node_size=3000,
        node_color='skyblue',
        alpha=0.9,
        nodelist=areas,
    )
    draw_networkx_edges(
        graph,
        pos,
        edgelist=edge_list,
        width=edge_widths,
        edge_color=edge_colors,
        alpha=0.7,
    )
    draw_networkx_labels(graph, pos, font_size=10, font_weight='bold')
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
        'series (2009\u20132023).\nGreen = positive; Red = negative.',
        wrap=True,
        horizontalalignment='center',
        fontsize=10,
    )
    pyplot.axis('off')
    pyplot.show()

    print(f'{Fore.GREEN}Done.{Style.RESET_ALL}')
    print()
    print('Goodbye!')
