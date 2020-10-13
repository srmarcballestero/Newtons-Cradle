# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: PlotAmplituds.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Representa l'amplitud del moviment en funció del temps.
 - Revisió: 17/09/2020
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from os.path import basename
from cycler import cycler
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
    Detecció i càlcul de l'amplitud dels màxims
    """
    j = 0
    maxims = np.zeros(int(sist.num_osc))
    t_max = np.zeros(int(sist.num_osc))

    for i in range(np.size(maxims)):
        while t[j] < (i+1)*sist.T0 and j < np.size(t)-1:
            if np.fabs(pos[j, 1]) > maxims[i]:
                maxims[i] = np.fabs(pos[j, 1])
                t_max[i] = t[j]
            j += 1

    """
    Representació gràfica de les dades
    """
    default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm'])
                      + cycler(linestyle=['-', '--', ':', '-.', '--']))
    plt.rc('axes', prop_cycle=default_cycler)

    plt.xlabel("t/T0 (-)", fontsize=18)
    plt.ylabel("x/A (-)", fontsize=18)
    # plt.legend(loc="upper right")

    plt.plot(np.array(range(1, int(sist.num_osc)+1)), maxims/np.max(sist.A), '.', color='blue')

    nom_figura = Path(nom_directori+"Amplituds/")
    try:
        nom_figura.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass

    with open(str(nom_figura)+"/"+nom_simulacio+"_Amp.csv", "w") as fitxer:
        for i in range(len(maxims)):
            fitxer.write("%e,%e\n" % (t_max[i], maxims[i]))

    plt.savefig(str(nom_figura)+"/"+nom_simulacio+"_Amp.png")
    # plt.show()
    plt.clf()

    final = time() - inici
    t_avg = (t_avg * iter + final) / (iter+1)

    printProgressBar(iter, len(noms_simulacions), len=30, temps_restant=t_avg * (len(noms_simulacions) - iter))

plt.close()
