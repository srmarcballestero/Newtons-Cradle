# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: DataGen.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Simulació del pèndol de Newton integrant numèricament l'equació
   diferencial que el regeix seguint l'algorisme de Verlet.
 - Revisió: 15/09/2020
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
    "pas": 2.5e-1,
    "num_osc": 30,
    "salt": 10
}
parametres_sist["A"] = np.array([np.sin(4*const.pi/180)*parametres_sist["L"]]
                                + [0 for i in range(parametres_sist["N"]-1)])

"""
Ús dels fitxer de dades i metadades
"""
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/Simetries/"
nom_simulacio = nom_directori + input("Nom de la simulació?\n")


"""
Iteració de les condicions inicials i generació de la Simulació
"""
sist = sim.Sistema(**parametres_sist)

energia_sist = 0.035

# AVÍS: Només vàlid per boles amb masses idèntiques
amplituds = np.linspace(np.sqrt(2.*energia_sist / np.max(sist.kg)), np.sqrt(energia_sist / np.max(sist.kg)), 10)

for i in range(len(amplituds)):
    iter_nom_simulacio = nom_simulacio+"_"+str(i)

    parametres_sist["A"] = np.array([amplituds[i], -1.*np.sqrt(2.*energia_sist / np.max(sist.kg) - pow(amplituds[i], 2.))])

    print("--- Iteració %d ---" % (i+1))
    simulaSistema(parametres_sist, iter_nom_simulacio)
