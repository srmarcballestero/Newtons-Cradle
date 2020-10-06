# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: Variavar.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Fer simulacions iterant un paràmetre.
 - Revisió: 06/10/2020
"""

import numpy as np
from scipy import constants as const
from datetime import timedelta

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
    "pas": 2.5e-2,
    "num_osc": 30,
    "salt": 10
}
parametres_sist["A"] = np.array([np.sin(4*const.pi/180)*parametres_sist["L"]]
                                + [0 for i in range(parametres_sist["N"]-1)])

"""
Ús dels fitxer de dades i metadades
"""
nom_simulacio = input("Nom de la simulació?\n")
nom_directori = sim.directori_simulacions + nom_simulacio + "/"

"""
Iteració de les condicions inicials i generació de la Simulació
    var: str (nom del paràmetre del sistema a iterar)
"""
nom_var = "gamma"

vars = np.linspace(50, 1500, num=200)

t_acum = 0.
ts_exec = []
t_iter = 0.

for i, var in enumerate(vars):
    iter_nom_simulacio = nom_simulacio+"_"+str(i)

    parametres_sist[nom_var] = var

    sist = sim.Sistema(**parametres_sist)

    print(f'--- Iteració {i+1} / {len(vars)} | Progrés total {((i+1) / len(vars) * 100.):.1f} % | Temps estimat {str(timedelta(seconds=(t_iter * (len(vars) - i)))).split(".")[0]} ---')
    print("Generant el fitxer "+iter_nom_simulacio+".csv")
    t_exec = simulaSistema(parametres_sist, nom_directori, iter_nom_simulacio)
    ts_exec.append(t_exec)
    t_iter = np.mean(ts_exec)
    t_acum += t_exec
    print(f'--- temps d\'execució: {str(timedelta(seconds=t_exec)).split(".")[0]}.{str(timedelta(seconds=t_exec)).split(".")[1][:2]} --- |'
          + f'| --- temps acumulat: {str(timedelta(seconds=t_acum)).split(".")[0]}.{str(timedelta(seconds=t_acum)).split(".")[1][:2]} ---\n')
