#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:59:29 2018

@author: louis
"""

import math
import numpy as np

_CONSTANTE = 0.001


class Ensemble:
	
	def __init__(self, points, mode_incr = False):
		self.dimension = len(points[0])
		self.nombre_descendant = len(points)
		if mode_incr:
			self.centre = points[0]
			self.matrice = np.eye(self.dimension)
			self.points = None
		else:
			self.points = points
			self.actualise()
		
		
	
	def actualise(self):
		
		self.centre = np.zeros(self.dimension)
		for el in self.points:
			self.centre += el
		self.centre /= len(self.points)
		
		self.matrice = np.zeros((self.dimension, self.dimension))
		for i in range(self.dimension):
			for j in range(i,self.dimension):
				for el in self.points :
					self.matrice[i][j] += (el[i] - self.centre[i])*(el[j] - self.centre[j])
				self.matrice[j][i] = self.matrice[i][j]
		self.matrice /= len(self.points)
		self.matrice += np.eye((self.dimension, self.dimension)) * _CONSTANTE / len(self.points)

	def distance(self, point):
		point_centre = point - self.centre
		return math.sqrt(np.dot(	np.dot(point_centre,np.linalg.inv(self.matrice)),\
								np.transpose(point_centre)))
	
	def __add__(self, point):
		
		"""actualise l'espérence et la matrice de covariance
		d'un cluster après l'ajout d'un point, en temps constant par 
		rapport au nombre de points."""
		
		point = np.array(point)
		self.matrice /= 1 + 1/self.nombre_descendant
		for i in range(len(point)):
			for j in range(i, len(point)):
				
				self.matrice[i][j] += ( self.nombre_descendant * point[i] * point[j] - \
									self.centre[i] * point[j] - \
									self.centre[j] * point[i] ) / \
									(self.nombre_descendant + 1)**2
				self.matrice[j][i] = self.matrice[i][j]
		self.centre = (self.nombre_descendant * self.centre + point)/(self.nombre_descendant + 1)
		
		self.nombre_descendant += 1
		return self