from tkinter import *
from PIL import Image, ImageTk

  
class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0
        
        # Création de nos widgets
        
        self.message = Label(self, text="Vous n'avez pas cliqué sur le bouton.")
        self.message.pack()
        
        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.pack(side="left")
        
        self.bouton_cliquer = Button(self, text="Cliquez ici", fg="red",
                command=self.cliquer)
        self.bouton_cliquer.pack(side="right")
 
        
        image = Image.open("ping.png") 
        photo = ImageTk.PhotoImage(image)
        
        canvas = Canvas(self, width = image.size[0], height = image.size[1])  
        canvas.create_image(0,0, anchor = NW, image=photo) 
        canvas.pack()  

            
    def cliquer(self):
        """Il y a eu un clic sur le bouton.
        
        On change la valeur du label message."""
        
        self.nb_clic += 1
        self.message["text"] = "Vous avez cliqué {} fois.".format(self.nb_clic)
        
fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
interface.destroy()