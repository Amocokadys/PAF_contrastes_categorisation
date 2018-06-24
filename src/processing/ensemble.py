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
	
	def __truediv__(self,nombre):
		if self.z > 0:
			return Transfini(self.n, self.w, self.z - 1)
		elif self.w > 0:
			return Transfini(self.n, self.w - 1)
		else:
			return Transfini(self.n / nombre)
	
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
		if type(points) == dict:
			self.centre = points
			for el in points:
				if Ensemble.distribution[el] == None:
					if points[el] > 0:
						self.centre[el] = math.log(self.centre[el])
					else:
						self.centre[el] = Transfini(0,1)
		if type(points) == list:
			self.centre = {}
			for el in points[0]:
				
				self[el] = points[0][el]
				
					
				for enf in points[1:]:
					if (not el in enf.centre) or \
								(Ensemble.distribution[el] == 0 and enf[el] != self[el]):
						del self[el]
						break
					else:
						self[el] += enf[el] * enf.nombre_descendant
				if Ensemble.distribution[el] != 0:
					self[el] /= 
				
	
	def __getitem__(self, clef):
		return self.centre[clef]
	
	def __setitem__(self, clef, val):
		self.centre[clef] = val
	
	def __delitem__(self, clef):
		del self.centre[clef]
	
	def distance(self, point):
				
		somme = Transfini()
		for clef in self.centre:
			if clef in point.centre:
				if Ensemble.distribution[clef] == None:
					if self[clef] <= 0 or point[clef] <= 0:
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
									
	
	def __add__(self, point):
		
		"""actualise l'espérence et la matrice de covariance
		d'un cluster après l'ajout d'un point, en temps constant par 
		rapport au nombre
		de points."""
		
		
		self.centre = (self.nombre_descendant * self.centre + point)/(self.nombre_descendant + 1)
		
		self.nombre_descendant += 1
		
		if self.centre != None:
			self.centre.append(point)
					
		return self
	
	def __iter__(self):
		return iter(self.centre)