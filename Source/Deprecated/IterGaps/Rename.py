from os import rename
from sys import exit

mode = input("Mode? GAP [G] / RADI [R]?\n")

if mode == 'G':

    nom_inp = input("Nom de les simulacions? \n")

    str_R = input("Radi de les simulacions (e-1 mm)?\n")


    nom_carpeta = "../Simulacions/Gaps"+str_R+"dmm/"

    for i in range(10, 100):
        print("Renombrant els arxius %s" % ("Gaps_"+str(i)+"_"+str(i)[1]+"_"+nom_inp+"_"+str_R+"dmm"))
        rename(nom_carpeta+"Gaps_"+str(i)+"_"+str(i)[1]+"_"+nom_inp+"_"+str_R+"dmm.csv", nom_carpeta+"Gaps_"+str(i)[0]+"_"+str(i)[1]+"_"+nom_inp+"_"+str_R+"dmm.csv")
        rename(nom_carpeta+"Gaps_"+str(i)+"_"+str(i)[1]+"_"+nom_inp+"_"+str_R+"dmm.dat", nom_carpeta+"Gaps_"+str(i)[0]+"_"+str(i)[1]+"_"+nom_inp+"_"+str_R+"dmm.dat")

if mode == 'R':

    nom_inp = input("Nom de les simulacions? \n")

    str_R0 = input("Radi incorrecte de les simulacions (e-1 mm)?\n")

    str_R1 = input("Radi correcte de les simulacions (e-1 mm)?\n")

    nom_carpeta = "../Simulacions/Gaps"+str_R0+"dmm/"

    for i in range(10):
        for j in range(10):
            print("Renombrant els arxius %s" % ("Gaps_"+str(i)+"_"+str(j)+"_"+nom_inp+"_"+str_R0+"dmm"))
            rename(nom_carpeta+"Gaps_"+str(i)+"_"+str(j)+"_"+nom_inp+"_"+str_R0+"dmm.csv", nom_carpeta+"Gaps_"+str(i)+"_"+str(j)+"_"+nom_inp+"_"+str_R1+"dmm.csv")
            rename(nom_carpeta+"Gaps_"+str(i)+"_"+str(j)+"_"+nom_inp+"_"+str_R0+"dmm.dat", nom_carpeta+"Gaps_"+str(i)+"_"+str(j)+"_"+nom_inp+"_"+str_R1+"dmm.dat")

    print("Renombrant el directori %s" % (nom_carpeta))
    rename(nom_carpeta, "../Simulacions/Gaps"+str_R1+"dmm/")
else:
    exit(1)
