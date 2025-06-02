import math
import networkx as nx
import numpy as np


def maze_to_graph(is_wall, allowed_steps):
    node_idx = list(range(np.sum(~is_wall)))
    node_pos = list(zip(*np.where(~is_wall)))
    pos2idx = dict(zip(node_pos, node_idx))

    g = nx.DiGraph()

    for (i, j) in node_pos:
        for (delta_i, delta_j) in allowed_steps:  
            if (i + delta_i, j + delta_j) in pos2idx: 
                g.add_edge((i, j), (i + delta_i, j + delta_j),
                           weight=int((round((math.sqrt(abs(delta_i) + abs(delta_j))), 1)) * 10))

    idx2pos = dict(zip(node_idx, node_pos))
    return g, idx2pos, pos2idx

def A_star(map, begin, end):
    steps = [(0, 1),  # right
             (-1, 1),  # diagonal up-right
             (-1, 0),  # up
             (-1, -1),  # diagonal up-left
             (0, -1),  # left
             (1, -1),  # diagonal down-left
             (1, 0),  # down
             (1, 1)]  # diagonal down-right

    g, idx2pos, pos2idx = maze_to_graph(map.astype(bool), steps)

    path = nx.astar_path(g, begin, end)
    return(path)