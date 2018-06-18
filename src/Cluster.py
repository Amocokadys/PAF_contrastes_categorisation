import sys
import pandas as pd
import numpy as np
import sklearn.metrics as sm
import matplotlib.pyplot as plt
import math as m

class Cluster:
    """classe décrivant un cluster par
        -son centre
        -sa matrice de covariance
        -les points qu'il contient
        -son numero"""

    def __init__(self,dataframePoints,centre,numero):
        self.centre=centre
        self.numero=numero
        self.points=dataframePoints
        self.matriceCov=self.matriceCovariance()

    #On calcul la matrice de covariance d'un ensemble de point
    #argument=dataframe correspondant à la liste des points d'un cluster (avec leur catégorie)
    #sortie=matrice de covariance du cluster sous forme d'array    
    def matriceCovariance(self):
        nbColonne=len(self.points.columns)
        nbLigne=len(self.points)
        Esperances=self.points.mean()
        matrice=[]
        for i in self.points.columns:
            ligneI=[]
            for j in self.points.columns:
                covIJ=0
                for k in range(nbLigne):
                    covIJ+=(self.points[i][k]-Esperances[i])*(self.points[j][k]-Esperances[j])
                covIJ=covIJ/nbLigne
                ligneI.append(covIJ)
            matrice.append(ligneI)
        return(np.array(matrice))

    #fonction qui calcule la distance d'un point à un cluster en nombre d'ecarts types    
    #arguments=point : arraylist contenant uniquement les coordonnées du point
    #sortie=float distance du point au cluster
    def distance(self,point):
        matriceInverse=np.linalg.inv(self.matriceCov)
        vect=np.dot(matriceInverse,point)
        norme=0
        for x in vect:
            norme+=x*x
        norme=np.sqrt(norme)
        return(norme)
