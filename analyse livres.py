# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from os import listdir
import csv
import math
import pandas
import numpy

mots = ["amour", "guerre", "homme", "femme", "courage"\
		, "argent", "dieu", "arme", "oeuvre"]

mots.sort()

class Tf_idf:
	
	nombre_bouquins = 0
	
	def __init__(self):
		self.dictionnaire = set()
		self.idf = []
		with open("dictionnaire", "r", encoding="utf-8") as fichier:
			cursor = csv.reader(fichier, delimiter=";")
			for el in cursor:
				self.dictionnaire.add(el[0])
	

	def insertion(self, el):
		if not el in self.dictionnaire:
			return
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
		
		temp = open("livres/"+livre, "r", encoding="utf-8")
		bouquin = temp.read() + " "
		temp.close()
		
		i_début = -1
		for i in range(len(bouquin)):
			if not bouquin[i].lower() in "abcdefghijklmnopqrstuvwxyzéèàçùêâ-":
				if i - i_début > 1:
					self.insertion(bouquin[i_début+1:i].lower())
				i_début = i
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
		
	return meilleurs

def livre2csv():
	with open("données_livres.csv","w",encoding="utf-8") as fichier:
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