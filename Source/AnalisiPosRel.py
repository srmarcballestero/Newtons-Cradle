# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: AnalisiPosRel.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Analitza el moviment del centre de masses.
 - Revisió: 06/10/2020
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from os.path import basename

import Simulacio as sim
from DataGen import printProgressBar

"""
Ús dels fitxer de dades i metadades
"""
inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n")
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/"

# ATENCIÓ: canviar *Sim* per *Rel*
noms_simulacions = list(Path(nom_directori + "/Data/").glob("*Sim*"))

for iter, nom_simulacio in enumerate(noms_simulacions):
    """
    Variables caracterísitques del sistema i generació de l'objecte
    """
    nom_simulacio = str(basename(nom_simulacio)).replace(".csv", "")
    nom_simulacio = nom_simulacio.replace("_Sim", "")
    nom_data = nom_directori + "Data/" + nom_simulacio + "_Sim.csv"
    nom_metadata = nom_directori + "Metadata/" + nom_simulacio + "_Sim.dat"
    # ATENCIÓ: canviar _Sim per _Rel
    nom_rel = nom_directori + "CmRel/Rel/" + nom_simulacio + "_Rel.csv"

    parametres_sist = sim.llegeixMetadata(nom_metadata)
    sist = sim.Sistema(**parametres_sist)

    data = np.genfromtxt(nom_rel, delimiter=",")
    t = data[:, 0]
    pos_rel = data[:, 1]
    mins_rel = [np.array([]), np.array([])]
    maxs_rel = [np.array([]), np.array([])]

    """
    Detecta mínims i màxims relatius en la posició relativa.
    """
    for i in range(1, len(t)-1):
        # Detecta els mínims.
        if pos_rel[i] - pos_rel[i-1] < 0 and pos_rel[i+1] - pos_rel[i] > 0:
            mins_rel[0] = np.append(mins_rel[0], t[i])
            mins_rel[1] = np.append(mins_rel[1], pos_rel[i])
            continue
        # Detecta els màxims.
        if pos_rel[i] - pos_rel[i-1] > 0 and pos_rel[i+1] - pos_rel[i] < 0:
            maxs_rel[0] = np.append(maxs_rel[0], t[i])
            maxs_rel[1] = np.append(maxs_rel[1], pos_rel[i])
            continue
        else:
            pass

    """
    Analitza la diferència entre el temps dels mínims
    """
    periodes = []
    t_col = []
    for i in range(len(mins_rel[0]) - 1):
        periodes += [mins_rel[0][i+1] - mins_rel[0][i]]
        t_col += [(mins_rel[0][i+1] + mins_rel[0][i]) / 2]
    for i in range(len(mins_rel[0]) - 1):
        plt.plot(t_col/sist.T0, periodes)

    printProgressBar(iter, len(noms_simulacions))
    plt.savefig(nom_directori + "CmRel/Rel/" + nom_simulacio + "_Tdiff.png")
    plt.clf()

plt.close()
