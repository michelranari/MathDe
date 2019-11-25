#return le nombre de trinomes max en fonctions de nombre n d'eleves
def nombres_groupes_min(n):
 if (n <= 1):
     return 0
 elif (n % 3 == 0):
     return (int) (n / 3)
 else:
     nb = nombres_groupes_min(n - 2)
     nb = nb + 1
     return nb

#return le nombre de binomes max en fonctions de nombre n d'eleves
def nombres_groupes_max(n):
 if (n <= 1):
     return 0
 elif (n % 2 == 0):
     return (int) (n / 2)
 else:
     nb = nombres_groupes_max(n - 3)
     nb = nb + 1
     return nb


# passe a la prochaine formation en supprimant 3 binomes pour creer 2 trinomes
# fonctions qui trouve la prochaine formation/repartition possible car on commence par
# le nombre de binomes max
def prochaine_formation(formation):
 formation[0] = formation[0] - 3
 formation[1] = formation[1] + 2
 return formation


#return le nb de [binomes,trinomes] selon le nb d'eleves et le nombre de groupes total desiré
def formation_selon_nb_eleves_et_nb_groupes(nbEleves,nbGroupes):
 if (nbEleves % 2 == 0 ):
   res = [ (int) (nbEleves/2) ,0]
   while (res[0] + res[1] > nbGroupes) :
     res = prochaine_formation(res)
   return res
 else :
   res = formation_selon_nb_eleves_et_nb_groupes(nbEleves - 3,nbGroupes - 1)
   res[1] = res[1] + 1
   return res


def enumerations(set_eleves):
 if len(set_eleves) < 2:
     return []
 else:
     nbMax = nombres_groupes_max(len(set_eleves))
     nbMin = nombres_groupes_min(len(set_eleves))
     formation = formation_selon_nb_eleves_et_nb_groupes(len(set_eleves), nbMax)
     nbGroupe = formation[0] + formation[1]
     enumerations = []
     while nbGroupe >= nbMin:
         enumerations.extend(lister_enumerations(set_eleves, formation))
         formation = prochaine_formation(formation)
         nbGroupe = formation[0] + formation[1]
     return enumerations


def lister_enumerations(set_eleves, formation ):
 listEleves = set_eleves.copy()
 if formation[0] <= 1 and formation[1] <= 0:
     return [[[listEleves.pop(), listEleves.pop()]]]
 elif formation[0] <= 0 and formation[1] <= 1:
     return [[[listEleves.pop(), listEleves.pop(), listEleves.pop()]]]
 eleve = listEleves.pop() # on enleve un eleve du set et on le memorise
 enumerations = []
 if formation[0] > 0:
     for eleve2 in listEleves:
         listEleves2 = listEleves.copy()
         listEleves2.discard(eleve2) #on enleve l'eleve2 de listEleves2 et on le memorise
         list_enum = lister_enumerations(listEleves2, [formation[0] - 1, formation[1]])
         for i in range(0, len(list_enum)):
             list_enum[i].append([eleve, eleve2]) # on ajoute les 2 eleves memoriser
         enumerations.extend(list_enum)
 if formation[1] > 0:
     for eleve2 in listEleves:
         listEleves2 = listEleves.copy()
         listEleves2.discard(eleve2) #on enleve l'eleve2 de listEleves2
         for eleve3 in listEleves:
             if eleve2 < eleve3: #on evite les doublons
                 listEleves3 = listEleves2.copy()
                 listEleves3.discard(eleve3)
                 list_enum = lister_enumerations(listEleves3, [formation[0], formation[1] - 1])
                 for i in range(0, len(list_enum)):
                     list_enum[i].append([eleve, eleve2, eleve3])
                 print(list_enum)
                 enumerations.extend(list_enum)
 return enumerations

def lister_enumerations2(set_eleves, formation , meilleurPoidsTrouve , poidsEnCours):
 listEleves = set_eleves.copy()
 if formation[0] <= 1 and formation[1] <= 0:
     #ajouter le dernier poids à poidsEnCours
     poidsEnCours = poidsEnCours + calculValeurPreferenceBinome(formation[0])
     #verifier poidsEnCours < meilleurPoidsTrouve
     return [[[listEleves.pop(), listEleves.pop()]]]
 elif formation[0] <= 0 and formation[1] <= 1:
     #ajouter le dernier poidsà poidsEnCours
     poidsEnCours = poidsEnCours + calculValeurPreferenceBinome(formation[1])
     #verifier poidsEnCours < meilleurPoidsTrouve
     return [[[listEleves.pop(), listEleves.pop(), listEleves.pop()]]]
 eleve = listEleves.pop() # on enleve un eleve du set et on le memorise
 enumerations = []
 if formation[0] > 0:
     for eleve2 in listEleves:
         listEleves2 = listEleves.copy()
         listEleves2.discard(eleve2) #on enleve l'eleve2 de listEleves2 et on le memorise
         #on verifie que le poidsEnCours n'est pas deja supperieur au meilleurPoidsTrouve
         poidsEnCours = poidsEnCours + calculValeurPreferenceBinome(formation[0])
         #si le poidsEnCours est deja plus grand que le meilleurPoidsTrouve ciao on le prend pas
         if(poidsEnCours > meilleurPoidsTrouve):
             return []
         list_enum = lister_enumerations(listEleves2, [formation[0] - 1, formation[1]],meilleurPoidsTrouve , poidsEnCours)
         for i in range(0, len(list_enum)):
             list_enum[i].append([eleve, eleve2]) # on ajoute les 2 eleves memoriser
         enumerations.extend(list_enum)
 if formation[1] > 0:
     for eleve2 in listEleves:
         listEleves2 = listEleves.copy()
         listEleves2.discard(eleve2) #on enleve l'eleve2 de listEleves2
         for eleve3 in listEleves:
             if eleve2 < eleve3: #on evite les doublons
                 listEleves3 = listEleves2.copy()
                 listEleves3.discard(eleve3)
                 list_enum = lister_enumerations(listEleves3, [formation[0], formation[1] - 1])
                 for i in range(0, len(list_enum)):
                     list_enum[i].append([eleve, eleve2, eleve3])
                 enumerations.extend(list_enum)
 return enumerations

notes = ["TB", "B", "AB", "P", "I", "AR", "-1"]

def calculValeurPreferenceBinome(eleves):
    if len(eleves)<3:
        preferenceEleve1PourEleve2 = calculPoidsPreferences(getNote(preferencesE, eleve1, eleve2))
        preferenceEleve2PourEleve1 = calculPoidsPreferences(getNote(preferencesE, eleve2, eleve1))
        return preferenceEleve1PourEleve2 + preferenceEleve2PourEleve1
    else:
        preferenceEleve1PourEleve2 = calculPoidsPreferences(getNote(preferencesE, eleve1, eleve2))
        preferenceEleve2PourEleve1 = calculPoidsPreferences(getNote(preferencesE, eleve2, eleve1))
        preferenceEleve1PourEleve3 = calculPoidsPreferences(getNote(preferencesE, eleve1, eleve3))
        preferenceEleve3PourEleve1 = calculPoidsPreferences(getNote(preferencesE, eleve3, eleve1))
        preferenceEleve2PourEleve3 = calculPoidsPreferences(getNote(preferencesE, eleve2, eleve3))
        preferenceEleve3PourEleve2 = calculPoidsPreferences(getNote(preferencesE, eleve3, eleve2))
        return preferenceEleve1PourEleve2 + preferenceEleve2PourEleve1 + preferenceEleve1PourEleve3 + preferenceEleve3PourEleve1  + preferenceEleve2PourEleve3 + preferenceEleve3PourEleve2

def calculPoidsPreferences(note):
    if(note == "TB"):
        return 0
    elif(note =="B"):
        return 1
    elif(note =="AB"):
        return 2
    elif(note =="P"):
        return 3
    elif(note =="I"):
        return 4
    elif(note =="AR"):
        return 5
    else:
        print("erreur la note de l'élève n'a pas été trouvé")








def affichage2():
 eleves = {'a','b','c','d','e','f','g'}
 enum = enumerations(eleves)
 # print("il y a ",len(enum), "répartitions possibles en prenant ",len(eleves)," élèves" )
 # print()
 # print("voici les enumerations :")
 # i = 0
 # while i < len(enum) :
 #   if(i < len(enum) - 1 ) :
 #     print(i+1," : ",enum[i],' , ',i+2," : ",enum[i+1])
 #     i = i+2
 #   else :
 #     print(i+1," : ",enum[i])
 #     i = i+1
 # print()
 # print()

#affichage1()
affichage2()
