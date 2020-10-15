# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: PlotCmRel.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Representa la posició del centre de masses i la posició relativa.
 - Revisió: 03/10/2020
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

nom_cm = Path(nom_directori+"CmRel/Cm/")
nom_rel = Path(nom_directori+"CmRel/Rel/")
try:
    nom_cm.mkdir(parents=True, exist_ok=False)
    nom_rel.mkdir(parents=True, exist_ok=False)
except FileExistsError:
    pass

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
    Representació gràfica de la posició del centre de masses.
    """
    # ATENCIÓ: vàlid només per boles de masses idèntiques.
    plt.plot(t/sist.T0, .5*(pos[:, 0] + pos[:, 1]))

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('x_CM (-)', fontsize=18)
    # plt.legend(loc="upper right")

    data_cm = open(str(nom_cm)+"/"+nom_simulacio+"_CM.csv", "w")

    for i, temps in enumerate(t):
        data_cm.write("%e,%e\n" % (temps/sist.T0, .5*(pos[i, 0] + pos[i, 1])))

    data_cm.close()

    plt.savefig(str(nom_cm)+"/"+nom_simulacio+"_CM.png")
    # plt.show()
    plt.clf()

    """
    Representació gràfica de la posició relativa.
    """
    # ATENCIÓ: vàlid només per boles de masses idèntiques.
    plt.plot(t/sist.T0, -1.*(pos[:, 0] - pos[:, 1]))

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('x_r (-)', fontsize=18)
    # plt.legend(loc="upper right")

    data_rel = open(str(nom_rel)+"/"+nom_simulacio+"_Rel.csv", "w")

    for i, temps in enumerate(t):
        data_rel.write("%e,%e\n" % (temps/sist.T0, -1.*(pos[i, 0] - pos[i, 1])))

    data_rel.close()

    plt.savefig(str(nom_rel)+"/"+nom_simulacio+"_Rel.png")

    plt.clf()

    final = time() - inici
    t_avg = (t_avg * iter + final) / (iter + 1)

    printProgressBar(iter, len(noms_simulacions), len=30, temps_restant=t_avg * (len(noms_simulacions) - iter))

plt.close()
