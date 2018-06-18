import Cluster

import sys
import pandas as pd
import numpy as np
import sklearn.metrics as sm
import matplotlib.pyplot as plt
import math as m

def calcDiffs(cluster):
    diffs = pd.DataFrame(columns = cluster.points.columns)
    for idx, row in cluster.points.iterrows():
        new = row - cluster.centre
        norm_new = pd.Series(np.dot(np.linalg.inv(cluster.matriceCov), new), index = new.index)
        maxi = norm_new.max()
        m = norm_new < maxi/10 
        norm_new.mask(m, other = 0, inplace = True)
        diffs = diffs.append(norm_new, ignore_index = True)
    return diffs

if __name__ == "__main__":
    d = pd.DataFrame(np.array([[-5, 5, 0], [-4, 4, 0.1], [-7, 4, 0.5], [-4, 7, 6], [-7, 7, 0.9],\
                               [5, -5, 8], [4, -4, 0.05], [7, -4, 0.6], [4, -7, 2], [7, -7, 0]]),\
                     columns = ['x', 'y', 'z'])
    c = Cluster.Cluster(d, np.array([0, 0, 0.3]), 0)
    print(calcDiffs(c))
