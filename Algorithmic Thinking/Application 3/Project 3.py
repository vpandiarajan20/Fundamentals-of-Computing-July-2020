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
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    return_value = (float("inf"), -1, -1)
    for dummy_idx1 in range(len(cluster_list)):
        for dummy_idx2 in range(len(cluster_list)):
            if(dummy_idx1 == dummy_idx2):
                continue
            return_value = min(return_value, pair_distance(cluster_list, dummy_idx1, dummy_idx2))          
    return return_value


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    cluster_list_length = len(cluster_list)
    
    if(cluster_list_length <= 3):
        return slow_closest_pair(cluster_list)
    
    mid_index = cluster_list_length/2
    cluster_list_left = cluster_list[0:mid_index]
    cluster_list_right = cluster_list[mid_index:]
    
    left_tuple = fast_closest_pair(cluster_list_left)
    right_tuple = fast_closest_pair(cluster_list_right)
    
    right_tuple = (right_tuple[0], right_tuple[1] + mid_index, right_tuple[2] + mid_index)
    
    return_value = min(left_tuple, right_tuple)
        
    mid = (cluster_list[mid_index].horiz_center() + cluster_list[mid_index-1].horiz_center()) * 0.5
    
    return_value = min(return_value, closest_pair_strip(cluster_list, mid, return_value[0]))
    
    return return_value


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    return_value = (float("inf"), -1, -1)
    s_set = []
    
    for cluster in cluster_list:
        if abs(cluster.horiz_center() - horiz_center) < half_width:
            s_set.append(cluster)
    
    s_set.sort(key = lambda cluster: cluster.vert_center())
       
    for idx1 in range(len(s_set)-1):
        for idx2 in range(idx1 + 1, len(s_set)):
            dist = s_set[idx1].distance(s_set[idx2])
            if dist < return_value[0]:
                return_value = (dist, min(cluster_list.index(s_set[idx1]), cluster_list.index(s_set[idx2])), max(cluster_list.index(s_set[idx1]), cluster_list.index(s_set[idx2])))
    
    return return_value
            
 
    
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
        clusters.sort(key = lambda cluster: cluster.horiz_center())
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
    population_sorted.sort(key = lambda cluster: cluster.total_population(), reverse = True)
    cluster_list_copy = list(cluster_list)
    for dummy_idx in range(num_clusters):
        k_clusters.append(alg_cluster.Cluster(set(), population_sorted[dummy_idx].horiz_center(), population_sorted[dummy_idx].vert_center(), population_sorted[dummy_idx].total_population(), 0))
    
    for dummy_idx in range(num_iterations):
        cluster_centers = list()
        #creation of empty clusters
        for dummy_idx2 in range(num_clusters):
            cluster_centers.append(alg_cluster.Cluster(set(), 0, 0, 0, 0))
        #find the k_cluster that cluster is closest to
        for cluster in cluster_list_copy:
            shortest_dist = float("inf")
            k_cluster_index = 0
            for k_cluster in k_clusters:
                dist = cluster.distance(k_cluster)
                if(dist < shortest_dist):
                    k_cluster_index = k_clusters.index(k_cluster)
                    shortest_dist = dist
            #merge the cluster with the cluster_center that has the same index as the k_cluster it is closest to     
            cluster_centers[k_cluster_index].merge_clusters(cluster)
        
        #simple update of the k_clusters
        k_clusters = list(cluster_centers)
    return k_clusters            
