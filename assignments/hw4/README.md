<!-- KaTeX -->
<script
  type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<script
  type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>

# [Homework 4](https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4.pdf)

> For part 1, you should compare a few variables from the decennial census in
  2010 and the decennial census in 2020:
>
> - Population
> - Demographic
>
> Links for mapping Chicago Community Areas to census tracts:
>
> - [2020 Decennial Census](http://robparal.blogspot.com/)
> - [2010 Decennial Census](http://robparal.blogspot.com/2012/04/census-tracts-in-chicago-community.html)

Based on the decennial census data from 2010 and 2020, community area code 18
is Montclare with tracts **180100** and **831600.** The fetched data from the
Census API are filtered to include only these tracts in the given state (IL) and
county (Cook).

- **Selected community area:**

  18. Montclare
- **2010 tract to community area equivalency:**

  STUSAB | SUMLEV | COUNTY | COUSUB | PLACE | GEOID2 | CHGOCA | TRACT | NAME | Notes | Community
  --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | ---
  IL | 80 | 31 | 14000 | 14000 | 18180100 | 18 | **180100** | CA 18 Tract 180100 | | Montclare
  IL | 80 | 31 | 14000 | 14000 | 18831600 | 18 | **831600** | CA 18 Tract 831600 | | Montclare
- **2020 tract to community area equivalency:**

  GEOID20 | CA | COMMUNITY_1
  ---: | ---: | ---
  17031**180100** | 18 | Montclare
  17031**831600** | 18 | Montclare

> Each student has been assigned a Community Area (1-77) to explore. You will
  use data from [census.gov](https://www.census.gov/) to do an analysis of your
  CA using census data from the ACS (block group level) and decennial census
  (block level). Depending on the number of block groups in your CA, you may
  consider the broader geographic neighborhood of your CA as well (see
  instructions below).

The Census data can be accessed using the [census](https://pypi.org/project/census/)
Python package, provided that a valid API key is set in the `.env` file (not
tracked). Initially, the scripts fetch data and write it to CSV files.

<img
  width="320px"
  alt="Screenshot 1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/screenshot1.png">
<img
  width="320px"
  alt="Screenshot 2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/screenshot2.png">

After generating the CSV files, the table data are visualized using `matplotlib`
and `seaborn`. Hierarchical clustering and network graphs are created using
`networkx` with values computed by `scipy`.

<img
  width="320px"
  alt="Screenshot 3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/screenshot3.png">

## Problem 1

> A data-based characterization of your CA including the recent history (back
  to 2010) of your CA.

I am using the summary file endpoint `sf1` with variables such as `P001001`
(population) and `H001001` (housing units) for the [2010 Decennial](https://www.census.gov/data/developers/data-sets/decennial-census/2010.html) data. However, the summary file is not available in
the [2020 Decennial](https://www.census.gov/data/developers/data-sets/decennial-census/2020.html)
data. Instead, the redistricting data `pl` is used as a substitute with similar
table schemes and column names. There is also `acs5` based on [2019-2023 ACS
5-Year Estimates](https://www.census.gov/programs-surveys/acs/technical-documentation/table-and-geography-changes/2023/5-year.html), which are the most recent
available and represent block-group-level analysis of the community area.

## Problem 2

> A description of the data (i.e. variables) that you have chosen to use as the
  basis of your study along with a discussion of why you chose these variables
  and any preliminary analysis you did to narrow the data. You will choose at
  least 6 variables that are available at the block group level (i.e. from the
  ACS)

For block-level Decennial data from 2010 and 2020, the most important variables
are listed in the [Summary File 1 Dataset](https://www.census.gov/data/datasets/2010/dec/summary-file-1.html):

1.  `P001001` & `P1_001N`: General population
1.  `H001001` & `H1_001N`: Housing units

The full list of variables in the block-group-level ACS estimates is available
in the [Table Shells](https://www.census.gov/programs-surveys/acs/technical-documentation/table-shells.html). The variable structure is explained in the [Table ID Handbook](https://www.census.gov/content/dam/Census/library/publications/2021/acs/acs_summary_file_handbook_2021_ch03.pdf).
Below are my selected six variables, which cover various socioeconomic aspects,
ranging from income, race, transportation to education level:

1.  `B19013_001E`: Median household income
1.  `B17021_002E`: Population below poverty level
1.  `B03002_003E`: Hispanic or Latino population
1.  `B25003_002E`: Owner-occupied housing units
1.  `B08301_001E`: Workers 16+ with transportation
1.  `B15002_022E`: Population 25+ with Bachelor's degree

<img
  width="640px"
  alt="Figure 1.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/figure1_1.svg">
<img
  width="640px"
  alt="Figure 1.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/figure1_2.svg">

## Problem 3

> An analysis of similarity of the block groups that comprise your CA. If your
  CA has less than 60 block groups, you will add the block groups of geographic
  neighbors to get at least 60 block groups. This analysis should include
  modeling the block groups as a network.
>
> 1.  You will describe the modeling and analysis you did, stating assumptions
      and justifying decisions.

The block groups within community area 18 (Montclare) are analyzed based on
selected socioeconomic variables from the ACS data. The variables reflect the
six chosen variables from *Problem 2.* They also include additional topics to
provide a comprehensive view of the neighborhood, such as age, housing vacancy,
home market values, labor force participation and spoken language.

- `B01003_001E`: Total population
- `B01002_001E`: Median age
- `B03002_003E` & `B03002_004E`: White/Black alone population (non-Hispanic)
- `B25001_001E` & `B25002_003E`: Total/vacant housing units
- `B25077_001E` & `B25064_001E`: Median home value/gross rent
- `B23025_002E`: In labor force
- `B16001_002E` & `B16001_003E`: English only/Spanish speakers

<img
  width="640px"
  alt="Figure 2.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/figure2_1.svg">

> 2.  You will provide data-based arguments including visualizations to support
      why your CA is a community.

The socioeconomic profiles are visualized in a scatter plot using principal
component analysis, which generalizes the data into either Montclare or its
neighboring areas. Seeing that the distance between Montclare block groups is
smaller than that of the neighbors, it shows similarity across the selected
variables.

<img
  width="640px"
  alt="Figure 2.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/figure2_2.svg">

The table data can also be drawn as a network graph, where nodes that share
similar socioeconomic characteristics are connected by undirected edges.
Montclare nodes are densely connected internally, with few edges linking to
external nodes.

<img
  width="640px"
  alt="Figure 2.3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/figure2_3.svg">

> 3.  You will provide data-based arguments including visualizations to support
      why your CA is not a community.

The unclustered hierarchical plot shows that Montclare block groups are not
fully isolated: some neighbors occupy the same space. To dig deeper, apply
clustering of four groups using the `maxclust` criterion:

1.  Median household income
1.  Population 25+ with Bachelor's degree
1.  Hispanic or Latino population
1.  Vacant housing units

Since both Montclare and its neighbors are split across three clusters each, the
current area range does not reflect socioeconomic divisions.

<img
  width="640px"
  alt="Figure 2.4"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/figure2_4.svg">

> 4.  You will provide a proposal for alternative community(ies). If your CA has
      60 or more block groups, this will be a proposal for organizations of
      communities within your CA. If your CA has <60 block groups, you will
      propose an organization of block groups from your CA and neighbors
      (resulting in analysis of 60 or more). This proposal should include
      visualizations.

Based on the generated table data, Montclare has only 11 block groups, which is
less than the required 60. Therefore, an additional 18 neighboring block groups
are collected from adjacent community areas, totalling 29 block groups for the
analysis. Considering that Montclare block groups predominantly fall into the
same cluster as neighboring areas, I propose to define a larger community that
covers Montclare and its neighbors. The new community will have a similar
socioeconomic pattern and still has a considerably low amount of block groups.

<img
  width="640px"
  alt="Figure 2.5"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/hw4/figure2_5.svg">

## Problem 4

> If you are working in a team, there is an additional step where you will put
  all your data together and propose an organization of communities. Each team
  member must have a unique CA so if your team has duplicates, please email me
  asap.

No, I am not working in a team. I am evaluating community area 18 alone.

## Problem 5

> The above should be compiled into a report that includes citations and
  transcripts of any AI assistance. You will submit a pdf and code.

### Prompt 1

![Gemini 2.5 Flash][gemini-2.5-flash]

> Break down the variable code `B19013_001E` used in the ACS data. What does
  each part mean?

Understanding the structure of the code helps you find similar variables:

Code part | Example (`B19013_001E`) | Meaning
--- | --- | ---
**Prefix** | `B` | Indicates a **detailed table** (from `ACS` or `SF1`).
**Table ID** | `19013` | Specifies the **core subject** (e.g., `B19` tables are Income, `B01` are Age/Sex).
**Sequence** | `_001` | The **line number/sequence** within that table (e.g., 001 is often the TOTAL).
**Suffix** | `E` | Indicates the type of data: **estimate** (`E`) or **margin of error** (`M`).

### Prompt 2

![Gemini 2.5 Flash][gemini-2.5-flash]

> I can see in the [Table Shells](https://www.census.gov/programs-surveys/acs/technical-documentation/table-shells.html) that `B01001` is total population. But, where does the `_001E1` come from?

Here is the breakdown of why B01003 is the correct variable for total
population, and where that 001E comes from:

1.  Why `B01003` is Total Population:

    The Census Bureau organizes tables by their **Universe** (the population or
    group they measure).

    This table's universe is explicitly Total Population and has only one
    variable: the total count. It is the designated, most direct, and most
    efficient variable to pull when you only need the total population count for
    a given geography from the ACS.
1.  Where the `_001E` Comes From

    The suffix `_001E` is standard structure across almost all ACS tables and
    indicates the following:

    Code part | Meaning | Value in `B01003_001E`
    --- | --- | ---
    `_001` | **Sequence number** | Represents the **first line** of the table. In tables like `B01003` that only have a total, the first line is the total count.
    `E` | **Estimate** | Indicates this number is the **ACS Estimate** (the count itself). This is the value you use for calculations.
    `M` | **Margin of error** | If you requested the `M` suffix (e.g., `B01003_001M`), you would get the **margin of error** associated with the estimate.

Append the mandatory API sequence and estimate suffix to get the final code:
`B01003_001E`.

### Prompt 3

![Grok 4 0709][grok-4-0709]

> I am working on visualizing a network graph of block groups using `networkx`.
  How can `scipy` be used to calculate a percentile threshold to create a sparse
  graph?

To generate a meaningful and visually interpretable network of block groups, I
needed to connect only the most similar units while avoiding a dense, cluttered
graph. I achieved this by using `scipy` to compute pairwise Euclidean distances
between block groups based on standardized socioeconomic variables, then applied
a data-driven threshold using the 20th percentile of all distances. This ensures
that only the closest 20% of possible connections are retained, resulting in a
sparse graph that highlights local structure without overwhelming noise.

```py
from scipy

import numpy as np

# Standardize features
scaled = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

# Compute full pairwise Euclidean distance matrix
dist_matrix = cdist(scaled, scaled)

# Use 20th percentile as similarity threshold
threshold = np.percentile(dist_matrix.flatten(), 20)

# Build sparse graph
G = nx.Graph()
n = len(scaled)
for i in range(n):
    G.add_node(i, label=labels[i], is_montclare=is_montclare[i])
for i in range(n):
    for j in range(i + 1, n):
        if dist_matrix[i, j] < threshold:
            G.add_edge(i, j)
```

- `cdist`: Efficient $O(n^2)$ distance computation
- `np.percentile(..., 20)`: Adaptive, data-driven edge filtering
- Threshold validated via visual inspection at 10%, 20%, 30%

This percentile-based thresholding is a standard technique in network analysis
and dimensionality reduction, ensuring reproducibility and robustness across
datasets.

[gemini-2.5-flash]: https://img.shields.io/badge/llm-gemini--2.5--flash-4285F4
[grok-4-0709]: https://img.shields.io/badge/llm-grok--4--0709-black
