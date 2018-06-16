#!/usr/bin/python3.6

import sys
import pandas as pd
import numpy as np
import sklearn.metrics as sm
import matplotlib.pyplot as plt
import math as m

def clean_kmeans(data, centers):
    nb_clusters = len(centers)

    #get clusters from data
    clusters = [[d for d in data if d["category"] == i] for i in range(nb_clusters)]

    #removes the cluster feature from the dataset
    del(data["category"])
    
    #clean clusters by selecting the 20% points of the cluster nearest to the center
    clean_clusters = []
    for i in range(nb_clusters):
        clean_clusters.append(sorted(clusters[i], key = sum(lambda x:sum((k-centers[i])**2)))[:m.ceil(0.2*len(clusters[i]))])

    return clean_clusters

if __name__=="__main__":
    #TODO: test the functionality
