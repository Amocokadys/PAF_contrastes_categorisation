import numpy as np


class Clusterisation:
    """methods :
    init (input): -dataframe with category
                  -array of centers
                  
    result (output) : -list of clusters"""
    
    def __init__(self, dataframe, arrayCenters):
        self.dataframe=dataframe
        self.arrayCenters=arrayCenters
        
    def dataframeToCluster(self,dataframe,means):
        nb_clusters = len(means)
    
        # get clusters from data
        clusters=[]
        for i in range(nb_clusters):
            clusters.append(Cluster(dataframe.loc[dataframe['category']==i],\
                                means)) # for each cluster, selects the points in the cluster
    
        return clusters

    def result(self):
        return(self.dataframeToCluster(self.dataframe,self.arrayCenters))
 
 
 
 
 
 
        
class Cluster:
    """
        we calculate the covariance matrix of a set of points
        the input is a DataFrame containing the dataset of a cluster (including categories)
        the output is the covariance matrix of  the cluster in an array shape
    """          
    
    def __repr__(self):
        return (" dataframe: \n"+str(self.points)+"\n center:"+str(self.centre)+"\n label:"+str(self.label))

    def __init__(self,points,centre):
        
        if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        self.centre=centre
        self.points=points #un dataframe
        self.propDict={}
        self.label=""
        self.updateLabel()
      
      
        
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


    
    def updatePropDict(self):
        self.propDict = {}
        for idx in self.points.index:
            self.propDict[idx] = 0
        for row in  self.points.itertuples():
            self.propDict[row[0]] += 1
        for idx in self.points.index:
            self.propDict[idx] /= len(self.points)

    def updateLabel(self):
        self.updatePropDict()
        self.label=max(self.propDict, key = self.propDict.get)
        
        
        
        
class SubCluster(Cluster):
    """To use the subclusters, herites from Cluster"""
    
    def __init__(self,dataframe,centers):
        super(self,dataframe,centers)
    
        
class MainCluster(Cluster):
    """To use the subclusters, herites from Cluster"""
    
    def __init__(self,dataframe,centers):
        super(self,dataframe,centers)        