# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import string
import pygraphviz as pgv


def trifusion(T) :
    if len(T)<=1 :
        return T
    T1=[T[x] for x in range(len(T)//2)]
    T2=[T[x] for x in range(len(T)//2,len(T))]
    return fusion(trifusion(T1),trifusion(T2))

def fusion(T1,T2) :
    if T1==[] :
        return T2
    if T2==[] :
        return T1
    if T1[0]>T2[0] :
        return [T1[0]]+fusion(T1[1 :],T2)
    else :
        return [T2[0]]+fusion(T1,T2[1 :])
    
syn = []
chaineMot=""
def possedeSynonyme(mot):
    File = open("Synonyme/thes_fr.dat",'r')
    syn = File.read().split()
    chaineMot = mot + "|1"
    if(chaineMot in syn):
        return True
    return False

def getSynonyme(mot):     
    tabMotsAssocie = []   
    for i in range(len(syn)):
        if(syn[i]==chaineMot):
            tabMotsAssocie = syn[i+1].split("|")
            del tabMotsAssocie[0]
        
    return tabMotsAssocie

"""def TreeConversion(datapath):
    tabMots = TableauMots(datapath)
    Threes = []
    for i in range(0,len(tabMots)):
        for Mots in tabMots[i]:
            Threes.append(Tree(Mots,[x for x in tabMots[i] if x not in Mots]))
            print(Threes)
"""    
dico = dict()
def Reccurence(datapath):
    File = open(datapath,'r') #ouvre le fichier contenue l'article de presse
    txt = File.read() #stocke le contenu du fichier dans "txt"
    print(txt) 
    txtLow = txt.lower();#le texte est entierement en minuscule
    res = txtLow.translate(str.maketrans("","", string.punctuation)) #enleve toutes les  ponctuations du texte
    tokenized_word = res.split() #decoupe le texte en a tableau de mots.
    
    
    stopwords_file_fr = open("StopWord/stopword_fr.txt",'r')
    stop_words_fr = stopwords_file_fr.read().split() #stocke dans une liste tous les mots francais à retirer 
    
    stopwords_file_en = open("StopWord/stopword_en.txt",'r')
    stop_words_en = stopwords_file_en.read().split() #stocke dans une liste tous les mots francais à retirer 
    tabMot1dimension = [word for word in tokenized_word if word not in stop_words_fr + stop_words_en+['«','»']] #enleve tous les mots à retirer de l'analyse
    
    for i in tabMot1dimension:
        synonymeDejaPresent = False
        if(possedeSynonyme(i)):    
            tabSyn=getSynonyme(i)                        
            for j in tabSyn:
                if(dico.get(j) and not synonymeDejaPresent):
                    dico[j]+=1
                    synonymeDejaPresent = True
        if((possedeSynonyme(i) and not synonymeDejaPresent) or not possedeSynonyme(i)):
            if(dico.get(i)):
                dico[i]+=1
            else:
                dico[i] = 1
    return dico,txt   

    

def TableauMots(texte):        
    tabPhrases = texte.split(".")    #on découpe le texte en un tableau de phrases
    tabLow =[x.lower().translate(str.maketrans("","", string.punctuation)) for x in tabPhrases] ##on enleve la ponctuation de chaque phrases      
    tokenized_word = []
    for i in range(len(tabPhrases)):   
        tokenized_word.append(tabLow[i].split())   ##on creer une liste de tous les mots pour chaque phrases
    
    stopwords_file_fr = open("StopWord/stopword_fr.txt",'r')
    stop_words_fr = stopwords_file_fr.read().split()  ## on stocke dans une liste tous les mots qu'on ne veut pas garder
    
    stopwords_file_en = open("StopWord/stopword_en.txt",'r')
    stop_words_en = stopwords_file_en.read().split()
 
    tabMots = []
    for i in range(len(tokenized_word)) :
        tabMots.append([word for word in tokenized_word[i] if word not in stop_words_fr + stop_words_en+['«','»']])   ##on elimine les mots que nous ne voulons pas garder
    return tabMots 

tableauCoocurence = dict()
def coocurence(texte):
    tabMots = TableauMots(texte)
    for k in range(len(tabMots)):
        for i in range(len(tabMots[k])):            
                for j in range (i+1,len(tabMots[k])):
                        if(tableauCoocurence.get(tabMots[k][i]+"-"+tabMots[k][j])): ##on compte le nombre d'occurence pour chaque couple de mot
                            tableauCoocurence[tabMots[k][i]+"-"+tabMots[k][j]] += 1;
                        else:
                            tableauCoocurence[tabMots[k][i]+"-"+tabMots[k][j]] = 1;
    valueCoocurence = []
    [valueCoocurence.append(x) for x in tableauCoocurence.values()] ##on recupere toutes les valeurs du dictionnaires
    print(topKPaire({},trifusion(valueCoocurence),tableauCoocurence,10,0))
    return tableauCoocurence,topKPaire({},trifusion(valueCoocurence),tableauCoocurence,10,0)

def topKPaire(topTab,tabTri,dico,k,j):
    if(j >= k):
        return topTab  
    for cle,valeur in dico.items():
        if(tabTri[j] == 1):
            return topTab
        if(valeur == tabTri[j] and not(topTab.get(cle))):
            topTab[cle] =valeur
            break;
    return topKPaire(topTab,tabTri,dico,k,j+1)

   #print(tableauCoocurence)     


    
def creerGraphe(dico,tableauCoocurence,TopKPaire,nameFile):
    graphe = pgv.AGraph()#on initialise le graphe à construire 
    for cle, valeur in dico.items():
        graphe.add_node(cle,fontsize=30*valeur) #ajoute un sommet pour chaque mot du dictionnaire et de valeur sa frequence d'apparition dans le texte
        
    for cle,valeur in tableauCoocurence.items():
        if(cle in TopKPaire):
            graphe.add_edge(cle.split('-')[0],cle.split('-')[1],color = 'red', constraint = True, penwidth =valeur)
            #ajoute un arc de couleur rouge si le couple de mot relié à cet arc figure dans le classement de la methode topKPaire
        else :
            graphe.add_edge(cle.split('-')[0],cle.split('-')[1], constraint = True, penwidth =valeur)
            #sinon ajoute un arc par defaut (de couleur noir) pour chaque couple de mot appartenant à la meme phrase. 
    graphe.layout('dot')#choisit quel programme va permettre de dessiner le graphe
    graphe.draw('Graphe/'+nameFile+'.png',prog='dot')#dessine le graphe dans un fichier png.
    graphe.close()
    
    
def traitementArticle(FileName):
    [dico,texte] = Reccurence("Article de presse/"+FileName+".txt")
    print(dico)
    [tabCooccurrence, TopKPaire] = coocurence(texte)
    print(len(tabCooccurrence), " couples.")
    creerGraphe(dico,tabCooccurrence, TopKPaire, FileName)


traitementArticle("masque coronavirus")
    
    
