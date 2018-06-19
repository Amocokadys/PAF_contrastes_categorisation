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
        diffs = diffs.append(new, ignore_index = True)
    """
        valeursPropres,passage=np.linalg.eig(cluster.matriceCov)
        somme=0
        for sigma in valeursPropres:
            if (sigma != 0):
                somme+=(1/sigma**2)
        n=len(valeursPropres)
        for k in range(n):              #the diagonal matrix is being inversed, together with the replacement of the '1/0' by somme
            if (valeursPropres[k]==0):
                valeursPropres[k]=somme
            else:
                valeursPropres[k]=1/valeursPropres[k]
        diagonale=np.zeros((n,n))
        for k in range(n):
            diagonale[k][k] = valeursPropres[k]
        pseudo_inverse = np.dot(np.dot(passage, diagonale), np.linalg.inv(passage))

        norm_new = pd.Series(np.real(np.dot(pseudo_inverse, new)), index = new.index) # standardization
        maximum = norm_new.max()
        condition = norm_new < maximum/10
        norm_new.mask(condition, other = 0, inplace = True) # selection of the greatest values (greater than max/10)
        diffs = diffs.append(norm_new, ignore_index = True)
    """

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
    del contrast_data["category"]
    return processed_data, traitement(contrast_data)

if __name__ == "__main__":
    #test of the function
    """
    d = pd.DataFrame(np.array([[-5, 5, 0], [-4, 4, 0.1], [-7, 4, 0.5], [-4, 7, 6], [-7, 7, 0.9],\
                               [5, -5, 8], [4, -4, 0.05], [7, -4, 0.6], [4, -7, 2], [7, -7, 0]]),\
                     columns = ['x', 'y', 'z'])
    c = cluster.Cluster(d, np.array([0, 0, 0.3]), 0)
    print(calcDiffs(c)) """
    
    data = pd.read_csv("../../fruitsModified.csv")
    del data["Unnamed: 0"]
    del data["v_eau"]
    del data["v_longueur"]
    del data["v_largeur"]
    del data["v_rvb"]
    del data["v_sucre"]
    del data["v_fibre"]

    clst, crst  = contrast(data)
    print(*[cl.points for cl in clst], sep = '\n')
    print(*[cl.points for cl in crst], sep = '\n')
