# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: PlotOscillacions.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Representa els punts d'una simulació a escala d'oscil·lacions.
 - Revisió: 16/09/2020
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import Simulacio as sim


"""
Ús dels fitxer de dades i metadades
"""
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"
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

colors = ['b', 'g']

for i in range(sist.N):
    plt.fill_between(t/sist.T0, pos[:, i]/sist.R - 1, pos[:, i]/sist.R + 1,
                     interpolate=True, alpha=0.5, color=colors[i])
    plt.plot(t/sist.T0, pos[:, i]/sist.R, label="Bola "+str(i+1), color=colors[i])

plt.xlabel('t/T0 (-)', fontsize=18)
plt.ylabel('x/R (-)', fontsize=18)

plt.savefig(nom_simulacio+"OscAbs.png")

plt.legend(loc='lower left')
plt.show()
