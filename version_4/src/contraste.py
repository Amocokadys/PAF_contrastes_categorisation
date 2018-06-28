#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organisme de référence …… : Télécom ParisTech (https://www.telecom-paristech.fr/)
Contexte du projet ……………… : Projet PAF (https://paf.telecom-paristech.fr/)
Sujet ………………………………………………… : Contraste et catégorisation (http://teaching.dessalles.fr/Projects/P18051801.html)
Auteurs …………………………………………… : Bastien Vagne, Louis Penet de Monterno, Benoît Malézieux,Clément Bonet, Aurélien Blicq, Antoine Bellami
Date …………………………………………………… : 19/06/2018
Description du fichier …… : Computes the contrasts and categorize them
"""

import numpy as np
import pandas as pd
import math as m

import gmm
import clusterisation

from constantes import *

def sharpens(point):
    """
    only selects values from point that are smaller than p
    """
    point.mask(abs(point) < SHARPEN_PARAM, other = 0, inplace = True)


def contrastPoint(point, cluster):
    """
    returns the sharpened contrast between a point and a cluster
    """
    ctrst = (point - cluster.proto.centre) / cluster.proto.stdDev
    sharpens(ctrst)
    return ctrst


def constrastList(points, cluster):
    """
    returns a dataframe containing the contrasts between the points and
    the cluster
    """
    ctrst = pd.DataFrame(columns = points.columns)
    for _, row in points.iterrows():
        ctrst = ctrst.append(contrastPoint(row, cluster), ignore_index = True)
    return ctrst


def ContrastCluster(cluster):
    """
    returns the contrasts between the core and the cluster and between the 
    remaining points and the cluster
    """
    coreCtrst = constrastList(cluster.core, cluster)
    remainingCtrst = constrastList(cluster.remaining, cluster)
    return coreCtrst, remainingCtrst


def contrastClusterlist(clusters):
    """
    returns the appended contrasts of all the clusters
    """
    coreCtrst = pd.DataFrame(columns = clusters[0].core.columns)
    remainingCtrst = pd.DataFrame(columns = clusters[0].core.columns)
    for c in clusters:
        core, remaining = ContrastCluster(c)
        coreCtrst = coreCtrst.append(core)
        remainingCtrst = remainingCtrst.append(remaining)
    return coreCtrst, remainingCtrst
