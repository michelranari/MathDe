
import numpy as np
import csv
import sys
import Enumeration as enum

# On créé le tableau de notes
notes = ["TB", "B", "AB", "P", "I", "AR", "-1"]


#################################################
# Retourne l'élève qui a la moins bonne note maximum
# preferencesE : liste de préférences des élèves
# note : note courante à analyser pour les élèves
# eleve : numero de l'eleve courant
#################################################
def eleveMoinsBienNote(preferencesE, note=0, eleve=None):
    # Si c'est le premier passage
    if (eleve == None):
        # On crée une variable contenant l'élève courant le moins bien noté
        eleve = preferencesE[1, 0]

        # Aucun élève restant ou un seul
    if (preferencesE.shape[1] == 1 or preferencesE.shape[1] == 2):

        # Si un seul élève restant
        if (preferencesE.shape[1] == 2):
            # on sauvegarde l'élève
            eleve = preferencesE[0, 1]

        # on retourne l'élève courant
        return eleve

    # S'il reste plus d'un élève
    if (preferencesE.shape[1] > 2):
        # On baisse la note
        preferencesE = getPreferencesFiltreesParNote(preferencesE, note)

    return eleveMoinsBienNote(preferencesE, note + 1, eleve)


#################################################
# Retourne la liste des préférences donnée en supprimant tous les élèves ayant au moins une fois la note en paramètre
# preferencesE : liste de préférences des élèves
# note : note courante à analyser pour les élèves
#################################################
def getPreferencesFiltreesParNote(preferencesE, note):
    suppression = False

    # On cherche colonne par colonne pour avoir les notes d'un étudiant
    # Initialisation de l'indice
    i = 1
    # Pour chaque colonne (1 élève)
    for indiceEleve in range(1, preferencesE.shape[1]):

        if (suppression):
            # On recule l'indice car on a supprimé un élève
            i = i - 1
            suppression = False

        # Pour chaque ligne (note obtenue)
        for j in range(1, preferencesE.shape[0]):
            # si l'étudiant a un TB, on le supprime de la liste
            if (preferencesE[j, i] == notes[note]):
                suppression = True

        if (suppression):
            # Suppression de l'élève de la liste
            preferencesE = np.delete(preferencesE, i, axis=1)
            # On incrémente pour que la boucle fasse un tour de moins (car 1 élève en moins)
            indiceEleve = indiceEleve + 1

        i = i + 1
    return preferencesE


#################################################
# Retourne la liste des élèves qui ont mis la meilleure note à l'élève en paramètre
# preferencesE : liste de préférences des élèves
# eleve : numero de l'élève couran#eleve : numero de l'eleve courant
##################################################

def getElevesMeilleureNote(preferencesE, eleve):
    numColECourant = 0

    # Trouve le numerau de colone du joueur
    for i in range(1, (preferencesE.shape[1])):
        if (preferencesE[0, i] == eleve):
            numColECourant = i

    # erreur si on a pas trouver le joueur
    if (numColECourant == 0):
        return "erreur"

    else:
        noteMax = 5
        tabEleve = []
        # on parcour la colone de note attribue au joueur
        for i in range(1, (preferencesE.shape[0])):

            # si on trouve une note équivalente
            if (notes.index(preferencesE[i][numColECourant]) == noteMax):
                tabEleve.append(preferencesE[i][0])

            # si on trouve une meilleur note on change note max et on
            # recre le tableau
            elif (notes.index(preferencesE[i][numColECourant]) < noteMax):
                noteMax = notes.index(preferencesE[i][numColECourant])
                tabEleve = [preferencesE[i][0]]
    return tabEleve


#################################################
# Permet de recuperer l'indice de la colone(et ligne ils sont identiques) d'un eleve avec son numero
# preferencesE : liste de préférences des eleves
# eleve1 : eleve dont on cherche a connaitre l'indice dans la matrice
# Return : int : l'indice
#################################################

def indiceEleve(preferencesE, eleve):
    numColECourant = None
    # Trouve le numero de colonne du joueur
    for i in range(1, (preferencesE.shape[1])):
        if (preferencesE[0, i] == eleve):
            numColECourant = i
    return numColECourant


#################################################
# Détermine la note qu'un élève a attribué à un autre
# preferencesE : liste de préférences des eleves
# eleve1 : élève ayant mis la note
# eleve2 : élève ayant reçu la note
# Return : String : note que eleve1 a donné à eleve2
#################################################

def getNote(preferencesE, eleve1, eleve2):
    ligneNote = indiceEleve(preferencesE, eleve1)
    colNote = indiceEleve(preferencesE, eleve2)
    res = preferencesE[ligneNote][colNote]
    return res


#################################################
# Supprime l'eleve de la liste de préférences
# preferencesE : liste de préférences des eleves
# eleve : numero de l'eleve à supprimer
# Return : la matrice de preferences des eleves sans l'eleve en question
#################################################

def supprimerEleve(preferencesE, eleve):
    indiceColEleve = indiceEleve(preferencesE, eleve)
    # supprime la colone
    preferencesE = np.delete(preferencesE, indiceColEleve, axis=1)

    # supprime la ligne
    preferencesE = np.delete(preferencesE, indiceColEleve, axis=0)

    return preferencesE


#################################################
# Détermine le moins bonne note entre 2 élèves
# preferencesE : liste de préférences des eleves
# eleve1 : numero de l'eleve 1
# eleve2 : numero de l'eleve 2
# Return : String : Moins bonne note entre les 2 élèves
#################################################

def getNoteMin(preferencesE, eleve1, eleve2):
    note1 = getNote(preferencesE, eleve1, eleve2)
    note2 = getNote(preferencesE, eleve2, eleve1)

    if (notes.index(note1.upper()) > notes.index(note2.upper())):
        return note1.upper()
    else:
        return note2.upper()


#################################################
# Détermine le meilleur élève à attribuer avec l'autre élève en paramètre
# preferencesE : liste de préférences des eleves
# eleve : numero de l'eleve pour lequel il faut trouver un partenaire
# Return : int : élève de la liste à affecter avec l'eleve en parametre
#################################################

def getMeilleurPartenaire(preferencesE, eleve):
    indiceNoteMax = 6
    i = 1
    eleveSatissaisant = None

    while ((indiceNoteMax != 0) and (i < preferencesE.shape[0])):
        # on evite de le comparer à lui meme
        if (eleve != preferencesE[0][i]):
            noteMin = getNoteMin(preferencesE, eleve, preferencesE[0][i])
            note = notes.index(noteMin)
            if (note < indiceNoteMax):
                indiceNoteMax = notes.index(noteMin)
                eleveSatissaisant = preferencesE[0][i]
        i += 1

    return eleveSatissaisant


#################################################
# Détermine le meilleur binome dans lequel un élève peut être affecté
# preferencesE : liste de préférences des eleves
# matriceGroupes : matrice des groupes déjà créée
# eleve : élève à placer dans un binome
# Return : int : indice de la ligne du binome dans lequel eleve sera attribué
#################################################

def getMeilleurBinomeEleve(preferencesE, matriceGroupes, eleve):
    # ATTENTION : Ne pas rechercher parmi les trinomes
    # Pour savoir si c'est un binome, ils ont la valeur "None" dans la 3e colonne (2e en partant de 0)
    indiceNoteMin = 0
    i = 1
    indiceLigneBinome = 0
    # Tant que la pire note n'est pas AR et que la matrice des groupes n'est pas terminée
    while (indiceNoteMin != 5 and i < matriceGroupes.shape[0]):

        # Si c'est un binôme
        if (matriceGroupes[i][2] == None):
            # On regarde la note de chaque membre pour l'élève à insérer
            noteMembre1PourEleve = getNote(preferencesE, matriceGroupes[i][0], eleve)
            indexNoteMembre1PourEleve = notes.index(noteMembre1PourEleve)
            noteMembre2PourEleve = getNote(preferencesE, matriceGroupes[i][1], eleve)
            indexNoteMembre2PourEleve = notes.index(noteMembre2PourEleve)
            noteElevePourMembre1 = getNote(preferencesE, eleve, matriceGroupes[i][0])
            indexNoteElevePourMembre1 = notes.index(noteElevePourMembre1)
            noteElevePourMembre2 = getNote(preferencesE, eleve, matriceGroupes[i][1])
            indexNoteElevePourMembre2 = notes.index(noteElevePourMembre2)

            indiceNoteMinCourante = max(indexNoteMembre1PourEleve, indexNoteMembre2PourEleve, indexNoteElevePourMembre1,
                                        indexNoteElevePourMembre2)
            if (indiceNoteMinCourante > indiceNoteMin):
                indiceNoteMin = indiceNoteMinCourante
                indiceLigneBinome = i
        i = i + 1
    return indiceLigneBinome


def nomEleve(eleve):
    strN = str(eleve)
    return strN


def writeResult(matrice):
    # A remettre quand il y aura les projets
    # matrice = np.delete(matrice, (3), axis=1)

    # with open('BMR.csv', 'w+') as result_file:
    #     result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     ligneRepartition = []
    #     for groupe in matrice:
    #         eleves = ""
    #         for eleve in groupe:
    #             if eleve == None:
    #                 eleve = ""
    #             eleves = eleves + " " + nomEleve(eleve)
    #         ligneRepartition.append(eleves)
    #     result_writer.writerow(ligneRepartition)


    with open('BMR.csv', 'w+') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        enumerations = enum.enumerations(setStudent(data2[0]))
        for enumeration in enumerations :
            ligneRepartition = []
            for groupe in enumeration:
                eleves = ""
                for eleve in groupe:
                    if eleve == None:
                        eleve = ""
                    eleves = eleves + " " + nomEleve(eleve)
                ligneRepartition.append(eleves)
            result_writer.writerow(ligneRepartition)

#chargement du csv
#data = np.loadtxt("./DONNEES/preferencesTest.csv", dtype=str, delimiter=',')
#Données de test

ext=""
launch_mode = "exhaustif"
number_results_max = None
for arg in sys.argv[1:]:
    sub_arg = arg[2:]
    if sub_arg[:3] == "arg" :
        launch_mode = sub_arg[4:]
    elif sub_arg[:3] == "num":
        number_results_max = sub_arg[7:]
    elif sub_arg[:3] == "ext":
        ext = sub_arg[4:]

data=np.loadtxt("../DONNEES/preferences" + ext +".csv", dtype=str, delimiter=',')
data2=np.loadtxt("../DONNEES/preferences" + ext +".csv", dtype=str, delimiter=',')

def setStudent(students):
    res = set()
    for student in students:
        if student != '':
            print()
            res.add(student)
    #res.sort()
    #res
    return res

#On créé le tableau de notes
notes = ["TB", "B", "AB", "P", "I", "AR", "-1"]

#################################################
# Programme principal : Il cree des groupes de projet a partir des eleves les plus mal note
# preferencesE : liste de préférences entre les élèves
# Retourne une matrice des groupes
#################################################

def main(preferencesE):
    #Creation de la matrice des groupes
    #groupes = np.array([["eleve1","eleve2","eleve3","projet"]])
    groupes = np.array([["eleve1","eleve2","eleve3"]])
    #instanciation du nombre de projets
    nbProjet = 18

    #Création d'un tampon qui sera modifié tout au long du programme
    preferencesTmp = preferencesE

    nbBinome = 0

    ##TRAITEMENT DES BINOMES
    #Tant qu'il reste des élèves et qu'on n'a pas couvert tous les sujets de projets
    # while (nbBinome < 18 and preferencesTmp.shape[0] >= 3):
    #
    #     #On récupère l'élève le moins bien noté avec sa meilleure note
    #     eleveCourant = eleveMoinsBienNote(preferencesTmp)
    #
    #     #On récupère l'élève pour lequel la satisfaction du membre du binome le moins satisfait sera maximale
    #     partenaireEleveCourant = getMeilleurPartenaire(preferencesTmp, eleveCourant)
    #
    #     #On créé un groupe avec l'eleve courant et son partenaire
    #     #groupes = np.append(groupes,[[eleveCourant, partenaireEleveCourant, None, nbProjet]], axis = 0)
    #     groupes = np.append(groupes,[[eleveCourant, partenaireEleveCourant, None]], axis = 0)
    #     #Suppression des eleves
    #     preferencesTmp = supprimerEleve(preferencesTmp, eleveCourant)
    #     preferencesTmp = supprimerEleve(preferencesTmp, partenaireEleveCourant)
    #
    #     # Suppression du projet (Pour la prochaine version)
    #     # supprimerProjet()
    #     nbProjet = nbProjet - 1
    #     nbBinome = nbBinome + 1
    #
    # ##TRAITEMENT DES TRINOMES
    # #Tant qu'il reste des élèves à affecter
    # groupes = np.delete(groupes, (0), axis=0)
    # while (preferencesTmp.shape[0] != 1):
    #
    #     #On récupère l'élève courant
    #     eleveCourant = preferencesTmp[0][1]
    #
    #     #On récupère le binome dans lequel il faut l'affecter
    #     indexBinome = getMeilleurBinomeEleve(preferencesE, groupes, eleveCourant)
    #
    #     #On ajoute l'élève courant au groupe
    #     groupes[indexBinome][2] = eleveCourant
    #
    #     #On supprime l'élève courant de la matrice
    #     preferencesTmp = supprimerEleve(preferencesTmp, eleveCourant)
    #     print()
    return groupes
writeResult(main(data))
main(data)
