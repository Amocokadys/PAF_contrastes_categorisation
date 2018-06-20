import gmm
import clusterisation
import contraste
import contrasteur 

def clusters_from_dataframe(df, ncluster):
    """
    determines clusters from a given dataframe
    input : df the dataframe from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mgmm = gmm.GMM(df, ncluster)
    mclusters = clusterisation.Clusterisation(*mgmm.result())
    return mclusters.result()
    

def clusters_from_db(filename, ncluster):
    """
    determines clusters from a given data file (csv format)
    input : filename the name of the data file from whom infer the clusters
    input : ncluster the number of clusters to separate
    """
    mbdd = gmm.BDD(filename)
    return clusters_from_dataframe(mBDD.result; ncluster) # TODO : call the right result function


def main(filename, ncluster, point):
    """
    this function does something
    """
    mclusters = clusters_from_db(filename, ncluster)
    #mcontrastes = contraste.Contraste(mclusters)
    #mcontrastes = mcontrastes.result()
    mcontrasteur = contrasteur.Contrasteur(mclusters, point)
    return mcontrasteur.result()
