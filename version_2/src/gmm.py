# -*- coding: utf-8 -*-

"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Cartouche
"""

import pandas as pd
from sklearn.mixture import GaussianMixture


class BDD:
    """convert csv to DataFrame"""
    def __init__(self, fichierCSV):
        self.dataframe = pd.read_csv(fichierCSV)
    def resultFruit(self):
        """Processing for fruits data"""
        self.dataframe.index = self.dataframe["fruit"]
        del self.dataframe["fruit"]
        return self.dataframe
    def resultCancer(self):
        """Processing for cancer data"""
        self.dataframe.index = self.dataframe["diagnosis"]
        del self.dataframe["ID"]
        del self.dataframe["diagnosis"]
        return self.dataframe
    
    
class GMM:
    """Use the Gaussian Mixture Model to find clusters in a DataFrame"""
    def __init__(self, dataframe, number):
        self.dataframe = dataframe
        self.model = None
        self.number = number
        
    def gmm(self):
        """ execute gmm for n_clusters=self.number"""
        self.model = GaussianMixture(n_components = self.number)
        self.model.fit(self.dataframe)
        
    def newDataFrame(self):
        """ adds the column category in the dataframe with the labels of the clusters """
        self.dataframe['category'] = pd.Series(self.model.predict(self.dataframe), index = self.dataframe.index)
        
    def result(self):
        """ return the coordinates of cluster's centers and the dataframe"""
        self.gmm()
        self.newDataFrame()
        return self.dataframe, self.model.means_
    
    

        
        
        


