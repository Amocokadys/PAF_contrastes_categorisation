#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 10:57:46 2018

@author: louis
"""

import math
import numpy as np
import subprocess
from ensemble import Ensemble, _CONSTANTE, _SEUIL_NOUVEAU_CLUSTER, Dictionnaire, _RAPPORT_LOG

alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"



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

class Feuille:
	
	""" classe correspondant à une donnée"""
		
	def __init__(self, point, titre = ""):
		Arbre.nombreTotal += 1
		self.titre = titre
		self.code = ""
		for i in range(len(point)):
			if Arbre.distribution[i] == None:
				if point[i] <= 0:
					point[i] == np.inf
				else:
					point[i] = math.log(point[i]) * _RAPPORT_LOG
			else:
				point[i] /= Arbre.distribution[i]
		self.centre = point
		Ensemble.dico.ajout(titre,1)
		
	def feuille(self):
		return True
	
	def __iter__(self):
		return iter(self.centre)
	
	def matrice(self):
		return np.eye(len(self.centre)) * _CONSTANTE
	
	def distance(self, point):
		
		""" distance euclidienne """
		
		somme = 0
		for i in range(len(point.centre)):
				somme += (point.centre[i] - self.centre[i])**2
		return math.sqrt(somme) / _CONSTANTE
	
	def __add__(self, point):
		return Arbre([self, point], point.code)
    
	def updateC(self):
		self.complex = int(np.log2(1+Ensemble.dico[self.titre]))


	
	def __str__(self):
		return self.titre

class Arbre(Ensemble):
			
	nombre_instance = 0
	distribution = None
	nombreTotal = 0
	
	
	def __init__(self, enfants, label):
		self.enfants = enfants

		self.label = label
		Ensemble.dico.ajout(label,len(enfants))
		if len(enfants) != 0:
			
			descendants = self._private_liste_points()
			
			
			self.groupe = Ensemble.__init__(self, descendants, True)
			self.actualise_enfants()
			Arbre.nombre_instance += 1
		
	def feuille(self):
		return False
	
	def actualise_enfants(self):
		
		""" crée et actualise une espérance/matrice de covariance correspondant
		aux centres des noeuds enfants"""
		
		centres = [el.centre for el in self.enfants]
		self.matrice_enfants = Ensemble(centres, False)
        
    
	def cInsertion(self,feuille):
		"""fonction recursive pour inserer une feuille dans un arbre en suivant la complexite de Jean-Louis"""
		c,chemin=self.cNew(feuille)
		for fils in self.enfants:
			cActuel,cheminActuel=fils.cInsertion(feuille)
			if cActuel<c:
				chemin=cheminActuel
				c=cActuel
		chemin.append([self.id])
		return c, chemin
	
	def __add__(self, livre):
		
		""" ajout d'une donnée à l'arbre """

		Ensemble.dico.plus_un(self.label)
        
		self.cInsertion(livre)
        
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

	
	def dessin(self, final = True):
		texte = ""
		if final:
			texte += "digraph G { " + self.dessin(False) + "}"
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
					texte += "\"" + self.label + "\" -> \"" + el.titre + "\";"
				else:
					texte += "\"" + self.label + "\" -> \"" + el.label + "\";"
					texte += el.dessin(False)
		return texte
		
"""
Arbre.distribution = [None, None, None]
test = Arbre([], "~")

test += Feuille("abricot", [0,0,0])
test += Feuille("pêche", [1,0,0])
test += Feuille("poire",[0.001,0,0])

print(test)"""