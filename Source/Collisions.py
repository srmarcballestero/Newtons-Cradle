# -*- coding: utf-8 -*-

# ARXIU A RENOVAR SEGUINT L'ORIENTACIÓ A OBJECTES
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from scipy import constants as const

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

pos = pos/l0

i = 0

while i < np.size(pos,0):
    dist = 0
    for j in range(N-1):
        dist += pos[i,j+1]-pos[i,j]
    if dist < 3:
        inici = i
        while dist < 3 and i < np.size(pos,0):
            i += 1
            dist = 0
            for j in range(N-1):
                    dist += pos[i,j+1]-pos[i,j]
        final = i
        for j in range(N):
            plt.plot((t[inici:final]-t[inici])/t0, pos[inici:final,j]+j+1, label = "Bola "+str(j+1))
        plt.legend(loc = 'lower left')
        plt.savefig("../Simulacions/"+nom_inp+"Col_"+str(i)+".png")
        plt.show()
    i += 1
