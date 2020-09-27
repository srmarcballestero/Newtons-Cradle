# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from scipy import constants as const

noms_inp = ["Gaps_"+str(i)+"_"+str(j)+"_GG_25" for i in range(0,15) for j in range(0,10)]

for nom_inp in noms_inp:
    try:
        metadata = open("../Simulacions/Gaps/"+nom_inp + ".dat", "r")

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

        data = np.genfromtxt("../Simulacions/Gaps/"+nom_inp+".csv", delimiter=",")
        posicio = data[:,1:]
        temps = data[:,0]

        j = 0
        maxims = np.zeros(int(num_osc))

        for i in range(np.size(maxims)):
            while temps[j] < (i+1)*T0 and j < np.size(temps)-1:
                if np.fabs(posicio[j,1]) > maxims[i]:
                    maxims[i] = np.fabs(posicio[j,1])
                j += 1

        print(maxims)

        plt.plot(np.array(range(1, int(num_osc)+1)), maxims/np.max(A))#, '.', color='blue')
        print("Guardant figura %s" % (nom_inp+"_Amp.png"))
        plt.savefig("../Simulacions/Gaps/"+nom_inp+"_Amp.png")
        plt.clf()
        #plt.show()
    except FileNotFoundError:
        continue
