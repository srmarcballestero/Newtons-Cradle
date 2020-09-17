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
from pathlib import Path
from time import time

import Simulacio as sim


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
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/Simetries/"
nom_simulacio = nom_directori + input("Nom de la simulació?\n")
nom_metadata = Path(nom_simulacio+".dat")
nom_data = Path(nom_simulacio+".csv")


"""
Iteració de les condicions inicials i generació de la Simulació
"""

sist = sim.Sistema(**parametres_sist)

energia_sist = 0.035

# AVÍS: Només vàlid per boles amb masses idèntiques

amplituds = np.linspace(np.sqrt(2.*energia_sist / np.max(sist.kg)), np.sqrt(energia_sist / np.max(sist.kg)), 10)
print(amplituds)

for i in range(len(amplituds)):
    nom_metadata = Path(nom_simulacio+"_"+str(i)+".dat")
    nom_data = Path(nom_simulacio+"_"+str(i)+".csv")

    parametres_sist["A"] = np.array([amplituds[i], -1.*np.sqrt(2.*energia_sist / np.max(sist.kg) - pow(amplituds[i], 2.))])
    sist = sim.Sistema(**parametres_sist)

    print("--- Iteració %d ---" % (i+1))

    sist.escriuMetadata(nom_metadata)

    progres = 0.1
    fita = int(progres * sist.iteracions)

    inici = time()
    sist.t = sist.rungeKutta()
    sist.escriuData(nom_data, sist.t, sist.pos[0, :])
    # fitxer.write("%e\n" % (calculEnergia()))

    for n in range(1, sist.iteracions):
        dist = 0
        for j in range(sist.N-1):
            dist += sist.pos[1, j+1] - sist.pos[1, j]
        if dist < 3:
            salt = 100
        else:
            salt = 1e5
        sist.t = sist.verlet()
        sist.pos[0, :] = sist.pos[1, :]
        sist.pos[1, :] = sist.pos[2, :]
        if n % salt == 0:
            sist.escriuData(nom_data, sist.t, sist.pos[0, :])
            # fitxer.write("%e\n" % (calculEnergia()))
        if n > fita:
            print("%2.0f %%" % (100*progres), end="")
            print("\t temps restant: %.2f segons" % ((time() - inici) / progres * (1-progres)))
            progres += 0.1
            fita = int(progres * sist.iteracions)
    sist.escriuData(nom_data, sist.t + sist.dt, sist.pos[1, :])
    # fitxer.write("%e\n" % (calculEnergia()))

    print("--- temps total: %.2f segons ---\n" % (time() - inici))
