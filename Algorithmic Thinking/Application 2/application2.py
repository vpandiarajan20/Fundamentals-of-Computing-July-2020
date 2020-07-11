"""
Provided code for Application portion of Module 2
Vignesh P
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
# import simpleplot
# import codeskulptor
# codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt
############################################
# Code from project
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
            if (node in remaining_nodes):
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
        if (len(component) > length):
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


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm

    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that each node number
        appears in correct ratio

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        # update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[: -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1: -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


# print load_graph(NETWORK_URL)
##########################################################
# Code for creating sample graphs

# complete undirected graphs
def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary corresponding to a complete UNDIRECTED graph with the specified number of nodes.
    A complete graph contains all possible edges subject to the restriction that self-loops are not allowed.
    The nodes of the graph should be numbered  to num_nodes - 1 when num_nodes is positive.
    Otherwise, the function returns a dictionary corresponding to the empty graph.
    :param num_nodes: number of nodes
    :return: dictionary
    """
    return_value = dict()
    if (num_nodes < 0):
        return return_value
    for dummy_index1 in range(num_nodes):
        nodes = list(range(num_nodes))
        nodes.remove(dummy_index1)
        return_value[dummy_index1] = set(nodes)
    return return_value

    # undirected graphs with probability


def ER_Graph(num_nodes, probability):
    count = 0
    return_value = dict()
    # early break condition
    if (num_nodes < 0):
        return return_value
    # creates all keys, initialize to empty set
    for node in range(num_nodes):
        return_value[node] = set()
    # creates edges
    for node in range(num_nodes):  # iterates through every node
        # creates list that stores all other nodes
        # this list doesn't include nodes that came before this node because that would effectively 
        # double the probability, for example if an edge wasn't established between 1 and 2 
        # when 1 was the primary node, it shouldn't have another chance when 2 is the primary node
        other_nodes = range(node + 1, num_nodes)
        # for all nodes in other_nodes generates link based on probability
        for other_node in other_nodes:
            RNG = random.randrange(1 / probability)
            if (RNG == 0):
                return_value[node].add(other_node)
                return_value[other_node].add(node)
                count += 1
    return return_value

    # UPA Graphs


def upa_graph(m, n):
    # step 1: make a complete graph with m nodes
    graph_dic = make_complete_graph(m)

    graph = UPATrial(m)

    # step 2: add to graph from m to n nodes, one node per iteration
    # for each iteration, add m out-degree to each new node

    for i in range(m, n):
        graph_dic[i] = graph.run_trial(m)
        for node in graph_dic[i]:
            graph_dic[node].add(i)
    return graph_dic


##########################################################
# Question 1
# p = 0.003969, found by dividing 3047 by the sum of 1, 2, .. 1237, 1238
# the sequence going to 1238 is the number of comparisons, 3047 is number of edges
# m*n is the number of edges in a UPA graph, m is between 2 or 3

# helper function, count edges in a graph
def count_edges(ugraph):
    number_of_edges = 0
    for key in ugraph.keys():
        number_of_edges += len(ugraph[key])
    return number_of_edges / 2

    # returns nodes of the graph in a random order


def random_order(ugraph):
    keys = ugraph.keys()
    return_value = list()
    for dummy_index in range(len(ugraph)):
        random_remove = random.choice(keys)
        keys.remove(random_remove)
        return_value.append(random_remove)
    return return_value

"""
firstGraph = ER_Graph(1239, 0.004)
firstGraphResilience = compute_resilience(firstGraph,random_order(firstGraph))

secondGraph = upa_graph(2, 1239)
secondGraphResilience = compute_resilience(secondGraph,random_order(secondGraph))

computerNetwork = load_graph(NETWORK_URL)
computerNetworkResilience = compute_resilience(computerNetwork, random_order(computerNetwork))

line1 = plt.plot(firstGraphResilience, label="ER Graph, P = 0.004 " )
line2 = plt.plot(secondGraphResilience, label="UPA Graph, M = 2")
line3 = plt.plot(computerNetworkResilience, label="Computer Network")
plt.legend()
plt.xlabel('Number of nodes removed')
plt.ylabel('Longest chain')
plt.title('Resilience of different graphs with a random attack order')
plt.savefig("Application2Q1.png")
"""
##########################################################
# Question 3
def fast_targeted_order(ugraph):
    new_graph = copy_graph(ugraph)
    degree_sets = dict()
    for dummy_index in range(len(new_graph)):  #O(n)
        degree_sets[dummy_index] = set()
    for dummy_index in range(len(new_graph)):  #O(n)
        d = len(new_graph[dummy_index])
        degree_sets[d].add(dummy_index)
    L = list()
    i = 0
    for dummy_index in range(len(new_graph)-1, -1, -1): #O(n)
        while len(degree_sets[dummy_index]) != 0:
            u = degree_sets[dummy_index].pop()
            for neighbor in new_graph[u]:
                d = len(new_graph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d-1].add(neighbor)
            L.insert(i, u)
            i += 1
            delete_node(new_graph,u)
    return L

# big O bound of targeted_order is O(n^2)
# big O bound of fast_targeted_order is O(n)
"""
fast_targeted_order_timing = dict()
targeted_order_timing = dict()
for dummy_index in range(10, 1000, 10):
    test_graph = upa_graph(5,dummy_index)
    pre_fast_targeted_order_time = time.time()
    fast_targeted_order(test_graph)
    fast_targeted_order_timing[dummy_index/10] = time.time() - pre_fast_targeted_order_time
    pre_targeted_order_time = time.time()
    targeted_order(test_graph)
    targeted_order_timing[dummy_index/10] = time.time() - pre_targeted_order_time


line1 = plt.plot(fast_targeted_order_timing.values(), label="fast_targeted_order Timing")
line2 = plt.plot(targeted_order_timing.values(), label="targeted_order Timing")
plt.legend()
plt.xlabel('M value / 10')
plt.ylabel('Runtime')
plt.title('Regular vs. Fast Targeted order, Pycharm implementation')
plt.savefig("Application2Q3.png")
"""

##########################################################
# Question 4

firstGraph = ER_Graph(1239, 0.004)
firstGraphResilience = compute_resilience(firstGraph, fast_targeted_order(firstGraph))

secondGraph = upa_graph(2, 1239)
secondGraphResilience = compute_resilience(secondGraph, fast_targeted_order(secondGraph))

computerNetwork = load_graph(NETWORK_URL)
computerNetworkResilience = compute_resilience(computerNetwork, targeted_order(computerNetwork))

line1 = plt.plot(firstGraphResilience, label="ER Graph, P = 0.004")
line2 = plt.plot(secondGraphResilience, label="UPA Graph, M = 2")
line3 = plt.plot(computerNetworkResilience, label="Computer Network")
plt.legend()
plt.xlabel('Number of nodes removed')
plt.ylabel('Longest chain')
plt.title('Resilience of different graphs with a targeted attack order')
plt.savefig("Application2Q4.png")
