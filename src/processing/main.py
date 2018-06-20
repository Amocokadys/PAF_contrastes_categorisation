import algo
import contrastes
import etape2
import kmeans
import pandas as pd

def traitement(data, number):
    pafGmm = gmm.PafGMM(data, number)
    clusters, centres = pafGmm.result()
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
    del data["Unnamed: 0"]
    clst, crst_clst = contrast(data)

    plt.scatter(clst.teinte,clst.fibres,c=pafkmeans.model.labels_.astype(np.float),edgecolor='k')
    plt.title('Classification K-means ')
    plt.xlabel("teintes")
    plt.ylabel("fibres")
    plt.show()
