import pandas as pd
import numpy as np
import clusterisation as cl

df2 = pd.DataFrame(np.random.randint(low=0, high=10, size=(10,3)), columns=['a', 'b', 'c'], index=['A','B','C','D','E','F','G','H','I','J'])

df2["category"]=[0,0,1,1,1,0,0,1,1,1]

centres=[np.random.randint(low=0, high=10) for k in range(2)]

clust=cl.Clusterisation(df2,centres)
print(*clust.result(), sep = '\n')