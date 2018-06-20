#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:57:46 2018

@author: louis
"""

import math
import numpy as np
import pandas as pd


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
	
	def distance(self, point):
		somme = 0
		for i in range(len(point)):
			somme += (point[i] - self.point[i])**2
		return math.sqrt(somme) * _CONSTANTE

class Arbre(Ensemble):
			
	self.nombre_instance = 0
	
	def __init__(self, enfants, pater=None, label=None):
		self.enfants = enfants
		descendants = self._private_liste_points()
		
		self.label = label
		self.pater = pater
		self.groupe = Ensemble.__init__(self, descendants, True)
		self.nombre_instance += 1
		
	def feuille():
		return False
	
	def actualise_enfants(self):
		centres = [el.centre for el in enfants]
		self.matrice_enfants = Ensemble.__init__(self, centres, False)
	
	def nouvelle_donne(self, livre):
		min_enfant, min_distance = argmax_(enfants, key=lambda x:-)
	
	
		
		#random = np.random.random(len(enfants[0]),len(enfants[0]))
		#self.matriceCov += pd.DataFrame(random * 10e-6)
	
	def 
	
	def _private_liste_points(self):
		points = []
		for el in self.enfants:
			if el.feuille():
				points.append(el.points)
			else:
				points += el._private_liste_points()
		return points
		

