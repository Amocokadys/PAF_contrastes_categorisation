import pandas as pd
from numpy.linalg import *
import numpy as np


class Cluster:
    """classe décrivant un cluster par
        -son centre
        -sa matrice de covariance
        -les points qu'il contient
        son numero"""
        
#On calcul la matrice de covariance d'un ensemble de point
#argument=dataframe correspondant à la liste des points d'un cluster (avec leur catégorie)
#sortie=matrice de covariance du cluster sous forme d'array    
    def matriceCovariance(self,dataframe):
        nbColonne=len(dataframe.columns)
        nbLigne=len(dataframe)
        Esperances=dataframe.mean()
        matrice=[]
        for i in dataframe.columns:
            ligneI=[]
            for j in dataframe.columns:
                covIJ=0
                for k in range(nbLigne):
                    covIJ+=(dataframe[i][k]-Esperances[i])*(dataframe[j][k]-Esperances[j])
                covIJ=covIJ/nbLigne
                ligneI.append(covIJ)
            matrice.append(ligneI)
        return(np.array(matrice))
    
    
    def __init__(self,points,centre,numero):
        if (len(points)==2):
            pointMoyen=[(points[i][0]+points[i][1]+1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        self.centre=centre
        self.numero=numero
        self.points=points
        self.matriceCov=self.matriceCovariance(points)
        
    #fonction qui calcule la distance d'un point à un cluster en nombre d'ecarts types    
    #arguments=point : arraylist contenant uniquement les coordonnées du point
    #sortie=float distance du point au cluster
    def distance(self,point):
        """function that calculates the distance between the argument point and the cluster"""
        valeursPropres,passage=eig(self.matriceCov)
        print(passage)
        point=np.dot(passage,point)
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
            diagonale[k][k]=valeursPropres[k]
        vect=np.dot(diagonale,point)
        norme=0
        for x in vect:
            norme+=x*x
        norme=np.sqrt(norme)
        return(norme)
        
    def ajouterPoint(self,point):
        new_data = pd.DataFrame([point], columns = self.points.columns, index = pd.RangeIndex(start=100, stop=101, step=1))
        self.points = self.points.append(new_data)