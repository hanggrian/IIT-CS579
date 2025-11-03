from json import load

from matplotlib import pyplot
from networkx import Graph, spring_layout, bipartite, draw_networkx_nodes, draw_networkx_edges, \
    draw_networkx_labels
from numpy import linspace

from _lib import LARGE_FIGURE, LARGE_NODE, SMALL_NODE, LARGE_FONT, SMALL_FONT, \
    check_exists, plot_degree_distribution

INPUT_FILE = 'class_entities.json'
ADAPTIVE_SIZE_THRESHOLD = 20


def adaptive_node_size(size):
    return SMALL_NODE if size > ADAPTIVE_SIZE_THRESHOLD else LARGE_NODE


def adaptive_font_size(size):
    return SMALL_FONT if size > ADAPTIVE_SIZE_THRESHOLD else LARGE_FONT


def strip_email_domain(emails):
    return {e: e.split('@')[0] for e in emails}


if __name__ == '__main__':
    check_exists(INPUT_FILE)
    with open(INPUT_FILE, 'r', encoding='UTF-8') as file:
        participants = load(file)

    for entity_type in [key for key in participants[0].keys() if key != 'email']:
        all_participants = {}
        all_entities = set()

        # collect string or list of strings
        for participant in participants:
            email = participant.get('email')
            entities = participant.get(entity_type)
            if isinstance(entities, str):
                entities = [entities]
            for entity in entities:
                all_entities.add(entity)
            all_participants[email] = entities

        # create bipartite graph
        bipartite_graph = Graph()
        all_participant_emails = all_participants.keys()
        bipartite_graph.add_nodes_from(all_participant_emails, bipartite=0)
        bipartite_graph.add_nodes_from(all_entities, bipartite=1)
        for participant, entities in all_participants.items():
            [bipartite_graph.add_edge(participant, entity) for entity in entities]
        pyplot.figure(figsize=LARGE_FIGURE)
        pyplot.suptitle(
            f'Class participants bipartite graph: {entity_type.title()}',
            fontweight='bold',
        )
        positions = {}
        for i, participant in enumerate(all_participant_emails):
            positions[participant] = (0, linspace(1, 0, len(all_participant_emails))[i])
        for i, entity in enumerate(all_entities):
            positions[entity] = (1, linspace(1, 0, len(all_entities))[i])
        draw_networkx_nodes(
            bipartite_graph,
            positions,
            nodelist=all_participant_emails,
            node_size=adaptive_node_size(len(all_participant_emails)),
            node_color='lightblue',
        )
        draw_networkx_nodes(
            bipartite_graph,
            positions,
            nodelist=all_entities,
            node_size=adaptive_node_size(len(all_entities)),
            node_color='lightcoral',
        )
        draw_networkx_edges(bipartite_graph, positions, edge_color='gray')
        draw_networkx_labels(
            bipartite_graph,
            positions,
            labels=strip_email_domain(all_participant_emails),
            font_size=adaptive_font_size(len(all_participant_emails)),
        )
        draw_networkx_labels(
            bipartite_graph,
            positions,
            labels={e: e for e in all_entities},
            font_size=adaptive_font_size(len(all_entities)),
        )
        pyplot.axis('off')
        pyplot.show()

        # create unimodal graph
        unimodal_graph = bipartite.projected_graph(bipartite_graph, all_participants)
        pyplot.figure(figsize=LARGE_FIGURE)
        pyplot.suptitle(
            f'Class participants unimodal graph: {entity_type.title()}',
            fontweight='bold',
        )
        positions = spring_layout(unimodal_graph, k=3)
        draw_networkx_edges(
            unimodal_graph,
            positions,
            width=0.5,
            edge_color='gray',
        )
        draw_networkx_nodes(
            unimodal_graph,
            positions,
            node_color='lightgreen',
            node_size=LARGE_NODE,
        )
        draw_networkx_labels(unimodal_graph, positions, strip_email_domain(unimodal_graph.nodes()))
        pyplot.axis('off')
        pyplot.show()

        # create degree distribution
        plot_degree_distribution(
            unimodal_graph,
            f'Class participants degree distribution: {entity_type.title()}',
        )
