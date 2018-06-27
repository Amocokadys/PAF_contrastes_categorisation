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
		self.w = int(w)
		self.z = int(z)
		self.signe = True
	
	def __gt__(self, autre):
		if (not self.signe) and autre.signe:
			return False
		if (not autre.signe) and self.signe:
			return True
		if self.z != 0 or autre.z != 0:
			return self.signe == (self.z > autre.z)
		elif self.w != 0 or autre.w != 0:
			return self.signe == (self.w > autre.w)
		else:
			return self.signe == (self.n > autre.n)


	
	def __ge__(self, autre):
		return self.__gt__(autre) or self.__eq__(autre)
	
	def __lt__(self, autre):
		return not self.__ge__(autre)
	
	def __le__(self, autre):
		return not self.__gt__(autre)
	
	def __eq__(self, autre):
		if self.z != 0:
			return self.z == autre.z
		elif self.w != 0:
			return self.w == autre.w
		else:
			return autre.n == self.n
		
	
	def _neq__(self, autre):
		return not self.__eq__(self,autre)
	
	def __add__(self,autre):
		if type(autre) == Transfini:
			return Transfini(autre.n + self.n, autre.w + self.w, autre.z + self.z)
		else:
			return Transfini(autre + self.n, self.w, self.z)
	
	def __truediv__(self,nombre):
		if self.z > 1:
			return Transfini(self.n,self.w,self.z - 1)
		elif self.z == 1:
			return Transfini(self.n, self.w)
		elif self.w > 1:
			return Transfini(self.n, self.w - 1)
		elif self.w == 1:
			return Transfini(self.n)
		else:
			return Transfini(self.n / nombre)
	
	def __neg__(self):
		self.signe = not self.signe
		return self
		
	def __str__(self):
		if self.signe:
			return str(self.n) + " + " + str(self.w) + "w + " + str(self.z) + "w2"
		else:
			return "- " + str(self.n) + " + " + str(self.w) + "w + " + str(self.z) + "w2"
	
	"""def __sub__(self, autre):
		if self.z < autre.z:
			raise ArithmeticError
		elif self.n < autre.n:
			return Transfini(0,self.w - autre.w)
		else:
			return Transfini(self.n - autre.n, self.w - autre.w)"""



class Ensemble:
	
	distribution = {}				
	
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
						somme += abs(math.log(self[clef] / point[clef]))
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


	def __iter__(self):
		return iter(self.centre)