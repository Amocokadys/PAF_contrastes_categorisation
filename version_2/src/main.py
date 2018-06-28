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

import numpy as np

def clusters_from_dataframe(df, ncluster):
    """
    determines clusters from a given dataframe
    input : df the dataframe from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mgmm = gmm.GMM(df, ncluster)
    clusters, centres = mgmm.result()
    mclusters = clusterisation.Clusterisation(clusters, centres)
    return mclusters.result()
    

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
    this function categorize the given data by giving its category and contrast
    category according to the model learnt from the given data
    """
    mclusters = clusters_from_db(filename, ncluster)
    #mcontrastes = contraste.Contraste(mclusters)
    #mcontrastes = mcontrastes.result()
    
    #test de contraste, ajouter contrasteur après
    contrasteObject = contraste.Contraste(mclusters)
    listeContrastes = contrasteObject.result()

    return contrasteur.result(mclusters, listeContrastes, point) 

    #return contrasteur.result(mclusters, point)

if __name__ == "__main__":
    data = np.array([10, 10, 222, 41, 22, 220, 94, 1.2]) # the test point to be classified
    
    cat, adj = main("../data/fruitsModifiedAdjectives.csv", 10, data)
    

    
    print(cat, adj)
