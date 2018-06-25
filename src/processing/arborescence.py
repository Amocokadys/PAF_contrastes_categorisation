#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:57:46 2018

@author: louis
"""

import math
import numpy as np
from ensemble import Ensemble, _CONSTANTE, _SEUIL_NOUVEAU_CLUSTER, _RAPPORT_LOG, Transfini
import subprocess

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
		if i == 0 or key(test) > key(maximum):
			idx = i
			maximum = test

class Feuille(Ensemble):
	
	""" classe correspondant à une donnée"""
		
	def __init__(self, point, titre = ""):
		self.nombre_descendant = 1
		self.titre = titre
		self.centre = point
		for el in point:
			if Ensemble.distribution[el] == None:
				if point[el] > 0:
					self.centre[el] = math.log(self.centre[el])
				else:
					self.centre[el] = Transfini(0,1)
		
	def feuille(self):
		return True
	
	def __iter__(self):
		return iter(self.centre)
	
	def __add__(self, point):
		return Arbre([self, point])
	
	def __str__(self):
		return self.titre

class Arbre(Ensemble):
			
	nombre_instance = 0
	
	def __init__(self, enfants, label=None):
		self.enfants = enfants
		self.nombre_descendant = len(self._private_liste_points())
		if len(enfants) >= 2:
			
			self.centre = {}
			for el in enfants[0]:
				
				self[el] = enfants[0][el]
				
				poids_total = 0
				for enf in enfants[1:]:
					if (not el in enf.centre) or \
								(Ensemble.distribution[el] == 0 and enf[el] != self[el]):
						del self[el]
						break
					else:
						poids_total += enf.nombre_descendant
						self[el] += enf[el] * enf.nombre_descendant
				if Ensemble.distribution[el] != 0 and el in self.centre:
					self[el] /= poids_total
			
			self.variance = Transfini()
			for i in range(len(enfants)):
				for j in range(i+1,len(enfants)):
					temp = enfants[i].distance(enfants[j])
					if temp > self.variance:
						self.variance = temp
			
			Arbre.nombre_instance += 1
		
	def feuille(self):
		return False
	
	def __add__(self, livre):
		
		""" ajout d'une donnée à l'arbre """
		if len(self.enfants) == 0:
			return Arbre([livre],"~")
		if len(self.enfants) == 1:
			return Arbre([livre, self.enfants[0]],"~")
		min_enfant, min_distance = argmax_(self.enfants, key=lambda x:-x.distance(livre))
		
		if min_distance.distance(livre) > self.variance / 2:
			
			self.enfants.append(livre)						
			self.regroupement()
		
		else:			
			self.enfants[min_enfant] += livre
			
		Ensemble.__add__(self, livre)
		return self
					
		
		#random = np.random.random(len(enfants[0]),len(enfants[0]))
		#self.matriceCov += pd.DataFrame(random * 10e-6)
		
	def _private_liste_points(self):
		
		""" recherche récursive des descendants """
		
		points = []
		for el in self.enfants:
			if el.feuille():
				points.append(el.centre)
			else:
				points += el._private_liste_points()
		return points
		
	def regroupement(self):
		"""méthode visant à regrouper si besoin les enfants d'un noeud,
		pour les regrouper dans un cluster fils """
		pass
	
	def __str__(self):
		chaine = "[ "
		for el in self.enfants:
			if el.feuille():
				chaine += "\"" + el.titre + "\", "
			else:
				chaine += str(el)
		return chaine + " ]"
	
	def dessin(self, chemin=""):
		texte = ""
		if chemin == "":
			texte += "digraph G { " + self.dessin("~") + "}"
			test = open("/tmp/bla.dot","w")
			test.write(texte)
			test.close()
			pipe=subprocess.Popen(['dot','-Tpng', '/tmp/bla.dot'],stdout=subprocess.PIPE)
			l=pipe.stdout.read()
			pipe.wait()
			pipe=subprocess.Popen(['display'],stdin=subprocess.PIPE)
			pipe.stdin.write(l)
			pipe.stdin.close()
			
			
		else:
			for idx, el in enumerate(self.enfants):
				if el.feuille():
					texte += "\"" + chemin + "\" -> \"" + el.titre + "\";"
				else:
					texte += "\"" + chemin + "\" -> \"" + chemin + str(idx) + "\";"
					texte += el.dessin(chemin + str(idx))
		return texte
		

Ensemble.distribution = {"taille" : None, "noyau" : 0, "peau" : 1}


fraise = Feuille({"taille" : 3, "noyau" : 0}, "fraise" )
peche = Feuille({"taille" : 7, "noyau" : 1, "peau" : 1}, "pêche")
poire = Feuille({"taille" : 8, "noyau" : 0, "peau" : 2}, "poire")

test = Arbre([])
test += fraise
test += peche
test += poire

print(test.dessin())