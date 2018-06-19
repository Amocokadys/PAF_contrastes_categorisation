import numpy as np
import pandas as pd

"""
class describing a cluster with :
    - its center
    - its covariance matrix
    - the points it contains
    - its number
"""
class Cluster:
    """
        we calculate the covariance matrix of a set of points
        the input is a DataFrame containing the dataset of a cluster (including categories)
        the output is the covariance matrix of  the cluster in an array shape
    """          
    def matriceCovariance(self,dataframe) :
        nbLigne = len(dataframe)
        Esperances = dataframe.mean() # mean vector
        matrice = [] # covariance matrix to calculate
        for i in dataframe.columns :
            ligne_i=[]
            for j in dataframe.columns :
                covIJ = 0
                for k in range(nbLigne) :
                    covIJ += (dataframe[i][k] - Esperances[i]) * (dataframe[j][k] - Esperances[j])
                covIJ = covIJ/nbLigne
                ligne_i.append(covIJ)
            matrice.append(ligne_i)
        return(np.array(matrice))
    
    
    def __init__(self,points,centre,numero):
        if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        self.centre=centre
        self.numero=numero
        self.points=points
        self.matriceCov=self.matriceCovariance(points)
        
    """ this function calculates the distance from a point to a cluster in terms of
        number of standard deviations
        the input is an arraylist containing the coordinates of the point
        the output is a float representing the distance
    """
    def distance(self,point):
        """function that calculates the distance between the argument point and the cluster"""
        valeursPropres,passage=eig(self.matriceCov)
        print(passage)
        point=np.dot(passage,(point-self.centre))
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
        
    """ function to add points to a cluster when rebuilding it
        with standard deviation normalisation
    """
    def ajouterPoint(self,point):
        new_data = pd.DataFrame([point], columns = self.points.columns, index = pd.RangeIndex(start=100, stop=101, step=1))
        self.points = self.points.append(new_data)
