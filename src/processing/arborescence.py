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
from random import randint

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
		self.titre = titre
		point[i] /= Ensemble.distribution[i]
		Ensemble.__init__(self,point)
		
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
		if len(enfants) != 0:
			
			descendants = self._private_liste_points()
			
			self.label = label
			self.groupe = Ensemble.__init__(self, descendants, True)
			self.actualise_enfants()
			Arbre.nombre_instance += 1
		
	def feuille(self):
		return False
	
	def actualise_enfants(self):
		
		""" crée et actualise une espérance aux centres des noeuds enfants"""
		
		centres = [el.centre for el in self.enfants]
		self.matrice_enfants = Ensemble(centres, False)
	
	def __add__(self, livre):
		
		""" ajout d'une donnée à l'arbre """
		if len(self.enfants) == 0:
			return Arbre([livre])
		min_enfant, min_distance = argmax_(self.enfants, key=lambda x:-x.distance(livre))
	
		if min_distance.distance(livre) > _SEUIL_NOUVEAU_CLUSTER:
			
			try:
				livre.feuille()
				self.enfants.append(livre)
			except AttributeError:
				self.enfants += livre
			
			Ensemble.__add__(self,livre.centre)
			self.matrice_enfants.points.append(livre.centre)
			self.matrice_enfants.actualise()
			
			self.regroupement()
		
		else:
			
			self.enfants[min_enfant] += livre
			Ensemble.__add__(self, livre.centre)
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
			texte += "digraph G { " + self.dessin("r") + "}"
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
		


racine = Arbre([], "~")




feuilles = []
predistribution = []

with open("../../jeux de donne/fruits_transfinis.csv", "r") as fichier:
	cursor = csv.reader(fichier, delimiter=",")
	
	for ligne in cursor:
		if len(predistribution) == 0:
			predistribution = ligne[1:]
		elif len(Ensemble.distribution) == 0:
			for i in range(len(predistribution)):
				if ligne[i+1] == "none":
					Ensemble.distribution[predistribution[i]] = None
				else:
					print("-",ligne[i],"-")
					Ensemble.distribution[predistribution[i]] = float(ligne[i+1])
		else:
			dico = {}
			for i in range(1, len(ligne)):
				if len(ligne[i]) > 0:
					dico[predistribution[i-1]] = float(ligne[i])
			feuilles.append(Feuille(dico, ligne[0]))
			

while len(feuilles) > 0:
	au_sort = randint(0, len(feuilles)-1)
	racine += feuilles[au_sort]
	del feuilles[au_sort]
	

print(racine.dessin())
