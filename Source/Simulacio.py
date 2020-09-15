# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Funcions genèriques comunes per als mòduls del projecte.
 - Revisió: 15/09/2020

IMPORTANT: les següents són les dependències d'aquest mòdul
    # import numpy as np
    # from scipy import constants as const
"""

import numpy as np
from scipy import constants as const


def readMetadata(nom_metadata):
    """
    Llegeix el conjunt mínim de variables en un fitxer de metadades .dat.

    Paràmetres
        nom_metadata: pathlib.Path  # ruta de l'arxiu de metadades
    Retorna
        readMetadata(nom_metadata): dict # diccionari de metadades
    """
    file_metadata = open(nom_metadata, "r")
    metadata = {}

    metadata["N"] = int(file_metadata.readline())
    metadata["g"] = float(file_metadata.readline())
    metadata["L"] = float(file_metadata.readline())
    metadata["R"] = float(file_metadata.readline())
    metadata["gap"] = float(file_metadata.readline())
    metadata["eta"] = float(file_metadata.readline())
    metadata["gamma"] = float(file_metadata.readline())

    A = file_metadata.readline().split(" ")[:-1]
    m = file_metadata.readline().split(" ")[:-1]
    E = file_metadata.readline().split(" ")[:-1]
    j = file_metadata.readline().split(" ")[:-1]

    metadata["A"] = np.array([float(i) for i in A])
    metadata["m"] = np.array([float(i) for i in m])
    metadata["E"] = np.array([float(i) for i in E])
    metadata["j"] = np.array([float(i) for i in j])

    metadata["pas"] = float(file_metadata.readline())
    metadata["num_osc"] = float(file_metadata.readline())
    metadata["salt"] = float(file_metadata.readline())

    file_metadata.close()

    return metadata

class Sistema():
    """
    Classe que conté el conjunt de variables mínim per generar una simulació
    i els seus mètodes genèrics.
    """

    def __init__(self, N, g, L, R, gap, eta, gamma, A, m, E, j, pas, num_osc, salt):
        """
        Inicialitza els paràmetres mínims per generar la simulació.

            Paràmetres
              Físics
                N: int                 # nombre de boles
                g: float               # acceleració de la gravetat
                L: float               # longitud del fil
                R: float               # radi de les boles
                gap: float             # espai entre les boles
                eta: float             # coef. de fregament dinàmic
                gamma: float           # coef. de dissipació viscoelàstica
                A: np.ndarray          # amplitud inicial
                m: np.ndarray          # massa de les boles
                E: np.ndarray          # mòdul de Young de les boles
                j: np.ndarray          # ràtio de Poisson de les boles
              Numèrics
                pas: float             # pas dels algorismes numèrics
                num_osc: float         # nombre d'oscil·lacions a simular
                salt: float            # salt de desada de les dades (malla adaptativa)
        """
        self.N = N
        self.g = g
        self.L = L
        self.R = R
        self.gap = gap
        self.eta = eta
        self.gamma = gamma
        self.A = A
        self.m = m
        self.E = E
        self.j = j

        self.pas = pas
        self.num_osc = num_osc
        self.salt = salt

        """
        Variables calculades a partir del conjunt mínim
            T0: float                  # període dels pèndols
            k: np.ndarray              # constant recuperadora de les boles
            v: float                   # velocitat d'impacte
            kg: float                  # constant recuperadora de la gravetat
            l0: float                  # escala dels desplaçaments
            t0: float                  # escala de temps
            dt: float                  # pas de temps
            t: float                   # temps fisic
            temps_exec: float          # temps d'execució
            iteracions: int            # nombre d'iteracions (dos períodes)
        """

        self.T0 = 2.*const.pi*np.sqrt(self.L / self.g)
        self.k = np.append(np.sqrt(2*self.R)*self.E / (3*(1-self.j*self.j)),
                           [0.])
        self.v = A*np.sqrt(self.g / self.L)
        self.kg = self.m*self.g / self.L
        self.l0 = np.max(pow(pow(self.m, 2)*pow(self.v, 4) / pow(np.max(self.k), 2), 0.2))
        self.t0 = 0.
        for i in range(self.N):
            if self.v[i] != 0:
                if self.t0 == 0:
                    self.t0 = pow(pow(self.m[i], 2) / ((pow(self.k[i], 2)*self.v[i])), 0.2)
                elif pow(pow(self.m[i], 2) / ((pow(self.k[i], 2)*self.v[i])), 0.2) < self.t0:
                    self.t0 = pow(pow(m[i], 2)/((pow(self.k[i], 2)*self.v[i])), 0.2)

        self.dt = self.pas*self.t0
        self.t = -self.dt
        self.temps_exec = self.num_osc*self.T0
        self.iteracions = int(self.temps_exec / self.dt)

        """
        Inicialitazió de les posicions i velocitats inicials.
            pos_eq: posició d'equilibre de les boles
            pos: s'hi guarden les últimes posicions de les boles
            vel_inici: velocitat inicial de les boles
        """
        self.pos_eq = np.array([(2.*self.R + self.gap)*i for i in range(self.N)])
        self.pos = np.empty((3, self.N))
        self.vel_inici = np.zeros(self.N)

        self.pos[0, :] = self.pos_eq
        self.pos[1, :] = self.pos_eq
        self.pos[:2, :] -= A

    def writeMetadata(self, nom_metadata):
        """
        Escriu el conjunt mínim de variables en un fitxer de metadades .dat.

        Paràmetres
            nom_metadata: pathlib.Path  # ruta de l'arxiu de metadades
        Retorna
            None
        """
        metadata = open(nom_metadata, "w")

        metadata.write("%d\n" % (self.N))
        metadata.write("%e\n" % (self.g))
        metadata.write("%e\n" % (self.L))
        metadata.write("%e\n" % (self.R))
        metadata.write("%e\n" % (self.gap))
        metadata.write("%e\n" % (self.eta))
        metadata.write("%e\n" % (self.gamma))

        for i in range(self.N):
            metadata.write("%e " % (self.A[i]))
        metadata.write("\n")

        for i in range(self.N):
            metadata.write("%e " % (self.m[i]))
        metadata.write("\n")

        for i in range(self.N):
            metadata.write("%e " % (self.E[i]))
        metadata.write("\n")

        for i in range(self.N):
            metadata.write("%e " % (self.j[i]))
        metadata.write("\n")

        metadata.write("%e\n" % (self.pas))
        metadata.write("%e\n" % (self.num_osc))
        metadata.write("%e\n" % (self.salt))

        metadata.close()
