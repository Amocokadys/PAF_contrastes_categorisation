import cluster
import contrastes
import gmm
import pandas as pd
from arborescence import Feuille, Arbre
import numpy as np
import ensemble

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
ensemble.Ensemble.dimension = len(data.columns)

del data["ID"]
data.index = data["diagnosis"]


racine = Arbre([], "~")
i = 0
try:
	for k, row in data.iterrows():
		print("ajout de l'élément ",i)
		racine += Feuille(np.array(row.values[1:], dtype=np.float32), row.values[0])
		i += 1
	print(racine)
except KeyboardInterrupt:
	print(racine)
	
	

		
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