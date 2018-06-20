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

from sklearn.mixture import GaussianMixture
from mpl_toolkits.mplot3d import Axes3D



class PafGMM:
    """ class with attributs a GaussianMixture objects 
        the dataframe on which we use kmean
        the number of clusters we want
    """
    
    def __init__(self, dataframe, number):
        self.dataframe = dataframe
        self.model = None
        self.number = number
        
    def gmm(self, number):
        """ execute gmm for n_clusters=number"""
        self.model = GaussianMixture(n_components = number)
        self.model.fit(self.dataframe)
        
    def newDataFrame(self):
        """ adds the column category in the dataframe with the labels of the clusters """
        self.dataframe['category'] = pd.Series(self.model.predict(self.dataframe), index = self.dataframe.index)
        
    def result(self):
        """ return the coordinates of cluster's centers and the dataframe"""
        #self.findElbow()
        self.gmm(self.number)
        self.newDataFrame()
        return self.dataframe
    
    
class Contraste:
    def __init__(self, categorisation, means, number):
        self.categorisation = categorisation
        shape = np.shape(means)
        self.means = np.append(means, np.zeros((shape[0], 1)), axis=1)
        self.contraste = pd.DataFrame([], columns = self.categorisation.columns)
        self.pafgmm = None
        self.number = number
    def createContraste(self):
        for k, row in self.categorisation.iterrows():
            new = row - self.means[int(row["category"])]
            self.contraste = self.contraste.append(new)
        del self.contraste["category"]
    def calcul(self):
        self.createContraste()
        self.pafgmm = PafGMM(self.contraste, self.number)
        return self.pafgmm.result()
    
    

def graphic_clusters_fruits(data):
    """ Visualisation des clusters  """

    plt.scatter(data.longueur,data.fibres,c=data.category.astype(np.float),edgecolor='k')
    plt.title('Classification K-means ')
    plt.xlabel("longueur")
    plt.ylabel("fibres")
    plt.show()
    
    plt.scatter(data.r,data.longueur,c=data.category.astype(np.float),edgecolor='k')
    plt.xlabel("rouge")
    plt.ylabel("longueur")
    plt.show()
    
    #cluster en 3D
    fig=plt.figure(1,figsize=(4,3))
    ax=Axes3D(fig,rect=[0,0,0.95,1],elev=48,azim=134)
    ax.scatter(data.r, data.v, data.b,c=data.category.astype(np.float), edgecolor='k')

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

def afficherChaqueCluster(pafGMM):
    """ Print each cluster """
    dataframe = pafGMM.dataframe
    for k in range(pafGMM.number):
        masque = dataframe['category']==k
        newDataframe=dataframe[masque]
        plt.scatter(newDataframe.longueur,newDataframe.fibres)
        plt.title('Classification GMM ')
        plt.xlabel("longueur")
        plt.ylabel("fibres")
        plt.show()
        print(newDataframe.index)

    
data = pd.read_csv("../../fruitsModified.csv")
data.index = data["Unnamed: 0"]
del data["Unnamed: 0"]


pafgmm = PafGMM(data, 10)
categorisation = pafgmm.result()

cr = Contraste(categorisation, pafgmm.model.means_, 10)
contraste = cr.calcul()

print(categorisation.sort_values(by = "category"))
print(contraste.sort_values(by = "category"))


#graphic_clusters_fruits(categorisation)
#afficherDatasCategory(categorisation)
afficherDatasCategory(contraste)
afficherChaqueCluster(pafgmm)
print("******************************")
afficherChaqueCluster(cr.pafgmm)


