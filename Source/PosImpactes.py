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
metadata = open("../Simulacions/"+nom_inp + ".dat", "r")


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

pos_eq = np.array([(2*R+gap)*i for i in range(1,N+1)])

default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm']) +
                  cycler(linestyle=['-', '--', ':', '-.', '--']))
plt.rc('axes', prop_cycle=default_cycler)

data = np.genfromtxt("../Simulacions/"+nom_inp+".csv", delimiter=",")
pos = data[:,1:-1]
t = data[:,0]

xocs = np.array([])
tempsImp = np.array([])

ctrl = 0

for i in range(np.size(pos,0)):
    if not ctrl:
        if xi(pos[i,:], 0, 1) > 0:
            ctrl = 1
            xocs = np.append(xocs, pos[i,0])
            tempsImp = np.append(tempsImp, t[i])
    if ctrl:
        if xi(pos[i,:], 0, 1) == 0:
            ctrl = 0

plt.plot(tempsImp/T0, xocs/l0)
plt.savefig("../Simulacions/"+nom_inp+"PosImp.png")
plt.show()
