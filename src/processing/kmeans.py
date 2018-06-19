# -*- coding: utf-8 -*-
#

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

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

#from sklearn import metrics

class PafKmeans:
    """ class with attributs a KMeans objects 
        the dataframe on which we use kmean
        the number of clusters we want
    """
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.model = None
        self.number = 4
        
    def kmeans(self, number):
        """ execute kmeans for n_clusters=numbe r"""
        self.model = KMeans(n_clusters = number)
        self.model.fit(self.dataframe)
        
    def sseTab(self):
        """ return the distorsion in all clusters, distorsion = mean distance with cluster's center """
        sse = []
        for clusters_number in range(1, 30):
            sse.append(0)
            self.kmeans(clusters_number)
            sse[clusters_number-1] += self.model.inertia_           
        return sse
        
    def findElbow(self):
        """ method to find k through the elbow method with slopes"""
        sse = self.sseTab()
        pentes = []
        for i in range(1, len(sse)):
            pentes.append(sse[i] - sse[i-1])
            
        k=1
        ang=180
        while(k<len(pentes)-1 and (abs(180-ang*180/np.pi)>110)):
            ang=abs(np.arctan(pentes[0])-np.arctan(pentes[k]))
            k+=1
            
        self.number=k
        
    def newDataFrame(self):
        """ adds the column category in the dataframe with the labels of the clusters """
        self.dataframe['category'] = pd.Series(self.model.labels_, index = self.dataframe.index)
        
    def result(self):
        """ return the coordinates of cluster's centers and the dataframe"""
        self.findElbow()
        self.kmeans(self.number)
        self.newDataFrame()
        return self.model.cluster_centers_, self.dataframe
    

def test_fruits():
    test = pd.read_csv("../../fruitsModified.csv")
    del test["Unnamed: 0"]
    pafkmeans=PafKmeans(test)
    #centers,data = pafkmeans.result()
    return pafkmeans

def test_livres():
    test=pd.read_csv("../../bibliothq.csv")
    test.index=test["livres"]
    del test["livres"]
    pafkmeans = PafKmeans(test)
    #centers, data = pafkmeans.result()
    return pafkmeans

def graphic_elbow(pafkmeans,title):
    """ 
        Trace the elbow curve
        arg : Pafkmeans object    
    """
    centers, data = pafkmeans.result()
    sse = pafkmeans.sseTab()
    plt.plot(np.arange(1, 30), sse, 'ro')
    plt.xlabel("k")
    plt.ylabel("distorsion") #distorsion = Somme variance (distance avec centre cluster)
    plt.title(title)
    plt.show()

def graphic_clusters_fruits(pafkmeans):
    #Visualisation des clusters formés par K-Means
    centers,data=pafkmeans.result()
    plt.scatter(data.r,data.fibres,c=pafkmeans.model.labels_.astype(np.float),edgecolor='k')
    plt.title('Classification K-means ')
    plt.xlabel("teintes")
    plt.ylabel("fibres")
    plt.show()
    
    plt.scatter(data.r,data.longueur,c=pafkmeans.model.labels_.astype(np.float),edgecolor='k')
    plt.xlabel("teintes")
    plt.ylabel("longueur")
    plt.show()
    
    #cluster en 3D
    fig=plt.figure(1,figsize=(4,3))
    ax=Axes3D(fig,rect=[0,0,0.95,1],elev=48,azim=134)
    ax.scatter(data.r, data.v, data.b,c=pafkmeans.model.labels_.astype(np.float), edgecolor='k')

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])

    plt.title("Classification k-mean 3D")

    ax.dist = 12
    plt.show()
    
    
def datasList(data):
    """ create list of datas """
    data = data.sort_values(by='category')
    ordo = [[] for k in range(len(data.columns)-1)] #datas
    absc = [] #categories
    for row in data.iterrows():
        absc.append(row[1][len(data.columns)-1])
        for k in range(len(data.columns)-1):
            ordo[k].append(row[1][k])
    return ordo,absc
    
def afficherDatasCategory(data):
    """ print all datas/categories """
    ordo,absc=datasList(data)
    for k in range(len(data.columns)-1):
        plt.plot(absc,ordo[k],'or')
        plt.xlabel("categories")
        plt.ylabel(data.columns[k])
        plt.title(data.columns[k] + "/category")
        plt.show()


def main():
    pafkmean_livres=test_livres()
    pafkmean_fruits=test_fruits()
    graphic_elbow(pafkmean_livres,"Elbow of books")
    graphic_elbow(pafkmean_fruits,"Elbow of fruits")
    graphic_clusters_fruits(pafkmean_fruits)
    
    afficherDatasCategory(pafkmean_livres.dataframe)
    afficherDatasCategory(pafkmean_fruits.dataframe)
    
    print("k_fruits = ",pafkmean_fruits.number)
    print("k_books = ",pafkmean_livres.number)
    
if __name__ == "__main__":
    main()
    """
    gmm = GaussianMixture(n_components=2)
    test=pd.read_csv("../../bibliothq.csv")
    test.index=test["livres"]
    del test["livres"]
    gmm.fit(test)
    print(gmm.means_)
    print(gmm.covariances_)
"""

