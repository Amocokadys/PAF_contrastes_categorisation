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

from constantes import *

class Clusterisation:
    """methods :
    init (input): -dataframe with category
                  -array of centers
                  
    result (output) : -list of clusters"""
    
    def __init__(self, dataframe, arrayCenters, isContrast = False):
        self.dataframe = dataframe
        self.arrayCenters = arrayCenters
        self.isContrast = isContrast


    def dataframeToCluster(self,dataframe,means):
        nb_clusters = len(means)
    
        # get clusters from data
        clusters = []
        for i in range(nb_clusters):
            if self.isContrast:
                clusters.append(ContrastCluster(dataframe.loc[dataframe['category']==i],\
                                                means[i])) # for each cluster, selects the points in the cluster
            else:
                clusters.append(Cluster(dataframe.loc[dataframe['category']==i],\
                                        means[i])) # for each cluster, selects the points in the cluster
        return clusters


    def result(self):
        return(self.dataframeToCluster(self.dataframe,self.arrayCenters))
 

class Prototype:
    """
    this class contains the prototype of an object abstracted by a cluster
    it contains a center an a standard deviation over every dimension of the space
    """
    def __init__(self, points):
        self.centre = points.mean()
        self.stdDev = points.std()
        

class Cluster:
    """
    this represents a cluster
    it contains a core, points closest to the center, a Prototype, an abstraction
    of the cluster, and the remaining points, that are not in the core but that
    the GMM algorithm affilited to it
    """
    def __repr__(self):
        return (" dataframe: \n"+str(self.points)+"\n center:"+str(self.centre)+"\n label:"+str(self.label))


    def __init__(self, points, centre):
        """
        first, segregate the core and the remaining points
        then compute the prototype, and the label
        """
        del(points['category'])
        centre = np.delete(centre, -1)
        self.core, self.remaining = self.selectCore(points, centre)
        self.proto = Prototype(self.core)
        self.propDict = {}
        self.label = []
        self.updateLabel()
        

    def selectCore(self, points, centre):
        """
        returns the core of the cluster, ie the elements that, on all directions,
        deviate by a most p standard deviantions
        """
        var = points.std() + EPSILON
        core = pd.DataFrame(columns = points.columns)
        remaining = pd.DataFrame(columns = points.columns)
        for idx, row in points.iterrows():
            new_data = pd.DataFrame([row], columns = core.columns, index = [idx])
            inCore = True
            for i in (row - centre) / var:
                if i > CORE_PARAM:
                    inCore = False
            if inCore:
                core = core.append(new_data)
            else:
                remaining = remaining.append(new_data)
        return core, remaining


    def updatePropDict(self):
        """
        this method computes a dictionnary that contains the proportions of presence of 
        each label among the data of the cluster
        """
        self.propDict = {}
        for idx in self.core.index:
            i = idx.split('#')[0]
            self.propDict[i] = 0

        for row in  self.core.itertuples():
            i = idx.split('#')[0]
            self.propDict[i] += 1

        for key in self.propDict.keys():
            self.propDict[key] /= len(self.core)


    def updateLabel(self):
        """
        this method gets the major labels of the cluster by selecting only the ones that
        at least 50% of the cluster have
        """
        self.updatePropDict()
        for k in self.propDict.keys():
            if self.propDict[k] >= 0.5:
                self.label.append(k)


    def distance(self, point):
        """
        computes the normalized distance between the point and the center of the
        Cluster
        """
        return np.linalg.norm((point-self.proto.centre)/self.proto.stdDev)


    def getContrast(self, point):
        """
        computes the contrast between the given point and the cluster
        """
        return (point-self.proto.centre)/self.proto.stdDev

        
class ContrastCluster(Cluster):
    """
    a contrastCluster differs from a cluster by the computation of the label
    """
    def __init__(self,points,centre):
        del(points['category'])
        centre = np.delete(centre, -1)
        self.core, self.remaining = self.selectCore(points, centre)
        self.proto = Prototype(self.core)
        self.label=[]
        self.updateLabel()
        

    def updateLabel(self, p = 0.5):
        for i in range(len(self.proto.centre)):
            if abs(self.proto.centre.values[i]) > p:
                if self.proto.centre.values[i] > 0:
                    sgn = '+'
                else:
                    sgn = '-'
                self.label.append(self.core.columns[i] + sgn)
        print(self.label)

