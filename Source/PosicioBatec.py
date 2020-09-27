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

import Simulacio as sim


"""
Ús dels fitxer de dades i metadades
"""
inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n")
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/"

noms_simulacions = Path(nom_directori + "/Data/").glob("*Sim*")

nom_figura = Path(nom_directori+"Amplituds/")
try:
    nom_figura.mkdir(parents=True, exist_ok=False)
except FileExistsError:
    pass

t_vs_gamma = np.empty((10, 2))

for iter, nom_simulacio in enumerate(noms_simulacions):
    """
    Variables caracterísitques del sistema i generació de l'objecte
    """
    nom_simulacio = str(basename(nom_simulacio)).replace(".csv", "")
    nom_simulacio = nom_simulacio.replace("_Sim", "")
    nom_amplituds = nom_directori + "Amplituds/" + nom_simulacio + "_Amp.csv"
    nom_metadata = nom_directori + "Metadata/" + nom_simulacio + "_Sim.dat"

    parametres_sist = sim.llegeixMetadata(nom_metadata)

    sist = sim.Sistema(**parametres_sist)

    data = np.genfromtxt(nom_amplituds, delimiter=",")

    t = data[:, 0]
    amps = data[:, 1]

    """
    Detecció del primer mínim en les amplituds
    """
    for i in range(1, len(t)-1):
        if amps[i] - amps[i-1] < 0 and amps[i+1] - amps[i] > 0:
            t_batec = t[i]
            break
        else:
            pass

    """
    Representació gràfica de les dades
    """
    default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm'])
                      + cycler(linestyle=['-', '--', ':', '-.', '--']))
    plt.rc('axes', prop_cycle=default_cycler)

    plt.xlabel("$\gamma$ ($\mathrm{kg}/\mathrm{s} \mathrm{m}^2}$)", fontsize=18)
    plt.ylabel("$t/T_0$ (-)", fontsize=18)
    # plt.legend(loc="upper right")

    t_vs_gamma[iter] = np.array([sist.gamma, t_batec/sist.T0])

    plt.plot(sist.gamma, t_batec/sist.T0, '.', color='blue')
    print("Gamma = %.2e" % (sist.gamma))


plt.savefig(str(nom_figura)+"/"+nom_simulacio+"_GammaVsBatec.png")
print(t_vs_gamma[:, 0])
print(t_vs_gamma[:, 1])
# plt.show()
plt.clf()
