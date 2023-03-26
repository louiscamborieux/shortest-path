import math
import time
import matplotlib.pyplot as plt
from random import randint, random, shuffle


#Algorithmes de création de matrice

#Constantes utilisées pour obtenir des matrices comparables
import numpy as np

TAILLE_N = 8
BORNE_A = 1
BORNE_B = 8

"""Crée une matrice de taille nxn contenant des poids de valeur infinie ou comprise entre a et b
Chaque poids a une chance sur deux de valoir +∞"""
def creermatrice(n, a, b):
    resultat = []
    for i in range (n):
        resultat.append([])
        for y in range (n):
            if randint(0,1) == 0:
                resultat[i].append(math.inf)
            else:
                resultat[i].append(randint(a,b))
    return resultat

"""Variante de creermatrice mais chaque poids a p% de chance de valoir +∞ """
def creermatriceprop(n, a, b,p):
    resultat = []
    for i in range (n):
        resultat.append([])
        for y in range (n):
            if random()*100 <=p:
                resultat[i].append(math.inf)
            else:
                resultat[i].append(randint(a,b))
    return resultat

#Creation de matrice d'exemples
mat1 = creermatrice(TAILLE_N,BORNE_A,BORNE_B)
mat2 = creermatriceprop(TAILLE_N,BORNE_A,BORNE_B,40)
mat3 = creermatriceprop(TAILLE_N,BORNE_A,BORNE_B,60)

#Exemples du cours
matcours = [[math.inf,8,6,2],[math.inf]*4,[math.inf,3,math.inf,math.inf],[math.inf,5,1,math.inf]]
matcourspoidsnegatif = [[math.inf,8,6,2],[math.inf]*4,[-4,3,math.inf,math.inf],[math.inf,5,1,math.inf]]



"""
#Affiche une matrice dans la console
#lettres permet de choisir d'afficher ou non les lettres associées au sommets, si non renseigné vaut True
#inf permet de choisir le caractère représentant l'infini, si non renseigné vaut ∞
"""
def affichermatrice (mat,inf='∞',lettres=True):
    l = len(mat)
    entete = '  '
    if lettres:
        for i in range (l):
            entete+=chr(65+i)
            entete+=" "
        print(entete)
    for i in range (l):
        if lettres:
            ligne =chr(65+i)+' '
        else:
            ligne =' '
        for y in range (l):
            if mat[i][y] == math.inf :
                ligne+= inf #Variable contenant la représentation du l'infinité sur l'affichage
            else:
                ligne+= str(mat[i][y])
            ligne+= ","
        print(ligne)

print("Matrice de",TAILLE_N,"x",TAILLE_N,"50% de chance de poids infinis")
affichermatrice(mat1)
print("Matrice de ",TAILLE_N,"x",TAILLE_N,"40% de chance de poids infinis")
affichermatrice(mat2)
print("Matrice de ",TAILLE_N,"x",TAILLE_N,"60% de chance de poids infinis")
affichermatrice(mat3)
print()

for i in range (3):
    affichermatrice(creermatrice(4,1,8))

#Algorithmes de résolution



def dijkstra(M, s0):
    #Initialisation des sommets
    longM = len(M)
    restants = []
    for i in range (longM):
        restants.append(i)
    distpreds = [[math.inf,None]] * longM  # Tableau a deux dimensions contenant la distance [0] et le prédecesseur direct [1]
    distpreds[s0] = [0, s0]
    A = []
    s = s0
    A.append(s) #On considere s0 comme exploré en l'ajoutant à la liste
    while len(A) < longM: #Iteration tant qu'il reste des sommets à explorer
        #Analyse des successeurs
        for i in range (longM):
            """On vérifie si la distance totale entre le sommet vérifié  et l'origine 
            est inferieure à celle notée précedement"""
            sommedistance = distpreds[s][0] + M[s][i]
            if sommedistance < distpreds[i][0]:
                 distpreds[i] = [sommedistance,s]

        restants.remove(s)
        s = restants[0]
        for i in restants:
            if distpreds[i][0] < distpreds[s][0]:
                s = i
        A.append(s) #On ajoute s dans a pour le considéré comme exploré
    return itineraire(distpreds, s0) #Renvoie la distance l'itinéraire le plus court



def bellmanFord(m,s0,methode=None) :
    #Initialisation des sommets
    longM = len(m)
    nbtour = longM-1
    """
    Remplit la liste des arrêtes
    Tableau a deux dimensions contenant la source[0] et la destination[1] de chaque arête
    """
    if methode == "p":
        arêtes = parcoursprofondeur(m,s0)
    elif methode =="l":
        arêtes = parcourslargeur(m,s0)
    else: #Application de la méthode arbitraire
        arêtes = []
        for i in range(longM):
            for j in range(longM):
                if i != j and m[i][j] != math.inf:
                    arêtes.append([i, j])
        shuffle(arêtes) #Mélange de l'ordre des flèches
    distpreds = [[math.inf,None]] * longM  # Tableau a deux dimensions contenant la distance [0] et le prédecesseur direct [1]
    distpreds[s0] = [0, s0]
    i = 0 #Compteur de tour
    tourprecedent = [] #Represente la ligne precedente du tableau
    while (i < nbtour and distpreds!= tourprecedent): #Itere tant que l'on a effectué moins de n-1 tour et pas trouvé de solution
        tourprecedent = distpreds.copy() #Recopie la ligne précedente du tableau
        #Ananlyse chaque arête dans l'ordre
        for arete in arêtes:
            sommedistance = distpreds[arete[0]][0] + m[arete[0]][arete[1]]
            if sommedistance < distpreds[arete[1]][0]:
                distpreds[arete[1]] = [sommedistance,arete[0]]
        i+=1
    if tourprecedent == distpreds:
        return (itineraire(distpreds,0),i)
    else:
        return "pas de plus court chemin : présence d’un cycle de poids négatif."

#Prend le graphe m et un sommet de depart s0
#Retourne la liste des arêtes déduite du parcours en largeur
def parcourslargeur (m, s0):
    listesommet = []
    listearetes = []
    longM = len(m)
    file = []
    file.append(s0);listesommet.append(s0)
    while file != []:
        s = file[0]
        for i in range (longM):
            if s != i and m[s][i] != math.inf :
                listearetes.append([s,i])
                if not i in listesommet:
                    listesommet.append(i)
                    file.append(i)
        file.pop(0)
    return listearetes

#Prend le graphe m et un sommet de depart s0
#Retourne la liste des arêtes déduite du parcours en profondeur
def parcoursprofondeur(m,s0):
    listearetes = []
    longM = len(m)
    pile = [s0]
    while pile != []:
        s= pile[-1] #On arrive sur le sommet de la pile
        i= 0
        while (i < longM): #Recherche les successeurs du sommet s
            if m[s][i] != math.inf and not [s,i] in listearetes: #Verifie que le successeur n'a pas déja été marqué
                break;
            i+=1
        if i == longM: #Si aucun successeur trouvé, dépiler
            pile.pop()
        else : #Sinon empiler et avancer dans le graphe
            listearetes.append([s,i])
            pile.append(i)
    return listearetes

#Donne l'itinéraire à partir du résultat d'un algorithme de plus court chemin
def itineraire(t, s0):
    itineraires = []
    for i in range (len(t)):
        etape = t[i][1] #Assigne le prédecesseur comme étape
        itineraires.append([ (t[i][0])] )
        if etape == None :
            itineraires[i]=("sommet "+chr(i+65)+" non joignable à "+chr(s0+65)+" par un chemin dans le graphe G")
        else :
            itineraires[i].append([chr(etape+65)])
            while etape != 0 :
              etape = t[etape][1]
              itineraires[i][1].insert(0,chr(etape+65))
    return itineraires

print(dijkstra(matcours, 0))


print ("Matrice à résoudre")
affichermatrice(matcours)
print("\nTest des parcours\n")
print("Parcours en largeur")
print (parcourslargeur(matcours,0))
print("\nParcours en profondeur")
print (parcoursprofondeur(matcours,0))

print("\nTest des résolutions\n")
print("Résolution par algorithme de BellmanFord")
print (bellmanFord(matcours, 0))
print("\nRésolution par algorithme de Dijkstra")
print(dijkstra(matcours,0))
print("\nTest résolution de matrice à cycle négatif par BellmanFord\n")
affichermatrice(matcourspoidsnegatif)
print (bellmanFord(matcourspoidsnegatif, 0))

print("\n Test résolution par l'algorithme de BelmanFord selon l'ordre des arêtes")
mat50 =creermatrice(60,BORNE_A,10000)
print("Flèches aléatoires")
print(bellmanFord(mat50,0)[1])
print("Parcours en profondeur")
print(bellmanFord(mat50,0,"p")[1])
print("Parcours en largeur")
print(bellmanFord(mat50,0,"l")[1])


def Dij(n):
    mat = creermatrice(n,BORNE_A,5000)
    debut = time.perf_counter()
    dijkstra(mat, 0)
    fin = time.perf_counter()
    return (fin-debut)

def BF(n):
    mat = creermatrice(n, BORNE_A, 5000)
    debut = time.perf_counter()
    bellmanFord(mat, 0)
    fin = time.perf_counter()
    return (fin-debut)

print(Dij(50))
print(BF(50))

"""Représentations graphique"""

Dijs = []
BFs = []
x = np.arange(0,1)
for i in range (1,200):
    Dijs.append(Dij(i))
    BFs.append(BF(i))

plt.plot(Dijs)
plt.plot(BFs)
plt.ylabel("Temps (en s)")
plt.xlabel("Taille des matrices")
plt.title("Temps de résolution en fonction de la taille des matrices")
plt.legend(["Dijkstra","Belman Ford"])
plt.show()

plt.semilogy(Dijs)
plt.semilogy(BFs)
plt.ylabel("Temps (en s)")
plt.xlabel("Taille des matrices")
plt.title("Temps de résolution en fonction de la taille des matrices")
plt.legend(["Dijkstra","Bellman Ford"])
plt.show()

