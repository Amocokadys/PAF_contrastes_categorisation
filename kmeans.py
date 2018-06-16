# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np



class PafKmeans(object):
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.model = None
        self.number = 4
    def kmeans(self, number):
        self.model = KMeans(n_clusters = number)
        self.model.fit(self.dataframe)
    def sseTab(self):
        sse = []
        for clusters_number in range(1, 10):
            sse.append(0)
            self.kmeans(clusters_number)
            sse[clusters_number-1] += self.model.inertia_           
        return sse
    def findN(self):
        sse = self.sseTab()
        pentes = []
        for i in range(1, len(sse)):
            pentes.append(sse[i] - sse[i-1])
        k = -1
        pourcentage = 100
        while k < len(pentes)-1 and pourcentage > 10:
            k+=1
            pourcentage = abs(pentes[k] / sse[0]) * 100
        self.number = k+1    
    def newDataFrame(self):
        self.dataframe['category'] = pd.Series(self.model.labels_, index = self.dataframe.index)
    def result(self):
        self.findN()
        self.kmeans(self.number)
        self.newDataFrame()
        return self.model.cluster_centers_, self.dataframe
    


test = pd.read_csv("fruits.csv")
test.index = test["fruit"]
del test["fruit"]

pafkmeans = PafKmeans(test)

centers, data = pafkmeans.result()
sse = pafkmeans.sseTab()
plt.plot(np.arange(1, 10), sse, 'ro')
plt.show()

print(pafkmeans.result())



