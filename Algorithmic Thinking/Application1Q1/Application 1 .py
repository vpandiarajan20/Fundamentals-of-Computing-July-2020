"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import simpleplot
import math
import random
# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

#citation_graph = load_graph(CITATION_URL)
###################################
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

###################################
# All other code

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
    takes in directed graph
    returns normalized in degree distribution
    """
    distribution = in_degree_distribution(digraph)
    if(0 in distribution.keys()):
        distribution.pop(0)
    count = sum(distribution.values())
    return_value = dict()
    for element in distribution:
        return_value[element] = distribution[element] / float(count)
    return return_value

def algorithim_ER(n, p):
    v = dict()
    for index in range(n):
        v[index] = 0
    for index_i in range(n):
        all_other_elements = range(index_i)
        all_other_elements.extend(range(index_i+1, n))
        for index_j in all_other_elements:
            a = random.random()
            if(a > p):
                if(v[index_i] == 0):
                    v[index_i] = set([index_j])
                else:
                    v[index_i].update(set([index_j]))
    return v
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

    
EX_GRAPH2 = dict([(0, set([1,4,5])), (1, set([2,6])), (2, set([3, 7])), (3, set([7])),
                  (4, set([1])), (5, set([2])), (6, set()), (7, set([3])), (8, set([1, 2])),
                  (9, set([0, 3, 4, 5, 6, 7]))])
algorithim = algorithim_ER(50, 0.5)
x = normalize_distribution(algorithim)
print x

## Plotting
plot1 = build_plot(x.keys(), x.values(), STANDARD)

simpleplot.plot_scatter("Normalized in-degree distribution on a log/log scale, log e", 800, 800, 
                     "Number of citations (log e)", "Fraction of papers (log e)", [plot1])



