#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Computes the contrasts and categorize them
"""

import numpy as np
import pandas as pd
import math as m

import gmm
import clusterisation

class Contraste:
    
    def __init__(self,clustersList,critere=0.5,numberCluster=3):
        self.clustersList=clustersList
        self.critere=critere
        self.numberCluster=numberCluster
        self.infinitiesPoints=[]
        
    def difference(self,dataframe,center):
        """ return the difference between a dataframe and its center """
        del dataframe['category']
        diff = (dataframe-center[:len(dataframe.columns)])
        var=self.variance(dataframe)
        infinities=[]
        for j in range(len(var)):
            if(var[j]==0):
                infinities.append(j)
        diffNormal = diff/var
        for k in dataframe.iterrows():
            for j in infinities:
                if(k[1][j]==0):
                    diffNormal[j][k[0]]=0
                else:
                    self.infinitiesPoints.append(diffNormal.loc[k[0]])
                    diffNormal=diffNormal.drop(axis=1,index=k[0])
        
        return diffNormal
             
    def variance(self,dataFrame):
        var=dataFrame.var(axis=0)                  
        return var
        
        
    def sharpening(self,diff):
        """ sharps the dataframe in function a critere"""
        
        maxiListe = diff.max(axis=1)
        
        for k in diff.iteritems():
            for j in range(len(k[1])):
                if(abs(k[1][j])<self.critere*maxiListe[j]):
                    k[1][j]=0
        
        return diff
        
    def contrast(self):
        """ reapply gmm on each sharpens cluster """

        newListDatas=[]
        
        remainingDatas=[]

        for cluster in self.clustersList:
            diff = self.difference(cluster.core,cluster.prototype.center)
            sharp = self.sharpening(diff)
            newListDatas.append(sharp)
            
            diff2=self.differenceRemaining(cluster.remaining,cluster.center)
            sharp2=self.sharpening(diff2)
            remainingDatas.append(sharp2)
            
        newDataFrame=pd.concat(newListDatas) 
        dataFrameRemaining = pd.concat(remainingDatas)
            
        newGmm = gmm.GMM(newDataFrame)
        lastDataFrame, centers = newGmm.result()
        clusterObject = clusterisation.Clusterisation(lastDataFrame,centers, isContrast = True,dimension = lastDataFrame.columns[0])
        listeClusters = clusterObject.result()
                
        return listeClusters,dataFrameRemaining
            
            
    def result(self):
        """ return the dataframe centré réduit sharpené """
        return self.contrast()
        
