# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Simulació del pèndol de Newton integrant numèricament l'equació
   diferencial que el regeix seguint l'algorisme de Verlet.
 - Revisió: 15/09/2020
"""

import numpy as np
from scipy import constants as const
import time


"""
Variables caracterísitques dels sistema.
"""
N = 2                             # nombre de boles
g = const.g                       # acceleracio de la gravetat
L = 1.3                           # longitud del fil
R = 0.025                         # radi de les boles
eta = 6.8e-4*1                    # coeficient de fregament dinàmic
gamma = 1.47e2*1                  # coeficient de dissipacio viscoelàstica
pas = 2.5e-3                      # pas de l'algoritme
num_osc = 30                      # nombre d'oscil·lacions
gap = 1.0e-3                      # espai entre les boles
salt = 10                         # salt de desada de les dades en els impactes

A = np.array([np.sin(4*const.pi/180)*L]+[0 for i in range(N-1)])    # amplitud inicial
m = np.array([0.1113, 0.1113])                                      # massa de les boles
E = np.array([2.55e7, 2.55e7])                                      # mòdul de Young
j = np.array([0.48, 0.48])                                          # ràtio de Poisson


T0 = 2.*const.pi*np.sqrt(L/g)                             # període dels pèndols
k = np.append(np.sqrt(2*R)*E / (3*(1-j*j)),
              [0. for i in range(N-1)])                   # constant recuperadora de les boles
v = A*np.sqrt(g/L)                                        # velocitat d'impacte
kg = m*g/L                                                # constant recuperadora de la gravetat
l0 = np.max(pow(pow(m, 2)*pow(v, 4)/pow(k, 2), 0.2))      # escala dels desplaçaments
t0 = 0.                                                   # escala de temps
for i in range(N):
    if v[i] != 0:
        if t0 == 0:
            t0 = pow(pow(m[i], 2) / ((pow(k[i], 2)*v[i])), 0.2)
        elif pow(pow(m[i], 2) / ((pow(k[i], 2)*v[i])), 0.2) < t0:
            t0 = pow(pow(m[i], 2)/((pow(k[i], 2)*v[i])), 0.2)

dt = pas*t0                                # pas de temps
t = -dt                                    # temps fisic
temps_exec = num_osc*T0                    # temps d'execució
iteracions = int(temps_exec/dt)            # nombre d'iteracions (dos períodes)

"""
Inicialitazió de les posicions i velocitats inicials.
    pos_eq: posició d'equilibre de les boles
    pos: s'hi guarden les últimes posicions de les boles
    vel_inici: velocitat inicial de les boles
"""

pos_eq = np.array([(2*R+gap)*i for i in range(N)])
pos = np.empty((3, N))
vel_inici = np.zeros(N)

pos[0, :] = pos_eq
pos[1, :] = pos_eq
pos[:2, :] -= A

"""
Declaració de funcions
"""


def xi(x, i, j):
    """
    Retorna el solapament entre les boles i-èssima i j-èssima.

        Paràmetres
            x: np.ndarray,
            i, j: int,
        Retorna
            xi(x, i, j): float.
    """
    if i < 0 or j < 0 or i >= N or j >= N:
        return 0.

    xi = 2.*R-np.fabs(x[i]-x[j])

    if xi > 0:
        return xi

    else:
        return 0.


def dxi(i, j):
    """
    Retorna la derivada temporal del solapament entre les boles en un lapse dt.

        Paràmetres
            i, j: int
        Retorna
            dxi(i, j): np.ndarray
    """
    return (pow(xi(pos[1, :], i, j), 1.5)-pow(xi(pos[0, :], i, j), 1.5)) / dt


def vel():
    """
    Retorna les velocitats mitjanes de les boles en un lapse de temps dt.

        Paràmetres
            None
        Retorna
            vel(): np.ndarray
    """
    return (pos[1, :]-pos[0, :]) / dt


def acc(x, v):
    """
    Retorna les acceleracions de les boles.

        Paràmetres
            x, v: np.ndarray
        Retorna
            acc(x, v): np.ndarray
    """
    return np.array([(k[i]*pow(xi(x, i-1, i), 1.5)-k[i+1]*pow(xi(x, i, i+1), 1.5)
                    + kg[i]*(pos_eq[i]-x[i])-eta*v[i]+gamma
                    * (dxi(i, i-1)-dxi(i, i+1))) / m[i] for i in range(N)])


def verlet(dt):
    """
    Implementa l'algorisme de Verlet i calcula i desa la següent posició de les
    boles en la variable pos, en funció de les dues posicions anteriors,
    amb un pas dt.

        Paràmetres
            dt: float
        Retorna
            t + dt: float
    """
    pos[2, :] = 2.*pos[1, :] - pos[0, :] + dt*dt*acc(pos[1, :], vel())

    return t + dt


def rungeKutta(dt):
    """
    Implementa el mètode RK4 per calcular les dues primeres posicions del sistema.

        Paràmetres
            dt: float
        Retorna
            t + dt: float
    """
    k1v = dt*acc(pos[0, :], vel_inici)
    k1x = vel_inici*dt

    k2v = acc(pos[0, :]+0.5*k1x, vel_inici)*dt
    k2x = (vel_inici+0.5*k1v)*dt

    k3v = acc(pos[0, :]+0.5*k2x, vel_inici)*dt
    k3x = (vel_inici+0.5*k2v)*dt

    k4x = (vel_inici+k3v)*dt

    pos[1, :] = pos[0, :] + 1./6.*(k1x+2*k2x+2*k3x+k4x)

    return t + dt


def calculEnergia():
    """
    Retorna l'energia mecànica del sistema en un instant determinat.

        Paràmetres
            None
        Retorna
            E: float
    """
    E = 0.
    vel_inst = vel()
    pos_inst = (pos[1, :]+pos[0, :]) / 2.
    for j in range(N):
        E += 0.5*m[i]*vel_inst[j]*vel_inst[j]
        E += 0.5*kg[i]*(pos_inst[j]-pos_eq[j])*(pos_inst[j]-pos_eq[j])

    return E


def escriureFitxer(fitxer, t, x):
    """
    Escriu en un fitxer .csv les posicions de les boles.

        Paràmetres
            fitxer: _io.TextIOWrapper
        Retorna
            None
    """
    fitxer.write("%e," % (t))
    for i in range(N-1):
        fitxer.write("%e," % (x[i]))
    fitxer.write("%e," % (x[N-1]))


# Treball amb els fitxers de dades i de metadades

nom_inp = input("Nom de l'execucio?\n")
fitxer = open("../Simulacions/"+nom_inp+".csv", "w")
metadata = open("../Simulacions/"+nom_inp+".dat", "w")

metadata.write("%d\n" % (N))
metadata.write("%e\n" % (g))
metadata.write("%e\n" % (L))
metadata.write("%e\n" % (R))
metadata.write("%e\n" % (eta))
metadata.write("%e\n" % (gamma))
metadata.write("%e\n" % (pas))
metadata.write("%e\n" % (num_osc))
metadata.write("%e\n" % (gap))

for i in range(N):
    metadata.write("%e " % (A[i]))
metadata.write("\n")

for i in range(N):
    metadata.write("%e " % (m[i]))
metadata.write("\n")

for i in range(N):
    metadata.write("%e " % (E[i]))
metadata.write("\n")

for i in range(N):
    metadata.write("%e " % (j[i]))
metadata.write("\n")


# Iteració de l'algorisme de Verlet

progres = 0.1
fita = int(progres*iteracions)

tempsInteraccio = 0.
primeraColisio = 3              #0: ja s'ha produit; 1: s'esta produint (l'ultima bola es mou); 2: s'esta produint (l'ultima bola esta en repos); 3: encara no s'ha produit
inici = time.time()
t = rungeKutta(dt)
escriureFitxer(fitxer, t, pos[0,:]-pos_eq)
fitxer.write("%e\n" % (calculEnergia()))
for n in range(1, iteracions):
    if primeraColisio:
        if primeraColisio == 3:
            if xi(pos[1,:], 0, 1) != 0:
                primeraColisio = 2
                tempsInteraccio -= t
        if primeraColisio == 2:
            if xi(pos[1,:], N-2, N-1) != 0:
                primeraColisio = 1
        if primeraColisio == 1:
            if xi(pos[1,:], N-2, N-1) == 0:
                primeraColisio = 0
                tempsInteraccio += t
                metadata.write("%e\n" % (tempsInteraccio))
                metadata.close()
    dist = 0
    for j in range(N-1):
        dist += pos[1,j+1]-pos[1,j]
    if dist < 3:
        salt = 100
    else:
        salt = 1e5
    t = verlet(dt)
    pos[0,:] = pos[1,:]
    pos[1,:] = pos[2,:]
    if n%salt == 0:
        escriureFitxer(fitxer, t, pos[0,:]-pos_eq)
        fitxer.write("%e\n" % (calculEnergia()))
    if n > fita:
        print("%2.0f %%" % (100*progres), end = "")
        print("\t temps restant: %.2f segons" % ((time.time() - inici)/progres*(1-progres)))
        progres += 0.1
        fita = int(progres*iteracions)
escriureFitxer(fitxer, t+dt, pos[1,:]-pos_eq)
fitxer.write("%e\n" % (calculEnergia()))

'''
data = np.genfromtxt("./Simulacions/"+nom_inp+".csv", delimiter=",")
posicio = data[:,1:-1]
temps = data[:,0]
energia = data[:,-1]

E_inici = energia[0]          #energia inicial del sistema
E_final = energia[-1]          #energia final del sistema

varEnergia = np.fabs((E_final-E_inici)/E_inici*100)
'''

print("\n--- temps total: %.2f segons ---" % (time.time() - inici))
fitxer.close()
