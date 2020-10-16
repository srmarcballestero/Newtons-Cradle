# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: AssajaFuncio.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Assaja funció.
 - Revisió: 12/10/2020
"""

import numpy as np
from scipy import constants as const
from scipy import integrate
import matplotlib.pyplot as plt
from pathlib import Path
from os.path import basename
from time import time

import Simulacio as sim
from Simulacio import csvwrite
from DataGen import printProgressBar


def xr_prova(nom_rel, t):
    """
    Retorna la posició relativa assajada segons els ajustos realitzats.

        Paràmetres:
            nom_rel: str
            t: float
        Retorna:
            xr_prova(t): float
    """
    with open(str(nom_rel).replace("Rel.csv", "FitEnv.dat"), "r") as fitxer:
        a = float(fitxer.readline())
        b = float(fitxer.readline())
        c = float(fitxer.readline())
    with open(str(nom_rel).replace("Rel.csv", "FitFreq.dat"), "r") as fitxer:
        Q = float(fitxer.readline())
        D = float(fitxer.readline())
        v = float(fitxer.readline())
    if a == b == c == 1 or Q == D == v == 1:
        return 0.

    amplitud = a*np.exp(-b*t) + c - 0.02  # 0.02 <- sist.radi
    fase = integrate.quad(lambda x: ((const.pi / (0.5 * (1. + 1./(pow(1. + Q*np.exp(-D*(x)), 1./v)))))), 0, t)[0]

    return amplitud * np.cos(fase)


def xcm_prova(sist, t):
    """
    Retorna la posició relativa assajada segons els ajustos realitzats.

        Paràmetres:
            sist: obj sim.Sistema
            t: float
        Retorna:
            xcm_prova(sist, t): float
    """
    # ATENCIÓ: Vàlid només per boles de masses idèntiques.

    """amp = (np.max(sist.A) + 2.*sist.R + sist.gap) / 2."""
    amp = np.max(sist.A)/2
    omega = np.sqrt(sist.g / sist.L)
    transl = sist.R + sist.gap/2.
    return -1.*amp*np.cos(omega*t*sist.T0) + transl


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
    nom_rel = nom_directori + "CmRel/Rel/" + nom_simulacio + "_Rel.csv"

    parametres_sist = sim.llegeixMetadata(nom_metadata)
    sist = sim.Sistema(**parametres_sist)

    data = np.genfromtxt(nom_rel, delimiter=",")
    t = data[:, 0]
    pos_rel = data[:, 1]

    with open(str(nom_rel).replace("Rel.csv", "AdjRel.csv"), "r") as fitxer:
        pos_rel_sgn = np.genfromtxt(fitxer, delimiter=",")

    pos_rel_sgn = pos_rel_sgn[:, 1]

    """
    Representa la funció assajada.
    """
    xr_s = np.array([np.abs(xr_prova(nom_rel, t_i)) for t_i in t[1:]]) + 2.*sist.R

    csvwrite(str(nom_rel).replace("Rel.csv", "AdjPro.csv"), t[1:], xr_s)

    plt.plot(t[1:], xr_s, color='orange')
    plt.plot(t[1:-1], pos_rel_sgn[1:-1], color='b')

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('x_r(sgn) (-)', fontsize=18)

    plt.savefig(str(nom_rel).replace("Rel.csv", "AdjPro.png"))

    plt.clf()

    """
    Representa la diferència entre l'ajust realitzat i la corba simulada.
    """
    xr_diff = np.abs(pos_rel_sgn[1:-1] - xr_s[:-1])

    plt.plot(t[1:-1], xr_diff)

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('err(x_r(sgn)) (-)', fontsize=18)

    plt.savefig(str(nom_rel).replace("Rel.csv", "AdjDiff.png"))

    plt.clf()

    """
    Genera i representa posicions del centre de masses i posicions de les boles.
    """
    xcm_s = np.array([xcm_prova(sist, t_i) for t_i in t[1:]])

    x1_prova = xcm_s - np.abs(xr_s)/2.
    x2_prova = xcm_s + np.abs(xr_s)/2.

    plt.plot(t[1:], x1_prova, color='b', label="Bola 1")
    plt.plot(t[1:], x2_prova, color='g', label="Bola 2")

    plt.xlabel("t/T0 (-)", fontsize=18)
    plt.ylabel("x (m)", fontsize=18)

    plt.legend(loc="upper right")

    plt.savefig(nom_directori + "Oscillacions/" + nom_simulacio + "_OscPro.png")

    plt.clf()

    """
    Representa la diferència entre l'ajust realitzat i la corba simulada.
    """
    data_pos = sim.Data(nom_data)

    x1_diff = np.abs(x1_prova - data_pos.posicions[1:, 0])
    x2_diff = np.abs(x2_prova - data_pos.posicions[1:, 1])

    plt.plot(data_pos.temps[1:], x1_diff, color='b', label="err(x1)")
    plt.plot(data_pos.temps[1:], x2_diff, color='g', label="err(x2)")

    plt.xlabel('t/T0 (-)', fontsize=18)
    plt.ylabel('err(x_cm) (-)', fontsize=18)

    plt.legend(loc="upper right")

    plt.savefig(nom_directori + "Oscillacions/" + nom_simulacio + "_OscDiff.png")

    plt.clf()

    final = time() - inici
    t_avg = (t_avg * iter + final) / (iter + 1)
    printProgressBar(iter, len(noms_simulacions), len=30, temps_restant=t_avg * (len(noms_simulacions) - iter))

plt.close()
