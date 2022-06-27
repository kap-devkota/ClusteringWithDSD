"""
Author: Charlotte Versavel
Date:   June 2022

                             degreelist_class.py

Purpose: a class TODO

"""

import pandas as pd 
import numpy as np

from matrix_class import *
from cluster_class import *



class DegreeList:
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    * * * * * * * * * * * * * MEMBER VARIABLES * * * * * * * * * * * * * *  
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    protein_matrix : ProteinMatrix = ProteinMatrix

    sorted_protein_degree_dict = dict()


    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    * * * * * * * * * * * * * * INITIALIZERS * * * * * * * * * * * * * * *  
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def __init__(self, matrix : ProteinMatrix) -> None:
        """            
        Parameters: matrix is populated with proteins and their interaction 
                    weights
        Purpose:    to take in a proteinMatrix (or submatrix) and create a 
                    sorted dictionary of protein:degree for all proteins in the 
                    matrix.
        Returns:    n/a
        """
        self.protein_matrix = matrix

        protein_degree_dict = {name:matrix.find_degree(name) for name in matrix.get_list_of_proteins()}

        self.sorted_protein_degree_dict = sorted(protein_degree_dict.items(), key=lambda x: x[1], reverse=True)


    def __repr__(self): 
        """             
        Purpose:    to override the print function for this class to print the 
                    sorted dictionary when called
        Returns:    a string of the dictionary
        """
        
        return str(self.sorted_protein_degree_dict)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    * * * * * * * * * * * * * * * GETTERS * * * * * * * * * * * * * * * * *  
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def get_degree_list(self) -> list():
        """             
        Purpose:    to allow access to the sorted degree list
        Returns:    a list of tuples of (protein, degree)
        """
        return self.sorted_protein_degree_dict
    
    def get_list_of_proteins_sorted_by_degree(self) -> list():
         
        reverse_list_of_proteins = []

        for protein_degree_pair in reversed(self.sorted_protein_degree_dict):
            reverse_list_of_proteins.append(protein_degree_pair[0])

        return reverse_list_of_proteins

    def get_protein_at_index(self, index : int, degree = False) -> str or tuple:
        """             
        Parameters: index is the index of the protein in the sorted list
                    degree is a boolean that determines if the degree is returned as well
        Purpose:    to return the protein at the specified index
        Returns:    the protein at the specified index, or if degree is True, a 
                    tuple of (protein, degree)
        """
        if not degree:
            return self.sorted_protein_degree_dict[index][0]
        else:
            return self.sorted_protein_degree_dict[index]
    

    
    
    def determine_num_edges_to_cluster(self, protein : str, cluster_of_proteins : list(), max_edges_until_return : int = -1, also_return_which_proteins : bool = False) -> int and list:
        """             
        Parameters: protein is a single protein in the matrix
                    cluster_of_proteins is converted to cluster_list, a list of proteins in a cluster
                    max_edges_until_return allows the function to stop counting edges once a certain target is reached
                    also_return_which_proteins if set to true, will return which proteins have have edges to the given protein. should not be set to true when max_edges is set to a specific value
        Purpose:    to determine the number of edges between the protein and the proteins in the cluster
        Returns:    the number of edges, and identify_connections: a list of bools in the same order as proteins in the cluster, with true if a the protein is connected, false otherwise
        """

        for already_in_cluster in cluster_of_proteins:
            if protein == already_in_cluster:
                return 0
        
        num_edges = 0
        identify_connections = [False for i in range(len(cluster_of_proteins))]
        # which_proteins = list() 

        if max_edges_until_return == -1: # max_edges_until_return has been left unspecified
            i = 0
            for cluster_protein in cluster_of_proteins:
                if (self.protein_matrix).has_edge(protein, cluster_protein):
                    num_edges += 1
                    identify_connections[i] = True
                    # which_proteins.append(cluster_protein)
                i += 1
        else: # max_edges_until_return has been specified
            for cluster_protein in cluster_of_proteins:
                # print(f"about to call has edge 1")
                if (self.protein_matrix).has_edge(protein, cluster_protein):
                    num_edges += 1
                if num_edges >= max_edges_until_return:
                    return num_edges
        
        
        if (also_return_which_proteins):
            return num_edges, identify_connections
            # return num_edges, which_proteins
        return num_edges
        


    def create_list_of_proteins_connected_to_cluster(self, list_of_proteins: np.array, cluster_list : np.array, max_list_length : int = -1, min_num_connections : int = 3) -> list:
        """             
        Parameters: cluster_list is a list of proteins in a cluster
                    max_list_length is an upper bound for the number of proteins to return in a list. If None, all proteins with at least min_num_connections connections are added to the list
                    min_num_connections is the minimum number of connections a protein must have to be added to the list and considered 'connected' to the cluster
        Purpose:    to create a list of proteins that are connected to the cluster
        Returns:    a list of proteins that are connected to the cluster
        """
        
        qualifying_proteins = []
        if max_list_length == -1: # max_list_length left unspecified
            for protein in list_of_proteins:
                num_edges = self.determine_num_edges_to_cluster(protein, cluster_list, max_edges_until_return=min_num_connections)

                if (num_edges >= min_num_connections):
                        qualifying_proteins.append(protein)
        else: # max_list_length has been specified    
            for protein in list_of_proteins:
                num_edges = self.determine_num_edges_to_cluster(protein, cluster_list, max_edges_until_return=min_num_connections)
                
                if (num_edges >= min_num_connections):
                        qualifying_proteins.append(protein)
                        if (len(qualifying_proteins) >= max_list_length):
                            return qualifying_proteins
            
        
        return qualifying_proteins
        

    def which_components_of_a_cluster_would_a_protein_connect(self, protein : str, cluster_of_proteins, cluster_component_labels : tuple) -> set:
        """
        Parameters: 
            -   cluster is a cluster containing a group of proteins that are 
                in some way related
            -   cluster_component_labels are the labels for each protein. 
                proteins with the same label are connected to eachother
        Purpose:    to determine if a protein could re-attach different 
                    components of a cluster
        Returns:    a set of the components that would be connected by the 
                    given protein
        """
        which_components_were_connected = set()

        # obtain which cluster proteins the given protein is connected to
        num_edges, connected_proteins = self.determine_num_edges_to_cluster(protein, cluster_of_proteins, also_return_which_proteins = True)
        
        # for each protein that was connected, store it's component label
        for i in range(len(connected_proteins)):
            if (connected_proteins[i]):
                which_components_were_connected.add(cluster_component_labels[i])

        return which_components_were_connected # type: set


    def determine_if_a_protein_will_connect_a_cluster(self, protein : str, cluster_of_proteins : list(), cluster_component_labels : tuple, min_num_connections : int = 2) -> bool: 
        """
        Parameters: 
            -   cluster is a cluster containing a group of proteins that are 
                in some way related
            -   cluster_component_labels are labels corresponding to a 
                protein's component within the cluster. connected proteins will 
                be in the same component.
            -   min_num_connections is the minimum number of 
                components that need to be connected for a protein to be 
                considered successful in connecting a cluster
        Purpose:    to determine if the components that a protein could 
                    reconnect are satisfactory.
        Returns:    true if a protein connects >= 2 elements in a cluster
        """
        set_of_components = self.which_components_of_a_cluster_would_a_protein_connect(protein, cluster_of_proteins, cluster_component_labels)

        if ((len(set_of_components)) >= min_num_connections):
            return True

        return False



