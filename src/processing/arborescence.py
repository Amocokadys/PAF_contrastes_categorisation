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

_CONSTANTE = 0.001

def argmax_(liste,key=lambda x:x):
	if len(liste) == 0:
		assert "liste vide"
	toto = iter(liste)
	i = -1
	idx = 0
	maximum = 0
	while True:
		try:
			test = next(toto)
		except StopIteration:
			return idx, maximum
		i += 1
		if key(test) > maximum or i == 0:
			idx = i
			maximum = key(test)

class Feuille:
	
	def __init__(self, titre, point):
		self.titre = titre
		self.point = point
	
	def feuille(self):
		return True
	
	def __iter__(self):
		return iter(self.point)
	
	def matrice(self):
		return np.eye(len(point)) * _CONSTANTE

class Arbre(Cluster):
			
	self.nombre_instance = 0	
	
	def mahalanobis(self, point):
		point_centre = np.array([point]) - np.array([centre])
		return math.sqrt(np.dot(	np.dot(point_centre,np.inv(self.matriceCov)),\
								np.transpose(point_centre)))

	
	def __init__(self, enfants, pater=None, label=None):
		self.enfants = enfants
		descendants = self._private_liste_points()
		self.nombre_descendant = len(descendants)
		
		self.label = label
		self.pater = pater
		self.groupe = Cluster.__init__(self, descendants, None, self.nombre_instance)
		self.nombre_instance += 1
		
	def feuille():
		return False
	
	def nouvelle_donne(self, livre):
		min_enfant, min_distance = argmax_(enfants, key=lambda x:-)
	
	def actualise_matrice(self, point):
		
		"""actualise l'espérence et la matrice de covariance
		d'un cluster après l'ajout d'un point, en temps constant par 
		rapport au nombre de points."""
		
		self.matriceCov /= 1 + 1/self.nombre_descendant
		for i in range(len(point)):
			for j in range(i, len(point)):
				
				self.matriceCov += ( self.nombre_descendant * point[i] * point[j] - \
									self.centre[i] * point[j] - \
									self.centre[j] * point[i] ) / \
									(self.nombre_descendant + 1)**2
		self.centre = (self.nombre_descendant * self.centre + point)/(self.nombre_descendant + 1)
		
		self.nombre_descendant += 1
		
		#random = np.random.random(len(enfants[0]),len(enfants[0]))
		#self.matriceCov += pd.DataFrame(random * 10e-6)
	
	def _private_liste_points(self):
		points = []
		for el in self.enfants:
			if type(el) == tuple:
				points += el
			else:
				points += el.actualise()
		return points
		
