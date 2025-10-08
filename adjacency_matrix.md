# Adjacency matrix

## Undirected

Undirected graphs are symmetric.

### Unweighted

> $$
> \def\arraystretch{1.5}
> \begin{array}{c|c:c:c:c:c:c}
>     & A & B & C & D \\ \hline
>   A & 0 & 1 & 0 & 0 \\
>   B & 1 & 0 & 1 & 0 \\
>   C & 0 & 1 & 0 & 1 \\
>   D & 0 & 0 & 1 & 0 \\
> \end{array}
> $$

```mermaid
graph LR
  A((A)) -- 1 --- B((B))
  B -- 1 --- C((C))
  C -- 1 --- D((D))
```

### Weighted

> $$
> \def\arraystretch{1.5}
> \begin{array}{c|c:c:c:c:c:c}
>     & A & B & C & D & E \\ \hline
>   A & \infin & 5 & \infin & \infin & \infin \\
>   B & 5 & \infin & 7 & 10 & \infin \\
>   C & \infin & 7 & \infin & 3 & \infin \\
>   D & \infin & 10 & 3 & \infin & 6 \\
>   E & \infin & \infin & \infin & 6 & \infin \\
> \end{array}
> $$

```mermaid
graph LR
  A((A)) -- 5 --- B((B))
  B -- 7 --- C((C))
  B -- 10 --- D((D))
  C -- 3 --- D((D))
  D -- 6 --- E((E))
```

## Directed

Directed graphs are not necessarily symmetric.

### Unweighted

> $$
> \def\arraystretch{1.5}
> \begin{array}{c|c:c:c:c:c:c}
>     & A & B & C & D \\ \hline
>   A & 0 & 1 & 0 & 0 \\
>   B & 0 & 0 & 1 & 0 \\
>   C & 0 & 0 & 0 & 1 \\
>   D & 0 & 1 & 0 & 0 \\
> \end{array}
> $$

```mermaid
graph LR
  A((A)) --> B((B))
  B --> C((C))
  C --> D((D))
  D --> B((B))
```

### Weighted

> $$
> \def\arraystretch{1.5}
> \begin{array}{c|c:c:c:c:c:c}
>     & A & B & C & D & E \\ \hline
>   A & \infin & 5 & \infin & \infin & \infin \\
>   B & \infin & \infin & 7 & 10 & \infin \\
>   C & \infin & \infin & \infin & 3 & \infin \\
>   D & \infin & \infin & \infin & \infin & 6 \\
>   E & \infin & 2 & \infin & \infin & \infin \\
> \end{array}
> $$

```mermaid
graph LR
  A((A)) -- 5 --> B((B))
  B -- 7 --> C((C))
  B -- 10 --> D((D))
  C -- 3 --> D((D))
  D -- 6 --> E((E))
  E -- 2 --> B((B))
```
