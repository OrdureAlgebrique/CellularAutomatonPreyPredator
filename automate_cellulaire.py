# rassasié predateur
# rassasié proie
# probleme sur appetit 2



from tkinter import *
from random import randrange
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
sys.setrecursionlimit(10000)



plt.ion()





haut = 50  # hauteur du tableau
larg = 50  # largeur du tableau
cote = 10  # cÃ´tÃ© d'une cellule
proie = 1
predateur = 10
plante = 100
mort = 0
flag = 0




nombre_proie=haut*16
nombre_predateur=haut*10
nombre_plante=haut*30
proietemps=[nombre_proie]
predateurtemps=[nombre_predateur]

proiedt=[nombre_proie]
predateurdt=[nombre_predateur]

moyenneproie=[nombre_proie]
moyennepredateur=[nombre_predateur]


temps=[0]
fig, ax = plt.subplots(1,2,figsize=(10,4))
line1, = ax[0].plot(temps, proietemps)
line2, = ax[0].plot(temps,predateurtemps)
line3, = ax[1].plot(proiedt,predateurdt, alpha=0.09, color='red')

ax[0].set_xlabel('Temps')
ax[0].set_ylabel('Proie/Predateurs')
ax[1].set_xlabel('Proies')
ax[1].set_ylabel('Predateurs')





fig.show()






# Créer les matrices
lievre =     [[0 for ligne in range(haut)] for colonne in range(larg)]
lynx = [[0 for ligne in range(haut)] for colonne in range(larg)]
herbe = [[0 for ligne in range(haut)] for colonne in range(larg)]
fleurissement = [[0 for ligne in range(haut)] for colonne in range(larg)]
etat = [[mort for ligne in range(haut)] for colonne in range(larg)]
sur1 = [[mort for ligne in range(haut)] for colonne in range(larg)]
sur2 = [[mort for ligne in range(haut)] for colonne in range(larg)]
depl1 = [[mort for ligne in range(haut)] for colonne in range(larg)]
depl2 = [[mort for ligne in range(haut)] for colonne in range(larg)]
rep1 = [[mort for ligne in range(haut)] for colonne in range(larg)]
rep2 = [[mort for ligne in range(haut)] for colonne in range(larg)]
repro1 = [[mort for ligne in range(haut)] for colonne in range(larg)]
feconde1 = [[mort for ligne in range(haut)] for colonne in range(larg)]
feconde2 = [[mort for ligne in range(haut)] for colonne in range(larg)]



appetit1 = [[0 for ligne in range(haut)] for colonne in range(larg)]
appetit2 = [[0 for ligne in range(haut)] for colonne in range(larg)]
age1 = [[0 for ligne in range(haut)] for colonne in range(larg)]
age2 = [[0 for ligne in range(haut)] for colonne in range(larg)]
cell = [[0 for row in range(haut)] for col in range(larg)]

deplacement=[(3,3),(8,3),(13,3),(18,3),(23,3),(3,8),(8,8),(13,8),(18,8),(23,8),(3,13),(8,13),(13,13),(18,13),(23,13),(3,18),(8,18),(13,18),(18,18),(23,18),(3,23),(8,23),(13,23),(18,23),(23,23)]
# Calculer et dessiner le prochain tableau
def tableau():
    global flag
    global temps
    calcultemps()
    reset()
    reproduction_plante()
    reproduction_predateur()
    reproduction_proie()
    deplacement_proie()
    deplacement_predateur()
    survis()
    concatener()
    dessiner_ecosysteme()
    dessiner_population()
    if flag==1:
        fenetre.after(0, tableau)
    else:
        flag=0

# Données initiales
def init():
    for y in range(haut):
        for x in range(larg):
            etat[x][y] = mort
            sur1[x][y] = mort
            sur2[x][y] = mort
            depl1[x][y] = mort
            depl2[x][y] = mort
            cell[x][y] = canvas.create_rectangle((x*cote, y*cote, (x+1)*cote, (y+1)*cote), outline="grey", fill="white")

    # placer au hasard 25% de lievres vivantes
    for i in range(nombre_proie):
        x=randrange(1,larg-1)
        y=randrange(1,larg-1)
        faim=randrange(1,10)
        vieil=randrange(1,10)
        lievre[x][y] = proie
        appetit1[x][y]=faim
        age1=vieil
    for i in range(nombre_predateur):
        x=randrange(1,larg-1)
        y=randrange(1,larg-1)
        faim=randrange(1,10)
        vieil=randrange(1,10)
        lynx[x][y] = proie
        appetit2[x][y]=faim
        age2=vieil
    for i in range(nombre_plante):
        x=randrange(1,larg-1)
        y=randrange(1,larg-1)
        fleuri=randrange(1,5)
        herbe[x][y] = 100
        fleurissement[x][y]=fleuri

#Reproduction des animaux

def reproduction_predateur():
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            if mangerpredateur(x,y):
                feconde2[x][y]=feconde2[x][y]+1
                lievre[x][y]=0
                if feconde2[x][y] == 3:
                    """naissance d'un bébé, tue le lievre sur le lieu de naissance et predateur rassasié"""
                    feconde2[x][y]=0
                    if lynx[x+1][y] == 0 and rep2[x+1][y] ==0 and (x+1) !=(haut-1):
                        rep2[x+1][y]=predateur
                        age2[x+1][y] = 0
                        appetit2[x][y]=0
                        appetit2[x+1][y]=0
                        feconde2[x+1][y]=feconde2[x][y]
                    elif lynx[x][y+1] == 0 and rep2[x][y+1] ==0 and (y+1) != (haut-1):
                        rep2[x][y+1]=predateur
                        age2[x][y+1] = 0
                        appetit2[x][y]=0
                        appetit2[x][y+1]=0
                        feconde2[x][y+1]=feconde2[x][y]
                    elif lynx[x-1][y] == 0 and rep2[x-1][y] ==0 and (x-1)!= 0 :
                        rep2[x-1][y]=predateur
                        age2[x-1][y] = 0
                        appetit2[x][y]=0
                        appetit2[x-1][y]=0
                        feconde2[x-1][y]=feconde2[x][y]
                    elif lynx[x][y-1] == 0 and rep2[x][y-1] ==0 and (y-1) != 0 :
                        rep2[x][y-1]=predateur
                        age2[x][y-1] = 0
                        appetit2[x][y]=0
                        appetit2[x][y-1]=0
                        feconde2[x][y-1]=feconde2[x][y]
                else:
                    False

    for y in range(1,haut-1):
        for x in range(1,larg-1):
            lynx[x][y] = rep2[x][y]


def reproduction_proie():
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            if mangerproie(x,y):
                herbe[x][y] = 0
                feconde1[x][y]=feconde1[x][y]+1
                """naissance d'un bébé, tue la plante et proie rassasié"""
                if feconde1[x][y]==2:
                    feconde1[x][y]=0
                    if lievre[x+1][y] == 0 and rep1[x+1][y] == 0 and (x+1) !=(haut-1):
                        rep1[x+1][y]=proie
                        age1[x+1][y] = 0
                        appetit1[x][y]=0
                        appetit1[x+1][y]=0
                        feconde1[x+1][y]=feconde1[x][y]
                    elif lievre[x][y+1] == 0 and rep1[x][y+1] ==0 and (y+1) != (haut-1):
                        rep1[x][y+1]=proie
                        age1[x][y+1] = 0
                        appetit1[x][y]=0
                        appetit1[x][y+1]=0
                        feconde1[x][y+1]=feconde1[x][y]
                    elif lievre[x-1][y] == 0 and rep1[x-1][y] ==0 and (x-1)!= 0:
                        rep1[x-1][y]=proie
                        age1[x-1][y] = 0
                        appetit1[x][y]=0
                        appetit1[x-1][y]=0
                        feconde1[x-1][y]=feconde1[x][y]
                    elif lievre[x][y-1] == 0 and rep1[x][y-1] ==0 and (y-1) != 0:
                        rep1[x][y-1]=proie
                        age1[x][y-1] = 0
                        appetit1[x][y]=0
                        appetit1[x][y-1]=0
                        feconde1[x][y-1]=feconde1[x][y]
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            lievre[x][y]= rep1[x][y]



def reproduction_plante():
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            if herbe[x][y]==plante:
                fleurissement[x][y]= fleurissement[x][y]+1
                if fleurissement[x][y] >= 2:
                    fleurissement[x][y] = 0
                    depla=randrange(1,5)
                    if depla == 1:
                        herbe[x+1][y]=plante
                    elif depla == 2:
                        herbe[x][y+1]=plante
                    elif depla == 3:
                        herbe[x-1][y]=plante
                    elif depla == 4:
                        herbe[x][y-1]=plante






#Deplacer les animaux
def deplacement_predateur():
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            if lynx[x][y] > 0:
                depla=randrange(0,5)
                if depla == 0:
                    depl2[x][y]=+predateur
                elif depla == 1:
                    if lynx[x+1][y] == 0 and depl2[x+1][y] ==0 and (x+1) !=(larg-1):
                        depl2[x+1][y]=+predateur
                        depl2[x][y] =0
                        age2[x+1][y] = age2[x][y]
                        age2[x][y] = 0
                        appetit2[x+1][y] = appetit2[x][y]
                        appetit2[x][y] = 0
                        feconde2[x+1][y]=feconde2[x][y]
                        feconde2[x][y]=0
                    else:
                        depl2[x][y]=+predateur
                elif depla == 2:
                    if lynx[x][y+1] == 0 and depl2[x][y+1] ==0 and (y+1) != (haut-1):
                        depl2[x][y+1]=+predateur
                        depl2[x][y] =0
                        age2[x][y+1] = age2[x][y]
                        age2[x][y] = 0
                        appetit2[x][y+1] = appetit2[x][y]
                        appetit2[x][y] = 0
                        feconde2[x][y+1]=feconde2[x][y]
                        feconde2[x][y]=0
                    else:
                        depl2[x][y]=+predateur
                elif depla == 3:
                    if lynx[x-1][y] == 0 and depl2[x-1][y] ==0 and (x-1)!= 0:
                        depl2[x-1][y]=+predateur
                        depl2[x][y] =0
                        age2[x-1][y] = age2[x][y]
                        age2[x][y] = 0
                        appetit2[x-1][y] = appetit2[x][y]
                        appetit2[x][y] = 0
                        feconde2[x-1][y]=feconde2[x][y]
                        feconde2[x][y]=0
                    else:
                        depl2[x][y]=+predateur
                elif depla == 4:
                    if lynx[x][y-1] == 0 and depl2[x][y-1] ==0 and (y-1) != 0:
                        depl2[x][y-1]=+predateur
                        depl2[x][y] =0
                        age2[x][y-1] = age2[x][y]
                        age2[x][y] = 0
                        appetit2[x][y-1] = appetit2[x][y]
                        appetit2[x][y] = 0
                        feconde2[x][y-1]=feconde2[x][y]
                        feconde2[x][y]=0
                    else:
                        depl2[x][y]=+predateur
            else:
                if depl2[x][y] == 0:
                    depl2[x][y] =0
                else:
                    pass
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            lynx[x][y] = depl2[x][y]










def deplacement_proie():
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            if lievre[x][y] > 0:
                depla=randrange(0,5)
                if depla == 0:
                    depl1[x][y]=+proie
                elif depla == 1:
                    if lievre[x+1][y] == 0 and depl1[x+1][y] ==0 and (x+1) !=(larg-1):
                        depl1[x+1][y]=+proie
                        depl1[x][y] =0
                        age1[x+1][y] = age1[x][y]
                        age1[x][y] = 0
                        appetit1[x+1][y] = appetit1[x][y]
                        appetit1[x][y] = 0
                    else:
                        depl1[x][y]=+proie
                elif depla == 2:
                    if lievre[x][y+1] == 0 and depl1[x][y+1] ==0 and (y+1) != (haut-1):
                        depl1[x][y+1]=+proie
                        depl1[x][y] =0
                        age1[x][y+1] = age1[x][y]
                        age1[x][y] = 0
                        appetit1[x][y+1] = appetit1[x][y]
                        appetit1[x][y] = 0
                    else:
                        depl1[x][y]=+proie
                elif depla == 3:
                    if lievre[x-1][y] == 0 and depl1[x-1][y] ==0 and (x-1)!= 0:
                        depl1[x-1][y]=+proie
                        depl1[x][y] =0
                        age1[x-1][y] = age1[x][y]
                        age1[x][y] = 0
                        appetit1[x-1][y] = appetit1[x][y]
                        appetit1[x][y] = 0
                    else:
                        depl1[x][y]=+proie
                elif depla == 4:
                    if lievre[x][y-1] == 0 and depl1[x][y-1] ==0 and (y-1) != 0:
                        depl1[x][y-1]=+proie
                        depl1[x][y] =0
                        age1[x][y-1] = age1[x][y]
                        age1[x][y] = 0
                        appetit1[x][y-1] = appetit1[x][y]
                        appetit1[x][y] = 0
                    else:
                        depl1[x][y]=+proie
            else:
                if depl1[x][y] == 0:
                    depl1[x][y] =0
                else:
                    pass
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            lievre[x][y] = depl1[x][y]

# Appliquer  règles de survis

def survis():
    for y in range(1,haut-1):
        for x in range(1,larg -1):
            if lievre[x][y] == proie:
                appetit1[x][y]=appetit1[x][y] +1
                age1[x][y]= age1[x][y] +1
            if lynx[x][y] == predateur:
                appetit2[x][y]=appetit2[x][y] +1
                age2[x][y]= age2[x][y] +1

            '''si la proie trop vieille elle meurt'''
            if lievre[x][y] == proie or lynx[x][y] == predateur:
                if (lievre[x][y] == proie) and not meurt(appetit1[x][y],age1[x][y]):
                    pass
                else:
                    lievre[x][y] = mort
                    age1[x][y]=0
                    appetit1[x][y]=0
                    feconde1[x][y]=0
                if (lynx[x][y] == predateur) and not meurt(appetit2[x][y],age2[x][y]):
                    pass
                else:
                    lynx[x][y] = mort
                    age2[x][y]=0
                    appetit2[x][y]=0
                    feconde2[x][y]=0
            else:
                pass




# Dessiner tout les animaux
def calcultemps():
     temps.append(len(temps))
     return temps

def concatener():
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            etat[x][y]=lievre[x][y]+lynx[x][y] + herbe[x][y]

def dessiner_ecosysteme():
    '''reste de la division euclidienne par 10 -> proie
       reste de la divi euclidienne par 10 du quotient de la division euclidienne par 100 -> predateur
       quotient de la division euclidienne par 100 -> plante
       ici herbe predateur proie'''
    for y in range(1,haut-1):
        for x in range(1,larg-1):
            if etat[x][y]==0:
                coul = "white"
            elif (etat[x][y]//100)==1 and ((etat[x][y]//10)%10) == 0 and (etat[x][y]%10)==0 :
                coul = "green"
            elif (etat[x][y]//100)==0 and ((etat[x][y]//10)%10) == 0 and (etat[x][y]%10)==1 :
                coul = "blue"
            elif (etat[x][y]//100)==0 and ((etat[x][y]//10)%10) == 1 and (etat[x][y]%10)==0 :
                coul = "red"
            elif (etat[x][y]//100)==0 and ((etat[x][y]//10)%10) == 1 and (etat[x][y]%10)==1 :
                coul = "#AB4BFF"
            elif (etat[x][y]//100)==1 and ((etat[x][y]//10)%10) == 1 and (etat[x][y]%10)==0 :
                coul = "#FF4F00"
            elif (etat[x][y]//100)==1 and ((etat[x][y]//10)%10) == 0 and (etat[x][y]%10)==1 :
                coul = "#4BB4FF"
            elif (etat[x][y]//100)==1 and ((etat[x][y]//10)%10) == 1 and (etat[x][y]%10)==1 :
                coul = "black"
            else:
                pass
            canvas.itemconfig(cell[y][x], fill=coul)



def dessiner_population():
    nombrepredateur=0
    nombreproie=0
    for y in range(haut):
        for x in range(larg):
            nombreproie += lievre[x][y]
            nombrepredateur += lynx[x][y]/10

    proietemps.append(nombreproie)
    predateurtemps.append(nombrepredateur)

    proiedt=[proietemps[-2],proietemps[-1]]
    predateurdt=[predateurtemps[-2],predateurtemps[-1]]

    line1.set_data(temps,proietemps)
    line2.set_data(temps,predateurtemps)
    ax[1].plot(proiedt,predateurdt, alpha=0.09,color='red')

    ax[0].set_xlim(0,temps[-1]+1)
    ax[0].set_ylim(0,max(max(proietemps),max(predateurtemps))+1)
    ax[1].set_xlim(0,max(proietemps)+1)
    ax[1].set_ylim(0,max(predateurtemps)+1)
    fig.canvas.draw()







'''
    plt.plot(proietemps,predateurtemps)'''

def reset():
    for y in range(1,haut-1):
        for x in range(1,larg -1):
            sur1[x][y] = 0
            sur2[x][y] = 0
            depl1[x][y] = 0
            depl2[x][y] = 0
            rep2[x][y]=lynx[x][y]
            rep1[x][y]=lievre[x][y]


# arret de l'animation"
def stop():
    global flag
    flag=0

#démarrage de l'animation"
def start():
    global flag
    if flag==0:
        flag=1
    tableau()


#animation pas à pas
def pasapas():
    global flag
    flag=2
    tableau()


# fonctions regissant les proies


def mangerpredateur(x,y):
    if appetit2[x][y] > 2:
        if lievre[x][y] != 0 and lynx[x][y]!=0:
            return True
        else:
            pass

def mangerproie(x,y):
    if appetit1[x][y] > 3:
        if lievre[x][y] != 0 and herbe[x][y]!=0:
            return True
        else:
            return False

def meurt(faim,vieillesse):

    if faim > 13:
        return True
    elif vieillesse > 25:
        return True
    else:
        return False






# Lancement du programme

fenetre = Tk()
fenetre.title("Simulation ecosysteme")
canvas = Canvas(fenetre, width=cote*larg, height=cote*haut, highlightthickness=0)
canvas.pack()
bou1 = Button(fenetre,text='Quitter', width=8, command=fenetre.destroy)
bou1.pack(side=RIGHT)
bou2 = Button(fenetre, text='Démarrer', width=8, command=start)
bou2.pack(side=LEFT)
bou3 = Button(fenetre, text='Arrêter', width=8, command=stop)
bou3.pack(side=LEFT)
bou4 = Button(fenetre, text='Pas à  pas', width=8, command=pasapas)
bou4.pack(side=LEFT)
init()

tableau()
fenetre.mainloop()
