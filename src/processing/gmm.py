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
    
    
        
    
data = pd.read_csv("fruitsModified.csv")
data.index = data["Unnamed: 0"]
del data["Unnamed: 0"]


pafgmm = PafGMM(data, 10)
categorisation = pafgmm.result()

contraste = Contraste(categorisation, pafgmm.model.means_, 10).calcul()

print(categorisation)
print(contraste)



