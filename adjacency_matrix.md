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
>   A & \infty & 5 & \infty & \infty & \infty \\
>   B & 5 & \infty & 7 & 10 & \infty \\
>   C & \infty & 7 & \infty & 3 & \infty \\
>   D & \infty & 10 & 3 & \infty & 6 \\
>   E & \infty & \infty & \infty & 6 & \infty \\
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
>   A & \infty & 5 & \infty & \infty & \infty \\
>   B & \infty & \infty & 7 & 10 & \infty \\
>   C & \infty & \infty & \infty & 3 & \infty \\
>   D & \infty & \infty & \infty & \infty & 6 \\
>   E & \infty & 2 & \infty & \infty & \infty \\
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
