# -*- coding: utf-8 -*-

"""
Projecte: Newton's Cradle.

 - Mòdul: Fragments.py
 - Autors: Parker, Neil i Ballestero, Marc.
 - Descripció: Fragments de codi interessants de preservar
 - Revisió: 15/09/2020
"""

"""
Detecció i càlcul del temps d'interacció de la primera colisio.

La variable de control primeraColisio prèn els valors
    # 0: ja s'ha produït;
    # 1: s'esta produint (l'ultima bola es mou);
    # 2: s'esta produint (l'ultima bola esta en repos);
    # 3: encara no s'ha produït.
"""
# primeraColisio = 3
# for n in range(1, iteracions):
#     if primeraColisio:
#         if primeraColisio == 3:
#             if xi(pos[1,:], 0, 1) != 0:
#                 primeraColisio = 2
#                 tempsInteraccio -= t
#         if primeraColisio == 2:
#             if xi(pos[1,:], N-2, N-1) != 0:
#                 primeraColisio = 1
#         if primeraColisio == 1:
#             if xi(pos[1,:], N-2, N-1) == 0:
#                 primeraColisio = 0
#                 tempsInteraccio += t
#                 metadata.write("%e\n" % (tempsInteraccio))
#                 metadata.close()

"""
Càlcul de la variació d'energia mecànica del sistema, per comprovar la
fiabilitat del mètode numèric.
"""
# data = np.genfromtxt("./Simulacions/"+nom_inp+".csv", delimiter=",")
# posicio = data[:,1:-1]
# temps = data[:,0]
# energia = data[:,-1]
#
# E_inici = energia[0]          #energia inicial del sistema
# E_final = energia[-1]          #energia final del sistema
#
# varEnergia = np.fabs((E_final-E_inici)/E_inici*100)
