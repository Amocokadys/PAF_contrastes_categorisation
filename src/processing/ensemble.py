#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:59:29 2018

@author: louis
"""

import math
import numpy as np

_CONSTANTE = 0.5
_SEUIL_NOUVEAU_CLUSTER = 3
_RAPPORT_LOG = 1

class Transfini:
	
	def __init__(self, n = 0, w = 0, z = 0):
		self.n = n
		self.w = w
		self.z = z
	
	def __gt__(self, autre):
		return (self.w > autre.w) or (self.w == autre.w and self.n > autre.n)
	
	def __ge__(self, autre):
		return (self.w >= autre.w) or (self.w == autre.w and self.n >= autre.n)
	
	def __lt__(self, autre):
		return (self.w < autre.w) or (self.w == autre.w and self.n < autre.n)
	
	def __le__(self, autre):
		return (self.w <= autre.w) or (self.w == autre.w and self.n <= autre.n)
	
	def __eq__(self, autre):
		return self.n == autre.n and self.w == autre.w
	
	def _neq__(self, autre):
		return self.n != autre.n or self.w != autre.w
	
	def __add__(self,autre):
		if type(autre) == Transfini:
			return Transfini(autre.n + self.n, autre.w + self.w, autre.z + self.z)
		else:
			return Transfini(autre + self.n, self.w, self.z)
	
	"""def __sub__(self, autre):
		if self.z < autre.z:
			raise ArithmeticError
		elif self.n < autre.n:
			return Transfini(0,self.w - autre.w)
		else:
			return Transfini(self.n - autre.n, self.w - autre.w)"""



class Ensemble:
	
	distribution = {}
	
	def __init__(self, points):
		
		self.points = points
		self.actualise()
		self.points = None
	
	def __getitem__(self, clef):
		return self.centre[clef]
	
	def distance(self, point):
				
		somme = Transfini()
		for clef in self.centre:
			if clef in point.centre:
				if Ensemble.distribution[clef] == None:
					if self[clef] == 0 or point[clef] == 0:
						somme += Transfini(0,1)
					else:
						somme += math.abs(math.log(self[clef] / point[clef]))
				elif Ensemble.distribution[clef] == 0:
					if point[clef] != self[clef]:
						somme += Transfini(0,1)
				else:
					somme += (point[clef] - self[clef]) / Ensemble.distribution[clef]
			else:
				somme += Transfini(0,0,1)
		for clef in point.centre:
			if not clef in self.centre:
				somme += Transfini(0,0,1)
		return somme			
	
	def actualise(self):
		
		""" recalcule l'espérance et la matrice de covariance
		(non valable en mode incr) """
		
		self.nombre_descendant = len(self.points)
		self.centre = np.zeros(self.dimension)
		
		for el in self.points:
			self.centre += el
		self.centre /= self.nombre_descendant
									
	
	def __add__(self, point):
		
		"""actualise l'espérence et la matrice de covariance
		d'un cluster après l'ajout d'un point, en temps constant par 
		rapport au nombre
		de points."""
		
		
		self.centre = (self.nombre_descendant * self.centre + point)/(self.nombre_descendant + 1)
		
		self.nombre_descendant += 1
		
		if self.points != None:
			self.points.append(point)
					
		return self
	
	def __iter__(self):
		return iter(self.points)