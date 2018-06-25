#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:59:29 2018

@author: louis
"""

import math
import numpy as np

_CONSTANTE = 0.01
_SEUIL_NOUVEAU_CLUSTER = 2
_RAPPORT_LOG = 1

class Dictionnaire():
	
	def __init__(self):
		self.liste = []
	
	def plus_un(self, code):
		for i in range(len(self.liste)):
			if code == self.liste[i][0]:
				self.liste[i] = (self.liste[i][0], self.liste[i][1] + 1)
				self.liste.sort(key=lambda x:-x[1])
				return 
		print(code + " non trouvé")
		assert False
		
	
	def __getitem__(self, code):
		for i in range(len(self.liste)):
			if code == self.liste[i][0]:
				return i
		raise IndexError("\"" + code + "\" non trouvé dans le dictionnaire")
	
	def ajout(self, code, nombre):
		for i in range(len(self.liste)):
			if code == self.liste[i][0]:
				self.liste[i] = (self.liste[i][0], nombre)
				self.liste.sort(key=lambda x:-x[1])
				return
		self.liste.append((code,nombre))
		self.liste.sort(key=lambda x:-x[1])

class Ensemble:
	
	"""classe gérant une liste de vecteurs, et calculant leur espérance et leur complexité"""
	
	dico = Dictionnaire()
	dimension = 0
	nombreTotal = 0
	
	def __init__(self, points, mode_incr = False):
		
		"""
		- mode_incr == False    --> la liste des points est stockée dans la classe
		- mode_incl == True     --> seule la matrice est stockée, 
								les points sont ajoutées un à un, et sont oubliés
								dès que la matrice de covariance a été modifiée
		"""
		
		self.dimension = len(points[0])
		
		
		self.points = points
		self.complex = 0
		self.actualise()
		if mode_incr:
			self.points = None				
	
	def actualise(self):
		
		""" recalcule l'espérance et la matrice de covariance
		(non valable en mode incr) """
		
		self.nombre_descendant = len(self.points)
		self.centre = np.zeros(self.dimension)
		
		for el in self.points:
			self.centre += el
		self.centre /= self.nombre_descendant
	
		
	def cNew(self,feuille):
		"""fonction de calcul de la complexite lors de la creation d'un nouveau cluster au niveau du noeud courant"""
		c=0
		
		for fils in self.enfants:
			c+=int(np.log2(1+Ensemble.dico[fils.code]))
			for i in range(self.dimension):
				c+=int(np.log2(1+abs((self.centre[i]*self.dimension+feuille.centre[i])/(self.dimension+1)-fils.centre[i])))
			c+=fils.complex
            
		cActuelle = 0
		for i in range(self.dimension):
			cActuelle += int(np.log2(1+abs(feuille.centre[i]-self.centre[i])))
		cActuelle += np.log2(1+Ensemble.nombreTotal)
		return(c+cActuelle,[self.code])
								
		
		
	def updateC(self):
		for fils in self.enfants:
			self.complex += int(np.log2(1+Ensemble.dico[fils.code]))
			for i in range(self.dimension):
				self.complex += int(np.log2(1+abs(self.centre[i]-fils.centre[i])))
			self.complex += fils.complex
		
	def updateGlobal(self):
		if self.feuille():
			self.updateC()
		else :
			for fils in self.enfants:
				self.complex=fils.updateGlobal()
			self.updateC()
	
	def __add__(self, point):
		
		"""actualise l'espérence et la matrice de covariance
		d'un cluster après l'ajout d'un point, en temps constant par 
		rapport au nombre
		de points."""
		
		
		point = np.array(point)
		self.centre = (self.nombre_descendant * self.centre + point)/(self.nombre_descendant + 1)
		
		self.nombre_descendant += 1
		
		if self.points != None:
			self.points.append(point)
			
		self.updateGlobal()
		
		return self
	
	def __iter__(self):
		return iter(self.points)



	
	