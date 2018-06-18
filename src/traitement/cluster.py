import pandas as pd

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
        matriceInverse=np.linalg.inv(self.matriceCov)
        vect=np.dot(matriceInverse,point)
        norme=0
        for x in vect:
            norme+=x*x
        norme=np.sqrt(norme)
        return(norme)
        
    def ajouterPoint(self,point):
        new_data = pd.DataFrame([point], columns = self.points.columns, index = pd.RangeIndex(start=100, stop=101, step=1))
        self.points = self.points.append(new_data)