#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:57:11 2018

@author: antoine

On prend en entrée une liste d'objets cluster (comportant un dataframe, un vecteur centre,
un label et une liste de sous-clusters)
On prend également un nouvel élément en entrée (un array)

On ressort un array contenant la catégorie et la dimension dominante de l'élément
"""

import numpy as np
import pandas as pd
from math import sqrt

def result(listeClusters, element ) :
    """ on attribue à element le cluster dont il est le plus proche du centre """
    distance_min = -1
    for cluster in listeClusters :
        distance_tmp = distanceEuclidienne(cluster.centre, element)
        if (distance_tmp < distance_min or distance_min < 0) :
            distance_min = distance_tmp
            cluster_element = cluster
    
    label = cluster_element.getLabel()
    dataframe_cluster = cluster_element.getDataFrame()
    center_cluster = cluster_element.getCenter()
    
    data = element - center_cluster
    
    values = []
    for k in range(len(element)):
        values.append(abs(data[k])/sqrt(np.array(dataframe_cluster.var(axis=0))[k]))
    
    indiceDominant = values.index(max(values))
    dimensionDominante = dataframe_cluster.columns[indiceDominant]    
            
    """ on attribue à element la dimension dominante sur laquelle la difference
    entre element et le centre du cluster auquel il appartient a la valeur la plus
    importante par rapport à la variance sur cette dimension """
    
    return label, dimensionDominante

def distanceEuclidienne(point_1, point_2):
    distance = 0
    for k in range(len(point_1)):
        distance += (point_1[k] - point_2[k])**2
    return distance

if __name__ == "__main__":
    ar = np.array([[1.1, 2, 3.3, 4], [2.7, 10, 5.4, 7], [5.3, 9, 1.5, 15]])
    df = pd.DataFrame(ar, index = ['a1', 'a2', 'a3'], columns = ['A', 'B', 'C', 'D'])

    element = np.array([0, 5, 3.5, 8])
    center = np.array([3.03, 7, 3.4, 8.67])

    values = []
    for k in range(len(element)):
        values.append((abs(element[k] - center[k]))/sqrt(np.array(df.var(axis=0))[k]))

    indiceDominant = values.index(max(values))
    dimensionDominante = df.columns[indiceDominant]

    print(dimensionDominante)
