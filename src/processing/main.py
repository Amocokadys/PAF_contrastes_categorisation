import cluster
import contrastes
import gmm
import pandas as pd
from arborescence import Feuille, Arbre
import numpy as np
import interfaceGraph

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


if __name__ == "__main__":
    appli = interfaceGraph.ApplicationInterface()
    appli.mainloop()
