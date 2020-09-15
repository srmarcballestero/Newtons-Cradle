# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from scipy import constants as const

def vel(i):
    return (pos[i,:]-pos[i-1,:])/(t[i]-t[i-1])

def calculEnergia(i):
    E = np.zeros(N)
    vel_inst = vel(i)
    pos_inst = (pos[i,:]+pos[i-1,:])/2
    E += 0.5*m*vel_inst*vel_inst
    E += 0.5*kg*pos_inst*pos_inst

    return E

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
t = data[:,0]

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

energies = np.array([calculEnergia(i) for i in range(1, len(t))])

default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm']) +
                  cycler(linestyle=['-', '--', ':', '-.', '--']))
plt.rc('axes', prop_cycle=default_cycler)


for i in range(N):
    plt.plot(t[1:]/T0, energies[:,i], label = "Bola "+str(i+1))

plt.xlabel('t/T0 (-)', fontsize=18)
plt.ylabel('E (J)', fontsize=18)


plt.show()

#plt.savefig("../Simulacions/"+nom_inp+".png")
