import gmm
import clusterisation
import contraste
import contrasteur 

import numpy as np

def clusters_from_dataframe(df, isContrast = True):
    """
    determines clusters from a given dataframe
    input : df the dataframe from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mgmm = gmm.GMM(df)
    clusters, centres = mgmm.result()
    mclusters = clusterisation.Clusterisation(clusters, centres, isContrast)
    return mclusters.result()
    

def clusters_from_db(filename):
    """
    determines clusters from a given data file (csv format)
    input : filename the name of the data file from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mbdd = gmm.BDD(filename)
    return clusters_from_dataframe(mbdd.resultFruit(), False) # TODO : call the right result function


def getContrasteur(filename):
    """
    this function takes a filename as argument and build a contraster to classify
    data that would be provided later on
    """
    listCategory = clusters_from_db(filename)

    coreCtrst, remainingCtrst = contraste.contrastClusterlist(listCategory)
    listeContrastes = clusters_from_dataframe(coreCtrst)

    return contrasteur.Contrasteur(listCategory, listeContrastes)


def main(filename, point):
    ctrst = getContrasteur(filename)
    category, contrast = ctrst.classify(point)
    return category.label, contrast.label


if __name__ == "__main__":
    data = np.array([20, 10, 222, 41, 22, 220, 94, 1.2])
    
    res = main("../data/fruitsModifiedAdjectives.csv", data)
    print(*res)
