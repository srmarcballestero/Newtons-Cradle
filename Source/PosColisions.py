# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from scipy import constants as const



def xi(x, i, j):
    if i < 0 or j < 0 or i >= N or j >= N:
        return 0.

    xi = 2.*R-np.fabs(x[i]-x[j])

    if xi > 0:
        return xi

    else:
        return 0.


nom_inp = input("Nom de l'execucio?\n")
metadata = open("../Simulacions/Gaps200dmm/"+nom_inp+".dat", "r")

N = int(metadata.readline())
g = float(metadata.readline())
L = float(metadata.readline())
R = float(metadata.readline())
eta = float(metadata.readline())
gamma = float(metadata.readline())
pas = float(metadata.readline())
num_osc = float(metadata.readline())
gap = float(metadata.readline())

A = metadata.readline().split(" ")[:-1]
m = metadata.readline().split(" ")[:-1]
E = metadata.readline().split(" ")[:-1]
j = metadata.readline().split(" ")[:-1]


A = np.array([float(i) for i in A])
m = np.array([float(i) for i in m])
E = np.array([float(i) for i in E])
j = np.array([float(i) for i in j])

data = np.genfromtxt("../Simulacions/Gaps200dmm/"+nom_inp+".csv", delimiter=",")
pos = data[:,1:-1]
temps = data[:,0]

T0 = 2*const.pi*np.sqrt(L/g)               #periode dels pèndols
k = np.sqrt(2*R)*E/(3*(1-j*j))             #constant recuperadora de les boles
v = A*np.sqrt(g/L)                        #velocitat d'impacte
kg = m*g/L                                 #constant recuperadora de la gravetat
l0 = np.max(pow(pow(m,2)*pow(v,4)/pow(k,2),0.2))   #escala dels desplaçaments
t0 = 0
for i in range(N):
    if v[i] != 0:
        if t0 == 0:
            t0 = pow(pow(m[i],2)/((pow(k[i],2)*v[i])),0.2)
        elif pow(pow(m[i],2)/((pow(k[i],2)*v[i])),0.2) < t0:
            t0 = pow(pow(m[i],2)/((pow(k[i],2)*v[i])),0.2)


dt = pas*t0                                #pas de temps
temps_exec = num_osc*T0                    #temps d'execució
iteracions = int(temps_exec/dt)            #nombre d'iteracions (dos períodes)

pos_eq = np.array([(2*R+gap)*i for i in range(N)])


# ---------------------------------------------------------------------------- #

t_col = np.array([])
colisions = np.array([])
vel = [np.array([]), np.array([])]
trans = []  #False: 0->1, True: 1->0
i = 0

while i < len(temps):
    if xi(pos[i,:]+pos_eq, 0, 1) != 0:
        t_col = np.append(t_col, [temps[i]])
        colisions = np.append(colisions, [pos[i,0]])
        vel[0] = np.append(vel[0],[(pos[i-1,0]-pos[i-2,0])/(temps[i-1]-temps[i-2])])
        vel[1] = np.append(vel[1],[(pos[i-1,1]-pos[i-2,1])/(temps[i-1]-temps[i-2])])
        if vel[0][len(vel[0])-1] * vel[1][len(vel[1])-1] > 0:
            if vel[0][len(vel[0])-1] > 0:
                trans.append(False)
            else:
                trans.append(True)
        else:
            print("Col·lisió oposada detectada, a la oscil·lació %f" % (temps[i]/T0))
            if vel[0][len(vel[0])-1] > vel[1][len(vel[1])-1]:
                trans.append(False)
            else:
                trans.append(True)

        ctrl = temps[i] + 0.75*T0
        while i < len(temps):
            if temps[i] < ctrl:
                i += 1
            else:
                break
    else:
        i += 1

trans = np.array(trans)

plt.plot(t_col/T0, colisions, color='y', label = "Posició de les colisions (m)")
plt.plot(t_col[trans]/T0, colisions[trans], ".", color="green", markersize=10, label = "Posició de les colisions 1->0 (m)")
plt.plot(t_col[np.invert(trans)]/T0, colisions[np.invert(trans)], "*", color="red", markersize=10, label = "Posició de les colisions 0->1 (m)")
plt.plot(t_col/T0, vel[0][:], color = "orange", linestyle = "--", label = "Velocitat bola 0 (m/s)")
plt.plot(t_col/T0, vel[1][:], color = "blue", linestyle = ":", label = "Velocitat bola 1 (m/s)")
plt.axhline(0, color='black', linewidth = 0.4)
plt.xlabel('t/T0 (-)', fontsize=18)
plt.legend()
plt.show()
