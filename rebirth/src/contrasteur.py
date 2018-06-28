#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:32:13 2018

@author: antoine

On prend en entrée une liste d'objets cluster (comportant un dataframe, un vecteur centre,
un label) catégorisation ; et une liste d'objets clusters contraste
On prend également un nouvel élément en entrée (un array numpy)

On ressort un array contenant la catégorie et une liste d'adjectifs correspondant à l'élément
"""

import numpy as np
import pandas as pd
from math import sqrt

def result(clustersCategories, clustersContrast, element) :
    """ on attribue à element le cluster dont il est le plus proche du centre """
    distance_min = -1
    for cluster in clustersCategories :
        distance_tmp = distanceEuclidienne(cluster.centre, element)
        if (distance_tmp < distance_min or distance_min < 0) :
            distance_min = distance_tmp
            cluster_category = cluster
    
    label = cluster_category.getLabel() 
    
    """ on attribue à element la liste de labels associé au cluster de contrastes
    dans lequel il se trouve s'il en est assez proche en nombre d'écarts-types """

    adjectifs = "pas d'adjectif pertinent trouvé"
    distance_min = -1
    for cluster in clustersContrast :
        distance_tmp = distanceEuclidienne(cluster.centre, element)
        """ si une des composantes de la différence entre element et le centre du cluster
            dépasse 3 variances, alors la condition n'est pas remplie """
        if (distance_tmp < distance_min or (distance_min < 0 and assezProche(element, cluster))) :
            distance_min = distance_tmp
            cluster_contrast = cluster
    
    adjectifs = cluster_contrast.getLabel()
    
    return label, adjectifs

def assezProche(point, cluster):
    data = point - cluster.getCenter()
    for k in range(len(point)):
        if (abs(data[k])/sqrt(np.array(cluster.getDataFrame().var(axis=0))[k]) > 3):
            return False
    return True

def distanceEuclidienne(point_1, point_2):
    distance = 0
    for k in range(len(point_1)):
        distance += (point_1[k] - point_2[k])**2
    return distance

if __name__ == "__main__":
    ar = np.array([[1.1, 2, 3.3, 4], [2.7, 10, 5.4, 7], [5.3, 9, 1.5, 15]])
    df = pd.DataFrame(ar, index = ['a1', 'a2', 'a3'], columns = ['A', 'B', 'C', 'D'])

    element = np.array([3, 5, 3.5, 8])
    center = np.array([3.03, 7, 3.4, 8.67])

    for k in range(len(element)):
        if ((abs(element[k] - center[k]))/sqrt(np.array(df.var(axis=0))[k]) > 3):
            print((abs(element[k] - center[k]))/sqrt(np.array(df.var(axis=0))[k]))
