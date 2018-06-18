import algo
import cluster
import contrastes
import etape2
import kmeans

def traitement(data):
    pafKmeans=kmean.PafKmeans(data)
    centres, clusters=pafKmeans.result()
    cln_clusters = algo.clean_cluster(clusters, centres)
    return etape2.mainEtape2(cln_clusters)

def contrast(data):
    processed_data = traitement(data)
    contrast_data = pd.DataFrame(columns = data.columns)
    for clst in processed_data:
        diffs = contrastes.calcDiffs(clst)
        contrast_data = contrast_data.append(diffs)
    return traitement(contrast_data)