# -*- coding: utf-8 -*-
"""
Created on Fri May  1 16:51:58 2015

@author: mrinmoymaity
"""
import csv
import json
from os import listdir
from os.path import isfile, join
import operator
import numpy as np
from correlation import spearman_corr_coef, pearson_corr_coef
import matplotlib as plt
from matplotlib.colors import ListedColormap


def preprocess_word(word):
    word = word.strip(' ')
    word = word.strip(',')
    return word


# Create words dictionary by category . provided Excel by Bo-Chiuan
def create_words_dict_categorized_by_topic():
    inputFile = "target_words.csv"
    words_dict = {}
    with open(inputFile,'r') as file:
        csv_reader = csv.reader(file, delimiter=' ')
        line_count = 0
        for lines in csv_reader:
            if line_count == 0:
                categories = lines[0].split(',')
                for word in categories:
                    words_dict[word] = []
            else:
                words = lines[0].split(',')
                for i in range(len(words_dict)):
                    if len(words[i]) > 0:
                        words_dict[categories[i]].append(words[i])   
            line_count += 1
                    
    return words_dict


def parse_govt_files_for_word_count(jsonFile, words_dict):
    category_count = {}
    for keys in words_dict.keys():
        category_count[keys] = 0
    for lines in jsonFile:
        json_object = json.loads(lines)
        try:
            tweet_words = json_object['text'].split()
        except KeyError:
            continue
        for word in tweet_words:
            for key in words_dict.keys():
                preprocess_word(word)
                if word in words_dict[key]:
                    category_count[key] += 1
                
    return category_count        
        

def parse_all_files_to_create_category_dict(words_dict):
    primary_dir_gov_accounts = "data\GovtAccounts"
    state_level_dict = {}
    files = [ f for f in listdir(primary_dir_gov_accounts) if isfile(join(primary_dir_gov_accounts,f))]
    for file in files:
        print file
        inputFile = open(primary_dir_gov_accounts+"\\"+file,'r')
        dict = parse_govt_files_for_word_count(inputFile, words_dict)
        state_level_dict[file.split('.')[0]] = dict
        inputFile.close()
    return state_level_dict

        
def rank_categories(state_level_dict, words_dict):
    rank_dict = {}
    category_list = []
    for key in words_dict.keys():
        category_list.append(key)
#    print category_list

    for key in state_level_dict.keys():
        sorted_by_category = sorted(state_level_dict[key].items(), key=operator.itemgetter(1), reverse = True)
#        print sorted_by_category
        list = []
        for category in sorted_by_category:   
            index = category_list.index(category[0])
            list.append(index+1)
        rank_dict[key] = list 
    return rank_dict


def find_correlations_among_states(rank_dict):
    len_user_relations = len(rank_dict)
    user_relations = np.zeros([len_user_relations,len_user_relations])
    print rank_dict
    labels = rank_dict.keys()
    outer_index = 0
    for key_outer in rank_dict.keys():
        inner_index = 0
        for key_inner in rank_dict.keys():
            if outer_index <= inner_index:
                user_relations[outer_index,inner_index] = spearman_corr_coef(rank_dict[key_outer],rank_dict[key_inner])
                user_relations[inner_index, outer_index] = user_relations[outer_index, inner_index]
            inner_index += 1
        outer_index  += 1
    print labels
    print user_relations
    user_relations = np.asarray(user_relations)
    print "Completed"
    np.savetxt("UserRelationships.csv", user_relations, delimiter=",")
    f = open("Labels.csv","w")
    try:
        writer = csv.writer(f)
        writer.writerow(labels)
    finally:
        f.close()
    return labels   

def heatmap(labels):
#    cMap = ListedColormap(['white', 'green', 'blue','red'])

    plt.figure(figsize=(40,20))
    # Data
    data = np.genfromtxt("UserRelationships.csv", delimiter=",")
    rows = len(labels)
    columns = rows
    
    
    #  Finishing Touches
    fig,ax=plt.subplots()
    # using the ax subplot object, we use the same
    # syntax as above, but it allows us a little
    # bit more advanced control
    heatmap = ax.pcolor(data,cmap=plt.cm.Reds,edgecolors='k')
    ax.set_xticks(np.arange(0,6)+0.5)
    ax.set_yticks(np.arange(0,10)+0.5)
    cbar = plt.colorbar(heatmap)
    # Here we put the x-axis tick labels
    # on the top of the plot.  The y-axis
    # command is redundant, but inocuous.
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()

 
 # Here we use a text command instead of the title
 # to avoid collision between the x-axis tick labels
 # and the normal title position
    plt.text(0.5,1.08,'User User Opinion Matrix',
         fontsize=20,
         horizontalalignment='center',
         transform=ax.transAxes
         )
 
     # standard axis elements
    plt.ylabel('Govt. Accounts',fontsize=10)
    plt.xlabel('Govt. Accounts',fontsize=10)
    plt.savefig("user_user_correlation.jpg")
    plt.show()

from matplotlib import pyplot
def correlation_distribution():
    data = np.genfromtxt("UserRelationships.csv", delimiter=",")
    weights = []
    for i in range(len(data)):
        for j in range(len(data)):
            if i<j:
               weights.append(data[i][j])
    weights = np.array(weights)
    pyplot.hist(weights,facecolor='green', bins = 20)
    pyplot.title("Weight Distribution")
    pyplot.xlabel("Weights")
    pyplot.ylabel("Frequencies")
    pyplot.show()

def main():
    words_dict = create_words_dict_categorized_by_topic()
    print "----Creating Dictionary"
    state_level_dict = parse_all_files_to_create_category_dict(words_dict)
    print "----Ranking Categories"
    rank_dict = rank_categories(state_level_dict,words_dict)
    print "----Find Correlations"
    labels = find_correlations_among_states(rank_dict)
    print "----Creating Heatmap"
#    heatmap(labels)

main()
#correlation_distribution()