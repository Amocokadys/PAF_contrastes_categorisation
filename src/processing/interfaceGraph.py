from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
import gmm
import csv
import contrasteur
from arborescence import Arbre, Feuille, lire_csv
from ensemble import Ensemble


def graphic_clusters_fruits(gmm,colonne1,colonne2,point):
	"""fonction pour enregistrer l'image du cluster de l'objet gmm projetés sur les dimensions
	colonne1 et colonne2 ainsi que le point. Le graphique est enregistré sur graphique.png"""
	#Visualisation des clusters formés par gmm
	data, centers=gmm.result()
	colorlist= list(matplotlib.colors.cnames.keys())
	random.shuffle(colorlist)
	colorpoints=[]
	labels=[]
	for p in data.itertuples():
		#print(type(p))
		#print(p)
		colorpoints.append(colorlist[p[-1]])
		#labels.append(p.index[0])
	plt.plot(point[0],point[1],"b:*",markersize=20)
	plt.scatter(data[colonne1],data[colonne2],c=colorpoints,edgecolor='k',label=labels)
	plt.title('Classification gmm ')
	plt.xlabel(colonne1)
	plt.ylabel(colonne2)
	plt.savefig('graphique.png')
	plt.clf()
	
class Frame_principal (Frame):
	"""classe qui permet de construire notre interface graphique"""
	
	def __init__(self,listelabels,mclusters,listeContrastes,mgmm):
		Frame.__init__(self, borderwidth = 50, bg='darkslateblue')
		self.mclusters=mclusters
		self.listeContrastes=listeContrastes
	
#----#----#----#----#----#----#        l'input des valeurs           #----#----
		self.listelabels=listelabels
		self.attributs=[]
		self.buttons=[]
		self.mgmm=mgmm
		
		#pour preremplir dans le cas des fruits
		valeur=False
		if len(listelabels==8):
			valeur=True
			listeValeurs=np.array([40, 10, 222, 41, 22, 220, 94, 1.2])
			
		#liste des champs à remplir 
		for k in range(len(listelabels)):
			champ_label = Label(self, text=listelabels[k])
			champ_label.grid(row=k+1,column=1)
			var_texte = StringVar()
			ligne_texte = Entry(self, textvariable=var_texte, width=30)
			if valeur:
				ligne_texte.insert(0,listeValeurs[k])
			self.attributs.append(var_texte)
			ligne_texte.grid(row=k+1,column=2)
			
	
#----#----#----#----#----#----#        l'image des clusters          #----#----#----#----


		#le menu deroulant des affichages qu on peut choisir
		self.var_choix = StringVar()
		for k in range(len(self.listelabels)):
			choix=Radiobutton(self, text=self.listelabels[k], variable=self.var_choix, value=self.listelabels[k]+str(k))
			choix.grid(row=k+1, column=4)
		self.var_choix.set(self.listelabels[0]+"0")
		
		
			
		self.var_choix1 = StringVar()
		for k in range(len(self.listelabels)):
			choix=Radiobutton(self, text=self.listelabels[k], variable=self.var_choix1, value=self.listelabels[k]+str(k))
			choix.grid(row=k+1, column=5)
		self.var_choix1.set(self.listelabels[1]+"1")
			
		graphic_clusters_fruits(self.mgmm,str(self.var_choix.get()[:-1]),str(self.var_choix1.get()[:-1]),np.array([40,10]))
		image = Image.open("graphique.png") 
		self.photo = ImageTk.PhotoImage(image)
		espace_image = Canvas(self, width = image.size[0], height = image.size[1], bg ='blue')
		espace_image.grid(row=1, column=0,rowspan=10)
		espace_image.create_image(323, 242, image =self.photo)
		
		button1=Button(self, text="resultat", command= self.fonctionTest)
		button1.grid(row=12, column=0)

		#pour retracer le graphe
		self.buttonGraph=Button(self, text="retracer graphe", command= self.tracerGraph)
		self.buttonGraph.grid(row=0,column=0)
		
	def tracerGraph(self):
		"""appelle la fonction qui enregistre l'image (en fonction des colonnes cochées et le trace"""
		index=[int(self.var_choix.get()[-1]),int(self.var_choix1.get()[-1])]
		point=np.array([float(self.attributs[k].get()) for k in index])
		graphic_clusters_fruits(self.mgmm,str(self.var_choix.get()[:-1]), str(self.var_choix1.get()[:-1]), point)
		image = Image.open("graphique.png") 
		self.photo = ImageTk.PhotoImage(image)
		espace_image = Canvas(self, width = image.size[0], height = image.size[1], bg ='blue')
		espace_image.grid(row=1, column=0,rowspan=10)
		espace_image.create_image(323, 242, image =self.photo)
		
	def on_button(self):
		print(self.var_choix.get(),"coucou")

	def fonctionTest(self):
		"""fonction qui donne la categorie d'un point et ses caractéristiques"""
		data=np.array([float(attribut.get()) for attribut in self.attributs])
		resultat=contrasteur.result(self.mclusters, self.listeContrastes, data)
		champ=Label(self, text="cluster : "+resultat[0][0])
		champ.grid(row=13, column=0)
		champ1=Label(self, text="caractéristiques : "+str(resultat[1]))
		champ1.grid(row=14, column=0)
		
		
class Application(Frame):
	def __init__(self,listelabels,mclusters,listeContrastes,mgmm):
	
		Frame.__init__(self)
		partie_principale =  Frame_principal(listelabels,mclusters,listeContrastes,mgmm)
		partie_principale.grid()
	

"""
appli = Application(["rouge","bleu","vert"]) 
appli.mainloop()"""


class FrameIncrementale(Frame):
	"""pour l'interface graphique de la methode incremnetale"""
	
	def __init__(self):
		
		racine = Arbre([], "~")
		feuilles = []
		self.predistribution = []
		
		self.monArbre, self.predistribution = lire_csv()

		
		Frame.__init__(self, borderwidth = 50, bg='darkslateblue')
		
		
		
		#liste des champs
		boolList=Ensemble.obligatoire
		nombreObligatoires=0
		ligneCourante=12
		listeNonObligatoires=[]

		self.attributs=[]
		for k in range(len(boolList)):
			if boolList[k]:
				v = StringVar()
				v.set(self.predistribution[k])
				champ_label = Label(self, text=self.predistribution[k])
				champ_label.grid(row=ligneCourante,column=1)
				if  type(Ensemble.distribution[self.predistribution[k]]) == list:
					var_choix=StringVar()
					om = OptionMenu(self,var_choix,*Ensemble.distribution[self.predistribution[k]] )
					self.attributs.append(var_choix)
					om.grid(row=ligneCourante, column=2)
				else:
					var_texte=StringVar()
					ligne_texte = Entry(self, textvariable=var_texte, width=30)
					self.attributs.append(var_texte)
					ligne_texte.grid(row=ligneCourante,column=2)
				ligneCourante+=1
			else:
				listeNonObligatoires.append(self.predistribution[k])
		
		self.listeChamps=[]
		for k in range(4):
			v = StringVar()
			v.set(listeNonObligatoires[0])
			om = OptionMenu(self, v, *listeNonObligatoires)
			self.listeChamps.append(v)
			om.grid(row=k+ligneCourante, column=1)
			var_texte = StringVar()
			ligne_texte = Entry(self, textvariable=var_texte, width=30)
			self.attributs.append(var_texte)
			ligne_texte.grid(row=k+ligneCourante,column=2)
			
			
			
		#image initiale
		image = Image.open("/tmp/graphviz.png")
		self.photo = ImageTk.PhotoImage(image)
		self.espace_image = Canvas(self, width = image.size[0], height = image.size[1], bg ='blue')
		self.espace_image.grid(row=0, column=0, columnspan=10)
		self.espace_image.create_image(image.size[0]/2, image.size[1]/2, image =self.photo)
			
			
		self.buttonInsert=Button(self, text="resultat", command= self.fonctionInsertion)
		self.buttonInsert.grid(row=12, column=1)
		self.buttonNom=Button(self, text="resultat", command= self.fonctionNom)
		self.buttonInsert.grid(row=11, column=3)
				
		
		
		
		champ_label = Label(self, text="donnez le nom de votre objet : ")
		champ_label.grid(row=11,column=0)
		self.var_nom = StringVar()
		ligne_texte = Entry(self, textvariable=self.var_nom, width=30)
		ligne_texte.grid(row=11,column=1)
		self.retracerGraph()
	
	
	# fonctions des boutons
	
	def fonctionInsertion(self):
		liste = {};
		self.listeChamps = ["taille (cm)", "régime alimentaire"] + [champ.get() for champ in self.listeChamps]
		print(self.listeChamps, [self.attributs[k].get() for k in range(len(self.attributs))])
		for i in range(len(self.listeChamps)):
			if len(self.attributs[i].get()) > 0:
				if type(Ensemble.distribution[self.listeChamps[i]]) == list:
					liste[self.listeChamps[i]] = Ensemble.distribution[self.listeChamps[i]].index(str(self.attributs[i].get()))
				else:
					if len(self.attributs[i].get()) > 0:
						liste[self.listeChamps[i]] = float(self.attributs[i].get())
		feuil = Feuille(liste, self.var_nom.get())
		feuil.commentaire = True
		print(feuil.centre)
		self.monArbre += feuil
		print(Feuille.commentaire)
		champ_label = Label(self, text=Feuille.commentaire)
		champ_label.grid(row=13,column=3)
		self.retracerGraph()
		
	def fonctionNom(self):
		pass
		
	def retracerGraph(self):
		"""appelle la fonction qui enregistre l'image (en fonction des colonnes cochées et le trace"""
		self.monArbre.dessin("*")
		image = Image.open("/tmp/graphviz.png") 
		self.photo = ImageTk.PhotoImage(image)
		self.espace_image = Canvas(self, width = image.size[0], height = image.size[1], bg ='blue')
		self.espace_image.grid(row=0, column=0, columnspan=10)
		self.espace_image.create_image(image.size[0]/2, image.size[1]/2, image =self.photo)
		
class ApplicationInterface(Frame):
	def __init__(self):
		Frame.__init__(self)
		partie_principale =  FrameIncrementale()
		partie_principale.grid()
		
