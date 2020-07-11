"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster
import matplotlib.pyplot as plt
# conditional imports
if DESKTOP:
    import App3 as alg_project3_solution      # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])]
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering

    Note that method may return num_clusters or num_clusters + 1 final clusters
    """

    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters

    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)

    return cluster_list


#####################################################################
# Code to load cancer data, compute a clustering and
# visualize the results
def compute_distortion(cluster_list, data_table):
    return_value = 0
    for cluster in cluster_list:
        return_value += cluster.cluster_error(data_table)
    return return_value

def run_example():
    """
    Load a data table, compute a list of clusters and
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_111_URL)

    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    #cluster_list = sequential_clustering(singleton_list, 15)
    #print "Displaying", len(cluster_list), "sequential clusters"

    #cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
    #print "Displaying", len(cluster_list), "hierarchical clusters"

    cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)
    print "Displaying", len(cluster_list), "k-means clusters"
    print compute_distortion(cluster_list, data_table)

    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers

def plot_distortion(dataset):

    data_table = load_data_table(dataset)

    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    # k clustering distortions
    distortion_of_k_clustering = dict()
    for idx1 in range(6, 20):
        copy_of_singleton_list = list(singleton_list)
        cluster_list = alg_project3_solution.kmeans_clustering(copy_of_singleton_list, idx1, 5)
        distortion_of_k_clustering[idx1] = compute_distortion(cluster_list, data_table)

    # Hierarchical clustering distortions
    distortion_of_hierarchical_clustering = dict()
    copy_of_singleton_list = list(singleton_list)
    for idx1 in range(20,5,-1):
        copy_of_singleton_list = alg_project3_solution.hierarchical_clustering(copy_of_singleton_list, idx1)
        distortion_of_hierarchical_clustering[idx1] = compute_distortion(copy_of_singleton_list, data_table)

    line1 = plt.plot(distortion_of_hierarchical_clustering.keys(), distortion_of_hierarchical_clustering.values(), label="hierarchical clustering")
    line2 = plt.plot(distortion_of_k_clustering.keys(), distortion_of_k_clustering.values(), label="k clustering")
    plt.legend()
    plt.xlabel('Number of Clusters')
    plt.ylabel('Distortion * 10^12')
    plt.title('distortion of hierarchical and k clustering for 896 points')
    plt.show()

plot_distortion(DATA_896_URL)