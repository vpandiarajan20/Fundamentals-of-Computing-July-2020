"""
Project 2:
Vignesh P
"""

#Project 2
import random

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node 
    start_node and returns the set consisting of all nodes that are 
    visited by a breadth-first search that starts at start_node.
    """
    queue = list()
    visited = set()
    visited.add(start_node)
    queue.append(start_node)
    while len(queue) != 0:
        popped = queue.pop(0)
        for neighbor_h in ugraph[popped]:
            if (neighbor_h not in visited):
                visited.add(neighbor_h)
                queue.append(neighbor_h)
    return visited

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of 
    sets, where each set consists of all the nodes 
    (and nothing else) in a connected component, and there is
    exactly one set in the list for each connected component 
    in ugraph and nothing else.
    """
    remaining_nodes = list()
    remaining_nodes.extend(ugraph.keys())
    connect_components = list()
    while len(remaining_nodes) != 0:
        initial = random.choice(remaining_nodes)
        visited = bfs_visited(ugraph, initial)
        connect_components.append(visited)
        for node in visited:
            if(node in remaining_nodes):
                remaining_nodes.remove(node)
    return connect_components
def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (an integer) 
    of the largest connected component in ugraph.
    """
    connected_components = cc_visited(ugraph)
    length = 0
    for component in connected_components:
        if(len(component) > length):
            length = len(component)
    return length
def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order and
    iterates through the nodes in attack_order. For each node in the 
    list, the function removes the given node and its edges from the 
    graph and then computes the size of the largest connected component 
    for the resulting graph. The function should return a list whose 
    k + 1th entry is the size of the largest connected component in 
    the graph after the removal of the first kk nodes in attack_order. 
    The first entry (indexed by zero) is the size of the largest 
    connected component in the original graph.
    """
    largest_components = list()
    largest_components.append(largest_cc_size(ugraph))
    for node in attack_order:
        ugraph.pop(node)
        for value in ugraph.values():
            if node in value:
                value.remove(node)
        largest_components.append(largest_cc_size(ugraph))
    return largest_components
    
    
EX_GRAPH1 = dict([(0, set([1,4,5])), 
                  (1, set([2])), 
                  (2, set([3])), 
                  (3, set([0])),
                  (4, set([1])), 
                  (5, set([2])), 
                  (6, set())])

GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}


print compute_resilience(GRAPH0, [1,2])