# -*- coding: utf-8 -*-
"""
Created on Fri May  1 14:54:03 2015

@author: mrinmoymaity
"""

from scipy.stats import spearmanr,pearsonr
import numpy as np 

def spearman_corr_coef(A, B):
    rho,p_value = spearmanr(A, B)
    return rho
    
def pearson_corr_coef(A, B):
    rho, p_value = pearsonr(A, B)
    return rho
    
#A = [1,2,3,4,5]
#B = [5,4,3,2,1]
#C = [4,3,2,5,1]
#rho,pval = spearman_corr_coef(A, C)
#print(rho)

# Input: Rank list of all users. Each column represents a category, each row represents a user. Each cell is a rank.
# Output: user_relation matrix where each cell calculated using spearman rank correlation coef. Dimension square matrix of size = number of users
def generate_spearman_corr_matrix(A):
    len_user_relations = len(A[:,0])
    user_relations = np.zeros([len_user_relations,len_user_relations])
    for i in range(len_user_relations):
        for j in range(len_user_relations):
            if i<=j:
                user_relations[i,j] = spearman_corr_coef(A[i],A[j])
                user_relations[j,i] = user_relations[i,j]
#                print("Relation between ",i+1,"and",j+1,":",user_relations[i,j])
    print(user_relations)
    return user_relations
    
#A  = np.array([[1,2,3,4,6,7,5],[3,2,1,4,5,7,6],[1,2,3,4,5,6,7],[6,7,3,1,4,5,2]])
#generate_spearman_corr_matrix(A)


# Similar to generate_spearman_corr_matrix. Only difference it is used to measure actual count of words in a particualar category instead of rankings of categories    
def generate_pearson_corr_matrix(A):
    len_user_relations = len(A[:,0])
    user_relations = np.zeros([len_user_relations,len_user_relations])
    for i in range(len_user_relations):
        for j in range(len_user_relations):
            if i<=j:
                user_relations[i,j] = pearson_corr_coef(A[i],A[j])
                user_relations[j,i] = user_relations[i,j]
#                print("Relation between ",i+1,"and",j+1,":",user_relations[i,j])
    print(user_relations)
    return user_relations
    
