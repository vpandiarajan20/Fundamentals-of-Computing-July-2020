#Application 1 Part 3-4

import random
import alg_dpa_trial as alg
import simpleplot
import math

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary corresponding to a complete directed graph with the specified number of nodes.
    A complete graph contains all possible edges subject to the restriction that self-loops are not allowed.
    The nodes of the graph should be numbered  to num_nodes - 1 when num_nodes is positive.
    Otherwise, the function returns a dictionary corresponding to the empty graph.
    :param num_nodes: number of nodes
    :return: dictionary
    """
    return_value = dict()
    if(num_nodes < 0):
        return return_value
    for dummy_index1 in range(num_nodes):
        nodes = list(range(num_nodes))
        nodes.remove(dummy_index1)
        return_value[dummy_index1] = set(nodes)
    return return_value


def dpa_graph(n,m):

    # step 1: make a complete graph with m nodes
    graph_dic = make_complete_graph(m)

    graph = alg.DPATrial(m)

    # step 2: add to graph from m to n nodes, one node per iteration
    # for each iteration, add m out-degree to each new node

    for i in range(m, n):
        graph_dic[i] = graph.run_trial(m)

    return graph_dic

def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) and computes the in-degrees for the nodes in the
    graph. The function should return a dictionary with the same set of keys (nodes) as digraph whose corresponding
    values are the number of edges whose head matches a particular node.
    :param digraph: directed graph
    :return: stated above
    """
    return_value = dict()
    for key in digraph.keys():
        return_value[key] = 0
    for value in digraph.values():
        for head in value:
            return_value[head] += 1
    return return_value

def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph.
    The function should return a dictionary whose keys correspond to in-degrees of nodes in the graph.
    The value associated with each particular in-degree is the number of nodes with that in-degree.
    In-degrees with no corresponding nodes in the graph are not included in the dictionary.
    :param digraph:
    :return:
    """
    in_degrees = compute_in_degrees(digraph)
    return_value = dict()
    for value in in_degrees.values():
        if value not in return_value.keys():
            return_value[value] = 1
        else:
            return_value[value] += 1
    return return_value

def normalize_distribution(digraph):
    """
    takes in in_degree_distribution graph
    returns normalized in degree distribution
    """
    count = sum(digraph.values())
    return_value = dict()
    for element in digraph:
        return_value[element] = digraph[element] / float(count)
    return return_value
# Code for plotting

# Plot options
STANDARD = True
LOGLOG = False

def build_plot(inputs, outputs, plot_type = STANDARD):
    """
    Insert input and output values
    appends to an list
    returns list
    """
    plot = []
    for dummy_index in range(len(inputs)):
        if plot_type == STANDARD:
            plot.append([inputs[dummy_index], outputs[dummy_index]])
        else:
            plot.append([math.log(inputs[dummy_index],10), math.log(outputs[dummy_index],10)])
    return plot

#print dpa_graph(100, 13)

citation_graph = dpa_graph(27770, 13)
citation_dic = in_degree_distribution(citation_graph)

# create a normalized in-degree distribution

x = normalize_distribution(citation_dic)

plot1 = build_plot(x.keys(), x.values(), LOGLOG)

simpleplot.plot_scatter("Normalized in-degree distribution for DPA graph on a log/log scale, log 10", 800, 800, 
                     "Number of edges (log 10)", "Fraction of nodes (log 10)", [plot1])


