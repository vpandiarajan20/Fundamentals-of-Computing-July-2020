EX_GRAPH0 = dict([(0, set([1, 2])), (1, set()), (2, set())])EX_GRAPH1 = dict([(0, set([1,4,5])), (1, set([2,6])), (2, set([3])), (3, set([0])),                  (4, set([1])), (5, set([2])), (6, set())])EX_GRAPH2 = dict([(0, set([1,4,5])), (1, set([2,6])), (2, set([3, 7])), (3, set([7])),                  (4, set([1])), (5, set([2])), (6, set()), (7, set([3])), (8, set([1, 2])),                  (9, set([0, 3, 4, 5, 6, 7]))])def make_complete_graph(num_nodes):    """    Takes the number of nodes num_nodes and returns a dictionary corresponding to a complete directed graph with the specified number of nodes.    A complete graph contains all possible edges subject to the restriction that self-loops are not allowed.    The nodes of the graph should be numbered  to num_nodes - 1 when num_nodes is positive.    Otherwise, the function returns a dictionary corresponding to the empty graph.    :param num_nodes: number of nodes    :return: dictionary    """    return_value = dict()    if(num_nodes < 0):        return return_value    for dummy_index1 in range(num_nodes):        nodes = list(range(num_nodes))        nodes.remove(dummy_index1)        return_value[dummy_index1] = set(nodes)    return return_valuedef compute_in_degrees(digraph):    """    Takes a directed graph digraph (represented as a dictionary) and computes the in-degrees for the nodes in the    graph. The function should return a dictionary with the same set of keys (nodes) as digraph whose corresponding    values are the number of edges whose head matches a particular node.    :param digraph: directed graph    :return: stated above    """    return_value = dict()    for key in digraph:        count = 0        for dummy_index in digraph:            if(key in digraph[dummy_index]):                count = count + 1        return_value[key] = count    return return_valuedef in_degree_distribution(digraph):    """    Takes a directed graph digraph (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph.    The function should return a dictionary whose keys correspond to in-degrees of nodes in the graph.    The value associated with each particular in-degree is the number of nodes with that in-degree.    In-degrees with no corresponding nodes in the graph are not included in the dictionary.    :param digraph:    :return:    """    in_degrees = compute_in_degrees(digraph)    return_value = dict()    for dummy_index in range(len(digraph)):        count = 0        for key in in_degrees:            if in_degrees[key] == dummy_index:                count += 1        if count != 0:            return_value[dummy_index] = count    return return_value