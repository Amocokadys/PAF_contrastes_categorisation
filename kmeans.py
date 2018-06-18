# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from sklearn import metrics

class PafKmeans(object):
    """ class with attributs a KMeans objects 
        the dataframe on which we use kmean
        the number of clusters we want
    """
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.model = None
        self.number = 4
        
    def kmeans(self, number):
        """ execute kmeans for n_clusters=numbe r"""
        self.model = KMeans(n_clusters = number)
        self.model.fit(self.dataframe)
        
    def sseTab(self):
        """ return the distorsion in all clusters """
        sse = []
        for clusters_number in range(1, 10):
            sse.append(0)
            self.kmeans(clusters_number)
            sse[clusters_number-1] += self.model.inertia_           
        return sse
    
    def findN(self):
        """ finds the ideal k through the silhouette metric """        
        res=np.arange(7,dtype='double')
        for k in np.arange(2,9):
            self.kmeans(k)
            res[k-2]=metrics.silhouette_score(self.dataframe,self.model.labels_)            
        self.number=np.argmax(res)+2
        
    def newDataFrame(self):
        """ adds the column category in the dataframe with the labels of the clusters """
        self.dataframe['category'] = pd.Series(self.model.labels_, index = self.dataframe.index)
        
    def result(self):
        """ return the coordinates of cluster's centers and the dataframe"""
        self.findN()
        self.kmeans(self.number)
        self.newDataFrame()
        return self.model.cluster_centers_, self.dataframe
    


test = pd.read_csv("fruitsModified.csv")
del test["Unnamed: 0"]
pafkmeans = PafKmeans(test)

# La courbe en "coude"
centers, data = pafkmeans.result()
sse = pafkmeans.sseTab()
plt.plot(np.arange(1, 10), sse, 'ro')
plt.xlabel("k")
plt.ylabel("Distorsion")
plt.show()


print("k = " + str(pafkmeans.number))
print(pafkmeans.result())

colormap=np.array(['Red','green','blue'])

#Visualisation des clusters formés par K-Means
plt.scatter(data.teinte,data.fibres,c=pafkmeans.model.labels_.astype(np.float),edgecolor='k')
plt.title('Classification K-means ')
plt.xlabel("teintes")
plt.ylabel("fibres")
plt.show()

plt.scatter(data.teinte,data.longueur,c=pafkmeans.model.labels_.astype(np.float),edgecolor='k')
plt.xlabel("teintes")
plt.ylabel("longueur")
plt.show()

#cluster en 3D
fig=plt.figure(1,figsize=(4,3))
ax=Axes3D(fig,rect=[0,0,0.95,1],elev=48,azim=134)
ax.scatter(data.teinte, data.fibres, data.longueur,c=pafkmeans.model.labels_.astype(np.float), edgecolor='k')

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])

ax.dist = 12
plt.show()


""" Tracé de la métrique silhouette : plus on est proche de 1, plus le nombre de clusters est ok"""

res2=np.arange(7,dtype='double')
for k in np.arange(2,9):
    km=KMeans(n_clusters=k)
    km.fit(test)
    res2[k-2]=(metrics.silhouette_score(test,km.labels_))
        
plt.plot(np.arange(2, 9,1), res2, 'ro')
plt.xlabel("k")
plt.ylabel("Score sur 1")
plt.show()