# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: PlotAmplituds.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Representa l'amplitud del moviment en funció del temps.
 - Revisió: 16/09/2020
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from cycler import cycler

import Simulacio as sim


"""
Ús dels fitxer de dades i metadades
"""
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/Simetries/"
nom_simulacio = nom_directori + input("Nom de la simulació?\n")
nom_metadata = Path(nom_simulacio+".dat")
nom_data = Path(nom_simulacio+".csv")


"""
Variables caracterísitques del sistema i generació de l'objecte
"""
parametres_sist = sim.llegeixMetadata(nom_metadata)

sist = sim.Sistema(**parametres_sist)

t = sim.Data(nom_data).temps
pos = sim.Data(nom_data).posicions

"""
Detecció i càlcul de l'amplitud dels màxims
"""
j = 0
maxims = np.zeros(int(sist.num_osc))

for i in range(np.size(maxims)):
    while t[j] < (i+1)*sist.T0 and j < np.size(t)-1:
        if np.fabs(pos[j, 0]) > maxims[i]:
            maxims[i] = np.fabs(pos[j, 0])
        j += 1

"""
Representació gràfica de les dades
"""
default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm'])
                  + cycler(linestyle=['-', '--', ':', '-.', '--']))
plt.rc('axes', prop_cycle=default_cycler)

plt.plot(np.array(range(1, int(sist.num_osc)+1)), maxims/np.max(sist.A), '.', color='blue')

plt.xlabel("t/T0 (-)", fontsize=18)
plt.ylabel("x/A (-)", fontsize=18)

plt.savefig(Path(nom_simulacio+"_Amp.png"))
plt.show()
