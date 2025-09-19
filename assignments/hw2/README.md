# Homework 2

> In this assignment you will create networks/graph models from 2 different
  datasets. You may use any tool/platform/language that you like. I have
  attached a few pages from the Elements of Network Science Book that illustrate
  basic use of Stata, R and [Python.Section 2.3 ElementsofNetworkScience.pdf](https://github.com/hanggrian/IIT-CS579/blob/assets/ext1.pdf)

## Problem 1

> The first dataset is [Chicago Community Areas](https://en.wikipedia.org/wiki/Community_areas_in_Chicago)
>
> - Nodes: Community areas
> - Edges: Shared physical boundary (i.e. adjacency) with other community area.
    Note that you may have to make some assumptions here since you are
    determining boundaries from the image of the map on the page cited above.
    State your assumptions.
>
> You will then create a labelled visualization of this graph and plot the
  degree distribution of the nodes. You will submit
>
>   1.  Input file with graph representation.

To build the adjacency map of Chicago communities, I am grouping areas that are
directly connected to each other and are in the same region defined in the
Wikipedia page. In the example below, there are four areas connected to
**Norwood Park** in the Far North Side region, ignoring two areas from the
Northwest Side. The result is tabulated into a JSON file, which is readable by
Python.

[View JSON file](https://github.com/hanggrian/IIT-CS579/blob/main/assignments/hw2/chicago_adjacency.json)

<img
  width="320"
  alt="Diagram 1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/diagram1.svg">

>   2.  Labelled visualization of network created.

| | |
--- | ---
**Central** | **Far North Side**
![Figure 1.1.1](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_1.png) | ![Figure 1.1.2](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_2.png)
**Far Southeast Side** | **Far Southwest Side**
![Figure 1.1.3](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_3.png) | ![Figure 1.1.4](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_4.png)
**North Side** | **Northwest Side**
![Figure 1.1.5](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_5.png) | ![Figure 1.1.6](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_6.png)
**South Side** | **Southwest Side**
![Figure 1.1.7](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_7.png) | ![Figure 1.1.8](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_8.png)
**West Side** |
![Figure 1.1.9](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_1_9.png) |

>   3.  Plot of degree distribution.

<img
  width="480"
  alt="Figure 1.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure1_2.png">

## Problem 2

> The second dataset is the CS 579 Class Participant Data `Social Network Data
  collection.xlsx`
>
> - Nodes: Class participants, entities in common
> - Edges: Shared entity
>
> You will create a bipartite graph. Some data cleaning will be necessary. State
  and justify any assumptions you make during the data cleaning. You will then
  create a unimodal graph that is a projection of the bipartite graph.
>
> You will create labelled visualizations of both the bipartite and unimodal
  graphs and plot the degree distribution of the unimodal graph. You will submit
>
> 1.  Input file for the bipartite graph.

Participants are represented by objects in a JSON array in the input file of
class entities. For each entity type (department, programming languages, etc.),
the entity value is connected to the participant’s email address. The input file
is deliberately not tracked in Git repository for privacy concern.

> 2.  Labelled visualization of bipartite graph.

<img
  width="100%"
  alt="Figure 2.1.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_1_1.png">
<img
  width="100%"
  alt="Figure 2.1.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_1_2.png">
<img
  width="100%"
  alt="Figure 2.1.3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_1_3.png">
<img
  width="100%"
  alt="Figure 2.1.4"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_1_4.png">
<img
  width="100%"
  alt="Figure 2.1.5"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_1_5.png">
<img
  width="100%"
  alt="Figure 2.1.6"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_1_6.png">
<img
  width="100%"
  alt="Figure 2.1.7"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_1_7.png">

> 3.  Description of method for projecting bipartite graph to unimodal graph
      including code.

A unimodal graph is created by projecting a bipartite graph with the NetworkX
package. Then, determine the node positions using the force-directed algorithm
and spread the distance by 3 points to avoid too many overlapping edges.
Finally, draw the nodes, edges and labels in the figure at the calculated
positions.

```py
unimodal_graph = bipartite.projected_graph(bipartite_graph, all_participants)
figure(figsize=LARGE_FIGURE)
title(f'Participants {entity_type} unimodal graph', fontweight='bold')
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
axis('off')
tight_layout()
show()
```

> 4.  Labelled visualization of unimodal graph.

<img
  width="100%"
  alt="Figure 2.2.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_2_1.png">
<img
  width="100%"
  alt="Figure 2.2.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_2_2.png">
<img
  width="100%"
  alt="Figure 2.2.3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_2_3.png">
<img
  width="100%"
  alt="Figure 2.2.4"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_2_4.png">
<img
  width="100%"
  alt="Figure 2.2.5"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_2_5.png">
<img
  width="100%"
  alt="Figure 2.2.6"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_2_6.png">
<img
  width="100%"
  alt="Figure 2.2.7"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_2_7.png">

> 5.  Plot of degree distribution of unimodal graph.

<img
  width="320"
  alt="Figure 2.3.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_3_1.png">
<img
  width="320"
  alt="Figure 2.3.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_3_2.png">
<img
  width="320"
  alt="Figure 2.3.3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_3_3.png">
<img
  width="320"
  alt="Figure 2.3.4"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_3_4.png">
<img
  width="320"
  alt="Figure 2.3.5"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_3_5.png">
<img
  width="320"
  alt="Figure 2.3.6"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_3_6.png">
<img
  width="320"
  alt="Figure 2.3.7"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw2/figure2_3_7.png">

## Problem 3

> Compare the degree distributions of the graphs from the two different
  datasets. What is similar? What is different? Is this what you expected? Why
  or why not?

Because we are drawing an adjacency map of geographical locations in the Chicago
community areas, the highest node count sits in the median degree, gradually
decreasing in value when traversing to both ends. Compared to physical
locations, the entities of class participants are selected by preference, making
the degree distributions unpredictable. Analyzing the final participant degree
distributions, it is safe to say that most students have something in common in
all entities except hobbies. The output is as expected by comparing the input
file to the generated graphs and charts.

## Problem 4

> Provide the details of how you did this assignment. What tools did you use to
  complete the assignment? Why did you choose the tool? Provide citations and
  links to references and code used. If AI (e.g. ChatGPT, etc.) was used, please
  include a transcript of the exchange.

The solutions rely on Matplotlib and NetworkX, the network analysis package for
Python. The source code itself is inspired by [the NetworkX tutorial](https://networkx.org/documentation/stable/tutorial.html)
that explains graph attributes and basic usage. When plotting a histogram, [the
Matplotlib documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html)
was a crucial resource to understand the desired output diagram.

However, an AI chatbot was used in one instance of this assignment to convert
the class participant spreadsheet into a JSON file. I saved the spreadsheet as a
CSV file so that the chatbot can read it without any formatting. Finally, the
final result is slightly modified to standardize residence and hobbies.

### AI prompts

> Convert the input CSV:
>
> ```
> Illinois Tech email address,Department (if you have multiple depts please enter them all separated by a comma),Degree Program (if you are pursuing multiple degrees at Illinois Tech please enter them all separated by a comma),Neighborhood you reside in,Computer Languages (separate with comma),Languages spoken (separate with comma),Hobbies (separate with comma),Student club memberships (separate with comma)
> ...
> ```
>
> into JSON format in the following format:
>
> ```json
> {
>   "email": "",
>   "department": "",
>   "degrees": [
>     ""
>   ],
>   "neighborhood": "",
>   "technologies": [
>     ""
>   ],
>   "languages": [
>     ""
>   ],
>   "hobbies": [
>     ""
>   ],
>   "clubs": [
>     ""
>   ]
> },
> ```

I’ve converted the CSV into the requested JSON format. You can download it here:

&#x1f4c2; `social_network_data.json`
