import numpy as np
import pandas as pd


class Clusterisation:
    """methods :
    init (input): -dataframe with category
                  -array of centers
                  
    result (output) : -list of clusters"""
    
    def __init__(self, dataframe, arrayCenters, isContrast = False, dimension = None):
        self.dataframe = dataframe
        self.arrayCenters = arrayCenters
        self.isContrast = isContrast
        self.dimension = dimension
        

    def dataframeToCluster(self,dataframe,means):
        nb_clusters = len(means)
    
        # get clusters from data
        clusters = []
        for i in range(nb_clusters):
            if self.isContrast:
                clusters.append(ContrastCluster(dataframe.loc[dataframe['category']==i],\
                                       means[i], self.dimension)) # for each cluster, selects the points in the cluster
            else:
                clusters.append(Cluster(dataframe.loc[dataframe['category']==i],\
                                        means[i])) # for each cluster, selects the points in the cluster

        protos = []
        for c in clusters:
            core = c.selectCore()
            protos.append(Prototype(core))
        return clusters, protos


    def result(self):
        return(self.dataframeToCluster(self.dataframe,self.arrayCenters))
 

class Prototype:
    """
    this class contains the prototype of an object abstracted by a cluster
    it contains a center an a standard deviation over every dimension of the space
    """
    def __init__(self, points):
        self.centre = points.mean()
        self.stdDev = points.std()
        

class Cluster:
    """
        we calculate the covariance matrix of a set of points
        the input is a DataFrame containing the dataset of a cluster (including categories)
        the output is the covariance matrix of  the cluster in an array shape
    """          
    
    def __repr__(self):
        return (" dataframe: \n"+str(self.points)+"\n center:"+str(self.centre)+"\n label:"+str(self.label))


    def __init__(self, points, centre):
        """
        if (len(points) == 2) :
            pointMoyen = [(points[i][0] + points[i][1] + 1.0001)/2 for i in points.columns]
            new_data = pd.DataFrame([pointMoyen], columns = points.columns, index = pd.RangeIndex(start=2, stop=3, step=1))
            points = points.append(new_data)
        """
        self.propDict = {}
        self.label = []
        self.updateLabel()
        # TODO : update the label function
        self.core, self.remaining = self.selectCore(points, centre)
        self.proto = Prototype(self.core)
        

    def selectCore(self, points, p = 3):
        """
        returns the core of the cluster, ie the elements that, on all directions,
        deviate by a most p standard deviantions
        """
        var = points.std()
        core = pd.DataFrame(columns = points.columns)
        remaining = pd.DataFrame(columns = points.colums)
        for _, row in points.iterrows():
            inCore = True
            for i in (row - centre) / var:
                if i > p:
                    inCore = False
            if inCore:
                core = core.append(row)
        return core, remaining


    def updatePropDict(self):
        """
        this method computes a dictionnary that contains the proportions of presence of 
        each label among the data of the cluster
        """
        self.propDict = {}
        for idx in self.points.index:
            if '#' in idx:
                lst_idx = [idx.split('#')[0]]
            else:
                lst_idx = idx.split('~')[:-1]
            for i in lst_idx:
                self.propDict[i] = 0

        for row in  self.points.itertuples():
            if '#' in idx:
                lst_idx = [idx.split('#')[0]]
            else:
                lst_idx = idx.split('~')[:-1]
            for i in lst_idx:
                self.propDict[i] += 1

        for key in self.propDict.keys():
            self.propDict[key] /= len(self.points)


    def updateLabel(self):
        """
        this method gets the major labels of the cluster by selecting only the ones that
        at least 50% of the cluster have
        """
        self.updatePropDict()
        for k in self.propDict.keys():
            if self.propDict[k] >= 0.5:
                self.label.append(k)
        
class ContrastCluster(Cluster):
    def __init__(self,points,centre,dimension):
        self.centre=centre
        self.points=points #un dataframe
        self.propDict = {'=':0, '+':0, '-':0}
        self.label=[]
        self.subClusters=None
        self.sharpedData = None
        self.dim=dimension
        self.updateLabel()
        
    def updatePropDict(self):
        s = self.points[self.dim]
        for idx, val in s.iteritems():
            if val == 0:
                self.propDict['=']+=1
            elif val < 0:
                self.propDict['-']+=1
            else:
                self.propDict['+']+=1

    def updateLabel(self):
        self.updatePropDict()
        self.label.append(max(self.propDict, key = self.propDict.get))
