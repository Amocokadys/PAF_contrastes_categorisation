"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Cartouche
"""

import cluster
import contrastes
import gmm
import pandas as pd
from arborescence import Feuille, Arbre
import numpy as np

def traitement(data, number):
    print(data.index)
    pafGmm = gmm.PafGMM(data, number)
    clusters, centres = pafGmm.result()
    print(clusters.index)
    clusterList = cluster.dataframeToCluster(clusters, centres)
    return clusterList

def contrast(data):
    processed_data = traitement(data)
    contrast_data = pd.DataFrame(columns = data.columns)
    for clst in processed_data:
        diffs = contrastes.calcDiffs(clst)
        contrast_data = contrast_data.append(diffs)
    return processed_data, traitement(contrast_data)


data = pd.read_csv("../../jeux de donne/breast_cancer/wdbc.csv")
del data["ID"]
data.index = data["diagnosis"]


""" 
	Arbre.distribution indique le comportement des différentes dimensions :
	-  None   -> l'échelle logarithmique est plus pertinente
	-  n > 0  -> l'échelle linéaire est plus pertinente, et les valeurs ne dépassent jamais n.
	"""

racine = Arbre([])
i = 0
try:
	for k, row in data.iterrows():
		print("ajout de l'élément ",i)
		racine += Feuille(np.array(row.values[1:], dtype=np.float32), \
					row.values[0] + str(i))
		i += 1
	print(racine)
except KeyboardInterrupt:
	racine.dessin()
	
	

		
"""
if __name__ == "__main__":
    data = pd.read_csv("../../fruitsModified.csv")
    data.index = data["Unnamed: 0"]
    del data["Unnamed: 0"]
    
    clstList = traitement(data, 10)

    pts = next(data.iterrows())[1]

    clust = clean.clusterPlusProcheEuclidien(clstList, pts)

    print(clust.label)
"""