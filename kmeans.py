# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.cluster import KMeans


class PafKmeans(object):
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.model = None
        self.number = 4
    def kmeans(self):
        self.model = KMeans(n_clusters = self.number)
        self.model.fit(self.dataframe)
    def findN(self):
        return None
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

print(centers)
print(data)
