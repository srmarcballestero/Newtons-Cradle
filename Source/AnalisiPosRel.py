# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: AnalisiPosRel.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Analitza el moviment relatiu entre les boles i n'ajusta la corba.
 - Revisió: 12/10/2020
"""

import numpy as np
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
    Reajust dels signes de la funció.
    """
    pos_rel_sgn = np.empty(np.size(pos_rel))
    sgn = 1

    for i in range(1, len(t)-1):
        pos_rel_sgn[i] = sgn * pos_rel[i]
        # Detecta els mínims.
        if pos_rel[i] - pos_rel[i-1] < 0 and pos_rel[i+1] - pos_rel[i] > 0:
            mins_rel[0] = np.append(mins_rel[0], t[i])
            mins_rel[1] = np.append(mins_rel[1], pos_rel[i])
            sgn *= -1
            continue
        # Detecta els màxims.
        if pos_rel[i] - pos_rel[i-1] > 0 and pos_rel[i+1] - pos_rel[i] < 0:
            maxs_rel[0] = np.append(maxs_rel[0], t[i])
            maxs_rel[1] = np.append(maxs_rel[1], pos_rel[i])
            continue
        else:
            pass

    """
    Reajusta la posició relativa per crear una gràfica contínua.
    """
    min_avg = np.mean(mins_rel[1])

    for i, pos_rel_sgn_i in enumerate(pos_rel_sgn):
        if pos_rel_sgn_i > 0.:
            pos_rel_sgn[i] -= min_avg
        else:
            pos_rel_sgn[i] += min_avg

    with open(nom_directori + "CmRel/Rel/" + nom_simulacio + "_AdjRel.csv", "w") as fitxer:
        for i, t_i in enumerate(t):
            fitxer.write("%e,%e\n" % (t_i, pos_rel_sgn[i]))

    plt.plot(t[:-1], pos_rel_sgn[:-1])

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('x_r(sgn) (-)', fontsize=18)

    plt.savefig(str(nom_rel).replace("Rel.csv", "AdjRel.png"))

    plt.clf()

    """
    Analitza la diferència entre el temps dels mínims
    """
    periodes = []
    t_col = []
    for i in range(len(maxs_rel[0]) - 1):
        periodes += [maxs_rel[0][i+1] - maxs_rel[0][i]]
        t_col += [(maxs_rel[0][i] + maxs_rel[0][i+1]) / 2.]
    for i in range(len(maxs_rel[0]) - 1):
        plt.plot(t_col/sist.T0, periodes)

    with open(nom_directori + "CmRel/Rel/" + nom_simulacio + "_Tdiff.csv", "w") as fitxer:
        for i, t_col_i in enumerate(t_col):
            fitxer.write("%e,%e\n" % (t_col_i, periodes[i]))

    plt.savefig(nom_directori + "CmRel/Rel/" + nom_simulacio + "_Tdiff.png")
    plt.clf()

    """
    Anàlisi dels màxims
    """
    with open(nom_directori + "CmRel/Rel/" + nom_simulacio + "_Tmax.csv", "w") as fitxer:
        for i, max in enumerate(maxs_rel[0]):
            fitxer.write("%e,%e\n" % (maxs_rel[0][i], maxs_rel[1][i]))

    final = time() - inici
    t_avg = (t_avg * iter + final) / (iter + 1)

    printProgressBar(iter, len(noms_simulacions), len=30, temps_restant=t_avg * (len(noms_simulacions) - iter))


plt.close()
