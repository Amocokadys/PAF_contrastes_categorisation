from tkinter import*
from PIL import Image, ImageTk
import main
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
import gmm
import contrasteur


def graphic_clusters_fruits(gmm):
 #Visualisation des clusters formés par K-Means
 data, centers=gmm.result()
 colorlist= list(matplotlib.colors.cnames.keys())
 random.shuffle(colorlist)
 colorpoints=[]
 for point in data.itertuples():
  colorpoints.append(colorlist[point[-1]])
 plt.scatter(data.r,data.fibres,c=colorpoints,edgecolor='k')
 plt.title('Classification K-means ')
 plt.xlabel("rouge")
 plt.ylabel("longueur")
 plt.savefig('rouge_longueur.png')
 
class Frame_principal (Frame):
 
 def __init__(self,listelabels,mclusters,listeContrastes):
  Frame.__init__(self, borderwidth = 50, bg='red')
  self.mclusters=mclusters
  self.listeContrastes=listeContrastes
 
#----#----#----#----#----#----#        l'input des valeurs           #----#----
  self.attributs=[]
  self.buttons=[]
  for k in range(len(listelabels)):
   champ_label = Label(self, text=listelabels[k])
   champ_label.grid(row=k+1,column=1)
   var_texte = StringVar()
   ligne_texte = Entry(self, textvariable=var_texte, width=30)
   self.attributs.append(ligne_texte)
   ligne_texte.grid(row=k+2,column=2)
   """
   button = Button(self, text="Get "+listelabels[k], command= lambda x=k: self.on_button(x))
   self.buttons.append(button)
   button.grid(row=3+2*k, column=1)"""
   
 
#----#----#----#----#----#----#        l'image des clusters          #----#----#----#----
  gmmTest=gmm.BDD("../data/fruitsModifiedAdjectives.csv")
  gmmTest=gmm.GMM(gmmTest.resultFruit())
  graphic_clusters_fruits(gmmTest)
  image = Image.open("rouge_longueur.png") 
  self.photo = ImageTk.PhotoImage(image)
  espace_image = Canvas(self, width = image.size[0], height = image.size[1], bg ='blue')
  espace_image.grid(row=1, column=0,rowspan=10)
  espace_image.create_image(323, 242, image =self.photo)
  
  button1=Button(self, text="resultat", command= self.fonctionTest)
  button1.grid(row=12, column=0)

 def on_button(self,k):
  print(self.attributs[k].get())

 def fonctionTest(self):
  data=np.array([float(attribut.get()) for attribut in self.attributs])
  resultat=contrasteur.result(self.mclusters, self.listeContrastes, data)
  champ=Label(self, text="cluster : "+resultat[0][0])
  champ.grid(row=13, column=0)
  champ1=Label(self, text="caractéristiques : "+str(resultat[1]))
  champ1.grid(row=14, column=0)
  
  
class Application(Frame):
 def __init__(self,listelabels,mclusters,listeContrastes):
 
  Frame.__init__(self)
  partie_principale = Frame_principal(listelabels,mclusters,listeContrastes)
  partie_principale.grid()
 

"""
appli = Application(["rouge","bleu","vert"]) 
appli.mainloop()"""