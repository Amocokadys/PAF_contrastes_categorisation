"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Cartouche
"""

import pandas as pd
import numpy as np
import clusterisation as cl

df2 = pd.DataFrame(np.random.randint(low=0, high=10, size=(10,3)), columns=['a', 'b', 'c'], index=['A','B','C','D','E','F','G','H','I','J'])

df2["category"]=[0,0,1,1,1,0,0,1,1,1]

centres=[np.random.randint(low=0, high=10) for k in range(2)]

clust=cl.Clusterisation(df2,centres)
print(*clust.result(), sep = '\n')