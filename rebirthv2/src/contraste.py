#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Cartouche
"""

import numpy as np
import pandas as pd

import gmm
import clusterisation

class Contraste:
    
    def __init__(self,clustersList,critere=0.05,numberCluster=3):
        self.clustersList=clustersList
        self.critere=critere
        self.numberCluster=numberCluster
        
    def difference(self,cluster):
        """ return the difference between a dataframe and its center """
        dataframe = cluster.getDataFrame()
        del dataframe['category']
        center = cluster.getCenter()
        diff = dataframe-center
        return diff
             
    def variance(self,dataFrame):
        return dataFrame.var(axis=0)
        
        
    def sharpening(self,diff):
        """ sharps the dataframe in function a critere"""

        var=self.variance(diff)

        for k in diff.iterrows():
            maxi=-1
            argMax=-1
            for j in range(len(k)):
                if(var[j]!=0):
                    normalise = k[1][j]/np.sqrt(var[j])
                    if(normalise>maxi):
                        maxi=normalise
                        argMax=j                    
            for i in range(len(k)):
                if(k[1][i]<self.critere*argMax):
                    k[1][i]=0
            
        return diff
        
    def contrast(self):
        """ reapply kmean on each sharpens cluster """

        for cluster in self.clustersList:
            diff = self.difference(cluster)
            sharp = self.sharpening(diff)
            
            newGmm = gmm.GMM(sharp,self.numberCluster)
            newDataFrame, centers = newGmm.result()
            clusterisationObject = clusterisation.Clusterisation(newDataFrame,centers)
            subClustersList = clusterisationObject.result()
            
            cluster.setSubClusters(subClustersList)
            cluster.setSharp(sharp)
        
            
    def result(self):
        """ return the clustersList modified """
        self.contrast()
        return self.clustersList