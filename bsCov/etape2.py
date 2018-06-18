import pandas as pd
import numpy as np

#On calcul la matrice de covariance d'un ensemble de point
#argument=dataframe correspondant à la liste des points d'un cluster (avec leur catégorie)
#sortie=matrice de covariance du cluster sous forme d'array
def matriceCovariance(dataframe):
    dataSansCategorie=dataframe.copy()
    del(dataSansCategorie['Categorie'])
    nbColonne=len(dataSansCategorie.columns)
    nbLigne=len(dataSansCategorie)
    Esperances=dataSansCategorie.mean()
    matrice=[]
    for i in dataSansCategorie.columns:
        ligneI=[]
        for j in dataSansCategorie.columns:
            covIJ=0
            for k in range(nbLigne):
                covIJ+=(dataSansCategorie[i][k]-Esperances[i])*(dataSansCategorie[j][k]-Esperances[j])
            covIJ=covIJ/nbLigne
            ligneI.append(covIJ)
        matrice.append(ligneI)
    return(np.array(matrice))
    

#fonction qui calcule la distance d'un point à un cluster en nombre d'ecarts types    
#arguments=cluster : objet contenant une dataframe de la liste de ses points, point : arraylist contenant uniquement les coordonnées du point
#sortie=float distance du point au cluster
def distance(cluster,point):
    #matriceInverse=np.linalg.inv.matriceCovariance(cluster.dataframe) 
     #TODO remplacer par l'expression exacte
    matriceInverse=np.linalg.inv(matriceCovariance(cluster))
    vect=np.dot(matriceInverse,point)
    norme=0
    for x in vect:
        norme+=x*x
    norme=np.sqrt(norme)
    return(norme)
    
    
#associe un point à au cluster duquel il est le plus proche en nombre d'ecarts types
def clusterPlusProche(dataframe,point):
    #TODO
    return()
    
    
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