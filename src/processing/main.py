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

max_cancer = [None, None, None, None, None, None, 0.4, 0.2, None, None ] * 3

""" 
	max_cancer indique le comportement des différentes dimensions :
	-  None   -> l'échelle logarithmique est plus pertinente
	-  n > 0  -> l'échelle linéaire est plus pertinente, et les valeurs ne dépassent jamais n.
	"""

racine = Feuille(distribution = max_cancer)
i = 0
try:
	for k, row in data.iterrows():
		print("ajout de l'élément ",i)
		racine += Feuille(row.values[0],np.array(row.values[1:], dtype=np.float32))
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