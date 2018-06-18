import pandas as pd
import numpy as np
    
#associe un point à au cluster duquel il est le plus proche en nombre d'ecarts types
def clusterPlusProche(listeCluster,listeCentre,point):
    plusProche=0
    distanceMin=1  #distance=1/(1+distance) en fait pour éviter d'avoir des infinis
    for k in range(len(listeCentre)):
        distanceCourante=1/(1+listeCluster[k].distance(point))
        if distanceCourante>distanceMin:
            plusProche=k
            distanceMin=distanceCourante
    return(plusProche)
    
def clusteriseAvecEcartsTypes(listeCluster,listeCentre,listePointsRestants):
    listeObjetsCluster=[]
    for k in range(len(listeCluster)):
        clusterk=Cluster(listeCluster[k],listeCentre[k],k)
        listeObjetsCluster.append(clusterk)
    listePointsRestants=np.array(listePointsRestants)
    for point in listePointsRestants:
        plusProche=clusterPlusProche(listeObjetsCluster,listeCentre,point)
        listeObjetsCluster[k].ajouterPoint(point)
    return(listeObjetsCluster)
        
def mainEtape2(clusters):
    return(clusteriseAvecEcartsTypes(clusters[0][:-1],clusters[1],clusters[0][-1]))
    
"""test:
import random as rd
ar=[]
for k in range(100):
    r=rd.randint(-1,1)
    ar.append([r+(rd.random()-0.5)/100,(rd.random()-0.5)/100-r,0])
dt=pd.DataFrame(np.array(ar),columns=['A','B','Categorie'])
point=[1,1]
print(matriceCovariance(dt))
print(distance(dt,point))"""