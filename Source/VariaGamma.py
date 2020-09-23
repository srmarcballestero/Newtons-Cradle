# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: DataGen.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Simulació del pèndol de Newton integrant numèricament l'equació
   diferencial que el regeix seguint l'algorisme de Verlet.
 - Revisió: 17/09/2020
"""

import numpy as np
from scipy import constants as const

import Simulacio as sim
from DataGen import simulaSistema

"""
Variables caracterísitques dels sistema.
"""
parametres_sist = {
    "N": 2,
    "g": const.g,
    "L": 1.3,
    "R": 0.010,
    "gap": 1.0e-3,
    "eta": 6.8e-4*0,
    "gamma": 1.47e2*1,
    "m": np.array([0.10, 0.10]),
    "E": np.array([2.55e7, 2.55e7]),
    "j": np.array([0.48, 0.48]),
    "pas": 2.5e-3,
    "num_osc": 30,
    "salt": 10
}
parametres_sist["A"] = np.array([np.sin(4*const.pi/180)*parametres_sist["L"]]
                                + [0 for i in range(parametres_sist["N"]-1)])

"""
Ús dels fitxer de dades i metadades
"""
nom_directori = sim.directori_simulacions + "Gammes/"
nom_simulacio = input("Nom de la simulació?\n")


"""
Iteració de les condicions inicials i generació de la Simulació
"""


gammes = np.logspace(1, 3, num=10, base=10.)
print(gammes)

for i, gamma in enumerate(gammes):
    iter_nom_simulacio = nom_simulacio+"_"+str(i)

    parametres_sist["gamma"] = gamma
    sist = sim.Sistema(**parametres_sist)

    print("--- Iteració %d ---" % (i+1))
    simulaSistema(parametres_sist, nom_directori, iter_nom_simulacio)
