import pandas as pd
import numpy as np
import clean
import kmeans
import matplotlib.pyplot as plt

def calcDiffs(cluster):
    """
        This function computes the differences between the points of the cluster and its center
        Then, it standardizes these by the covariance matrix, and keeps only the components that
        are greater than the max divided by 10 (arbitrary)
    
        returns a DataFrame containing the calculated rows
    """
    diffs = pd.DataFrame(columns = cluster.points.columns)
    for idx, row in cluster.points.iterrows():
        new = row - cluster.centre # computing the difference
        norm_new = pd.Series(np.dot(np.linalg.inv(cluster.matriceCov), new), index = new.index) # standardization
        maximum = norm_new.max()
        condition = norm_new < maximum/10
        norm_new.mask(condition, other = 0, inplace = True) # selection of the greatest values (greater than max/10)
        diffs = diffs.append(norm_new, ignore_index = True)
    return diffs

def traitement(data):
    pafKmeans=kmeans.PafKmeans(data)
    centres, clusters=pafKmeans.result()
    return clean.clean_kmeans(clusters, centres)

def contrast(data):
    processed_data = traitement(data)
    contrast_data = pd.DataFrame(columns = data.columns)
    for clst in processed_data:
        diffs = calcDiffs(clst)
        contrast_data = contrast_data.append(diffs)
    return processed_data, traitement(contrast_data)

def graphicsClusters(data):
    clusterList=traitement(data)
    for k in clusterList:
        plt.scatter(k.points.longueur,k.points.fibres)
        plt.title('Classification K-means ')
        plt.xlabel("longueur")
        plt.ylabel("fibres")
        plt.show()
        print(k.points.index)
        

if __name__ == "__main__":
    #test of the function
    """
    d = pd.DataFrame(np.array([[-5, 5, 0], [-4, 4, 0.1], [-7, 4, 0.5], [-4, 7, 6], [-7, 7, 0.9],\
                               [5, -5, 8], [4, -4, 0.05], [7, -4, 0.6], [4, -7, 2], [7, -7, 0]]),\
                     columns = ['x', 'y', 'z'])
    c = cluster.Cluster(d, np.array([0, 0, 0.3]), 0)
    print(calcDiffs(c)) 
    

    clst, crst_clst = contrast(data)
    print(*[cl.points for cl in clst], sep = '\n')
    print(*[cl.points for cl in crst_clst], sep = '\n')
    """
    """ TODO : affichage """
    
    data = pd.read_csv("../../fruitsModified.csv")
    del data["Unnamed: 0"]

    graphicsClusters(data)    
