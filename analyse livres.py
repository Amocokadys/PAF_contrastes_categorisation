# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from os import listdir
import csv
import math
import pandas

def remplir_dico(dico):
	with open("jeux de donne/dictionnaire", "r", encoding="utf-8") as fichier:
		cursor = csv.reader(fichier, delimiter=";")
		for el in cursor:
			dico.add(el[0])

class Iter_bouquin:
	
	def __init__(self, fichier):
		fich = open("livres/" + fichier, "r")
		self.bouquin = fich.read() + " "
		fich.close()
		
		self.dictionnaire = set()
		remplir_dico(self.dictionnaire)
		
		for i in range(len(self.bouquin)):
			if self.bouquin[i].lower() in "abcdefghijklmnopqrstuvwxyzéèàçùêâ-":
				self.i_début = i
				break
	
	def __iter__(self):
		return self
	
	def __next__(self):
		compteur = 0
		for i in range(self.i_début, len(self.bouquin)):
			if self.bouquin[i].lower() in "abcdefghijklmnopqrstuvwxyzéèàçùêâ-":
				compteur += 1
				if compteur == 1:
					début = i
			elif compteur > 1:
				if self.bouquin[début:i].lower() in self.dictionnaire:
					self.i_début = i
					return self.bouquin[début:i].lower()
				else:
					compteur = 0
			else:
				compteur = 0
		raise StopIteration

class Tf_idf:
	
	nombre_bouquins = 0
	
	def __init__(self):
		self.dictionnaire = set()
		remplir_dico(self.dictionnaire)
		self.idf = []
		
	

	def insertion(self, el):
		a = -1
		b = len(self.idf)
		while a + 1 < b:
			temp = self.idf[(a+b)//2][0]
			if temp < el:
				a = (a+b)//2
			elif temp > el:
				b = (a+b)//2
			else:
				self.idf[(a+b)//2][3] += 1
				return
		self.idf.insert(b,[el,0,0,1])
	
	def ajout_bouquin(self, livre):
		self.nombre_bouquins += 1
		
		bouquin = Iter_bouquin(livre)
		for mot in bouquin:
			self.insertion(mot)
		for mots in self.idf :
			if mots[3] != 0:
				mots[1] += mots[3]
				mots[2] += 1
				mots[3] = 0
	def __iter__(self):
		return iter(self.idf)		
			
def mots_pertinents(nombre):


	tfidf = Tf_idf()
	for livre in listdir("./livres/"):
		print("analyse de ",livre," ...")
		tfidf.ajout_bouquin(livre)
			
	meilleurs = []
	minimum = 0
	for mots in tfidf:
		toto = mots[1] * math.log(tfidf.nombre_bouquins / mots[2])
		if len(meilleurs) < nombre:
			meilleurs.append((mots[0],toto))
			minimum = min(meilleurs, key = lambda x:x[1])[1]
		elif toto > minimum:
			meilleurs[meilleurs.index(min(meilleurs, key=lambda x:x[1]))] = (mots[0],toto)
			minimum = min(meilleurs, key = lambda x:x[1])[1]
		
	return meilleurs.sort(key=lambda x:-x[1])

def livre2csv():
	with open("jeux de donne/bibliothq.csv","w",encoding="utf-8") as fichier:
		curseur = csv.writer(fichier, delimiter=",", quotechar="\"")
		curseur.writerow(["livres"] + mots)
		for livre in listdir("./livres/"):
			features = [0] * len(mots)
			
			with open("livres/"+livre, "r", encoding="utf-8") as fichier:
				ensemble_mots = fichier.read().split(' ')
				for mot in ensemble_mots:
					mot.lower()
					if mot in mots:	
						features[mots.index(mot)] += 1
			
			curseur.writerow([livre] + features)