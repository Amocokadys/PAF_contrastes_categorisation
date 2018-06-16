# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from os import listdir
from os.path import isfile, join
import csv
import math

mots = ["amour", "guerre", "homme", "femme", "courage"\
		, "argent", "dieu", "arme", "oeuvre"]

mots.sort()

def insertion(liste, el):
	a = -1
	b = len(liste)
	while a + 1 < b:
		temp = liste[(a+b)//2][0]
		if temp < el:
			a = (a+b)//2
		elif temp > el:
			b = (a+b)//2
		else:
			liste[(a+b)//2][3] += 1
			return
	liste.insert(b,[el,0,0,1])

def remplace_char_chelou():
	for livre in listdir("./livres/"):			
		temp = open("livres/"+livre, "r", encoding="utf-8")
		bouquin = temp.read()
		temp.close()
		for i in range(len(bouquin)):
			if bouquin[i] in "'’ ,;:!?.\"":
				bouquin = bouquin[:i] + "\n" + bouquin[i+1:]
		temp = open("livres/"+livre, "w", encoding="utf-8")
		temp.write(bouquin)
		temp.close()
		

def mots_pertinents(nombre):
	nombre_de_bouquins = 0
	with open("données_livres.csv","w",encoding="utf-8") as fichier:
		idf = []
		for livre in listdir("./livres/"):
			nombre_de_bouquins += 1
			
			with open("livres/"+livre, "r", encoding="utf-8") as fichier:
				ensemble_mots = fichier.read().split(' ')
				for mot in ensemble_mots:
					insertion(idf,mot.lower())
			
			for mots in idf :
				if mots[3] != 0:
					mots[1] += mots[3]
					mots[2] += 1
					mots[3] = 0
	for mots in idf:
		mots[1] = math.log(nombre_de_bouquins / mots[2])
	idf.sort(key=lambda x:-x[1])
	return idf[:nombre]
	
		 

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