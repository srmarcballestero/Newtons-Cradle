# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: PlotOscillacions.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Representa els punts d'una simulació a escala d'oscil·lacions.
 - Revisió: 17/09/2020
"""

import matplotlib.pyplot as plt
from pathlib import Path
from os.path import basename
from time import time

import Simulacio as sim
from DataGen import printProgressBar

"""
Ús dels fitxer de dades i metadades
"""
inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n")
nom_directori = sim.directori_simulacions+inp_nom_directori+"/"

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

    parametres_sist = sim.llegeixMetadata(nom_metadata)

    sist = sim.Sistema(**parametres_sist)

    t = sim.Data(nom_data).temps
    pos = sim.Data(nom_data).posicions

    """
    Representació gràfica de les dades
    """
    colors = ['b', 'g', 'c', 'k', 'm']

    for i in range(sist.N):
        plt.fill_between(t/sist.T0, pos[:, i]/sist.R - 1, pos[:, i]/sist.R + 1,
                         interpolate=True, alpha=0.5, color=colors[i])
        plt.plot(t/sist.T0, pos[:, i]/sist.R, label="Bola "+str(i+1), color=colors[i])

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('x/R (-)', fontsize=18)
    plt.legend(loc="upper right")

    nom_figura = Path(nom_directori+"Oscillacions/")
    try:
        nom_figura.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass

    plt.savefig(str(nom_figura)+"/"+nom_simulacio+"_OscAbs.png")
    # plt.show()
    plt.clf()

    final = time() - inici
    t_avg = (t_avg*iter + final) / (iter+1)
    printProgressBar(iter, len(noms_simulacions), len=30, temps_restant=t_avg * (len(noms_simulacions) - iter))


plt.close()
