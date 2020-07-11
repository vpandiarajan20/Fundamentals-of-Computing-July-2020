"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster
import random
import time
import matplotlib.pyplot as plt

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)
    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the
            clusters cluster_list[idx1] and cluster_list[idx2] have minimum
            distance dist.
    """

    if len(cluster_list) < 2:
        return (float('+inf'), -1, -1)

    dist_min = float('inf')
    idx1 = -1
    idx2 = -1

    for idx_i in range(0, len(cluster_list) - 1):
        for idx_j in range(idx_i + 1, len(cluster_list)):
            dist = pair_distance(cluster_list, idx_i, idx_j)[0]
            if dist_min > dist:
                dist_min = dist
                idx1 = idx_i
                idx2 = idx_j

    return (dist_min, idx1, idx2)


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    cluster_list_length = len(cluster_list)

    if (cluster_list_length <= 3):
        return slow_closest_pair(cluster_list)

    mid_index = cluster_list_length / 2
    cluster_list_left = cluster_list[0:mid_index]
    cluster_list_right = cluster_list[mid_index:]

    left_tuple = fast_closest_pair(cluster_list_left)
    right_tuple = fast_closest_pair(cluster_list_right)

    right_tuple = (right_tuple[0], right_tuple[1] + mid_index, right_tuple[2] + mid_index)

    return_value = min(left_tuple, right_tuple)

    mid = (cluster_list[mid_index].horiz_center() + cluster_list[mid_index - 1].horiz_center()) * 0.5

    return_value = min(return_value, closest_pair_strip(cluster_list, mid, return_value[0]))

    return return_value


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
           horiz_center is the horizontal position of the strip's vertical
           center line half_width is the half the width of the strip
           (i.e; the maximum horizontal distance that a cluster can lie from
           the center line)
    Output: tuple of the form (dist, idx1, idx2) where the centers of the
            clusters cluster_list[idx1] and cluster_list[idx2] lie in the
            strip and have minimum distance dist.
    """

    center_index = []

    for idx in range(0, len(cluster_list)):
        if math.fabs(horiz_center - cluster_list[idx].horiz_center()) <= half_width:
            center_index.append(idx)

    dist_min = float('inf')
    idx1 = -1
    idx2 = -1

    size = len(center_index)
    if size < 2:
        return (dist_min, idx1, idx2)

    center_index.sort(key=lambda idx: cluster_list[idx].vert_center())

    for idx_i in range(0, size - 1):
        for idx_j in range(idx_i + 1, min(idx_i + 4, size)):
            dist = pair_distance(cluster_list, center_index[idx_i], center_index[idx_j])[0]

            if dist < dist_min:
                dist_min = dist
                idx1 = min(center_index[idx_i], center_index[idx_j])
                idx2 = max(center_index[idx_i], center_index[idx_j])

    return (dist_min, idx1, idx2)
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    clusters = list(cluster_list)
    while len(clusters) > num_clusters:
        clusters.sort(key=lambda cluster: cluster.horiz_center())
        closest_pair = fast_closest_pair(clusters)
        clusters[closest_pair[1]].merge_clusters(clusters[closest_pair[2]])
        clusters.remove(clusters[closest_pair[2]])
    return clusters

######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    population_sorted = list(cluster_list)
    k_clusters = list()
    # create copy of cluster_list sorted ascending population
    population_sorted.sort(key=lambda cluster: cluster.total_population(), reverse=True)
    cluster_list_copy = list(cluster_list)
    for dummy_idx in range(num_clusters):
        k_clusters.append(alg_cluster.Cluster(set(), population_sorted[dummy_idx].horiz_center(),
                                              population_sorted[dummy_idx].vert_center(),
                                              population_sorted[dummy_idx].total_population(), 0))

    for dummy_idx in range(num_iterations):
        cluster_centers = list()
        # creation of empty clusters
        for dummy_idx2 in range(num_clusters):
            cluster_centers.append(alg_cluster.Cluster(set(), 0, 0, 0, 0))
        # find the k_cluster that cluster is closest to
        for cluster in cluster_list_copy:
            shortest_dist = float("inf")
            k_cluster_index = 0
            for k_cluster in k_clusters:
                dist = cluster.distance(k_cluster)
                if dist < shortest_dist:
                    k_cluster_index = k_clusters.index(k_cluster)
                    shortest_dist = dist
            # merge the cluster with the cluster_center that has the same index as the k_cluster it is closest to
            cluster_centers[k_cluster_index].merge_clusters(cluster)

        # simple update of the k_clusters
        k_clusters = list(cluster_centers)
    return k_clusters


######################################################
# Application Portion

def gen_random_clusters(num_clusters):
    return_value = list()
    while len(return_value) != num_clusters:
        return_value.append(alg_cluster.Cluster(set(), random.uniform(-1, 1), random.uniform(-1, 1), 0, 0))
    return return_value


"""
slow_closest_pair_timing = dict()
fast_closest_pair_timing = dict()
for dummy_index in range(2, 201):
    # generate clusters
    random_clusters1 = gen_random_clusters(dummy_index)
    # sort clusters by horizontal position
    random_clusters1.sort(key = lambda cluster: cluster.horiz_center())
    # time slow function
    pre_slow_closest_pair_time = time.time()
    slow_closest_pair(random_clusters1)
    post_slow_closest_pair_time = time.time()
    # store slow function time
    slow_closest_pair_timing[dummy_index-2] = post_slow_closest_pair_time - pre_slow_closest_pair_time
    # time fast function
    pre_fast_closest_pair_time = time.time()
    fast_closest_pair(random_clusters1)
    post_fast_closest_pair_time = time.time()
    # store fast function time
    fast_closest_pair_timing[dummy_index-2] = post_fast_closest_pair_time - pre_fast_closest_pair_time


line1 = plt.plot(slow_closest_pair_timing.values(), label="Slow Closest Pair Timing")
line2 = plt.plot(fast_closest_pair_timing.values(), label="Fast Closest Pair  Timing")
plt.legend()
plt.xlabel('Length of List')
plt.ylabel('Runtime')
plt.title('Slow Closest Pair Timing vs Fast Closest Pair  Timing, Pycharm implementation')
plt.show()
"""

"""
Q4
k clustering is much much faster than hierarchical clustering. The running time of hierarchical 
clustering is O(n^2 * log^2(n)) which is greater than the runtime of k clustering which is around
O(n)
Q7
for the cluster computed through hierarchical clustering the distortion is 1.75163886916e+11
for the cluster computed through k clustering the distortion is 2.71254226924e+11
Q8
There were multiple large population clusters to begin with on the south part of the west coast 
so many k clusters started there and when expanding were forced to distort. The initial k clusters
caused the large distortion. However hierarchical clustering does not have the same limitations
and produced less distortion.
Q9
Hierarchical clustering requires less oversight because it will return low distortion values with
only the number of clusters as an input. In order to do k clustering, one must develop a better
strategy or hand select the initial positions of the k clusters. 
Q11
Hierarchical clustering is more effective for the first data set of 111 points, but beyond that
there is no substantial difference between the two methods for the other data sets.
"""