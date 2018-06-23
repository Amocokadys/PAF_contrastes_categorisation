# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture

import matplotlib.pyplot as plt


class BDD:
    """convert csv to DataFrame"""
    def __init__(self, fichierCSV):
        self.dataframe = pd.read_csv(fichierCSV)
    def resultFruit(self):
        """Processing for fruits data"""
        self.dataframe.index = self.dataframe["fruit"]
        del self.dataframe["fruit"]
        return self.dataframe
    def resultCancer(self):
        """Processing for cancer data"""
        self.dataframe.index = self.dataframe["diagnosis"]
        del self.dataframe["ID"]
        del self.dataframe["diagnosis"]
        return self.dataframe
    
    
class GMM:
    """Use the Gaussian Mixture Model to find clusters in a DataFrame"""
    def __init__(self, dataframe, number=-1, critere=0.1):
        self.ordonnees = None
        self.abscisse = None
        self.regPoly = None
        self.dataframe = dataframe
        self.critere=critere
        self.model = None
        if(number!=-1):
            self.number=number
        else:
            self.number = self.findK()
        
    def gmm(self,n):
        """execute gmm for n_clusters=n"""
        self.model = GaussianMixture(n_components = n)
        self.model.fit(self.dataframe)
        
    def countDistorsion(self,dataCategory,centre):
        """Calculates the distorsion in each cluster (euclidian distance between center and points"""
        del dataCategory['category']
        variancePoint = (dataCategory-centre[:len(dataCategory.columns)])**2
        cpt=0
        for k,row in variancePoint.iterrows():
            cpt2=0
            for j in range(len(row)):
                cpt2+=row[j]
            cpt+=np.sqrt(cpt2)
        return cpt
        
    def elbowMethod(self):
        """calculate the distorsion for each k"""
        ordonnees = []
        for k in range(2,50):
            self.gmm(k)
            self.newDataFrame()
            cpt=0
            for j in range(k):
                masque = self.dataframe["category"]==j
                dataCategory = self.dataframe[masque]
                cpt+=self.countDistorsion(dataCategory,self.model.means_[j])
            ordonnees.append(cpt)
        self.ordonnees=ordonnees
        self.abscisse=[k for k in range(2,50)]
    
    def traceElbow(self):
        """ trace the elbow """
        if(self.ordonnees==None or self.abscisse==None):
            self.elbowMethod()
        plt.plot(self.abscisse,self.ordonnees,'or')
        plt.xlabel('k')
        plt.ylabel('distorsion')
        plt.title('Distorsion')
        plt.show()
        
    def findK(self):
        """Find the best number of clusters"""
        self.elbowMethod()
        fit=np.polyfit(self.abscisse,self.ordonnees,15)
        self.regPoly = np.poly1d(fit)(self.abscisse)
        coeff = abs(self.regPoly[0] - self.regPoly[1])
        k=abs(self.regPoly[1]-self.regPoly[0])
        cpt=2
        while(k>coeff*self.critere and cpt<len(self.regPoly)):
            k=abs(self.regPoly[cpt]-self.regPoly[cpt-1])
            cpt+=1
        return cpt
        
    def traceReg(self):
        """Trace the polynomial regression of the elbow"""
        try:
            plt.plot(self.abscisse,self.regPoly,'or')
            plt.xlabel('k')
            plt.ylabel('distorsion')
            plt.title('Regression polynômiale - Distorsion')
            plt.show()
        except:
            print("Error, call findK first")
        
    def newDataFrame(self):
        """ adds the column category in the dataframe with the labels of the clusters """
        self.dataframe['category'] = pd.Series(self.model.predict(self.dataframe), index = self.dataframe.index)
        
    def result(self):
        """ return the coordinates of cluster's centers and the dataframe"""
        self.gmm(self.number)
        self.newDataFrame()
        return self.dataframe, self.model.means_
    

        
if __name__ == "__main__":
    bddObject = BDD("../data/fruitsModifiedAdjectives.csv")
    #bddObject = BDD("../data/wdbc.csv")
    dataFruit = bddObject.resultFruit()
    #dataCancer = bddObject.resultCancer()
    gmmObject = GMM(dataFruit)
    #gmmObject=GMM(dataCancer)
    gmmObject.traceElbow()
    gmmObject.traceReg()
    print(gmmObject.number)
    dataframe,centres = gmmObject.result()
    
    
    


