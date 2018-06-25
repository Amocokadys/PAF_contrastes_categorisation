import numpy as np
import pandas as pd

infty = float(10**100)

class Clusterisation:
    """methods :
    init (input): -dataframe with category
                  -array of centers
                  
    result (output) : -list of clusters"""
    
    def __init__(self, dataframe, arrayCenters, isContrast = False):
        self.dataframe=dataframe
        self.arrayCenters=arrayCenters
        self.isContrast = isContrast

    def dataframeToCluster(self,dataframe,means):
        nb_clusters = len(means)
    
        # get clusters from data
        clusters=[]
        for i in range(nb_clusters):
            if not self.isContrast:
                clusters.append(Cluster(dataframe.loc[dataframe['category']==i],\
                                        means[i]))# for each cluster, selects the points in the cluster

            else:
                clusters.append(ContrastCluster(dataframe.loc[dataframe['category']==i],\
                                        means[i]))# for each cluster, selects the points in the cluster
    
        return clusters

    def result(self):
        return(self.dataframeToCluster(self.dataframe,self.arrayCenters))
 
 
"""
    functions for the manipulation of matrices
    useful to compute the normalized distance to a cluster
    see method Cluster.distance
"""

def emonde(D):
    """
        this function takes a diagonal matrix and returns it without the rows and
        columns that are null (the returned matrix is also square and diagonal)
        also returns the list of the suppressed dimensions
    """
    Mret = np.copy(D)
    supprDim = []
    for k in range(len(D)):
        if Mret[k][k] == 0:
            del(Mret[:, k])
            del(Mret[k, :])
            supprDim.append(k)
    return Mret, supprDim


def delDim(supprDim, x):
    """
        this function takes a vector and a list of dimensions to delete
        it returns the vector in which the given coordinates are deleted
    """
    xRet = np.copy(x)
    for k in supprDim:
        del(xRet[k])
    return xRet

"""
    End of definition of the matrices functions
"""

        
class Cluster:
    """
        we calculate the covariance matrix of a set of points
        the input is a DataFrame containing the dataset of a cluster (including categories)
        the output is the covariance matrix of  the cluster in an array shape
    """          
    
    def __repr__(self):
        return (" dataframe: \n"+str(self.points)+"\n center:"+str(self.centre)+"\n label:"+str(self.label))

    def __init__(self,points,centre):
        """ if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        """
        self.centre=centre
        self.points=points #un dataframe
        self.label=[]
        self.updateLabel()
        self.subClusters=None
        self.sharpedData = None
        self.compute_linalg()
        
    def setSubClusters(self,clusters):
        self.subClusters=clusters
      
    def setSharp(self,sharp):
        self.sharpedData = sharp
        
    def getSharp(self):
        return self.sharpedData
        
    def getDataFrame(self):
        return(self.points)    
       
    def getCenter(self):
        return(self.centre)
        
    def getLabel(self):
        return(self.label)
    
        
    """ function to add points to a cluster when rebuilding it
        with standard deviation normalisation
    """
    def ajouterPoint(self,point):
        new_data = pd.DataFrame([point], columns = self.points.columns, index = pd.RangeIndex(start=len(self.points), stop=len(self.points)+1, step=1))
        self.points = self.points.append(new_data)

    
    def compute_linalg(self):
        """
        compute the covariance matirx, its eigen properties and emondes it
        """
        self.cov = self.points.cov().values # the covariance matrix of the data set
        w, self.passage = np.linalg.eigh(self.cov) # the eigenvalues and eigenvectors of M
        D = np.diag(w) # M diagnalized
        self.diagCov, self.supprDim = emonde(D) # delete null values
        

    def distance(self, point):
        """
        this function computes the normalized distance between the center of the
        cluster and the point
        it is returned as a vector of two components : (n, d)
        n is the number of infinities of the diference (if the standard deviation
        along this axis is zero)
        d is the distance on the remaining axis
        """
        x = np.dot(self.passage, point-self.centre) # difference in the eigenbase of M
        n = 0
        xp = np.copy(x)
        for k in self.supprDim:
            if xp[k] != self.centre[k]:
                n += 1
            del(xp[k])
        d = np.linalg.norm(np.dot(np.linalg.inv(self.diagCov), xp)) # computes the normalized distance
        return (len(supprDim), d) # len(supprDim) is the number of infinity values


    def getContrast(self, point):
        """
        this function computes the normalized contrast of a point relative to the
        cluster
        if the standard deviation is infinite, returns np.inf
        """
        x = np.dot(self.passage, point-self.centre) # difference in the eigenbase of M
        xp = delDim(x, self.supprDim) # delete corresponding coordinates in x
        X = np.dot(np.linalg.inv(self.diagCov), xp) # computes the normalized distance
        for k in self.supprDim:
            if point[k] == self.centre[k]:
                np.insert(X, k, 0)
            else:
                np.insert(X, k, infty)
        return np.dot(np.linalg.inv(self.passage), X)


    def updatePropDict(self):
        """
        this method computes a dictionnary that contains the proportions of presence of 
        each label among the data of the cluster
        """
        self.propDict = {}
        for idx in self.points.index:
            i = idx.split('#')[0]
            self.propDict[i] = 0

        for idx, row in  self.points.iterrows():
            i = idx.split('#')[0]
            self.propDict[i] += 1

        for key in self.propDict.keys():
            self.propDict[key] /= len(self.points)


    def updateLabel(self):
        self.updatePropDict()
        for k in self.propDict.keys():
            if self.propDict[k] > 0.5:
                self.label.append(k)


class ContrastCluster(Cluster):
    def __init__(self,points,centre):
        """ if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        """
        self.centre=centre
        self.points=points #un dataframe
        self.label=[]
        self.updateLabel()
        self.subClusters=None
        self.sharpedData = None


    def updateLabel(self):
       """
       this method gives labels to the cluster according to the values of
       it center (if greater than 1, gives the label)
       """
       for k in range(len(self.centre)):
           if abs(self.centre[k]) >= 1:
               self.label.append(self.points.columns[k])
               print(self.label[-1], self.centre[k])

       if self.label == []:
           self.label.append("normal")
           print(self.label[-1], self.centre)
       print()

        
class SubCluster(Cluster):
    """To use the subclusters, herites from Cluster"""
    def __init__(self,dataframe,centers):
        super(self,dataframe,centers)
        
    #TODO nothing
    
        
class MainCluster(Cluster):
    """To use the subclusters, herites from Cluster"""
    def __init__(self,dataframe,centers):
        super(self,dataframe,centers,subClusters)
        self.subClusters=subClusters
        
    def getSubClusters(self):
        return(subClusters)
        
    def setClusters(self,subClusters):
        self.subClusters=subClustes
