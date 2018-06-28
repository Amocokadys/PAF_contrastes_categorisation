#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Cartouche
"""

# this parameter corresponds to the number bellow which a component of a contrast
# is set to zero during the sharpening
SHARPEN_PARAM = 0.5

# this parameter defines the vectors that are in the core and the other ones
# values that differs from less than this parameters are in the core
CORE_PARAM = 10

# this parameter is an epsilon add to the standard deviations to avoid the problem
# of a zero standard deviation
EPSILON = 10**(-6)
