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
		Ensemble.nombreTotal += 1
		self.titre = titre
		self.code = ""
		self.centre = point
		Ensemble.dico.ajout(titre,1)
		
	def feuille(self):
		return True
	
	def set_code(self, code):
		self.code = code
		Ensemble.dico.ajout(code, 1)
	
	def __iter__(self):
		return iter(self.centre)
	
	
	def __add__(self, point):
		return Arbre([self, point], point.code)
    
	def updateC(self):
		self.complex = int(np.log2(1+Ensemble.dico[self.titre]))
	
	def __str__(self):
		return self.titre
	
	def cInsertion(self,feuille):
		"""fonction de calcul de la complexite lors de la creation d'un nouveau cluster au niveau du noeud courant"""
            
		cActuelle = 0
		for i in range(Ensemble.dimension):
			cActuelle += int(np.log2(1+(feuille.centre[i]-self.centre[i])))
		cActuelle += np.log2(1+Ensemble.nombreTotal)
		return(cActuelle,[self.code])
	


class Arbre(Ensemble):
			
	nombre_instance = 0
	
	
	
	def __init__(self, enfants, code):
		self.enfants = enfants

		self.code = code
		Ensemble.dico.ajout(code,len(enfants))
		if len(enfants) != 0:
			
			descendants = self._private_liste_points()
			
			
			self.groupe = Ensemble.__init__(self, descendants, True)
			Arbre.nombre_instance += 1
	
	def __iter__(self):
		return iter(self.enfants)
	
	def __getitem__(self, nombre):
		return self.enfants[nombre]
		
	def feuille(self):
		return False
        
    
	def cInsertion(self,feuille):
		"""fonction recursive pour inserer une feuille dans un arbre en suivant la complexite de Jean-Louis"""
		c,chemin=self.cNew(feuille)
		for fils in self.enfants:
			cActuel,cheminActuel=fils.cInsertion(feuille)
			if cActuel<c:
				chemin=cheminActuel
				c=cActuel
		chemin.append(self.code)
		return c, chemin
	
	def __add__(self, livre):
		
		""" ajout d'une donnée à l'arbre """
		
		Ensemble.dico.plus_un(self.code)
		if len(self.enfants) == 0:
			livre.set_code("~0")
			self.enfants.append(livre)
			self.centre = livre.centre
			livre.complex = 0
			return self
		
		c, chemin = self.cInsertion(livre)
		chemin.reverse()
		livre.complex = 0
		
		
		
		self._private_ajout(chemin[1:], livre)
		return self
	
	def _private_ajout(self, chemin, livre):
		for i in range(len(self.enfants)):
			if self[i].code == chemin[0]:
				if self[i].feuille():
					livre.set_code(self[i].code + "0")
					self[i].set_code(self[i].code + "1")
					self.enfants[i] += livre
					return
				elif len(chemin) == 1:
					livre.set_code(chemin[0] + alphabet[len(self.enfants)])
					self.enfants.append(livre)
					return
				else:
					self[i]._private_ajout(chemin[1:], livre)
					Ensemble.dico.plus_un(self.code)
					return
		raise IndexError("adresse invalide : " + idx + " non trouvé !")
		
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
					texte += "\"" + self.code + "\" -> \"" + el.titre + "\";"
				else:
					texte += "\"" + self.code + "\" -> \"" + el.code + "\";"
					texte += el.dessin(False)
		return texte
		
"""
Arbre.distribution = [None, None, None]
test = Arbre([], "~")

test += Feuille("abricot", [0,0,0])
test += Feuille("pêche", [1,0,0])
test += Feuille("poire",[0.001,0,0])

print(test)"""