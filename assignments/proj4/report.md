<!-- KaTeX -->
<script
  type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<script
  type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>

::: title
Impact of &OpenCurlyDoubleQuote;L&CloseCurlyDoubleQuote; train stations on
vehicle ownership in Chicago
:::

::: authors
Hendra Wijaya<br>
*Illlinois Institute of Technology*<br>
Chicago, USA<br>
hwijaya@hawk.illinoistech.edu
:::

:::: content
## Abstract

There are 125 "L" train stations in Chicago covering most community areas. Using
public data from the U.S. Census Bureau and the Illinois Secretary of State,
this report investigates the relationship between the presence of Chicago's "L"
train stations and vehicle ownership trends across different regions of the
city. Findings indicate that while vehicle ownership has increased across all
regions from 2009 to 2023, areas with new "L" train stations added between 2013
and 2018 experienced a temporary decline in vehicle ownership during that
period.

## Introduction

### Background

Based on initial observations, **55%** of Chicago community areas have at least
one station as of 2025. With the majority of areas covered by public transit,
specifically the "L" train system, it is hypothesized that regions with better
access to these stations will exhibit lower rates of vehicle ownership growth
or even a decline in ownership over time. It is important to consider that,
according to the 2024 CTA Annual Ridership Report, bus transit is more popular
in Chicago and also covers more areas than the rail system.<sup>[\[1\]]</sup>
However, the study will only focus on rail because bus routes change on demand,
making it less reliable for long-term analysis.

::: figure
$$
\begin{array}{l r}
  \hline
  \textbf{Annual Ridership} & \\\\
  \hdashline
  \textsf{Bus} & 161,699,361 \to 181,733,617 \color{green}{+12.4\\%} \\\\
  \textsf{Rail} & 117,477,140 \to 127,463,409 \color{green}{+8.5\\%} \\\\
  \hline
\end{array}
$$
<br>
<small>
  Table 1: Bus to rail annual ridership comparison from 2019 to 2024
</small>
:::

In another note, the CTA ridership plummeted in 2020 due to the COVID-19
pandemic, dropping from more than half of annual trips in 2020 to just
**197 million.** And though ridership has been gradually recovering, it remains
below pre-pandemic levels. To accommodate this change, the analysis will
increase the range of vehicle ownership data from the latest to the earliest
available year in the Census data.

::: figure
<img
  width="320px"
  alt="Screenshot 1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/screenshot1.png"/>
<br>
<small>
  Screenshot 1: CTA Annual Ridership Report from 2019 to 2024
</small>
:::

### Thesis statement

The presence of recently opened Chicago "L" train stations in community areas is
associated with lower growth rates in vehicle ownership from 2009 to 2023.

## Literature review

### Key concepts

Vehicle ownership is confirmed when an individual aged 16 years or older
possesses at least one passenger-type vehicle (cars, trucks or vans). This
definition is different from means of transportation to work, which counts
people who has access to a vehicle, including those who borrow or carpool.

### Related studies

Other studies, such as a recent Argonne National Lab study of CTA, have shown
that public transit access can reduce vehicle miles traveled by approximately
15%, supporting the hypothesis.<sup>[\[2\]]</sup><sup>[\[3\]]</sup> The vision
of more accessible public transit is also shared by city planners in its GO TO
2040 plan, which, among other goals, aims for expansion of several rail line
extensions. Unfortunately, a Transit Ridership Growth Study by CMAP in reveals
that they are currently not on track to meet the public transit usage goal.<sup>[\[4\]]</sup>

## Methodology

### Data sources

The ACS 5-Year Estimates provide vehicle ownership statistics for the population
16 years and over. The latest available ACS data from the Census Bureau is from
2023. At 5-year intervals, the previous datasets are from 2018 and 2013, and end
in 2009 (2008 data is not available). In comparison, the Decennial Census data
reports population counts every 10 years. Although the Decennial data is
available from 2000, only the 2010 and 2020 datasets align with the ACS data
range.

- Chicago Data Portal<sup>[\[5\]]</sup>
- Chicago "L".org<sup>[\[6\]]</sup>
- Illinois Secretary of State<sup>[\[7\]]</sup>
- U.S. Census<sup>[\[8\]]</sup><sup>[\[9\]]</sup>

### Techniques

The research starts with manually mapping the locations of all Chicago "L" train
stations to their respective community areas into a JSON file. Then, create
another JSON file for total vehicle counts by county from the Illinois state
website.

::: figure
<img
  width="320px"
  alt="Figure 1.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/figure1_1.svg"/>
<br>
<small>
  Figure 1.1: Process #1
</small>
:::

Then, The tract IDs from the JSON file are then matched with Census API queries
to retrieve CSV files for population and vehicle ownership data. The specific
table IDs used here were obtained from the exercise in *Homework 4.*

::: figure
<img
  width="320px"
  alt="Figure 1.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/figure1_2.svg"/>
<br>
<small>
  Figure 1.2: Process #2
</small>
:::

Finally, generate the plots using the CSV files.

::: figure
<img
  width="240px"
  alt="Figure 1.3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/figure1_3.svg"/>
<br>
<small>
  Figure 1.3: Process #3
</small>
:::

## Findings

### Presentation

The Chicago population is mostly stable from 2010 to 2020, with most regions
experiencing less than **10%** change, except for the Central region, which saw a
significant increase of **72.7%.** In contrast, vehicle ownership has increased
substantially across all regions from 2009 to 2023, totalling a **19.5%** rise
citywide.

::: figure
<img
  width="320px"
  alt="Diagram 1.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/diagram1_1.svg"/>
<br>
<small>
  Diagram 1.1: Decennial result
</small>

<img
  width="320px"
  alt="Diagram 1.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/diagram1_2.svg"/>
<br>
<small>
  Diagram 1.2: ACS result
</small>
:::

::: figure
$$
\begin{array}{l c c c}
  \hline
  \textbf{Region} &
    \textbf{Population} &
    \textbf{Ownership} &
    \textbf{Stations} \\\\
  \hdashline
  \textsf{Central} & 86,830 & 149,977 & 24 \\\\
  & \downarrow & \downarrow & \downarrow \\\\
  & 12,355 & 26,517 & 26 \\\\
  & \color{green}{+72.7\\%} & \color{green}{+114.6\%} & \color{green}{+2} \\\\
  \textsf{Far North Side} & 487,023 & 97,646 & 22 \\\\
  & \downarrow & \downarrow & \\\\
  & 496,376 & 147,586 \\\\
  & \color{green}{+1.9\\%} & \color{green}{+51.2\\%} & \\\\
  \textsf{Far Southeast Side} & 197,740 & 43,904 & 3 \\\\
  & \downarrow & \downarrow & \\\\
  & 190,616 & 48,363 \\\\
  & \color{red}{-3.6\\%} & \color{green}{+10.2\\%} & \\\\
  \textsf{Far Southwest Side} & 177,974 & 44,231 & 0 \\\\
  & \downarrow & \downarrow & \\\\
  & 170,873 & 51,245 \\\\
  & \color{red}{-4.0\\%} & \color{green}{+15.9\\%} & \\\\
  \textsf{North Side} & 249,314 & 74,158 & 15 \\\\
  & \downarrow & \downarrow & \\\\
  & 263,286 & 56,717 \\\\
  & \color{green}{+5.6\\%} & \color{red}{-23.5\\%} & \\\\
  \textsf{Northwest Side} & 258,149 & 68,047 & 3 \\\\
  & \downarrow & \downarrow & \\\\
  & 255,451 & 90,038 \\\\
  & \color{red}{-1.0\\%} & \color{green}{+32.3\\%} & \\\\
  \textsf{South Side} & 180,341 & 36,517 & 14 \\\\
  & \downarrow & \downarrow & \\\\
  & 195,665 & 41,012 \\\\
  & \color{green}{+8.5\\%} & \color{green}{+12.3\\%} & \\\\
  \textsf{Southwest Side} & 338,135 & 88,419 & 8 \\\\
  & \downarrow & \downarrow & \\\\
  & 337,033 & 100,237 \\\\
  & \color{red}{-0.3\\%} & \color{green}{+13.4\\%} & \\\\
  \textsf{West Side} & 361,699 & 82,776 & 33 \\\\
  & \downarrow & \downarrow & \\\\
  & 363,453 & 93,118 \\\\
  & \color{green}{+0.5\\%} & \color{green}{+12.5\\%} & \\\\
  \hdashline
  \textbf{Total} & \textbf{2,637,205} & \textbf{547,753} & \textbf{122} \\\\
  & \downarrow & \downarrow & \downarrow \\\\
  & \textbf{2,632,730} & \textbf{654,832} & \textbf{125} \\\\
  & \color{red}{-0.2\\%} & \color{green}{+19.5\\%} & \color{green}{+3} \\\\
  \hline
\end{array}
$$
<br>
<small>
  Table 2: Population, vehicle ownership, and "L" train stations by region from
  2010 to 2020
</small>
:::

### Analysis

Using the growth rates calculated above, we can analyze the correlation network
graphs. Positive correlations are observed for vehicle ownership in most
regions, except for the North Side, which shows a negative correlation to every
other region.

::: figure
<img
  width="320px"
  alt="Diagram 2.1"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/diagram2_1.svg"/>
<br><small>Diagram 2.1: Decennial network graph</small>

<img
  width="320px"
  alt="Diagram 2.2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/diagram2_2.svg"/>
<br><small>Diagram 2.2: ACS network graph</small>
:::

Despite having abundant "L" train stations, the Far North Side exhibits a high
increase in vehicle ownership relative to its population growth, potentially
disputing the initial hypothesis. However, since the analysis focuses on growth
rates rather than absolute numbers, it is possible that areas with already high
vehicle ownership may continue to see increases, regardless of public transit
availability.

::: figure
<img
  width="320px"
  alt="Diagram 3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/diagram3.svg"/>
<br><small>Diagram 3: Regional working population heatmap</small>
:::

## Conclusion

### Summary

Looking at the map, it is apparent that only the Central and West Side regions
have at least one new "L" train station added between 2010 and 2020. Both
regions experienced significant growth in vehicle ownership. However, looking at
5-year intervals, it is apparent that the end results are heavily influenced by
the COVID-19 pandemic.

::: figure
<img
  width="240px"
  alt="Figure 2"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/figure2.svg"/>
<br><small>Figure 2: Chicago map with results</small>
:::

Narrowing down to the specific community areas that had new stations added, it
is apparent that Loop, Near West Side and Near South Side had reduced vehicle
ownership by **4.5%** from 2013 to 2018. This time period coincides with the
opening of new stations in these areas, as illustrated by the dotted lines
below. The 5-year period when no new stations were introduced saw significant
increases in vehicle ownership, peaking at the latest data from 2023.

::: figure
<img
  width="100%"
  alt="Figure 3"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/figure3.svg"/>
<br><small>Figure 3: Vehicle ownership trends in selected community areas</small>
:::

::: figure
$$
\begin{array}{l r r r r}
  \hline
  \textbf{Area} &
    \textbf{Ownership 2009} &
    \textbf{2013} &
    \textbf{2018} &
    \textbf{2023} \\\\
  \hdashline
  \textsf{Near West Side} & 4,822 & 5,845 & 5,803 & 6,791 \\\\
  &
    &
    \color{green}{+21.2\\%} &
    \color{red}{-0.7\\%} &
    \color{green}{+17.0\\%} \\\\
  \textsf{Near South Side} & 1,262 & 1,276 & 821 & 7,966 \\\\
  &
    &
    \color{green}{+1.1\\%} &
    \color{red}{-35.7\\%} &
    \color{green}{+870.4\\%} \\\\
  \textsf{Loop} & 896 & 1,097 & 1,226 & 3,602 \\\\
  &
    &
    \color{green}{+22.4\\%} &
    \color{green}{+11.8\\%} &
    \color{green}{+193.8\\%} \\\\
  \hdashline
  \textbf{Total} &
    \textbf{6,980} &
    \textbf{8,218} &
    \textbf{7,850} &
    \textbf{18,359} \\\\
  &
    &
    \color{green}{+17.7\\%} &
    \color{red}{-4.5\\%} &
    \color{green}{+133.9\\%} \\\\
  \hline
\end{array}
$$
<br>
<small>
  Table 3: Vehicle ownership growth in selected community areas
</small>
:::

In this normalized comparison, the green solid line represents vehicle ownership
growth in the selected areas with new stations. It is evident that the
introduction of new "L" train stations has a mitigating effect on vehicle
ownership growth, compared to the overall city trend represented by the blue
dashed line. Nevertheless, the long-term trend of citywide vehicle ownership is
still lower than the selected areas.

Interestingly, the Illinois Secretary of State vehicle registration data shows a
decline in total vehicle counts in Chicago from 2009 to 2023, while access to
personal vehicles has increased. This suggests Chicago residents may be opting
for fewer vehicles per household. While this could be influenced by better
public transit options, other factors such as remote work trends and economic
considerations may also play a role.

::: figure
<img
  width="100%"
  alt="Diagram 4"
  src="https://github.com/hanggrian/IIT-CS579/raw/assets/assignments/proj4/diagram4.svg"/>
<br><small>Diagram 4: Normalized vehicle ownership to vehicle counts</small>
:::

### Future research

Future work could explore additional socioeconomic factors that may influence
vehicle ownership trends, such as income levels, housing density, and employment
patterns. Additionally, incorporating bus transit data could provide a more
comprehensive understanding of public transportation's impact on vehicle
ownership. Finally, qualitative studies involving surveys or interviews with
residents could offer insights into personal transportation choices and the role
of public transit in their decision-making processes.

## Acknowledgements

This project uses techniques learned throughout the course
*CS 579: Online Social Network Analysis*. I thank Professor C. Hood for guiding
me to include relevant data points, particularly the total population as a key
comparison metric. To conclude the report, I would like to share an inspiring
quote on public transportation:

> &OpenCurlyDoubleQuote;We can’t just hope that people will use public
  transport; we have to provide a high-quality service that people want to
  use.&CloseCurlyDoubleQuote;
>
> *&mdash; Janette Sadik-Khan, former Commissioner of the New York City
  Department of Transportation (2020)*

::: references
## References

1.  [Chicago Transit Authority: Annual Ridership Report Calendar Year 2024][\[1\]]
1.  [Argonne National Lab: Mobility, Equity, and Economic Impact of Transit in Chicago Region][\[2\]]
1.  [Argonne National Lab Press Release: Argonne-led study highlights public transit’s critical role across Chicago][\[3\]]
1.  [Chicago Metropolitan Agency for Planning: Transit Ridership Growth Study][\[4\]]
1.  [Chicago Data Portal: Community Area Boundaries][\[5\]]
1.  [Chicago "L".org][\[6\]]
1.  [Illinois Secretary of State: Vehicle Statistics][\[7\]]
1.  [U.S. Census Bureau: Decennial Data][\[8\]]
1.  [U.S. Census Bureau: ACS 5-Year Estimates][\[9\]]
:::
::::

[\[1\]]: https://www.transitchicago.com/assets/1/6/2024_Annual_Ridership_Report.pdf
[\[2\]]: https://www.anl.gov/taps/reference/mobility-equity-and-economic-impact-of-transit-in-chicago-region/
[\[3\]]: https://www.anl.gov/article/argonneled-study-highlights-public-transits-critical-role-across-chicago/
[\[4\]]: https://cmap.illinois.gov/wp-content/uploads/Transit-Ridership-Growth-Study_final.pdf
[\[5\]]: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-Map/cauq-8yn6/
[\[6\]]: https://chicago-l.org/
[\[7\]]: https://ilsos.gov/departments/vehicles/statistics/lpcountycounts.html
[\[8\]]: https://census.gov/data/developers/data-sets/decennial-census.html
[\[9\]]: https://census.gov/data/developers/data-sets/acs-5year.html
