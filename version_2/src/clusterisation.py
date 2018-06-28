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


class Clusterisation:
    """methods :
    init (input): -dataframe with category
                  -array of centers

    result (output) : -list of clusters"""

    def __init__(self, dataframe, arrayCenters, isContrast = False):
        self.dataframe=dataframe
        self.arrayCenters=arrayCenters
        self.isContrast = isContrast

    def dataframeToCluster(self,dataframe,means):
        nb_clusters = len(means)

        # get clusters from data
        clusters=[]
        for i in range(nb_clusters):
            if not self.isContrast:
                clusters.append(Cluster(dataframe.loc[dataframe['category']==i],\
                                        means[i]))# for each cluster, selects the points in the cluster

            else:
                clusters.append(ContrastCluster(dataframe.loc[dataframe['category']==i],\
                                        means[i]))# for each cluster, selects the points in the cluster

        return clusters

    def result(self):
        return(self.dataframeToCluster(self.dataframe,self.arrayCenters))
 
 
class Cluster:
    """
        we calculate the covariance matrix of a set of points
        the input is a DataFrame containing the dataset of a cluster (including categories)
        the output is the covariance matrix of  the cluster in an array shape
    """

    def __repr__(self):
        return (" dataframe: \n"+str(self.points)+"\n center:"+str(self.centre)+"\n label:"+str(self.label))

    def __init__(self,points,centre):
        """ if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        """
        self.centre=centre
        self.points=points #un dataframe
        self.label=[]
        self.updateLabel()
        self.subClusters=None
        self.sharpedData = None


    def setSubClusters(self,clusters):
        self.subClusters=clusters

    def setSharp(self,sharp):
        self.sharpedData = sharp

    def getSharp(self):
        return self.sharpedData

    def getDataFrame(self):
        return(self.points)

    def getCenter(self):
        return(self.centre)

    def getLabel(self):
        return(self.label)


    """ function to add points to a cluster when rebuilding it
        with standard deviation normalisation
    """
    def ajouterPoint(self,point):
        new_data = pd.DataFrame([point], columns = self.points.columns, index = pd.RangeIndex(start=len(self.points), stop=len(self.points)+1, step=1))
        self.points = self.points.append(new_data)


    def updatePropDict(self):
        """
        this method computes a dictionnary that contains the proportions of presence of
        each label among the data of the cluster
        """
        self.propDict = {}
        for idx in self.points.index:
            i = idx.split('#')[0]
            self.propDict[i] = 0

        for idx, row in  self.points.iterrows():
            i = idx.split('#')[0]
            self.propDict[i] += 1

        for key in self.propDict.keys():
            self.propDict[key] /= len(self.points)

    def updateLabel(self):
        self.updatePropDict()
        for k in self.propDict.keys():
            if self.propDict[k] > 0.5:
                self.label.append(k)


class ContrastCluster(Cluster):

    def __init__(self,points,centre):
        """ if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        """
        self.centre=centre
        self.points=points #un dataframe
        self.label=[]
        self.updateLabel()
        self.subClusters=None
        self.sharpedData = None

    def updateLabel(self):
       """
       this method gives labels to the cluster according to the values of
       it center (if greater than 1, gives the label)
       """
       for k in range(len(self.centre)):
           if self.centre[k] >= 1:
               self.label.append(self.points.columns[k])

       if self.label == []:
           self.label.append("normal")


class SubCluster(Cluster):
    """To use the subclusters, herites from Cluster"""
    
    def __init__(self,dataframe,centers):
        super(self,dataframe,centers)


class MainCluster(Cluster):
    """To use the subclusters, herites from Cluster"""
    
    def __init__(self,dataframe,centers):
        super(self,dataframe,centers,subClusters)
        self.subClusters=subClusters

    def getSubClusters(self):
        return(subClusters)

    def setClusters(self,subClusters):
        self.subClusters=subClustes
