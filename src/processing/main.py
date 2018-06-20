import cluster
import contrastes
import clean
import gmm
import pandas as pd

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
    data = pd.read_csv("../../fruitsModified.csv")
    data.index = data["Unnamed: 0"]
    del data["Unnamed: 0"]
    
    clstList = traitement(data, 10)

    pts = next(data.iterrows())[1]

    clust = clean.clusterPlusProcheEuclidien(clstList, pts)

    print(clust.label)
