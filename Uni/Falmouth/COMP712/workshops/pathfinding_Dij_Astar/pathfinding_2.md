![Games Academy](../../../../Falmouth/common/ga_uni_logo.png)

# COMP712: Classical Artificial Intelligence 

# Workshop: Pathfinding (2)

Dr Daniel Zhang @ Falmouth University\
2023-2024 Study Block 1

![The Pathfinding Demo](ai_pathfinding_2.apng)

<div id="top"></div>

# Table of Contents
- [COMP712: Classical Artificial Intelligence](#comp712-classical-artificial-intelligence)
- [Workshop: Pathfinding (2)](#workshop-pathfinding-2)
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [`Dijkstra's` Algorithm](#dijkstras-algorithm)
  - [The Pseudocode](#the-pseudocode)
- [`A*` Algorithm](#a-algorithm)
  - [The Pseudocode](#the-pseudocode-1)
- [The Repository](#the-repository)
  - [The Code Structure](#the-code-structure)
- [Your Task](#your-task)
  - [Task 1: run the demos](#task-1-run-the-demos)
  - [Task 2: implement `BFS`](#task-2-implement-bfs)
  - [Task 3: implement `DFS`](#task-3-implement-dfs)
  - [Task 4: implement `GBFS`](#task-4-implement-gbfs)
  - [Task 5: different number of neighbours](#task-5-different-number-of-neighbours)
- [Further Reading](#further-reading)

# Introduction
[Top](#top)

This is the second workshop on the topic of pathfinding. After implementing `BFS`, `DFS`, and `GBFS`, you will focus on `Dijkstra's` and `A*` Algorithms in this session, which are very useful for pathfinding in **weighted** graphs.

**Note**: While the first workshop outlines three main tasks and this one has two, you have the flexibility to manage the content across the two workshops at your own pace. If you haven't completed the initial three implementations, it's recommended to continue working on those tasks before proceeding with the exercises assigned for this session.

# `Dijkstra's` Algorithm
[Top](#top)

`Dijkstra's` Algorithm, named after computer scientist [Edsger W. Dijkstra](https://www.wikiwand.com/en/Edsger_W._Dijkstra), stands as one of the fundamental algorithms in graph theory and network analysis. Primarily used to find the shortest path in a ***weighted*** graph, it operates effectively on graphs where all the edge weights are non-negative. The algorithm commences by designating a source node and initially assigning tentative distances to all other nodes, with the source set at zero and the rest at infinity. It then systematically explores neighbouring nodes, continually updating the shortest known distances from the source as it traverses the graph. Through a process of relaxation, where it reassesses and refines the distances, `Dijkstra's` Algorithm gradually reveals the shortest path from the source to every other node in the graph.

Its methodology revolves around a priority queue or min-heap, selecting the node with the smallest tentative distance as it proceeds, ensuring an efficient exploration of nodes in order of their shortest potential distance from the source. Dijkstra's Algorithm is a notable and widely implemented tool in network routing protocols, transportation networks, and various applications requiring efficient pathfinding in weighted graphs. Its simplicity, optimality for non-negative edges, and ability to efficiently find the shortest path make it a cornerstone in various computational fields.

> `BFS` can be considered as a special case of `Dijkstra's` Algorithm on unweighted graphs.

## The Pseudocode
[Top](#top)

The `Dijkstra's` algorithm can be presented using the following pseudocode[<sup>1</sup>](https://www.wikiwand.com/en/Dijkstra's_algorithm#Pseudocode):

```vb
function Dijkstra(Graph, source):
    for each vertex v in Graph.Vertices:
        dist[v] ← INFINITY
        prev[v] ← UNDEFINED
        add v to Q
    dist[source] ← 0
    
    while Q is not empty:
        u ← vertex in Q with min dist[u]
        if u is the target
            break
        remove u from Q
        
        for each neighbour v of u still in Q:
            alt ← dist[u] + Graph.Edges(u, v)
            if alt < dist[v]:
                dist[v] ← alt
                prev[v] ← u

    return dist[], prev[]
```

The following version of pseudocode[<sup>2</sup>](https://www.wikiwand.com/en/Dijkstra's_algorithm#Using_a_priority_queue) makes use of the `PriorityQueue` data structure we saw in the last workshop.

```vb
function Dijkstra(Graph, source):
    dist[source] ← 0                           // Initialisation
    create vertex priority queue Q
	
    for each vertex v in Graph.Vertices:
        if v ≠ source
            dist[v] ← INFINITY                 // Unknown distance from source to v
            prev[v] ← UNDEFINED                // Predecessor of v
        Q.add_with_priority(v, dist[v])
		
    while Q is not empty:                      // The main loop
        u ← Q.extract_min()                    // Remove and return best vertex
        if u is the target:
            break
        for each neighbour v of u:              // Go through all v neighbours of u
            alt ← dist[u] + Graph.Edges(u, v)
            if alt < dist[v]:
                dist[v] ← alt
                prev[v] ← u
                Q.decrease_priority(v, alt)
    return dist[], prev[]
```

# `A*` Algorithm
[Top](#top)

The `A*` algorithm, renowned for its heuristic-based approach to pathfinding, stands as a pivotal algorithm in computer science, particularly in traversing ***weighted*** graphs and searching for the shortest path. Building on the foundation of `Dijkstra's` Algorithm, `A*` integrates a heuristic function that guides its exploration, enabling more informed decisions about which paths to explore. This heuristic estimates the distance from the current node to the target node, influencing the algorithm to prioritize paths that appear to be closer to the goal. `A*` uses a blend of two types of costs for each node: the `actual cost` from the start node to the current node (known as the '`g`' value) and the `estimated cost` from the current node to the target (the '`h`' value).

`A*` balances between the '`g`' and '`h`' values, aiming to minimise the total estimated cost ('`f`' value) for reaching the destination node. It traverses the graph by expanding the nodes with the lowest '`f`' values, effectively combining the benefits of both `Dijkstra's` Algorithm and `greedy best-first` search. This integration of a heuristic function ensures efficiency by favouring paths that appear to be more promising, significantly reducing the number of nodes explored compared to uninformed search algorithms. The `A*` algorithm's adaptability to various domains, its optimality under certain conditions, and its balance between completeness and efficiency have made it a cornerstone in various applications, such as route planning, game AI, and robotics.

> The `A*` algorithm is a generalisation of `Dijkstra's` algorithm that cuts down on the size of the subgraph that must be explored, if additional information is available that provides a lower bound on the "distance" to the target.

## The Pseudocode
[Top](#top)


```c++
function reconstruct_path(cameFrom, current)
    total_path := {current}
    while current in cameFrom.Keys:
        current := cameFrom[current]
        total_path.prepend(current)
    return total_path

// A* finds a path from start to goal.
// h is the heuristic function. h(n) estimates the cost to reach goal from node n.
function A_Star(start, goal, h)
    // The set of discovered nodes that may need to be (re-)expanded.
    // Initially, only the start node is known.
    // This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet := {start}

    // For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
    // to n currently known.
    cameFrom := an empty map

    // For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore := map with default value of Infinity
    gScore[start] := 0

    // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    // how cheap a path could be from start to finish if it goes through n.
    fScore := map with default value of Infinity
    fScore[start] := h(start)

    while openSet is not empty
        // This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_path(cameFrom, current)

        openSet.Remove(current)
        for each neighbor of current
            // d(current,neighbor) is the weight of the edge from current to neighbor
            // tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore := gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]
                // This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := tentative_gScore + h(neighbor)
                if neighbor not in openSet
                    openSet.add(neighbor)

    // Open set is empty but goal was never reached
    return failure
```

# The Repository
[Top](#top)

This repository contains the materials for COMP712 - Pathfinding (1) workshop.

> **[https://github.falmouth.ac.uk/Daniel-Zhang/COMP712-Pathfinding-2.git](https://github.falmouth.ac.uk/Daniel-Zhang/COMP712-Pathfinding-2.git)**

There are three demos available:

- `demo_dijkstra.pyc`: Demonstrates Breadth-first search
- `demo_a_star.pyc`: Demonstrates Depth-first search
- 2 pre-defined maps are provided, which can be loaded by key <kbd>`L`</kbd>

## The Code Structure
[Top](#top)

The `gui_lib.py` file contains all the necessary GUI capabilities that shouldn't be altered. However, some functions might aid in pathfinding visualisation:

- `getValidNeighbour(Cell, direction):` Retrieves the neighbour on the specified `direction`.
  - `Cell` represents a cell object, while `direction` can be one of `east`, `north-east`, `north`, `north-west`, `west`, `south-west`, `south`, `south-east`.
- `colourCell(Cell, colour, ratio=0.8)`: Fills the specified `Cell` with the given `colour`. The default `ratio` is `0.8`, filling `80%` of the cell with the colour.
- The start and target cells are saved as `self.start` and `self.end`, while the finding path should be saved as a list of `Cell` objects in `self.path`.

Each algorithm should be implemented in its respective `.py` file:

- The `search()` function is mandatory in each file as the main lib relies on it for the search process. It should return `True` or `False` to indicate if a path can be found from `start` to `end`.
- Feel free to create additional helper functions as required.

# Your Task
[Top](#top)

## Task 1: run the demos
[Top](#top)

Run the demos to see how each of the algorithms work differently. You can either load the provided maps or create map by yourself. 

   - left-click to mark a block
   - right-click once to mark the start cell if no start defined
   - right-click again to mark the end cell if no end defined
   - right-click on any marked cell (start, end, or block) to reset the cell 
   - try to run the `demo_gbfs.pyc` with pre-defined map `map3.txt` to see how it can be simply trapped in the local optimal


## Task 2: implement `BFS`
[Top](#top)

- Complete the implementation of `BFS` algorithm in `bfs.py`. Again, you only need to make sure the `self.path` list has bee filled by `Cell` objects from the start to the end. Make use of the `parent` data field of the `Cell` class.
- **§** Run the `demo_bfs.pyc` with extra input parameters and compare the results. Think about where the differences come from.
  - `python demo_bfs.pyc 1`: which make the `BFS` search towards the target.
  - `python demo_bfs.pyc 2`: which randomly explore the surrounding area rather than searching by following a fixed order.
- Try to implement these two behaviour in your code.

> **RECALL**: 
> - The `self.search()` function is mandatory.
> - It should return `True` or `False` to indicate if a path can be found from `self.start` to `self.end`.
> - Make sure you fill up the `self.path` list with cells on the found path.
> - To enable animation, make use of the following code snippets in your `search()` function.
> ```python
> # other code blocks ...
> if self.animate:
>     self.animateCell(c)
>     self.update()
> # other code blocks ...
> ```

## Task 3: implement `DFS`
[Top](#top)

- Complete the implementation of `DFS`
- Compare the behaviour of `DFS` with `BFS` you implemented in the last task.
- **§** Run the `demo_dfs.pyc` with extra input parameters and compare the results. Think about where the differences come from.
  - `python demo_dfs.pyc 1`: which make the `DFS` search towards the target.
  - `python demo_dfs.pyc 2`: which randomly explore the surrounding area rather than searching by following a fixed order.
- Try to implement these two behaviour in your code.

## Task 4: implement `GBFS`
[Top](#top)

- complete the implementation of `GBFS` algorithm
- the heuristic function used in the `gbfs_demo.pyc` is the [Manhattan distance](https://www.wikiwand.com/simple/Manhattan_Distance). You can define your own heuristic function used as `Cell` priority.
- Compare the `GBFS` with `BFS` and `DFS` using the same map.
- Try to use other heuristic functions.

>**Note**: The `gui_lib.py` contains two helper functions that might assist in your implementation. Feel free to use alternative methods if preferred.

> - `getGridDist(c1, c2)`: Retrieves the Manhattan distance between two Cells by applying the equation `abs(c1.row - c2.row) + abs(c1.col - c2.col)`.
> - `getGridEuclideanDist2(c1, c2)`: Determines the squared Euclidean distance between two cells using the equation `(c1.row - c2.row)`<sup>2</sup> + `(c1.col - c2.col)`<sup>2</sup>. The actual Euclidean distance involves the `sqrt` operation, but for comparison purposes, the squared value is calculated for faster computation.
> - You can utilise Python's built-in data type `list` to serve as a priority queue by creating your own priority function if you prefer. Alternatively, the `PriorityQueue` class can be quite helpful in managing prioritised elements.

## Task 5: different number of neighbours
[Top](#top)

The default implementation focuses on exploring 4 neighbors around a given cell: north, south, east, and west. However, in certain games, characters are capable of moving in 8 different directions rather than just 4, as depicted in the image below.

![4-Neighbourhood vs 8-Neighbourhood](48_neighbourhood.png)
*Source: https://www.researchgate.net/publication/329579183_Membrane_Computing_for_Real_Medical_Image_Segmentation/figures?lo=1*

- To accommodate this, consider modifying your code to implement an 8-neighbourhood search and subsequently compare the outcomes with the 4-neighbourhood version.

**Note:**

You can submit a pull request to the original repository to showcase your work if you like.

# Further Reading
[Top](#top)

1. [MIT OpenCourse: Breadth-first Search](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-9-breadth-first-search/)
2. [Breadth-first Search with Example](https://www.guru99.com/breadth-first-search-bfs-graph-example.html#the-architecture-of-bfs-algorithm)
3. [MIT OpenCourse: Depth-first Search](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/f3e349e0eb3288592289d2c81e0c4f4d_MIT6_006S20_lec10.pdf)
4. [Introduction to DFS](https://www.baeldung.com/cs/depth-first-search-intro)
5. [Best-first Search Algorithm](https://iq.opengenus.org/best-first-search/)

