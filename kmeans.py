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
    def kmeans(self):
        self.model = KMeans(n_clusters = self.number)
        self.model.fit(self.dataframe)
    def sseTab(self):
        sse = []
        for clusters_number in range(1, 10):
            sse.append(0)
            self.number = clusters_number
            self.kmeans()
            for cluster in range(clusters_number):
                mean = self.model.cluster_centers_[cluster]
                for k, row in self.dataframe[self.dataframe["category"] == cluster].iterrows():
                    
                    sse[clusters_number-1] += (row - mean)**2            
        return sse
    def newDataFrame(self):
        self.dataframe['category'] = pd.Series(self.model.labels_, index = self.dataframe.index)
    def result(self):
        self.kmeans()
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

print(sse)

