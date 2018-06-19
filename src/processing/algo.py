#!/usr/bin/python3.6

import pandas as pd
import numpy as np
import math as m

# 
def clean_kmeans(data, centers):
    """
    clean the clusters returned by the kmeans algorithm
    first, it selects the core of each cluster, and then for each point not in that core, it associates it 
    with the closest cluster (for the standardized distance)

    returns a list of dataframes (one for each core cluster + one for the remaining points) and the centers
    """

    nb_clusters = len(centers)
    centers=np.array(centers)

    # get clusters from data
    clusters=[]
    for i in range(nb_clusters):
        clusters.append(data.loc[data['category']==i]) # for each cluster, selects the points in the cluster

     # removes the cluster feature from the dataset
    for c in clusters:
        del(c["category"])

    # clean clusters by selecting the 20% points of the cluster nearest to the center
    # we build as many dataframes as the number of clusters, and a dataframe which contains remaining data
    dataframeList = []
    remainingData = []
    for i in range(nb_clusters):
        srt_data = sorted(clusters[i].values, key = lambda x:sum((x-centers[i])**2))
        coreCluster = srt_data[:m.ceil(0.2*len(clusters[i]))+1]
        
        remainingData.append(srt_data[m.ceil(0.2*len(clusters[i]))+1:])
        
        coreDataframe = pd.DataFrame(coreCluster, columns=clusters[0].columns)

        dataframeList.append(coreDataframe)
        
    remainingData = np.array(remainingData)
    
    #tmpData is useful to list the points' coordinates in a single array
    tmpData=[]
    for i in range(len(remainingData)):
        for j in range(len(remainingData[i])):
            tmpData.append(remainingData[i][j])
            
    remainingData = pd.DataFrame(np.array(tmpData), columns=clusters[0].columns)
    dataframeList.append(remainingData)

    return dataframeList, centers


if __name__=="__main__":
    d = pd.DataFrame(np.array([[-5, 5, 0], [-4, 4, 0], [-7, 4, 0], [-4, 7, 0], [-7, 7, 0],\
                               [5, -5, 1], [4, -4, 1], [7, -4, 1], [4, -7, 1], [7, -7, 1]]),\
                     columns=["x", "y", "category"])
    
    centers = [[-5, 5], [5, -5]]
    dataframesList = clean_kmeans(d, centers)
    print(dataframesList)
