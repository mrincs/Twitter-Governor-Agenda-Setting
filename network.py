# -*- coding: utf-8 -*-
"""
Created on Fri May  1 16:06:12 2015

@author: mrinmoymaity
"""

import networkx as nx
from correlation import *
import numpy as np
import csv

# Input : User-user relationship matrix
# Output: Create undirected weighted social network with edges above certain threshold, by default show all
def create_relationship_network_governors(A, labels, thres=-1):
    user_relationship_graph = nx.Graph()
#    print labels
#    user_relationship_graph.add_nodes_from(labels)
#    for i in range(len(A)):
#        user_relationship_graph.add_node(labels[i])
    for i in range(len(A)):
        for j in range(len(A)):
            if i<j and A[i,j] > thres:
                user_relationship_graph.add_edge(labels[i],labels[j],weight=A[i,j])
    nx.write_gml(user_relationship_graph,"govt_relationship.gml")

## Test create_relationship_network_governors and open in Gephi    
#A  = np.array([[1,2,3,4,6,7,5],[3,2,1,4,5,7,6],[1,2,3,4,5,6,7],[6,7,3,1,4,5,2]])
#generate_spearman_corr_matrix(A)
#create_relationship_network_governors(A)

def load_correlation_matrix():
    data_matrix = np.genfromtxt("UserRelationships.csv", delimiter=",")
    file_labels = open("Labels.csv",'r')
    try:
        reader = csv.reader(file_labels)
        labels = []
        for label in reader:
            labels.append(label)
    finally:
        file_labels.close()
    labels = labels[0]
    create_relationship_network_governors(data_matrix, labels)
    
load_correlation_matrix()