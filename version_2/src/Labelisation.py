"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Cartouche
"""


class labelisation:
    """
    this class takes a cluster and give it  a ltabel depending
    on the labels of the objects into this cluster
    """

    def __init__(self, data, center):
        self.data = data
        self.center = center
        self.propDict = {}
        self.label = ""
        self.updateLabel()


    def updatePropDict(self):
        """
        function calculating a dictionary giving the proportion of 
        presence of each type in the data
        """
        self.propDict = {}
        for idx in self.data.index:
            self.propDict[idx] = 0
        for row in  self.data.itertuples():
            self.propDict[row[0]] += 1
        for idx in self.data.index:
            self.propDict[idx] /= len(self.data)


    def updateLabel(self):
        """
        function giving the label of a cluster as the type that is the most
        present in the cluster
        """
        self.updatePropDict()
        self.label = max(self.propDict, key = self.propDict.get)


    def result(self):
        return self.label, self.propDict

