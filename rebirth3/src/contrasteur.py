#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:56:53 2018

@author: antoine

On prend en entrée une liste d'objets cluster (comportant un dataframe, un vecteur centre,
un label) catégorisation ; et une liste par dimension de listes de 3 objets clusters contraste
On prend également un nouvel élément en entrée (un array numpy)

On ressort un array contenant la catégorie et pour chaque dimension une information '+', '6' ou ''
"""

import numpy as np
import pandas as pd
from math import sqrt

def result(clustersCategories, listClustersContrast, element) :
    """ on attribue à element le cluster dont il est le plus proche du centre """
    distance_min = -1
    for cluster in clustersCategories :
        distance_tmp = distanceEuclidienne(cluster.centre, element)
        if (distance_tmp < distance_min or distance_min < 0) :
            distance_min = distance_tmp
            cluster_category = cluster
    
    label = cluster_category.getLabel() 
    
    """ on attribue à element une liste de caractéristiques ('longueur +') pour chaque dimension
        il faut déterminer pour chaque dimension de quel cluster element est le plus proche """
    
    contraste = []
    
    for k in range(len(listClustersContrast)):
        distance_min = -1
        for cluster in listClustersContrast[k] :
            distance_tmp = (cluster.centre[k] - element[k])**2
            """ 3 clusters : normal, petit ou grand
                la dimension est celle de la colonne du dataframe non nulle """
            if (distance_tmp < distance_min or distance_min < 0):
                distance_min = distance_tmp
                cluster_contrast = cluster
    
        dimension = dimensionNonNulle(cluster_contrast.getDataFrame())
        caracteristique = cluster_contrast.getLabel()
        contraste.append(dimension + " " + caracteristique)
    
    return label, contraste

""" on renvoie la dimension associée à la première colonne dont on rencontre une valeur non nulle """
def dimensionNonNulle(dataframe):
    for i, row in dataframe.iterrows():
        for dim in dataframe.columns:
            if row[dim] != 0:
                return dim


def distanceEuclidienne(point_1, point_2):
    distance = 0
    for k in range(len(point_1)):
        distance += (point_1[k] - point_2[k])**2
    return distance

if __name__ == "__main__":
    #ar = np.array([[1.1, 2, 3.3, 4], [2.7, 10, 5.4, 7], [5.3, 9, 1.5, 15]])
    ar = np.array([[0.1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    df = pd.DataFrame(ar, index = ['a1', 'a2', 'a3'], columns = ['A', 'B', 'C', 'D'])

    element = np.array([3, 5, 3.5, 8])
    center = np.array([3.03, 7, 3.4, 8.67])

    print(dimensionNonNulle(df))
