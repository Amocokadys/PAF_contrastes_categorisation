#!/usr/bin/python3.6

from cluster import Cluster

import pandas as pd
import numpy as np
import math as m

def clusterPlusProche(listeCluster,listeCentre,point):
    """
    find the closest cluster from the point according to the standardized distance
    """
    # instead of computing min(distance) it computes max(1/(1+distance))
    # it is to initialize the min dist to 0, and avoid problems with infinity
    plusProche=0
    distanceMin=1 
    for k in range(len(listeCentre)):
        distanceCourante=1/(1+listeCluster[k].distance(point))
        if distanceCourante>distanceMin:
            plusProche=k
            distanceMin=distanceCourante
    return plusProche


def clusteriseAvecEcartsTypes(listeCluster,listeCentre,listePointsRestants):
    """
    this function associate each remaining data to its closest cluster
    for the standardized distance
    """
    listeObjetsCluster=[]
    for k in range(len(listeCluster)):
        clusterk=Cluster(listeCluster[k],listeCentre[k],k)
        listeObjetsCluster.append(clusterk)
    listePointsRestants=np.array(listePointsRestants)
    for point in listePointsRestants:
        plusProche=clusterPlusProche(listeObjetsCluster,listeCentre,point)
        listeObjetsCluster[k].ajouterPoint(point)
    return(listeObjetsCluster)


def clean_kmeans(data, centers):
    """
    clean the clusters returned by the kmeans algorithm
    first, it selects the core of each cluster, and then for each point not in that core, it associates it 
    with the closest cluster (for the standardized distance)

    returns a list of cluster objects (the cleaned clusters)
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
        lim = m.ceil(0.2*len(clusters[i]))+1 # the limit of the data to select (20% of the sorted data)
        coreCluster = srt_data[:lim]
        remainingData.extend(srt_data[lim:])
        coreDataframe = pd.DataFrame(coreCluster, columns=clusters[0].columns)
        dataframeList.append(coreDataframe)

    remainingData = pd.DataFrame(np.array(remainingData), columns=clusters[0].columns) # turns the remaining data list into an dataframe
    
    return clusteriseAvecEcartsTypes(dataframeList, centers, remainingData)



if __name__=="__main__":
    d = pd.DataFrame(np.array([[-5, 5, 0], [-4, 4, 0], [-7, 4, 0], [-4, 7, 0], [-7, 7, 0],\
                               [5, -5, 1], [4, -4, 1], [7, -4, 1], [4, -7, 1], [7, -7, 1]]),\
                     columns=["x", "y", "category"])
    
    centers = [[-5, 5], [5, -5]]
    dataframesList = clean_kmeans(d, centers)
    print(*[clst.points for clst in dataframesList], sep = '\n')
