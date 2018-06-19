import algo
import contrastes
import etape2
import kmeans
import pandas as pd

def traitement(data):
    pafKmeans=kmeans.PafKmeans(data)
    centres, clusters=pafKmeans.result()
    cln_clusters = algo.clean_kmeans(clusters, centres)
    return etape2.mainEtape2(cln_clusters)

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
