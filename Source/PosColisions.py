"""
Projecte: Newton's Cradle.

 - Mòdul: PosColisions.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Representa la posició de les col·lisions, la seva direccionalitat
    i les velocitats de les boles.
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

"""
Detecció de les col·lisions, la seva direccionalitat i velocitats
"""
t_col = np.array([])
colisions = np.array([])
vel = [np.array([]), np.array([])]
trans = []                                  # False: 0->1, True: 1->0
i = 0


while i < len(t):
    if sist.xi(pos[i, :], 0, 1) != 0:
        t_col = np.append(t_col, [t[i]])
        colisions = np.append(colisions, [pos[i, 0]])
        vel[0] = np.append(vel[0], [(pos[i-1, 0]-pos[i-2, 0]) / (t[i-1]-t[i-2])])
        vel[1] = np.append(vel[1], [(pos[i-1, 1]-pos[i-2, 1]) / (t[i-1]-t[i-2])])
        if vel[0][len(vel[0])-1] * vel[1][len(vel[1])-1] > 0:
            if vel[0][len(vel[0])-1] > 0:
                trans.append(False)
            else:
                trans.append(True)
        else:
            # print("Col·lisió oposada detectada, a la oscil·lació %f" % (t[i]/T0))
            if vel[0][len(vel[0])-1] > vel[1][len(vel[1])-1]:
                trans.append(False)
            else:
                trans.append(True)

        ctrl = t[i] + 0.75*sist.T0
        while i < len(t):
            if t[i] < ctrl:
                i += 1
            else:
                break
    else:
        i += 1

trans = np.array(trans)

plt.plot(t_col/sist.T0, colisions, color='y', label="Posició de les colisions (m)")
plt.plot(t_col[trans]/sist.T0, colisions[trans], ".", color="green", markersize=10, label="Posició de les colisions 1->0 (m)")
plt.plot(t_col[np.invert(trans)]/sist.T0, colisions[np.invert(trans)], "*", color="red", markersize=10, label="Posició de les colisions 0->1 (m)")
plt.plot(t_col/sist.T0, vel[0][:], color="orange", linestyle="--", label="Velocitat bola 0 (m/s)")
plt.plot(t_col/sist.T0, vel[1][:], color="blue", linestyle=":", label="Velocitat bola 1 (m/s)")
plt.axhline(0, color='black', linewidth=0.4)

plt.xlabel('t/T0 (-)', fontsize=18)
plt.legend(loc='upper right')

# plt.savefig(Path(nom_simulacio+"_PosCol.png"))
plt.show()
