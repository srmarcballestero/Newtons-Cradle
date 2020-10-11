# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: AssajaFuncio.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Assaja funció.
 - Revisió: 06/10/2020
"""

import numpy as np
from scipy import constants as const
import matplotlib.pyplot as plt
from pathlib import Path
from os.path import basename
from time import time

import Simulacio as sim
from DataGen import printProgressBar


def xr_prova(t):
    """
    Retorna la posició relativa assajada segons els ajustos realitzats.

        Paràmetres:
            t: float
        Retorna:
            xr_prova(t): float
    """
    a = .08499
    b = .1935
    c = .02374
    Q = 1.112
    B = .05639
    v = .1601

    return (a*np.exp(-b*t) + c - 0.02)*np.cos(const.pi / (0.5 * (1. + 1./(pow(1. + Q*np.exp(-B*t), 1./v))))*t)


"""
Ús dels fitxer de dades i metadades
"""
inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n")
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/"

noms_simulacions = list(Path(nom_directori + "/Data/").glob("*Sim*"))

t_avg = 0.

for iter, nom_simulacio in enumerate(noms_simulacions):
    """
    Variables caracterísitques del sistema i generació de l'objecte
    """
    inici = time()

    nom_simulacio = str(basename(nom_simulacio)).replace(".csv", "")
    nom_simulacio = nom_simulacio.replace("_Sim", "")
    nom_data = nom_directori + "Data/" + nom_simulacio + "_Sim.csv"
    nom_metadata = nom_directori + "Metadata/" + nom_simulacio + "_Sim.dat"
    nom_rel = nom_directori + "CmRel/Rel/" + nom_simulacio + "_Rel.csv"

    parametres_sist = sim.llegeixMetadata(nom_metadata)
    sist = sim.Sistema(**parametres_sist)

    data = np.genfromtxt(nom_rel, delimiter=",")
    t = data[:, 0]
    pos_rel = data[:, 1]

    xr_s = [xr_prova(t) for t in np.linspace(0., 30., num=1000)]

    plt.plot(np.linspace(0., 30., num=1000), xr_s)

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('x_r(sgn) (-)', fontsize=18)

    plt.savefig(str(nom_rel).replace("Rel.csv", "AdjPro.png"))

    plt.clf()

    final = time() - inici
    t_avg = (t_avg * iter + final) / (iter + 1)

    printProgressBar(iter, len(noms_simulacions), len=30, temps_restant=t_avg * (len(noms_simulacions) - iter))

plt.close()
