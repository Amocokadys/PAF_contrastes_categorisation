# -*- coding: utf-8 -*-
#
# Telecom ParisTech : https://www.telecom-paristech.fr
# Projet PAF - 2018 : https://paf.telecom-paristech.fr
#
# Antoine Bellami
# Aurelien Blicq
# Clement Bonet
# Benoit Malezieux
# Louis Penet de Monterno
# Bastien Vagne


import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from sklearn import metrics

class PafKmeans:
    """ class with attributs a KMeans objects 
        the dataframe on which we use kmean
        the number of clusters we want
    """
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.model = None
        self.number = 4
        self.silhouette=None
        
    def kmeans(self, number):
        """ execute kmeans for n_clusters=numbe r"""
        self.model = KMeans(n_clusters = number)
        self.model.fit(self.dataframe)
    
    def findN(self):
        """ finds the ideal k through the silhouette metric : https://en.wikipedia.org/wiki/Silhouette_(clustering) """        
        res=np.arange(20,dtype='double')
        for k in np.arange(2,22):
            self.kmeans(k)
            res[k-2]=metrics.silhouette_score(self.dataframe,self.model.labels_)   
        self.number=np.argmax(res[2:])+4 #first values not pertinent
        self.silhouette=res
        
    def newDataFrame(self):
        """ adds the column category in the dataframe with the labels of the clusters """
        self.dataframe['category'] = pd.Series(self.model.labels_, index = self.dataframe.index)
        
    def result(self):
        """ return the coordinates of cluster's centers and the dataframe"""
        self.findN()
        self.kmeans(self.number)
        self.newDataFrame()
        return self.model.cluster_centers_, self.dataframe
    

if __name__=="__main__":
    test = pd.read_csv("fruitsModified2.csv")
    del test["Unnamed: 0"]
    pafkmeans = PafKmeans(test)
    centers, data = pafkmeans.result()

    #Visualisation des clusters formés par K-Means
    plt.scatter(data.teinte,data.fibres,c=pafkmeans.model.labels_.astype(np.float),edgecolor='k')
    plt.title('Classification K-means ')
    plt.xlabel("teintes")
    plt.ylabel("fibres")
    plt.show()

    plt.scatter(data.teinte,data.longueur,c=pafkmeans.model.labels_.astype(np.float),edgecolor='k')
    plt.xlabel("teintes")
    plt.ylabel("longueur")
    plt.show()

    #cluster en 3D
    fig=plt.figure(1,figsize=(4,3))
    ax=Axes3D(fig,rect=[0,0,0.95,1],elev=48,azim=134)
    ax.scatter(data.teinte, data.fibres, data.longueur,c=pafkmeans.model.labels_.astype(np.float), edgecolor='k')

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])

    plt.title("Classification k-mean 3D")

    ax.dist = 12
    plt.show()

    """ Tracé de la métrique silhouette : plus on est proche de 1, plus le nombre de clusters est ok"""
    res=pafkmeans.silhouette
    print("res = ",res)
    print("k =",pafkmeans.number)
    plt.plot(np.arange(2, 11,1), res, 'ro')
    plt.xlabel("k")
    plt.ylabel("Score sur 1")
    plt.show()
