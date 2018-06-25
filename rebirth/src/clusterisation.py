import numpy as np
import pandas as pd


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
            clusters.append(Cluster(dataframe.loc[dataframe['category']==i],\
                                    means[i], self.isContrast))# for each cluster, selects the points in the cluster
    
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

    def __init__(self,points,centre, isContrast):
        """ if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        """
        self.centre=centre
        self.points=points #un dataframe
        self.propDict={}
        self.label=[]
        self.updateLabel(isContrast)
        self.subClusters=None
        self.sharpedData = None
        if isContrast: print(self.centre)
        
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


    def updatePropDict(self, isContrast):
        """
        this method computes a dictionnary that contains the proportions of presence of 
        each label among the data of the cluster
        """
        self.propDict = {}
        for idx in self.points.index:
            if not isContrast:
                lst_idx = [idx.split('#')[0]]
            else:
                lst_idx = idx.split('#')[1].split('~')[:-1]
            for i in lst_idx:
                self.propDict[i] = 0

        for idx, row in  self.points.iterrows():
            if not isContrast:
                lst_idx = [idx.split('#')[0]]
            else:
                lst_idx = idx.split('#')[1].split('~')[:-1]
            for i in lst_idx:
                self.propDict[i] += 1

        for key in self.propDict.keys():
            self.propDict[key] /= len(self.points)
        
        if isContrast:
            print(self.propDict)


    def updateLabel(self, isContrast):
        """
        this method gets the major labels of the cluster by selecting only the ones that
        at least 50% of the cluster have
        """
        self.updatePropDict(isContrast)
        for k in self.propDict.keys():
            self.label.append(k)
        
        
        
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