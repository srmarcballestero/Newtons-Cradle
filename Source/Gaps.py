# -*- coding: utf-8 -*-

# Projecte: Newton's Cradle
# Descripció: Simulacions amb gaps entre un inici i un final
# Revisió: 29/08/2020


import numpy as np
from scipy import constants as const
import time
from os import mkdir

# Aquesta funció retorna el "solapament" entre les boles i i j.


def xi(x, i, j):
    if i < 0 or j < 0 or i >= N or j >= N:
        return 0.

    xi = 2.*R-np.fabs(x[i]-x[j])

    if xi > 0:
        return xi

    else:
        return 0.


# Aquesta funció retorna un vector amb l'acceleració de cadascuna de les boles, en funció de la seva posició.

def vel():
    return (pos[1, :]-pos[0, :])/dt


def dxi(i, j):
    return (pow(xi(pos[1, :], i, j), 1.5)-pow(xi(pos[0, :], i, j), 1.5))/dt


def acc(x, v):
    return np.array([(k[i]*pow(xi(x, i-1, i), 1.5)-k[i+1]*pow(xi(x, i, i+1), 1.5)+kg[i]*(pos_eq[i]-x[i])-eta*v[i]+gamma*(dxi(i, i-1)-dxi(i, i+1)))/m[i] for i in range(N)])


# Aquesta funció implementa l'algorisme de Verlet i retorna la següent posició de les boles en funció de les dues posicions anteriors i el pas de temps dt.

def verlet(dt):
    pos[2, :] = 2.*pos[1, :] - pos[0, :] + dt*dt*acc(pos[1, :], vel())

    return t + dt


def rungeKutta(dt):
    k1v = dt*acc(pos[0, :], vel_inici)
    k1x = vel_inici*dt
    k2v = acc(pos[0, :]+0.5*k1x, vel_inici)*dt
    k2x = (vel_inici+0.5*k1v)*dt
    k3v = acc(pos[0, :]+0.5*k2x, vel_inici)*dt
    k3x = (vel_inici+0.5*k2v)*dt
    k4x = (vel_inici+k3v)*dt

    pos[1, :] = pos[0, :]+1/6*(k1x+2*k2x+2*k3x+k4x)

    return t + dt


def calculEnergia():
    E = 0
    vel_inst = vel()
    pos_inst = (pos[1, :]+pos[0, :])/2
    for j in range(N):
        E += 0.5*m[i]*vel_inst[j]*vel_inst[j]
        E += 0.5*kg[i]*(pos_inst[j]-pos_eq[j])*(pos_inst[j]-pos_eq[j])

    return E

# Aquesta funció escriu en un fitxer la posició de les cinc boles en format ".csv". Emmagatzemo les posicions en un fitxer ja que, si no ho faig, de seguida la memòria esdevé un factor limitant per a la simulació.


def escriureFitxer(fitxer, t, x):
    fitxer.write("%e," % (t))
    for i in range(N-1):
        fitxer.write("%e," % (x[i]))
    fitxer.write("%e," % (x[N-1]))


nom_inp = input("Nom de les simulacions?\n")

str_gap_inicial = input("Gap inicial (mm)?\n")
str_gap_final = input("Gap final (mm)?\n")
str_gap_pas = input("Pas de les iteracions (mm)?\n")

gap_inicial = 1.e-3 * float(str_gap_inicial)
gap_final = 1.e-3 * float(str_gap_final)
gap_pas = 1.e-3 * float(str_gap_pas)

radi_inicial = 52.5e-3
radi_final = 55.e-3
radi_pas = 2.5e-3

gap = gap_inicial

R = radi_inicial

N = 2                             # nombre de boles
g = const.g                       # acceleracio de la gravetat
L = 1.3                           # longitud del fil
eta = 6.8e-4*1                    # coeficient de fregament dinàmic 6.8e-4
gamma = 1.47e2*1                  # coeficient de dissipacio viscoelastica 1.47e2
pas = 2.5e-2                      # pas de l'algoritme
num_osc = 30                      # nombre d'oscil·lacions
salt = 10                         # salt de desada de les dades en els impactes

A = np.array([np.sin(4*const.pi/180)*L]+[0 for i in range(N-1)])     # amplitud
m = np.array([0.1, 0.1])                                             # massa de les boles
E = np.array([2.55e7, 2.55e7])                                       # mòdul de Young
j = np.array([0.48, 0.48])                                           # ratio de Poisson

T0 = 2*const.pi*np.sqrt(L/g)              # periode dels pèndols
v = A*np.sqrt(g/L)                        # velocitat d'impactegap
kg = m*g/L                                # constant recuperadora de la gravetat
temps_exec = num_osc*T0                   # temps d'execució

# -----------------------------------------------------------------------------

while R < radi_final:
    gap = gap_inicial
    nom_carpeta = "Gaps" + str(int(R*1e4)) + "dmm"
    mkdir("../Simulacions/"+nom_carpeta)

    print("--- RADI = %e ---" % (R))

    while gap < gap_final:

        k = np.sqrt(2*R)*E/(3*(1-j*j))                     # constant recuperadora de les boles
        l0 = np.max(pow(pow(m, 2)*pow(v, 4)/pow(k, 2), 0.2))   # escala dels desplaçaments
        t0 = 0                                             # escala de temps
        for i in range(N):
            if v[i] != 0:
                if t0 == 0:
                    t0 = pow(pow(m[i], 2)/((pow(k[i], 2)*v[i])), 0.2)
                elif pow(pow(m[i], 2)/((pow(k[i], 2)*v[i])), 0.2) < t0:
                    t0 = pow(pow(m[i], 2)/((pow(k[i], 2)*v[i])), 0.2)

        dt = pas*t0                                # pas de temps
        t = -dt                                    # temps fisic
        iteracions = int(temps_exec/dt)            # nombre d'iteracions (dos períodes)

        # Inicialitzo la posició d'equilibri de manera que les boles s'estiguin tocant. En la posició incial, totes les boles estan en repòs a la seva posició d'equilibri i la bola 0 està en repòs desplaçada una distància A de la seva posició d'equilibri.

        k = np.append(np.sqrt(2*R)*E/(3*(1-j*j)), [0.])
        pos_eq = np.array([(2*R+gap)*i for i in range(1, N+1)])
        pos = np.empty((3, N))
        vel_inici = np.zeros(N)
        pos[0, :] = pos_eq
        pos[1, :] = pos_eq
        pos[:2, :] -= A

        # Treball amb els fitxers de dades i de metadades

        if gap < 1.e-3:
            fitxer = open("../Simulacions/"+nom_carpeta+"/Gaps_0_"+str(int(round(gap*1e4)))
                          [0]+"_"+nom_inp+"_"+str(int(R*1e4))+"dmm.csv", "w")
            metadata = open("../Simulacions/"+nom_carpeta+"/Gaps_0_" +
                            str(int(round(gap*1e4)))[0]+"_"+nom_inp+"_"+str(int(R*1e4))+"dmm.dat", "w")
        else:
            fitxer = open("../Simulacions/"+nom_carpeta+"/Gaps_"+str(int(round(gap*1e4)))
                          [:2]+"_"+str(int(round(gap*1e4)))[-1]+"_"+nom_inp+"_"+str(int(R*1e4))+"dmm.csv", "w")
            metadata = open("../Simulacions/"+nom_carpeta+"/Gaps_"+str(int(round(gap*1e4)))
                            [:2]+"_"+str(int(round(gap*1e4)))[-1]+"_"+nom_inp+"_"+str(int(R*1e4))+"dmm.dat", "w")

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

        print("--- GAP = %e ---" % (gap))

        progres = 0.1
        fita = int(progres*iteracions)

        tempsInteraccio = 0.
        # 0: ja s'ha produit; 1: s'esta produint (l'ultima bola es mou); 2: s'esta produint (l'ultima bola esta en repos); 3: encara no s'ha produit
        primeraColisio = 3
        inici = time.time()
        t = rungeKutta(dt)
        escriureFitxer(fitxer, t, pos[0, :]-pos_eq)
        fitxer.write("%e\n" % (calculEnergia()))
        for n in range(1, iteracions):
            if primeraColisio:
                if primeraColisio == 3:
                    if xi(pos[1, :], 0, 1) != 0:
                        primeraColisio = 2
                        tempsInteraccio -= t
                if primeraColisio == 2:
                    if xi(pos[1, :], N-2, N-1) != 0:
                        primeraColisio = 1
                if primeraColisio == 1:
                    if xi(pos[1, :], N-2, N-1) == 0:
                        primeraColisio = 0
                        tempsInteraccio += t
                        metadata.write("%e\n" % (tempsInteraccio))
                        metadata.close()
            dist = 0
            for p in range(N-1):
                dist += pos[1, p+1]-pos[1, p]
            if dist < 3:
                salt = 100
            else:
                salt = 1e5
            t = verlet(dt)
            pos[0, :] = pos[1, :]
            pos[1, :] = pos[2, :]
            if n % salt == 0:
                escriureFitxer(fitxer, t, pos[0, :]-pos_eq)
                fitxer.write("%e\n" % (calculEnergia()))
            if n > fita:
                print("%2.0f %%" % (100*progres), end="")
                print("\t temps restant: %.2f segons" % ((time.time() - inici)/progres*(1-progres)))
                progres += 0.1
                fita = int(progres*iteracions)
        escriureFitxer(fitxer, t+dt, pos[1, :]-pos_eq)
        fitxer.write("%e\n" % (calculEnergia()))

        print("\n--- temps total: %.2f segons ---" % (time.time() - inici))
        fitxer.close()

        gap += gap_pas
    R += radi_pas
