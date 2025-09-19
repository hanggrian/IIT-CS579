from collections import Counter
from os.path import isfile

from matplotlib.pyplot import figure, title, bar, xlabel, ylabel, xticks, show
from networkx.classes import Graph

LARGE_FIGURE: tuple[int, int] = (10, 6)
SMALL_FIGURE: tuple[int, int] = (7, 4)

LARGE_NODE: int = 128
SMALL_NODE: int = 32

LARGE_FONT: int = 14
SMALL_FONT: int = 8


def check_exists(file: str) -> None:
    if not isfile(file):
        raise FileNotFoundError(f"File '{file}' not found.")


def plot_degree_distribution(
    graph: Graph,
    title_text: str,
    x_text: str = 'Degree',
    y_text: str = 'Fraction of nodes',
) -> None:
    degrees = [d for _, d in graph.degree()]
    degree_counts = Counter(degrees)
    steps = sorted(degree_counts.keys())
    figure(figsize=SMALL_FIGURE)
    title(title_text, fontweight='bold')
    total_nodes = len(graph.nodes())
    bar(steps, [degree_counts[d] / total_nodes for d in steps])
    xlabel(x_text)
    ylabel(y_text)
    xticks(steps)
    show()
