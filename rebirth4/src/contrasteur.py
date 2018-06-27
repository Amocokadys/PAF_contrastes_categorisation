#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:56:53 2018

@author: Antoine, Aurélien

this file contains methods to classify an new element using the knowledge
brought by the clusterisation of the dataset
gives a category and a contrast category
"""

import numpy as np
import pandas as pd
from math import sqrt
import clusterisation
import contraste

def closest(listCluster, point):
    """
    computes the closest cluster from point
    """
    distance_min = -1
    clusterMin = None
    for cluster in listCluster :
        distance_tmp = cluster.distance(point) 
        if (distance_tmp < distance_min or distance_min < 0) :
            distance_min = distance_tmp
            clusterMin = cluster
    return clusterMin


class Contrasteur:
    """
    this class contains the information to classify and contrast an element
    """
    def __init__(self, listCategoryClusters, listContrastClusters):
        self.listCategoryClusters = listCategoryClusters
        self.listContrastClusters = listContrastClusters
    

    def classify(self, element):
        """
        computes the category of element, its contrast from that category, and
        the category of this contrast.
        returns the labels associated to the clusters
        """
        categoryCluster = closest(self.listCategoryClusters, element)
        contrast_element = contraste.contrastPoint(element, categoryCluster)
        contrastCluster = closest(self.listContrastClusters, contrast_element)
        return categoryCluster, contrastCluster


if __name__ == "__main__":
    #ar = np.array([[1.1, 2, 3.3, 4], [2.7, 10, 5.4, 7], [5.3, 9, 1.5, 15]])
    ar = np.array([[0.1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    df = pd.DataFrame(ar, index = ['a1', 'a2', 'a3'], columns = ['A', 'B', 'C', 'D'])

    element = np.array([3, 5, 3.5, 8])
    center = np.array([3.03, 7, 3.4, 8.67])

    print(dimensionNonNulle(df))
