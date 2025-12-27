# Python-path-finder


An interactive pathfinding visualizer built with Python and Pygame that demonstrates how A* and Dijkstra’s Algorithm work on a grid-based environment.
Users can place start/end nodes, draw obstacles, and watch each algorithm explore the grid in real time.


**Features**

- Visualizes A* (heuristic-based) and Dijkstra’s Algorithm (uninformed search)
- Interactive grid with mouse controls
- Real-time animation of start, end, and final path nodes
- Ability to switch algorithms during runtime


**Tech used**
- Python
- Pygame
- Priority Queue (Heap based)
- Object oreiented programming


**How the project works**

The grid is made up of individual nodes (spots).
Each node stores its position, state, and valid neighbors.

A* uses:
- g_score: distance from start
- h: Manhattan distance heuristic
- f_score = g + h

Dijkstra’s Algorithm uses:
- Actual distance from the start only (no heuristic)

The algorithms progressively explore nodes and visually update their state until the shortest path is found.





**Installation Guide**
Pygame will depend on the OS you are using. After installation, download or clone this repo and run the following:
*python3 algorithm.py*




**Controls**

Left click:
- Place start node
- Place end node
- Place barriers

Right click:
- Remove nodes

Space:
- Run selected algorithm

D: Toggle between A* or Dijkstra

C: Clear


**Legend**

- Orange — Start node
- Turquoise — End node
- Black — Barrier
- Green — Open set (nodes to be evaluated)
- Red — Closed set (already evaluated nodes)
- Purple — Final shortest path\
- White — Empty cell



