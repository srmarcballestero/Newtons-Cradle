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
from pathlib import Path
from time import time
from datetime import timedelta

import Simulacio as sim


def printProgressBar(iter, total, prefix='Progrés', sufix='complet', decimals=1,
                     len=50, fill='█', printEnd='\r', temps_restant=0.):
    r"""
    Crea una barra de progrés a la sortida.

        Paràmetres
            iter: int
            total: int
            prefix: str (default = '')
            sufix: str (default = '')
            decimals: int (default = 1)
            len: int (default = 100)
            fill: str (default = '█')
            printEnd: str (default = '\r')
            temps_restant: float (default = 0.)
        Retorna
            None
    """
    iter += 1
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iter / float(total)))
    filledLen = int(len * iter // total)
    bar = fill * filledLen + '-' * (len - filledLen)
    print(f'\r{prefix} |{bar}| {percent}% {sufix} temps restant {str(timedelta(seconds=temps_restant)).split(".")[0]}', end=printEnd)

    if iter == total:
        print()


def simulaSistema(parametres_sist, nom_directori, nom_simulacio):
    """
    Itera el mètode de Verlet i genera el fitxer de dades d'una simulació.

    Paràmetres
        parametres_sist: dict
        nom_directori: str
        nom_simulacio: str
    Retorna
        None
    """
    dir_data = Path(nom_directori + "Data/")
    dir_metadata = Path(nom_directori + "Metadata/")

    try:
        dir_data.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass
    try:
        dir_metadata.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass

    nom_metadata = Path(str(dir_metadata)+"/"+nom_simulacio+"_Sim.dat")
    nom_data = Path(str(dir_data)+"/"+nom_simulacio+"_Sim.csv")

    sist = sim.Sistema(**parametres_sist)
    sist.escriuMetadata(nom_metadata)

    progres = 0.001
    fita = int(progres * sist.iteracions)

    inici = time()
    sist.t = sist.rungeKutta()
    sist.escriuData(nom_data, sist.t, sist.pos[0, :])
    # fitxer.write("%e\n" % (calculEnergia()))
    t_restant = 0.
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
            t_restant = (time() - inici) / progres * (1-progres)
            progres += 0.001
            fita = int(progres * sist.iteracions)
        printProgressBar(n, sist.iteracions, len=30, sufix='', temps_restant=t_restant)
    sist.escriuData(nom_data, sist.t + sist.dt, sist.pos[1, :])
    # fitxer.write("%e\n" % (calculEnergia()))

    # print("--- temps d'execució: %.2f segons ---\n" % (time() - inici))
    return time() - inici


if __name__ == '__main__':
    """
    Variables caracterísitques del sistema.
    """
    parametres_sist = {
        "N": 2,
        "g": const.g,
        "L": 1.0,
        "R": 0.020,
        "gap": 2.0e-3,
        "eta": 6.8e-4*1,
        "gamma": 1.47e2*1,
        "m": np.array([0.10, 0.10]),
        "E": np.array([2.55e7, 2.55e7]),
        "j": np.array([0.48, 0.48]),
        "pas": 2.5e-2,
        "num_osc": 10,
        "salt": 10
    }
    parametres_sist["A"] = np.array([np.sin(4*const.pi/180)*parametres_sist["L"]]
                                    + [0 for i in range(parametres_sist["N"]-1)])

    """
    Directoris i fitxers
    """
    nom_directori = sim.directori_simulacions
    nom_simulacio = input("Nom de la simulació?\n")

    """
    Itera el mètode de verlet
    """
    simulaSistema(parametres_sist, nom_directori, nom_simulacio)
