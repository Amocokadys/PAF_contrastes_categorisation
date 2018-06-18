# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

fruits = pd.read_csv("fruits.csv")

fruits.index = fruits["fruit"]

del fruits["fruit"]

print(fruits)

for row in fruits.iterrows():
    for i in range(100):
        if i%3 == 0:
            nouveau_fruit = pd.DataFrame([[np.random.normal(row[1][0], row[1][1]), row[1][1], np.random.normal(row[1][2], row[1][3]), row[1][3], row[1][4], row[1][5], row[1][6], row[1][7], row[1][8], row[1][9], row[1][10], row[1][11], row[1][12], row[1][13]]], columns = fruits.columns, index = [row[0] + str(i)])
            fruits = fruits.append(nouveau_fruit)
        elif i%3 == 1:
            nouveau_fruit = pd.DataFrame([[row[1][0], row[1][1], row[1][2], row[1][3], np.random.normal(row[1][4], row[1][7]), np.random.normal(row[1][5], row[1][7]), np.random.normal(row[1][6], row[1][7]), row[1][7], row[1][8], row[1][9], row[1][10], row[1][11], row[1][12], row[1][13]]], columns = fruits.columns, index = [row[0] + str(i)])
            fruits = fruits.append(nouveau_fruit)
        else:
            nouveau_fruit = pd.DataFrame([[np.random.normal(row[1][0], row[1][1]), row[1][1], np.random.normal(row[1][2], row[1][1]), row[1][3], np.random.normal(row[1][4], row[1][7]), np.random.normal(row[1][5], row[1][7]), np.random.normal(row[1][6], row[1][7]), row[1][7], np.random.normal(row[1][8], row[1][9]), row[1][9], np.random.normal(row[1][10], row[1][11]), row[1][11], np.random.normal(row[1][12], row[1][13]), row[1][13]]], columns = fruits.columns, index = [row[0] + str(i)])
            fruits = fruits.append(nouveau_fruit)
    
print(fruits)



fruits.to_csv("fruitsModified.csv")


