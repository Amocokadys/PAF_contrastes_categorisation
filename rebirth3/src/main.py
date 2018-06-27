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
    return clusters_from_dataframe(mbdd.resultCancer(), ncluster) # TODO : call the right result function


def main(filename, ncluster, point):
    """
    this function does something
    """
    mclusters,mgmm = clusters_from_db(filename, ncluster)
    
    colonnes=np.array(mclusters[0].getDataFrame().columns)
    if 'category' in colonnes:
        colonnes=colonnes[:-1]
    #mcontrastes = contraste.Contraste(mclusters)
    #mcontrastes = mcontrastes.result()
    
    #test de contraste, ajouter contrasteur après
    contrasteObject = contraste.Contraste(mclusters)
    listeContrastes = contrasteObject.result()
    res=contrasteur.result(mclusters, listeContrastes, point) 
    return res #mclusters,listeContrastes,mgmm 

    #return contrasteur.result(mclusters, point)

if __name__ == "__main__":
    point = np.array([40, 10, 222, 41, 22, 220, 94, 1.2])
    #mclusters,listeContrastes, mgmm=main("../data/wdbc.csv", 10, point)
    ret=main("../data/wdbc.csv", 10, point)
    colonnes=np.array(mclusters[0].points.columns)
    print(ret)

    #appli = interfaceGraph.Application(colonnes,mclusters,listeContrastes,mgmm) 
    #appli.mainloop()
