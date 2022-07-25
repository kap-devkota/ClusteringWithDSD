"""
Author: Charlotte Versavel
Date:   July 2022

                            reworked_clusters_main.py

Purpose: TODO

"""

import numpy as np
import json


from matrix_class import ProteinMatrix
from matrix_class import SubMatrix
from cluster_class import AllClusters
from degreelist_class import DegreeList

from reworked_clusters_class import ClusterInspection


def main():

    testing_matrix_file = "../data/testing_data/fake_cluster_dream.txt"
    testing_cluster_file = "../data/testing_data/fake_cluster.txt"

    dream3_matrix_file = "../data/networks/DREAM_files/dream_3.txt"
    
    dream3_cluster_dict = "../data/results/DREAM-3-cc/d3_5_100.json-cluster.json"
    dict_of_clusters = {}
    # # convert actual cluster file to a dictionary!!
    with open(dream3_cluster_dict,"r") as cluster_dict_file:
        dict_of_clusters = json.load(cluster_dict_file)
    

    dream2_matrix_file = "../data/networks/DREAM_files/dream_2.txt"
    dream3_old_cluster_file = "../data/clusters/3344522.7320912.1_ppi_anonym_v2.txt"


    # matrix = ProteinMatrix(dream3_matrix_file)
    matrix = ProteinMatrix(testing_matrix_file)
    # print(f"Matrix:\n{matrix}")


    
    # clusters = AllClusters(protein_to_cluster_dict=dict_of_clusters)
    clusters = AllClusters(testing_cluster_file)


    # # print(f"Clusters:\n{clusters}")
    # clusters.print_all()

    degreelist = DegreeList(matrix)
    # print(f"Degree list:\n{degreelist}")

    foo = ClusterInspection(matrix, clusters, degreelist)

    #foo.print_all_clusters_and_connected_proteins()

    # print(degreelist.determine_num_edges_to_cluster(protein, clusters.get_cluster_proteins(cluster_num), max_edges_until_return=3, also_return_which_proteins=True))
    
    



    qualifying_clusters = foo.find_clusters_that_match_criteria(ratio = 1, b = 0)
    # print(qualifying_clusters)

    # for cluster in qualifying_clusters:
        
    print(foo.find_proteins_that_match_criteria(1, ratio = 0, b = 0, max_degree=600))
        
    
    
if __name__ == "__main__":
    main()