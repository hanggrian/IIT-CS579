from colorama import Fore, Style
from matplotlib import pyplot
from networkx import Graph, spring_layout, get_node_attributes, draw
from numpy import nan, mean, std, dot, linalg, percentile
from pandas import read_csv
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import cdist
from seaborn import barplot, scatterplot, boxplot, color_palette

from _lib import MONTCLARE_TRACTS, TRACTS_FILE, BLOCKGROUPS_FILE


class Dimension:
    ONE = 'dim1'
    TWO = 'dim2'


def print_plot(title):
    print(f'Plotting {title}...')
    return title


def capitalize_labels(axes):
    axes.set_xlabel(axes.get_xlabel().capitalize())
    axes.set_ylabel(axes.get_ylabel().capitalize())


def show_tight():
    pyplot.tight_layout()
    pyplot.show()


if __name__ == '__main__':
    tract_frame = read_csv(TRACTS_FILE)

    txt = print_plot('Decennial 2010 vs 2020')
    fig, (axes1, axes2) = pyplot.subplots(1, 2, figsize=(10, 6))
    fig.suptitle(txt, fontweight='bold')
    for subject, ax in {
        'Population': axes1,
        'Housing': axes2,
    }.items():
        frame = \
            tract_frame[['tract', f'{subject} 2010', f'{subject} 2020']] \
                .melt(id_vars='tract', var_name='Year', value_name=subject)
        frame['Year'] = frame['Year'].str.split().str[-1]  # remove subject from '{subject} {year}'
        barplot(
            data=frame,
            x='tract',
            y=subject,
            ax=ax,
            hue='Year',
            palette='hls',
        )
        capitalize_labels(ax)
    show_tight()

    txt = print_plot('ACS 2019\u20132023')
    fig, ((axes1, axes2, axes3), (axes4, axes5, axes6)) = pyplot.subplots(2, 3, figsize=(10, 6))
    fig.suptitle(txt, fontweight='bold')
    for var, ax in {
        'Median household income': axes1,
        'Population below poverty level': axes2,
        'Hispanic or Latino population': axes3,
        'Owner-occupied housing units': axes4,
        'Workers 16+ with transportation': axes5,
        "Population 25+ with Bachelor's degree": axes6,
    }.items():
        barplot(
            data=tract_frame,
            x='tract',
            y=var,
            ax=ax,
            hue='tract',
            palette='husl',
            legend=False,
        )
        capitalize_labels(ax)
    show_tight()

    blockgroups_frame = read_csv(BLOCKGROUPS_FILE).dropna(axis=1, how='all')

    blockgroups_frame['is_montclare'] = \
        blockgroups_frame['tract'].astype(str).apply(lambda x: x in MONTCLARE_TRACTS)
    blockgroups_frame['label'] = \
        blockgroups_frame['tract'].astype(str) + '_' + blockgroups_frame['block group'].astype(str)

    num_cols = [
        col for col in blockgroups_frame.columns \
        if col not in ['state', 'county', 'tract', 'block group', 'is_montclare', 'label']
    ]
    blockgroups_frame[num_cols] = blockgroups_frame[num_cols].replace(-666666666.0, nan)

    for col in num_cols:
        median = blockgroups_frame[col].median()
        blockgroups_frame[col] = blockgroups_frame[col].fillna(median)

    data = blockgroups_frame[num_cols].values
    scaled = (data - mean(data, axis=0)) / std(data, axis=0)

    _, _, Vh = linalg.svd(scaled, full_matrices=False)
    reduced = dot(scaled, Vh[:2].T)
    blockgroups_frame[Dimension.ONE] = reduced[:, 0]
    blockgroups_frame[Dimension.TWO] = reduced[:, 1]

    txt = print_plot('Block groups: Hierarchical (unclustered)')
    pyplot.figure(figsize=(10, 6))
    pyplot.suptitle(txt, fontweight='bold')
    scatterplot(
        data=blockgroups_frame,
        x=Dimension.ONE,
        y=Dimension.TWO,
        hue='is_montclare',
        style='is_montclare',
        s=100,
        palette='Set1',
    )
    pyplot.xlabel('Socioeconomic axis 1')
    pyplot.ylabel('Socioeconomic axis 2')
    pyplot.legend(title='Is Montclare')
    pyplot.grid(True)
    pyplot.show()

    blockgroups_frame['cluster'] = \
        fcluster(linkage(scaled, method='ward'), t=4, criterion='maxclust')

    txt = print_plot('Block groups: Hierarchical (clusters)')
    pyplot.figure(figsize=(10, 6))
    pyplot.suptitle(txt, fontweight='bold')
    scatterplot(
        data=blockgroups_frame,
        x=Dimension.ONE,
        y=Dimension.TWO,
        hue='cluster',
        palette='Set2',
        s=100,
    )
    [
        pyplot.annotate(
            s,
            (blockgroups_frame[Dimension.ONE][i], blockgroups_frame[Dimension.TWO][i]),
            fontsize=8,
        ) for i, s in enumerate(blockgroups_frame['label'])
    ]
    pyplot.xlabel('Socioeconomic axis 1')
    pyplot.ylabel('Socioeconomic axis 2')
    pyplot.legend(title='Cluster')
    pyplot.grid(True)
    pyplot.show()

    txt = print_plot('Block groups: Proposed alternative communities')
    fig, ax = pyplot.subplots(figsize=(10, 6))
    fig.suptitle(txt, fontweight='bold')

    scatterplot(
        data=blockgroups_frame,
        x=Dimension.ONE,
        y=Dimension.TWO,
        hue='cluster',
        palette='Set2',
        s=120,
        ax=ax,
        legend=False,  # we will build a custom legend
    )
    montclare = blockgroups_frame[blockgroups_frame['is_montclare']]
    scatterplot(
        data=montclare,
        x=Dimension.ONE,
        y=Dimension.TWO,
        hue='cluster',
        palette='Set2',
        s=120,
        ax=ax,
        edgecolor='black',
        linewidth=1.5,
        legend=False,
    )

    handles = [
        pyplot.Line2D(
            [0],
            [0],
            marker='o',
            color='w',
            markerfacecolor=color_palette('Set3')[i],
            markersize=10,
            label=label,
        )
        for i, label in enumerate([
            'Median household income',
            "Population 25+ with Bachelor's degree",
            'Hispanic or Latino population',
            'Vacant housing units',
        ])
    ]
    ax.legend(handles=handles, title='Socioeconomic profile', loc='upper left')

    ax.set_xlabel('Socioeconomic axis 1')
    ax.set_ylabel('Socioeconomic axis 2')
    ax.grid(True)
    pyplot.show()

    txt = print_plot('Block groups: Network graph')
    dist = cdist(scaled, scaled)
    graph = Graph()
    blockgroups_frame_size = len(blockgroups_frame)
    threshold = percentile(dist.flatten(), 20)
    [
        graph.add_node(
            i,
            label=blockgroups_frame['label'][i],
            is_montclare=blockgroups_frame['is_montclare'][i],
        ) for i in range(blockgroups_frame_size)
    ]
    for i in range(blockgroups_frame_size):
        [
            graph.add_edge(i, j) \
            for j in range(i + 1, blockgroups_frame_size) \
            if dist[i, j] < percentile(dist.flatten(), 20)
        ]

    pyplot.figure(figsize=(10, 6))
    pyplot.suptitle(txt, fontweight='bold')
    pos = spring_layout(graph, seed=2)  # widen gap between nodes
    labels = get_node_attributes(graph, 'label')
    draw(
        graph,
        pos,
        with_labels=True,
        labels=labels,
        node_size=32,
        font_size=8,
        node_color=[
            'lightblue' if graph.nodes[n]['is_montclare'] else 'hotpink' for n in graph.nodes
        ],
    )
    pyplot.show()

    txt = print_plot('Block groups: Montclare vs neighboring areas')
    fig, ((axes1, axes2, axes3), (axes4, axes5, axes6)) = pyplot.subplots(2, 3, figsize=(10, 6))
    fig.suptitle(txt, fontweight='bold')
    xticks = {
        0: 'Neighbors',
        1: 'Montclare',
    }  # substitute of true/false
    for var, ax in {
        'Median household income': axes1,
        'Hispanic or Latino population': axes2,
        'Owner-occupied housing units': axes3,
        "Population 25+ with Bachelor's degree": axes4,
        'Median age': axes5,
        'Total population': axes6,
    }.items():
        boxplot(
            data=blockgroups_frame,
            x='is_montclare',
            y=var,
            ax=ax,
            palette='Set1',
            hue='is_montclare',
            legend=False,
        )
        ax.set_xticks(list(xticks.keys()))
        ax.set_xticklabels(list(xticks.values()))
        ax.set_xlabel('Area')
    show_tight()

    print(f'{Fore.GREEN}Done.{Style.RESET_ALL}')
    print()
    print('Goodbye!')
