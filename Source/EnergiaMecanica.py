# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: EnergiaMecanica.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Calcula i representa l'energia mecànica de les partícules.
 - Revisió: 16/09/2020
"""

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from pathlib import Path

import Simulacio as sim


def calculEnergia(sist, posicions, i):
    """
    Retorna l'energia mecànica del sistema en un instant determinat.

        Paràmetres
            sist: Simulacio.Sistema
            data: Simulacio.Data
            i: int
        Retorna
            E: np.ndarray
    """
    E = np.zeros(sist.N)
    vel_inst = sist.vel(posicions, i)
    pos_inst = (posicions[i, :] + posicions[i-1, :]) / 2.
    E += 0.5*sist.m*vel_inst*vel_inst
    E += 0.5*sist.kg*pos_inst*pos_inst

    return E


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

"""
Generació del vector d'energies
"""
energies = np.array([calculEnergia(sist, pos, i) for i in range(1, len(t))])


default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm'])
                  + cycler(linestyle=['-', '--', ':', '-.', '--']))
plt.rc('axes', prop_cycle=default_cycler)

for i in range(sist.N):
    plt.plot(t[1:]/sist.T0, energies[:, i], label="Bola "+str(i+1))

plt.xlabel('t/T0 (-)', fontsize=18)
plt.ylabel('E (J)', fontsize=18)


plt.show()

# plt.savefig("../Simulacions/"+nom_inp+".png")
