#!/usr/bin/python3.6

import sys
import pandas as pd
import numpy as np
import sklearn.metrics as sm
import matplotlib.pyplot as plt
import math as m

def clean_kmeans(data, centers):
    nb_clusters = len(centers)
    centers=np.array(centers)
    #get clusters from data
    clusters = [pd.DataFrame([d for _,d in data.iterrows() if d["category"] == i], columns=data.columns) for i in range(nb_clusters)]
    
    #removes the cluster feature from the dataset
    for c in clusters:
        del(c["category"])

    #clean clusters by selecting the 20% points of the cluster nearest to the center
    clean_clusters = []
    for i in range(nb_clusters):
        srt_data = sorted(clusters[i].values, key = lambda x:sum((x-centers[i])**2))
        clean_clusters.append(srt_data[:m.ceil(0.2*len(clusters[i]))+1])

    clean_clusters = np.array(clean_clusters)

    return clean_clusters


if __name__=="__main__":
    d = pd.DataFrame(np.array([[-5, 5, 0], [-4, 4, 0], [-7, 4, 0], [-4, 7, 0], [-7, 7, 0],\
                               [5, -5, 1], [4, -4, 1], [7, -4, 1], [4, -7, 1], [7, -7, 1]]),\
                     columns=["x", "y", "category"])
    print(d)
    centers = [[-5, 5], [5, -5]]
    dp = clean_kmeans(d, centers)
    print(dp)
