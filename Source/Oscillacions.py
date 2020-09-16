# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants as const
from pathlib import Path

nom_inp = input("Nom de l'execucio?\n")
metadata = open(Path("/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+nom_inp+".dat"), "r")

N = int(metadata.readline())
g = float(metadata.readline())
L = float(metadata.readline())
R = float(metadata.readline())
gap = float(metadata.readline())
eta = float(metadata.readline())
gamma = float(metadata.readline())

A = metadata.readline().split(" ")[:-1]
m = metadata.readline().split(" ")[:-1]
E = metadata.readline().split(" ")[:-1]
j = metadata.readline().split(" ")[:-1]

A = np.array([float(i) for i in A])
m = np.array([float(i) for i in m])
E = np.array([float(i) for i in E])
j = np.array([float(i) for i in j])

pas = float(metadata.readline())
num_osc = float(metadata.readline())
salt = float(metadata.readline())


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

data = np.genfromtxt(Path("/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+nom_inp+".csv"), delimiter=",")
pos = data[:,1:]
t = data[:,0]

print(pos)
for i in range(np.size(pos, 0)):
    pos[i, :] += pos_eq

colors = ['b', 'g']

for i in range(N):
    plt.fill_between(t[:5000]/T0, pos[:5000,i]/R-1, pos[:5000,i]/R+1, interpolate=True, alpha=0.5, color=colors[i])
    plt.plot(t[:5000]/T0, pos[:5000,i]/R, label = "Bola "+str(i+1), color=colors[i])

plt.xlabel('t/T0 (-)', fontsize=18)
plt.ylabel('x/R (-)', fontsize=18)

# plt.savefig("../Simulacions/"+nom_inp+"_Osc_Abs.png")

plt.legend(loc = 'lower left')
plt.show()
