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
import math as m

import gmm
import clusterisation

class Contraste:
    
    def __init__(self,clustersList,critere=m.pow(10,-16),numberCluster=3):
        self.clustersList=clustersList
        self.critere=critere
        self.numberCluster=numberCluster
        
    def difference(self,cluster):
        """ return the difference between a dataframe and its center """
        dataframe = cluster.getDataFrame()
        del dataframe['category']
        center = cluster.getCenter()
        diff = (dataframe-center)/self.variance(dataframe)
        return diff
             
    def variance(self,dataFrame):
        return dataFrame.var(axis=0)
        
        
    def sharpening(self,diff):
        """ sharps the dataframe in function a critere"""
        
        maxiListe = diff.max(axis=0)
        
        for k in diff.iterrows():
            for j in range(len(k[1])):
                if(abs(k[1][j])<self.critere*maxiListe[j]):
                    k[1][j]=0  
                
        return diff
    
    def putZeros(self,dataframe,i):
        result=dataframe.copy(deep=True)
        
        for k in result.iterrows():
            for j in range(len(k[1])):
                if(j!=i):
                    k[1][j]=0
        return result
        
    def mini(self,dataframe,k):
        minListe=dataframe.min(axis=0)
        minimum =minListe[k]
        
        for j in dataframe.iterrows():
            j[1][k]+=abs(minimum)
            
        return dataframe,minimum

    def soustractMin(self,dataframe,minimum,k):
        categories = dataframe['category']
        del dataframe['category']
        copy=dataframe.copy(deep=True)
        result=copy-abs(minimum)
        toReturn=self.putZeros(result,k)
        toReturn['category']=categories
        return toReturn
        
    def contrast(self):
        """ reapply gmm on each sharpens cluster """

        newListDatas=[]

        for cluster in self.clustersList:
            diff = self.difference(cluster)
            sharp = self.sharpening(diff)
            newListDatas.append(sharp)
            
        newDataFrame=pd.concat(newListDatas) 
        
        gmmList = []
    
        for k in range(len(newDataFrame.columns)):    
            zeroDatas = self.putZeros(newDataFrame,k)
            miniFrame,minimum=self.mini(zeroDatas,k)
            newGmm = gmm.GMM(miniFrame,self.numberCluster)
            dataFrame, centers = newGmm.result()
            lastDataFrame=self.soustractMin(dataFrame,minimum,k)
            clusterObject = clusterisation.Clusterisation(lastDataFrame,centers)
            listeClusters = clusterObject.result()
            gmmList.append(listeClusters)
        
        return gmmList
            
            
    def result(self):
        """ return the dataframe centré réduit sharpené """
        return self.contrast()
        