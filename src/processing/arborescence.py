#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:57:46 2018

@author: louis
"""

import cluster
import math
import numpy as np
import pandas as pd

class Arbre(Cluster):
	
	def __init__(self, points):
		
	
	def distance(self, point):
		point_centre = np.array([point]) - np.array([centre])
		return math.sqrt(np.dot(	np.dot(point_centre,np.inv(self.matriceCov)),\
								np.transpose(point_centre)))

	
	def __init__(self, enfants, pater=None, label=None):
		self.enfants = enfants
		self.label = label
		self.pater = pater
		self.groupe = Cluster(enfants, None, label)
		
		
	def ajout(self, livre):
		1+1
	
	def actualise_matrice(self):
		liste_points = self._private_liste_points()
		self.centre = liste_points.mean()
		self.matriceCov = self.matriceCovariance(liste_points)
		random = np.random.random(len(enfants[0]),len(enfants[0]))
		self.matriceCov += pd.DataFrame(random * 10e-6)
	
	def _private_liste_points(self):
		points = []
		for el in self.enfants:
			if type(el) == tuple:
				points += el
			else:
				points += el.actualise()
		return points
		

