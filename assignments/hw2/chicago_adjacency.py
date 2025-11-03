from json import load

from matplotlib import pyplot
from networkx import Graph, spring_layout, draw

from _lib import LARGE_FIGURE, LARGE_NODE, SMALL_FONT, check_exists, \
    plot_degree_distribution

INPUT_FILE = 'chicago_adjacency.json'

if __name__ == '__main__':
    check_exists(INPUT_FILE)
    with open(INPUT_FILE, 'r', encoding='UTF-8') as file:
        areas = load(file)

    # create adjacency graph
    graph = Graph()
    [graph.add_node(area) for area in areas.keys()]
    for area, neighbors in areas.items():
        [graph.add_edge(area, n) for n in neighbors]
    pyplot.figure(figsize=LARGE_FIGURE)
    pyplot.suptitle('Chicago community areas adjacency map', fontweight='bold')
    draw(
        graph,
        spring_layout(graph),
        with_labels=True,
        node_size=LARGE_NODE,
        font_size=SMALL_FONT,
        node_color='lightblue',
        edge_color='gray',
    )
    pyplot.show()

    # create degree distribution
    plot_degree_distribution(
        graph,
        'Chicago community areas degree distribution',
        '# of adjacent areas',
    )
