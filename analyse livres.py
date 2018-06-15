# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

mots = ["amour", "guerre", "homme", "femme", "courage"\
        , "argent", "dieu", "arme", "oeuvre"]

fichier = ["voyage au bout de la nuit", "la peste", "l'étranger"]

for livre in fichier:
    
    features = [0] * len(mots)
    
    with open("livres/"+livre, "r", encoding="utf-8") as fichier:
        
        ensemble_mots = fichier.read().split(' ')
        
        for mot in ensemble_mots:
            
            if mot in mots:
                
                features[mots.index(mot)] += 1
    
    print(livre + " -->    " + str(features))