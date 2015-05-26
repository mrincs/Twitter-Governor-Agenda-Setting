# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:24:49 2015

@author: mrinmoymaity
"""

import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join
from matplotlib.colors import ListedColormap

# Generate Data
primary_dir = "immigration-tweets-master"
internal_dir = "data\GovtAccounts"
files = [ f for f in listdir(internal_dir) if isfile(join(primary_dir+"\\"+internal_dir,f))]

#discrete color scheme
cMap = ListedColormap(['white', 'green', 'blue','red'])

plt.figure(figsize=(40,20))
# Data
#data = np.random.rand(len(files), len(files)) # Change this line. Data generation
data = np.genfromtxt("UserRelationships.csv", delimiter=",")
rows = files
columns = files


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
# similar syntax as previous examples
#ax.set_xticklabels(columns,minor=False,fontsize=2,rotation=90)
#ax.set_yticklabels(rows,minor=False,fontsize=2)
 
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