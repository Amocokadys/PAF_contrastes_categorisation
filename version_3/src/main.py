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
    #res=contrasteur.result(mclusters, listeContrastes, point) 
    return mclusters,listeContrastes,mgmm #res

    #return contrasteur.result(mclusters, point)

if __name__ == "__main__":
    #data = np.array([18, 10, 123, 1001, 0.12, 0.28, 0.3, 0.15, 0.24, 0.079, 1.1, 0.91, 8.6, 153, 0.0064, 0.049, 0.054, 0.016, 0.03, 0.0062, 25, 17, 185, 2019, 0.16, 0.66, 0.71, 0.27, 0.46, 0.12])
    point = np.array([40, 10, 222, 41, 22, 220, 94, 1.2])
    #print(*main("../data/fruitsModified.csv", 10, data), sep = '\n')
    #res = main("../data/fruitsModifiedAdjectives.csv", 10, data)
    data = pd.read_csv("../data/fruitsModifiedAdjectives.csv")
    if "fruit" in data.columns:
        del(data["fruit"])
    colonnes=np.array(data.columns)
    mclusters,listeContrastes, mgmm=main("../data/wdbc.csv", 10, point)

    appli = interfaceGraph.Application(colonnes,mclusters,listeContrastes,mgmm) 
    appli.mainloop()


#def main(filename, ncluster, point):
#    """
#    this function does something
#    """
#    mclusters,mgmm = clusters_from_db(filename, ncluster)
#    
#    colonnes=np.array(mclusters[0].getDataFrame().columns)
#    if 'category' in colonnes:
#        colonnes=colonnes[:-1]
#    #mcontrastes = contraste.Contraste(mclusters)
#    #mcontrastes = mcontrastes.result()
#    
#    #test de contraste, ajouter contrasteur après
#    contrasteObject = contraste.Contraste(mclusters)
#    listeContrastes = contrasteObject.result()
#    res=contrasteur.result(mclusters, listeContrastes, point) 
#    return res #mclusters,listeContrastes,mgmm 
#
#    #return contrasteur.result(mclusters, point)
#
#if __name__ == "__main__":
#    point = np.array([40, 10, 222, 41, 22, 220, 94, 1.2])
#    #mclusters,listeContrastes, mgmm=main("../data/wdbc.csv", 10, point)
#    ret=main("../data/wdbc.csv", 10, point)
#    colonnes=np.array(mclusters[0].points.columns)
#    print(ret)
#
#    #appli = interfaceGraph.Application(colonnes,mclusters,listeContrastes,mgmm) 
#    #appli.mainloop()
