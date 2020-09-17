# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: EnergiaMecanica.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Calcula i representa l'energia mecànica de les partícules.
 - Revisió: 17/09/2020
"""

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from pathlib import Path
from os.path import basename

import Simulacio as sim


def calculEnergia(sist, data, i):
    """
    Retorna l'energia mecànica del sistema en un instant determinat.

        Paràmetres
            sist: obj Simulacio.Sistema
            data: obj Simulacio.Data
            i: int
        Retorna
            E: np.ndarray
    """
    E = np.zeros(sist.N)
    vel_inst = sist.vel(data, i)
    pos_inst = (data.posicions[i, :] + data.posicions[i-1, :]) / 2. - sist.pos_eq
    E += 0.5*sist.m*vel_inst*vel_inst
    E += 0.5*sist.kg*pos_inst*pos_inst
    return E


if __name__ == "__main__":
    """
    Ús dels fitxer de dades i metadades
    """
    inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n")
    nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/"

    noms_simulacions = Path(nom_directori + "/Data/").glob("*Sim*")

    for nom_simulacio in noms_simulacions:
        """
        Variables caracterísitques del sistema i generació de l'objecte
        """
        nom_simulacio = str(basename(nom_simulacio)).replace(".csv", "")
        nom_simulacio = nom_simulacio.replace("_Sim", "")
        nom_data = nom_directori + "Data/" + nom_simulacio + "_Sim.csv"
        nom_metadata = nom_directori + "Metadata/" + nom_simulacio + "_Sim.dat"

        parametres_sist = sim.llegeixMetadata(nom_metadata)

        sist = sim.Sistema(**parametres_sist)

        data = sim.Data(nom_data)

        """
        Generació del vector d'energies
        """
        energies = np.array([calculEnergia(sist, data, i) for i in range(1, len(data.temps))])

        """
        Representació gràfica de les dades
        """
        default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm'])
                          + cycler(linestyle=['-', '--', ':', '-.', '--']))
        plt.rc('axes', prop_cycle=default_cycler)

        for i in range(sist.N):
            plt.plot(data.temps[1:]/sist.T0, energies[:, i], label="Bola "+str(i+1))

        plt.xlabel('t/T0 (-)', fontsize=18)
        plt.ylabel('E (J)', fontsize=18)
        plt.legend(loc='upper right')

        nom_figura = Path(nom_directori+"Energies/")
        try:
            nom_figura.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            pass

        print("Desant figura %s" % (nom_simulacio+"_Emc.png"))

        plt.savefig(str(nom_figura)+"/"+nom_simulacio+"_Emc.png", dpi=600)
        # plt.show()
        plt.clf()
