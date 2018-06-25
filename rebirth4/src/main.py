import gmm
import clusterisation
import contraste
import contrasteur 

import numpy as np

def clusters_from_dataframe(df):
    """
    determines clusters from a given dataframe
    input : df the dataframe from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mgmm = gmm.GMM(df)
    clusters, centres = mgmm.result()
    mclusters = clusterisation.Clusterisation(clusters, centres)
    return mclusters.result()
    

def clusters_from_db(filename):
    """
    determines clusters from a given data file (csv format)
    input : filename the name of the data file from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mbdd = gmm.BDD(filename)
    return clusters_from_dataframe(mbdd.resultFruit(), ncluster) # TODO : call the right result function


def getContrasteur(filename):
    """
    this function takes a filename as argument and build a contraster to classify
    data that would be provided later on
    """
    listCategory = clusters_from_db(filename)

    contrasteObject = contraste.Contraste(listCategory)
    listeContrastes = contrasteObject.result()

    return contrasteur.Contrasteur(listCategory, listeContrastes)


def main(filename, point):
    ctrst = getContrasteur(filename)
    category, contrast = ctrst.classify(point)
    return category.label, contrast.label


if __name__ == "__main__":
    #data = np.array([18, 10, 123, 1001, 0.12, 0.28, 0.3, 0.15, 0.24, 0.079, 1.1, 0.91, 8.6, 153, 0.0064, 0.049, 0.054, 0.016, 0.03, 0.0062, 25, 17, 185, 2019, 0.16, 0.66, 0.71, 0.27, 0.46, 0.12])
    data = np.array([40, 10, 222, 41, 22, 220, 94, 1.2])
    #print(*main("../data/fruitsModified.csv", 10, data), sep = '\n')
    
    res = main("../data/fruitsModifiedAdjectives.csv", 10, data)
    print(*res)
