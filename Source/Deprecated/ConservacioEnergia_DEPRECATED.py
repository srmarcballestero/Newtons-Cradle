# -*- coding: utf-8 -*-


import numpy as np
from scipy import constants as const
import matplotlib.pyplot as plt
import time
from cycler import cycler


N = 5                             #nombre de boles
m = 0.7                           #massa de les boles
R = 0.034                         #radi de les boles
g = const.g                       #acceleracio de la gravetat
L = 1.3                           #longitud del fil
E = 2e11                          #mòdul de Young
j = 0.33                          #ratio de Poisson
A = np.sin(4*const.pi/180)*L      #amplitud
'''pas = 2.5e-2'''
num_osc = 1                       #espai entre les boles
gap = 0
salt = 10

T0 = 2*const.pi*np.sqrt(L/g)               #periode dels pèndols
kr = np.sqrt(2*R)*E/(3*(1-j*j))             #constant recuperadora de les boles
v = A*np.sqrt(g/L)                         #velocitat d'impacte
kg = m*g/L                                 #constant recuperadora de la gravetat
l0 = pow(pow(m,2)*pow(v,4)/pow(kr,2),0.2)   #escala dels desplaçaments
t0 = pow(pow(m,2)/((pow(kr,2)*v)),0.2)      #escala de temps de les colisions

'''dt = pas*t0'''                                #pas de temps
temps_simulacio = num_osc*T0                    #temps d'execució
'''iteracions = int(temps_simulacio/dt)'''            #nombre d'iteracions (dos períodes)

def xi(x, i, j):
    if i < 0 or j < 0 or i >= N or j >= N:
        return 0.

    xi = 2.*R-np.fabs(x[i]-x[j])

    if xi > 0:
        return xi

    else:
        return 0.

# Aquesta funció retorna un vector amb l'acceleració de cadascuna de les boles, en funció de la seva posició.

def acc(pos_eq, x):
    return np.array([(kr*pow(xi(x,i-1,i),1.5)-kr*pow(xi(x,i,i+1),1.5)+kg*(pos_eq[i]-x[i]))/m for i in range(N)])

# Aquesta funció implementa l'algorisme de Verlet i retorna la següent posició de les boles en funció de les dues posicions anteriors i el pas de temps dt.

def verlet(pos, pos_eq,  dt):
    pos[2,:] = 2.*pos[1,:] - pos[0,:] + dt*dt*acc(pos_eq, pos[1,:])

    return t + dt

def rungeKutta(pos, pos_eq, dt):
    k1v = dt*acc(pos[0,:], pos_eq)
    k1x = vel_inici*dt
    k2v = acc(pos[0,:]+0.5*k1x, pos_eq)*dt
    k2x = (vel_inici+0.5*k1v)*dt
    k3v = acc(pos[0,:]+0.5*k2x, pos_eq)*dt
    k3x = (vel_inici+0.5*k2v)*dt
    k4x = (vel_inici+k3v)*dt

    pos[1,:] = pos[0,:]+1/6*(k1x+2*k2x+2*k3x+k4x)

    return t + dt

# Aquesta funció escriu en un fitxer la posició de les cinc boles en format ".csv". Emmagatzemo les posicions en un fitxer ja que, si no ho faig, de seguida la memòria esdevé un factor limitant per a la simulació.


def escriureFitxer(fitxer, t, x):
    fitxer.write("%e," % (t))
    for i in range(N-1):
        fitxer.write("%e," % (x[i]))
    fitxer.write("%e," % (x[N-1]))
    
def calculEnergia():
    E = 0
    vel_inst = (pos[1,:]-pos[0,:])/dt
    pos_inst = (pos[1,:]+pos[0,:])/2
    for j in range(N):
        E += 0.5*m*vel_inst[j]*vel_inst[j]
        E += 0.5*kg*(pos_inst[j]-pos_eq[j])*(pos_inst[j]-pos_eq[j])
        
    return E
    



default_cycler = (cycler(color=['b', 'g', 'r', 'y', 'm']) +
                      cycler(linestyle=['-', '--', ':', '-.', '--']))
plt.rc('axes', prop_cycle=default_cycler)

passos = np.linspace(1e-4,1e-3,5)
varEnergia = np.empty(10)
tempsExecucio = np.empty(10)
i = 0

print(passos)

for pas in passos:
    
    dt = pas*t0
    iteracions = int(temps_simulacio/dt)

    t = -dt
    nom_inp = "VarEnergia"+str(i)

    fitxer = open(nom_inp+".csv", "w")
    metadata = open(nom_inp+".dat", "w")

    metadata.write("%d\n" % (N))
    metadata.write("%e\n" % (m))
    metadata.write("%e\n" % (R))
    metadata.write("%e\n" % (g))
    metadata.write("%e\n" % (L))
    metadata.write("%e\n" % (E))
    metadata.write("%e\n" % (j))
    metadata.write("%e\n" % (A))
    metadata.write("%e\n" % (pas))
    metadata.write("%e\n" % (num_osc))
    metadata.write("%e\n" % (gap))

    pos_eq = np.array([(2*R+gap)*k for k in range(1,N+1)])
    pos = np.empty((3,N))
    vel_inici = np.zeros(N)
    pos[0,:] = pos_eq
    pos[:1,0] -= A

    inici = time.time()
    t = rungeKutta(pos, pos_eq, dt)
    escriureFitxer(fitxer, t, pos[0,:]-pos_eq)
    fitxer.write("%e\n" % (calculEnergia()))
    for n in range(1, iteracions):
        dist = 0
        for j in range(N-1):
            dist += pos[1,j+1]-pos[1,j]
        if dist < 3:
            salt = 1000
        else:
            salt = 1e6
        t = verlet(pos, pos_eq, dt)
        pos[0,:] = pos[1,:]
        pos[1,:] = pos[2,:]
        if n%salt == 0:
            escriureFitxer(fitxer, t, pos[0,:]-pos_eq)
            fitxer.write("%e\n" % (calculEnergia()))
    pos[0,:] = pos[1,:]
    pos[1,:] = pos[2,:]
    escriureFitxer(fitxer, t+dt, pos[0,:]-pos_eq)
    fitxer.write("%e\n" % (calculEnergia()))
    fitxer.close()
    
    tempsExecucio[i] = time.time() - inici

    # Llegeixo les dades del fitxer

    data = np.genfromtxt(nom_inp+".csv", delimiter=",")
    posicio = data[:,1:-1]
    temps = data[:,0]
    energia = data[:,-1]
  
    E_inici = energia[0]          #energia inicial del sistema
    E_final = energia[-1]          #energia final del sistema
    
    varEnergia[i] = np.fabs((E_final-E_inici)/E_inici*100)

    print(i)
    i += 1

plt.plot(passos, varEnergia)
plt.show()

plt.plot(passos, varEnergia/tempsExecucio)
plt.show()
