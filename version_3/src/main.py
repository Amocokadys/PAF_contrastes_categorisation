"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Cartouche
"""

import gmm
import clusterisation
import contraste
import contrasteur
import pandas as pd
import interfaceGraph

import numpy as np

def clusters_from_dataframe(df, ncluster):
    """
    determines clusters from a given dataframe
    input : df the dataframe from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mgmm = gmm.GMM(df)
    clusters, centres = mgmm.result()
    mclusters = clusterisation.Clusterisation(clusters, centres)
    return mclusters.result(),mgmm
    

def clusters_from_db(filename, ncluster):
    """
    determines clusters from a given data file (csv format)
    input : filename the name of the data file from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mbdd = gmm.BDD(filename)
    return clusters_from_dataframe(mbdd.resultFruit(), ncluster) # TODO : call the right result function

def main(filename, ncluster, point):
    """
    this function classify the point of the input by its category and its contrast
    category according to the model given as input
    """
    mclusters,mgmm = clusters_from_db(filename, ncluster)
    
    colonnes=np.array(mclusters[0].getDataFrame().columns)
    if 'category' in colonnes:
        colonnes=colonnes[:-1]
    
    #test de contraste, ajouter contrasteur après
    contrasteObject = contraste.Contraste(mclusters)
    listeContrastes = contrasteObject.result()
    return mclusters,listeContrastes,mgmm #res


if __name__ == "__main__":
    point = np.array([40, 10, 222, 41, 22, 220, 94, 1.2])
    data = pd.read_csv("../data/fruitsModifiedAdjectives.csv") # the test data to be classified
    if "fruit" in data.columns:
        del(data["fruit"])
    colonnes=np.array(data.columns)
    mclusters,listeContrastes, mgmm=main("../data/fruitsModifiedAdjectives.csv", 10, point)

    appli = interfaceGraph.Application(colonnes,mclusters,listeContrastes,mgmm) 
    appli.mainloop()


