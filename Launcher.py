# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 01:19:30 2020

@author: benja

objective : working version v1.0 ready on 21/04/2020
>> DONE

currrent editing version : v1.1.2
last add : automatic download

"""
import requests

import pandas as pd
from pandas.core.common import flatten
from pandas.plotting import table 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import math, random

from tkinter import *
from tkinter import ttk, Canvas, colorchooser, tix

import pygame

from PIL import Image, ImageTk #, ImageGrab

from fuzzywuzzy import process

import operator, os, threading, subprocess

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as ImReport
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


import tensorflow as tf
from learning import learn_model, build_match_features, build_database, build_all_database


#--------------------------------PROGRAMME------------------------------------#

pygame.mixer.init()

#fonctions générales

def mouseclick():
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/mouseclick.wav"))

def mouseclick2():
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/mouseclick2.wav"))

def mouseover(event):
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/mouseover.wav"))

def mouseover0():
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/mouseover.wav"))


LtoRemove = []
user = 'Profil IPSA'
def Launch():
    dfConfig = pd.read_csv("config.csv", sep = ',') 
    
    pygame.mixer.Channel(0).set_volume(1)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Main Menu.wav"), loops = -1)
    def login():
        user = cProfils.get()
        dprofil =(dfConfig[dfConfig['users']==user][['users','password']]) 
        profil = dprofil.iloc[0]['users']
        password = dprofil.iloc[0]['password']
        epassword = emdp.get()
        mouseclick2()
        if (user == profil) and (epassword == password):
            root.destroy()
            pygame.mixer.Channel(0).stop()
            analysefoot()
        else:
            llog['text']="Accès refusé"
            llog['fg'] = 'red'
    
    def loginev(event):
        login()
            
    def dynam(event):
        global user
        global macouleur
        user = cProfils.get()
        mouseover0()
        if user == 'Benjamin':
            user = 'Benjamin'
            bgROOT['image'] = launcherlfc
            leye['bg']= '#E0113A'
            Bquit['bg'] = "#E81123"
            Bquit['activebackground'] = "darkred"
        elif user == 'Louis':
            user = 'Louis'
            bgROOT['image'] = launcherpsg
            leye['bg']= '#009FBE'
            Bquit['bg'] = "#001D65"
            Bquit['activebackground'] = "#000040"
        else:
            user = 'Profil IPSA'
            bgROOT['image'] = launcherBG
            leye['bg']= '#009FBE'
            Bquit['bg'] = "#001D65"
            Bquit['activebackground'] = "#000040"
    
    def eye(event):
        if emdp['show'] == '⦁':
            mouseclick2()
            emdp['show'] = ''
        elif emdp['show'] == '':
            emdp['show'] = '⦁'
    
    def b_log(event):
        if blogin['bg'] == 'snow':
            mouseover0()
            blogin['bg'] = '#D9FFFF'
            blogin['fg'] = 'blue'
        else:
            blogin['bg'] = 'snow'
            blogin['fg'] = 'black'            

    Lprofils = ['Benjamin', 'Louis', 'Profil IPSA']
    root = Tk()
    launcherBG = PhotoImage(file = r"Images/Backgrounds/launcher.png")    
    root.geometry("600x400+600+300")
    root.title('Football Datas')
    root.iconphoto(False, PhotoImage(file='Images/icones/icone.png'))
    root.resizable(0,0)
    bgROOT = Label(root, image = launcherBG)
    bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
    
    tprofil = Text(root, width = 8, height = 1)
    tprofil.insert('1.0','Profil :')
    tprofil.place(x = 130, y = 200)
    cProfils = ttk.Combobox(root, values = Lprofils, width=32, state = 'readonly')
    cProfils.current(2)
    cProfils.bind("<<ComboboxSelected>>", dynam)
    cProfils.place(x = 200, y = 200)
    
    eyemdp = PhotoImage(file = r"Images/icones/eye.png") 
    tmdp = Text(root, width = 5, height = 1)
    tmdp.insert('1.0','Mdp :')
    tmdp.place(x = 154, y = 235)
    emdp = Entry(root, width = 35, show='⦁')
    emdp.bind("<Return>", loginev)
    emdp.place(x = 200, y = 235)
    
    blogin = Button(root, text ='Connexion', bg = 'snow',command = login, width = 12)
    blogin.place(x = 320, y = 270)
    blogin.bind("<Enter>",b_log)
    blogin.bind("<Leave>",b_log)
    
    llog = Label(root, text = 'Connexion', width = 15, bg = 'snow', fg = 'blue', relief = SUNKEN)
    llog.place(x = 489, y = 379)
    
    leye = Label(root, image = eyemdp, bg = "#009FBE")
    leye.place(x = 418, y = 233)
    leye.bind("<Enter>",eye)
    leye.bind("<Leave>",eye)
    
    Bquit = Button(root, text = "Quitter", bg = "#001D65", fg = "white", activebackground = "#000040", activeforeground = "snow" ,command = lambda:[root.destroy(), mouseclick2(),pygame.mixer.stop()])
    Bquit.place(x = 0, y = 374)
    Bquit.bind("<Enter>",mouseover)
    
    launcherlfc = PhotoImage(file = r"Images/Backgrounds/launcherlfc.png")
    launcherpsg = PhotoImage(file = r"Images/Backgrounds/launcherpsg.png")
    
    root.mainloop()
    

def analysefoot():

    dfConfig = pd.read_csv("config.csv", sep = ',') 

    config =(dfConfig[dfConfig['users']==user][['users','default_bg', 'default_jersey']])    
    # print(config)
    profil = config.iloc[0]['users']
    macouleur = config.iloc[0]['default_bg']

    #Fichiers CSV données nécessaires 
    chpnts = ['E0','E1','F1','F2','SP1', 'SP2','D1','D2','I1','I2','N1','P1','SC0','SC1', 'T1','B1','ARG','BRA','SWZ','MEX','IRL'] #Liste des championnats dont on veut récupérer les données
    Div1 = ['E0','B1','SP1','D1','N1','I1','P1','F1','T1','SC0']
    Div2 = ['E1','SP2','D2','F2','SC1','I2']    
    dict_df = {}                #initialisation du dictionnaire dataframe (panda)
    Teams = {}                  #initialisation du dictionnaire contenant tous les clubs
    color_chp = {}              #initialisation du dico pour l'attribution des couleurs selon le championnat
    joueurs = []


    Lflags = os.listdir('flags')
    Llogos = os.listdir('Ecussons')
    LlogosFIFA = os.listdir('Ecussons/Ecussons FIFA')
    LPlayers = os.listdir('images/Players')
    
    for c in chpnts:            #boucle permettant la lecture de tous les fichiers dans chpnts
        dict_df[c] = pd.read_csv(f"Data/{c}2020.csv", sep = ',') #attribution de la variable d'itération "c" à tous nos fichiers que l'on souhaite analyser (ceux du type /...2019)
        df = dict_df[c]         #simplification de la notation du dictionnaire
        Teams[c] = sorted(df['HomeTeam'].unique()) #récupération des équipes, tri alphabétique de celles-ci et regroupement des équipes itérées en une même équipe afin d'éviter la multiplicité de la même équipe


        # Attribution des couleurs des graphes par championnat
        if c == 'E0':
            color_chp[c] = 'red'
        elif c == 'E1':
            color_chp[c] = 'indianred'
        elif c == 'F1':
            color_chp[c] = 'blue'
        elif c == 'F2':
            color_chp[c] = 'dodgerblue'
        elif c == 'D1':
            color_chp[c] = 'darkgoldenrod'
        elif c == 'D2':
            color_chp[c] = 'peru'
        elif c == 'SP1':
            color_chp[c] = 'yellow'
        elif c == 'SP2':
            color_chp[c] = 'PeachPuff' 
        elif c == 'I1':
            color_chp[c] = 'green'
        elif c == 'I2':
            color_chp[c] = 'chartreuse'
        elif c == 'N1':
            color_chp[c] = 'turquoise'
        elif c == 'P1':
            color_chp[c] = 'crimson'
        elif c == 'B1':
            color_chp[c] = 'deeppink'
        elif c == 'BRA':
            color_chp[c] = 'gold'
        elif c == 'SC0':
            color_chp[c] = '#3838FF' 
        elif c == 'SC1':
             color_chp[c] = '#7171FF' 
        elif c == 'T1':
            color_chp[c] = '#E2001A'
        elif c == 'ARG':
            color_chp[c] = '#74ACDF'
        elif c == 'MEX':
            color_chp[c] = '#006845'
        elif c == 'SWZ':
            color_chp[c] = '#ED1B24'
        elif c == 'IRL':
            color_chp[c] = '#FF883E'
    
    dfPlayers   = pd.read_csv("Data/players_2020.csv", sep = ',') #Création d'un dataframe pour récupérer toutes les datas sur les joueurs provenant du jeu 'FIFA 20'
    TeamsName = dfPlayers['club'].unique() #permet de récupérer les différents noms des équipes provenant du fichier '..../players_2020.csv' car ceux-ci diffèrent des autres fichiers .csv précédents

    #Liste des Championnats disponibles
    Ligues = ["Ligue 1", "Ligue 2", "Premier League", "League Championship", "Liga BBVA", "Liga Adelante", "Serie A", "Serie B", "Bundesliga 1",
              "Bundesliga 2", "Liga Sagres", "Jupiler League", "Eredivisie", "Scottish Premier League", "Scottish First Division", "Süper Lig",
              "Brasileirão", "SuperLiga Argentina","Liga Mexico", "Super League (Suisse)","Airtricity League (Irlande)"]
    LiguesProno = ["Ligue 1", "Ligue 2", "Premier League", "League Championship", "Liga BBVA", "Liga Adelante", "Serie A", "Serie B", "Bundesliga 1",
              "Bundesliga 2", "Liga Sagres", "Jupiler League", "Eredivisie", "Scottish Premier League", "Scottish First Division", "Süper Lig"]
    
    #Liste des Options de Classement des équipes
    Options = ["Points", "Buts Pour", "Buts Contre (Best to Worst)", "Goal Average", "Victoires", "Matchs Nuls", "Défaites"]

    #------------------------Dynamique Tkinter------------------------------#
    
    def LigueGet(event):  #fonction permettant l'animation de la fenêtre tkinter (dynamique visuelle) et la sélection d'un championnat
                                #la sélection d'un championnat entraîne un changement des équipes présentes dans le volet combobox 'Sélection Equipe'
        c21.get()
        

        if c21.get() == "Ligue 1":
            championnat['text'] = 'F1'
            l20['image'] = drapeauFR
            lLigue['image'] = Ligue1
            #if son == True :
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Ligue 1 Theme.wav"))
            l10_3['text'] = "Now Playing 'Ligue 1 Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Ligue 2":
            championnat['text'] = 'F2'
            l20['image'] = drapeauFR
            lLigue['image'] = Ligue2
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Ligue 2 Theme.wav"))
            l10_3['text'] = "Now Playing 'Ligue 2 Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Premier League":
            championnat['text'] = 'E0'
            l20['image'] = drapeauEN
            lLigue['image'] = PremierLeague
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Premier League Theme.wav"))
            l10_3['text'] = "Now Playing 'Premier League Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "League Championship":
            championnat['text'] = 'E1'
            l20['image'] = drapeauEN
            lLigue['image'] = LeagueChampi
            l10_3['text'] = "No Music for League Championship"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "Liga BBVA":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Liga BBVA Theme.wav"))
            championnat['text'] = 'SP1'
            l20['image'] = drapeauES
            lLigue['image'] = LigaBBVA
            l10_3['text'] = "Now Playing 'Liga BBVA Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "Liga Adelante":
            championnat['text'] = 'SP2'
            l20['image'] = drapeauES
            lLigue['image'] = LigaAdelante
            l10_3['text'] = "No Music for Liga Adelante"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Bundesliga 1":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Bundesliga Theme.wav"))
            championnat['text'] = 'D1'
            l20['image'] = drapeauAL
            lLigue['image'] = Bundes1
            l10_3['text'] = "Now Playing 'Bundesliga Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "Bundesliga 2":
            championnat['text'] = 'D2'
            l20['image'] = drapeauAL
            lLigue['image'] = Bundes2
            l10_3['text'] = "No Music for Bundesliga 2"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Serie A":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Serie A Theme.wav"))
            championnat['text'] = 'I1'
            l20['image'] = drapeauIT
            lLigue['image'] = SerieA
            l10_3['text'] = "Now Playing 'Serie A Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL
 
        elif c21.get() == "Serie B":
            championnat['text'] = 'I2'
            l20['image'] = drapeauIT
            lLigue['image'] = SerieB
            l10_3['text'] = "No Music for Serie B"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "Eredivisie":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Eredivisie Theme.wav"))
            championnat['text'] = 'N1'
            l20['image'] = drapeauNL
            lLigue['image'] = Eredi
            l10_3['text'] = "Now Playing 'Eredivisie Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "Liga Sagres":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Liga Sagres Theme.wav"))
            championnat['text'] = 'P1'
            l20['image'] = drapeauPT
            lLigue['image'] = LigaNOS
            l10_3['text'] = "Now Playing 'Liga Sagres Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "Brasileirão":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Brasileirao Theme.wav"))
            championnat['text'] = 'BRA'
            l20['image'] = drapeauBR
            lLigue['image'] = Bras
            l10_3['text'] = "Now Playing 'Brasileirão Theme'"
            bprono['state'] = DISABLED
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Jupiler League":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Jupiler League Theme.wav"))
            championnat['text'] = 'B1'
            l20['image'] = drapeauBG
            lLigue['image'] = Jupi
            l10_3['text'] = "Now Playing 'Jupiler League Theme'"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Scottish Premier League":
            championnat['text'] = 'SC0'
            l20['image'] = drapeauSC
            lLigue['image'] = Eco1
            l10_3['text'] = "No Music for Scottish Premier League"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Scottish First Division":
            championnat['text'] = 'SC1'
            l20['image'] = drapeauSC
            lLigue['image'] = Eco2            
            l10_3['text'] = "No Music for Scottish First Division"
            bprono['state'] = DISABLED
            b91['state'] = DISABLED
            b81['state'] = DISABLED
            
        elif c21.get() == "Süper Lig":
            championnat['text'] = 'T1'
            l20['image'] = drapeauTU
            lLigue['image'] = Turq
            l10_3['text'] = "No Music for Süper Lig"
            bprono['state'] = NORMAL
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "SuperLiga Argentina":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/SuperLiga Argentina Theme.wav"))
            championnat['text'] = 'ARG'
            l20['image'] = drapeauARG
            lLigue['image'] = Arge
            l10_3['text'] = "Now Playing 'Liga Argentina Theme'"
            bprono['state'] = DISABLED
            b91['state'] = NORMAL
            b81['state'] = NORMAL
            
        elif c21.get() == "Liga Mexico":
            championnat['text'] = 'MEX'
            l20['image'] = drapeauMX
            lLigue['image'] = Mexi
            l10_3['text'] = "No Music for Liga Mexico"
            bprono['state'] = DISABLED
            b91['state'] = NORMAL
            b81['state'] = NORMAL
   
        elif c21.get() == "Super League (Suisse)":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Swiss Super League Theme.wav"))
            championnat['text'] = 'SWZ'
            l20['image'] = drapeauSU
            lLigue['image'] = Suis
            l10_3['text'] = "Now Playing 'Swiss Super League Theme'"
            bprono['state'] = DISABLED
            b91['state'] = NORMAL
            b81['state'] = NORMAL

        elif c21.get() == "Airtricity League (Irlande)":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("Musics/Themes/Airtricity League Theme.wav"))            
            championnat['text'] = 'IRL'
            l20['image'] = drapeauIRL
            lLigue['image'] = Irla
            l10_3['text'] = "Now Playing 'Airtricity League Theme'"
            bprono['state'] = DISABLED
            b91['state'] = NORMAL
            b81['state'] = NORMAL
         
        clubs = Teams[championnat['text']]
        # joueurs = 
        c71['values'] = clubs
        c71.current(0)
        
        cpt1['values'] = clubs
        cpt1.current(0)
        
        cpt2['values'] = clubs
        cpt2.current(1)        
        
        return (clubs)

    joueurs = ["-- Sélectionnez une Equipe avant --"]
    def GetPlayers(event):
        mouseclick2()
        c71.get()
        equipe = c71.get()
        joueurs = []
        tCompair = process.extractOne(equipe,TeamsName)[0]
        players = (dfPlayers[np.logical_and(dfPlayers['club']== tCompair,dfPlayers['team_position'] != 'RES')][['long_name']])

        for i in range(len(players)):
            name = players.iloc[i,:]['long_name']
            joueurs.append(name)

        c81['values'] = joueurs
        c81.current(0)

        return(players)
    
    #-------------------------------- FONCTIONS -------------------------------------#
    
    def TeamsResults(chp):
        global maxmatchs
        results = []            #initialisation de la liste contenant les données que l'on souhaite afficher en sortie
        maxmatchs=0
        nbMatchs = 0
        for t in Teams[chp]:    #itération des équipes (ici 't') par championnat (d'où la présence du paramètre 'chp')
            # print()
            # print("Saison de", t, ":")
            # print()
            
            df = dict_df[chp]   #changement du nom du paramètre du dictionnaire pour coincider avec le paramètre de fonction 'chp'
            # print(df[np.logical_or(df['HomeTeam']== t,df['AwayTeam']== t)][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR']]) #affiche les données 'Date','Time',...,'FTR' pour chaque match de l'équipe t
            
            nbMatchs = len(df[np.logical_or(df['HomeTeam']== t ,df['AwayTeam']== t)]) #calcul du nbre de matchs total joués par chaque équipe 't'en train d'être itérée
            TeamWins = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='H'),np.logical_and(df['AwayTeam']== t,df['FTR']=='A'))]) #ici le nbre de victoires pour l'équipe 't' en cours d'itération
            TeamDraws = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='D'),np.logical_and(df['AwayTeam']== t,df['FTR']=='D'))]) #idem pour les matchs nuls
            TeamLosses = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='A'),np.logical_and(df['AwayTeam']== t,df['FTR']=='H'))]) #idem pour les défaites
            
            ButsPourDomi = int(df[df['HomeTeam']== t][['FTHG']].sum())      #somme des buts marqués à domicile par l'équipe 't'
            ButsPourExte = int(df[df['AwayTeam']== t][['FTAG']].sum())      #idem pour les matchs à l'extérieur
            Buts_Pour = ButsPourDomi + ButsPourExte                         #calcul du nombre total de buts marqués
            
            ButsContreDomi = int(df[df['HomeTeam']== t][['FTAG']].sum())    #même raisonnement pour les buts encaissés
            ButsContreExte = int(df[df['AwayTeam']== t][['FTHG']].sum())
            Buts_Contre = ButsContreDomi + ButsContreExte
            
            Diff_Buts = Buts_Pour - Buts_Contre                             #calcul de la différence pour déterminer le 'Goal Average' de l'équipe 't'
            
            Points = int(TeamWins*3 + TeamDraws)                            #calcul de son nombre de points

            results.append([t,Points, nbMatchs, TeamWins, TeamDraws, TeamLosses, Buts_Pour, Buts_Contre, Diff_Buts]) #permet d'ajouter à notre liste les valeurs que l'on souhaite afficher et ce pour chaque équipe 't'

            if nbMatchs > maxmatchs:
                maxmatchs = nbMatchs

        return results          #return de la liste (ordonnée volontairement de la sorte pour l'affichage en sortie) de données de 't'
    
    
    def StatsTeam():
        global Ligue
        global nbMatchs
        global matchssavepath
        global clstsavepath
        
        mouseclick2()
        Ligue = c21.get()       #récupération du championnat sélectionné par l'utilisateur
        t = c71.get()           #récupération du nom de club sélectionné par l'utilisateur


        try :
            savepath = (f"saves/{user}")    #définition d'un chemin d'enregistrement
            os.mkdir(savepath)              #permet la création d'un nouveau répertoire si jamais nouvel utilisateur (même si non implémenté)   
        except:
            pass
             
        df = (dict_df[championnat['text']])

        if Ligue != 'Brasileirão' and Ligue != 'SuperLiga Argentina' and Ligue != 'Liga Mexico' and Ligue != 'Super League (Suisse)' and Ligue != 'Airtricity League (Irlande)':        
        #exclusion de ces championnats car absence de données dans les fichiers CSV sur 'HTR'
            dfFull = (df[np.logical_or(df['HomeTeam']== t,df['AwayTeam']== t)][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTR']]) #df correspond à notre dataframe, np.logical sont des portes logiques permettant la comparaison et/ou de données du tableau (dataframe) créé
        else:
            dfPartial = (df[np.logical_or(df['HomeTeam']== t,df['AwayTeam']== t)][['Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','FTR']])
        
        nbMatchs = len(df[np.logical_or(df['HomeTeam']== t ,df['AwayTeam']== t)]) #calcul du nbre de matchs joués par une équipe en testant la présence ou non de l'équipe itérée avec les colonnes HomeTeam & AwayTeam
        TeamWins = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='H'),np.logical_and(df['AwayTeam']== t,df['FTR']=='A'))])
        TeamDraws = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='D'),np.logical_and(df['AwayTeam']== t,df['FTR']=='D'))])
        TeamLosses = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['FTR']=='A'),np.logical_and(df['AwayTeam']== t,df['FTR']=='H'))])
        
        if Ligue != 'Brasileirão' and Ligue != 'SuperLiga Argentina' and Ligue != 'Liga Mexico' and Ligue != 'Super League (Suisse)' and Ligue != 'Airtricity League (Irlande)':            #exclusion de ces championnats car absence de données dans les fichiers CSV sur 'HTR'
            TeamHTWins = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['HTR']=='H'),np.logical_and(df['AwayTeam']== t,df['HTR']=='A'))])
            TeamHTDraws = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['HTR']=='D'),np.logical_and(df['AwayTeam']== t,df['HTR']=='D'))])
            TeamHTLosses = len(df[np.logical_or(np.logical_and(df['HomeTeam']== t,df['HTR']=='A'),np.logical_and(df['AwayTeam']== t,df['HTR']=='H'))])
            
            ShotsHome = int(df[df['HomeTeam']== t][['HS']].sum())
            ShotsAway = int(df[df['AwayTeam']== t][['AS']].sum())
            ShotsHomeTarg = int(df[df['HomeTeam']== t][['HST']].sum())
            ShotsAwayTarg = int(df[df['AwayTeam']== t][['AST']].sum())
            
            ShotsTot = ShotsHome + ShotsAway
            ShotsTargTot = ShotsHomeTarg + ShotsAwayTarg
            probTarget = ShotsTargTot/ShotsTot
            offTarget = (1 - probTarget)
            
            moyTarget = probTarget*100
            MoyOffTarget = (offTarget*100)


            def newpoint_ON():
                return np.random.randint(175,1000), np.random.randint(86, 350)
                                      #(min_x, max_x)              #(min_y, max_y)
            
            pointsOn = (newpoint_ON() for p in range(int(moyTarget)))
            LonTarget = []
            for point in pointsOn:
               LonTarget.append(point)
            # print(LonTarget)
            zip(*LonTarget)

            def newpoint_OFF():
                # nboffpoint =0
                
                offpoint = np.random.randint(10,1170), np.random.randint(10, 350)
                if (offpoint[0]<165) or (offpoint[0]>1015) or (offpoint[1]<75):
                    okpoint=True
                else:
                    okpoint=False
                return okpoint,offpoint

            LoffTarget = []
            nboff=0
            while nboff<int(MoyOffTarget):
                okpoint, offpoint = newpoint_OFF()
                if okpoint:
                    nboff+=1
                    LoffTarget.append(offpoint)
                    
       
            img = plt.imread("Images/Backgrounds/ShotsRatioBG.png")
            x = 1183
            y = 467
            plt.figure(figsize=(12, 12))
            fig, ax = plt.subplots()
            ax.imshow(img)
            plt.scatter(*zip(*LonTarget), c = '#99CC00')
            plt.scatter(*zip(*LoffTarget), c = '#FF4B4B')
            plt.xlim(right=x)
            plt.xlim(left=0)
            plt.ylim(top=0)
            plt.ylim(bottom=y)
            plt.axis('off')
            plt.title(f'Ratio de tirs cadrés de {t}')
            
            ratiosavepath = f"{savepath}/ratio{t}.png"
            plt.savefig(ratiosavepath, transparent=True, dpi = 128)
            plt.close()
            LtoRemove.append(ratiosavepath)
            
        ButsPourDomi = int(df[df['HomeTeam']== t][['FTHG']].sum())          #somme des buts marqués à domicile
        ButsPourExte = int(df[df['AwayTeam']== t][['FTAG']].sum())
        Buts_Pour = ButsPourDomi + ButsPourExte                             #somme des buts marqués total
        
        ButsContreDomi = int(df[df['HomeTeam']== t][['FTAG']].sum())
        ButsContreExte = int(df[df['AwayTeam']== t][['FTHG']].sum())
        Buts_Contre = ButsContreDomi + ButsContreExte
        
        Diff_Buts = Buts_Pour - Buts_Contre
        
        Points = int(TeamWins*3 + TeamDraws)                                #calcul des points total (1 victoire = 3pts, 1 match nul = 1pt, 1 défaite = 0 pt)

        classement, taillechp = Classementdefault()
        
        #-------------Affichage des résultats------------#

        
        Mpourcentage = [TeamWins, TeamLosses, TeamDraws]
        labels = 'Victoires', 'Défaites', 'Matchs Nuls'
        colors = ['#00FFFF','#0000FF', '#3366FF']
        explode = (0.15, 0, 0)
        plt.pie(Mpourcentage, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=165)
        plt.title("Statistiques de " + t)
        plt.legend(labels, title="Résultats", loc="center right", bbox_to_anchor = (1.15, 0.4))
        plotsavepath = f"{savepath}/plot{t}.png"
        plt.savefig(plotsavepath)
        # plt.show()
        plt.close()
        LtoRemove.append(plotsavepath)
        
        fig, ax = plt.subplots(figsize=(22, ((nbMatchs+4)/3))) # set size frame
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
        if Ligue != 'Brasileirão' and Ligue != 'SuperLiga Argentina' and Ligue != 'Liga Mexico' and Ligue != 'Super League (Suisse)' and Ligue != 'Airtricity League (Irlande)':
            tabla = table(ax, dfFull, loc='upper center', colWidths=[0.10225]*len(dfFull.columns))
        else:
            tabla = table(ax, dfPartial, loc='upper center', colWidths=[0.10225]*len(dfPartial.columns))
        tabla.auto_set_font_size(False) # Activate set fontsize manually
        tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
        tabla.scale(1.4, 1.8) # change size table
        matchssavepath = f"{savepath}/stats{t}.png"
        plt.savefig(matchssavepath, transparent=True)
        plt.close()
        LtoRemove.append(matchssavepath)

        fig, ax2 = plt.subplots(figsize=(20, taillechp/3.5)) # set size frame
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.set_frame_on(False)
        cellcol=[['#FFCC99' if classement['TEAM'].iloc[i]==t else 'white' for j in range(len(classement.columns))] for i in range(taillechp)]
        clst = table(ax2, classement, loc='upper center', colWidths=[0.1]*len(classement.columns),cellColours=cellcol)
        clst.auto_set_font_size(False)
        clst.set_fontsize(12)
        clst.scale(1.25, 1.3)
        clstsavepath = f"{savepath}/classement{t}.png"
        plt.savefig(clstsavepath, transparent=True)
        plt.close()
        LtoRemove.append(clstsavepath)

        #REPORTLAB
        doctitle = ("Statistiques de " +t)
        doc = SimpleDocTemplate(f"{savepath}/{doctitle}.pdf",pagesize=letter,rightMargin=72,leftMargin=72,topMargin=18,bottomMargin=18)
        Story=[]
        
        logo = process.extractOne(t, Llogos)[0]
        imlogo = (f'Ecussons/{logo}')
        im = ImReport(imlogo, 1.5*inch, 1.5*inch)
        Story.append(im)
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        Story.append(Spacer(1, 24))
        ptext = f'<font size="18"> Statistiques du club de {t} après {nbMatchs} journées :</font>'
        story_style = styles["Justify"]
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 32))
        ptext = '<font size="16">------------------- Statistiques à la Fin des Matchs -------------------</font>'
        story_style = styles["Justify"]
        story_style.alignment = 1
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 20))
        
        ptext = (f'<font size="12">{t} a gagné {TeamWins} matchs soit {(TeamWins/nbMatchs)*100.:.2f}% de victoires.<br/>\
                {t} a fait {TeamDraws} matchs nuls soit {(TeamDraws/nbMatchs)*100.:.2f}% de matchs nuls.<br/>\
                {t} a perdu {TeamLosses} matchs soit {(TeamLosses/nbMatchs)*100.:.2f}% de défaites.<br/><br/>\
                {t} a marqué {Buts_Pour} buts depuis le début de saison.<br/>\
                {t} a concédé {Buts_Contre} buts depuis le début de saison.<br/>\
                {t} a ainsi une différence de {Diff_Buts} buts depuis le début de saison.<br/><br/>\
                {t} a une moyenne de {(Buts_Pour/nbMatchs):.1f} buts marqués par match.<br/>\
                {t} a une moyenne de {(Buts_Contre/nbMatchs):.1f} buts concédés par match.</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))

        if Ligue != 'Brasileirão' and Ligue != 'SuperLiga Argentina' and Ligue != 'Liga Mexico' and Ligue != 'Super League (Suisse)' and Ligue != 'Airtricity League (Irlande)':
            msgb = messagebox.askquestion("Autres Stats", f"Souhaitez-vous enregistrer des statistiques plus complètes concernant {t} ?\n\nVous aurez notamment accès aux stats suivantes :\nStats Mi-Temps, Buts par Match, Scores, Stats Tirs par Match")
            if msgb == 'yes':
                Story.append(Spacer(1, 24))
                ptext = '<font size="16">-------------- Statistiques à la Mi-Temps des Matchs --------------</font>'
                story_style = styles["Justify"]
                story_style.alignment = 1
                Story.append(Paragraph(ptext, story_style))
                Story.append(Spacer(1, 20))
                ptext = (f'<font size="12">{t} a mené lors de {TeamHTWins} rencontres soit {(TeamHTWins/nbMatchs)*100.:.2f} % de victoires à la pause.<br/>\
                {t} faisait match nul {TeamHTDraws} fois soit {(TeamHTDraws/nbMatchs)*100.:.2f} % de matchs nuls à la pause.<br/>\
                {t} a été menée {TeamHTLosses} fois soit {(TeamHTLosses/nbMatchs)*100.:.2f} % de défaites à la pause.<br/></font>')
                Story.append(Paragraph(ptext, styles["Normal"]))
    
                Story.append(Spacer(1, 24))
                ptext = '<font size="16">------------------------------- Autres Stats -------------------------------</font>'
                story_style = styles["Justify"]
                story_style.alignment = 1
                Story.append(Paragraph(ptext, story_style))
                Story.append(Spacer(1, 20))
                ptext = (f'<font size="12">{t} tire en moyenne {(ShotsTot/nbMatchs):.1f} fois au but par match.<br/>\
                {t} cadre en moyenne {(ShotsTargTot/nbMatchs):.1f} tirs par match.<br/>\
                {t} cadre donc {(probTarget)*100:.1f}% de ses tirs.<br/>\
                {t} marque sur {(Buts_Pour/ShotsTot)*100:.1f}% de ses tirs et {(Buts_Pour/ShotsTargTot)*100:.1f}% de ses tirs cadrés.</font>')
                Story.append(Paragraph(ptext, styles["Normal"]))

        Story.append(Spacer(1, 24))
        ptext = '<font size="16">------------------------------- Bilan Points -------------------------------</font>'
        story_style = styles["Justify"]
        story_style.alignment = 1
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 20))
        ptext = (f'<font size="12">{t} a ainsi un total de {Points} Points après {nbMatchs} matchs.<br/>\
        Soit une moyenne {(Points/nbMatchs):.2f} points pris par match pour {t}.</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        if Points/nbMatchs < 0.9:
            text = "Le bilan est très insuffisant. La situation est alarmante."
        elif Points/nbMatchs >= 0.9 and Points/nbMatchs < 1.15:
            text = "Le bilan est insuffisant. Attention à ne pas sombrer."
        elif Points/nbMatchs >= 1.15 and Points/nbMatchs < 1.48:
            text = "Le bilan est mitigé. Il faut encore faire des efforts."
        elif Points/nbMatchs >= 1.48 and Points/nbMatchs < 1.68:
            text = "Le bilan est globalement satisfaisant. Bonnes performances."
        elif Points/nbMatchs >= 1.68 and Points/nbMatchs < 2:
            text = "Le bilan est très satisfaisant. Il faut continuer ainsi."
        else:
            text = "Le bilan est excellent. Félicitations."
        ptext = (f'<font size="12">{text}</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 30))        
        ptext = ('<font size="10">Données extraites grâce à FOOTBALL DATAS<br/>\
            Base de données provenant de : https://www.football-data.co.uk/</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(PageBreak())
        
        Story.append(Spacer(1, 10))
        ptext = f'<font size="16">Matchs joués par {t}</font>'
        story_style = styles["Justify"]
        story_style.alignment = 1
        Story.append(Paragraph(ptext, story_style))
        Story.append(Spacer(1, 6))
        im = ImReport(matchssavepath, 9*inch ,6*inch)
        Story.append(im)
        # Story.append(Spacer(1, 6))
        # im = ImReport(plotsavepath,2.75*inch ,2.75*inch)
        # Story.append(im)
        
        Story.append(Spacer(1, 10))        
        ptext = ('<font size="10">Données extraites grâce à FOOTBALL DATAS<br/>\
            Base de données provenant de : https://www.football-data.co.uk/</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(PageBreak())

        Story.append(Spacer(1, 78))
        ptext = f'<font size="14">Classement de {t} en {Ligue}</font>'
        story_style = styles["Justify"]
        story_style.alignment = 1
        Story.append(Paragraph(ptext, story_style))
        im = ImReport(clstsavepath, 9*inch ,6*inch)
        Story.append(im)
        Story.append(Spacer(1, 10))        
        ptext = ('<font size="10">Données extraites grâce à FOOTBALL DATAS<br/>\
            Base de données provenant de : https://www.football-data.co.uk/</font>')
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(PageBreak())
        
        if Ligue != 'Brasileirão' and Ligue != 'SuperLiga Argentina' and Ligue != 'Liga Mexico' and Ligue != 'Super League (Suisse)' and Ligue != 'Airtricity League (Irlande)':
            Story.append(Spacer(1, 24))
            im = ImReport(ratiosavepath, 9*inch ,6*inch)
            Story.append(im)

            Story.append(Spacer(1, 2))        
            ptext = ('<font size="10">Données extraites grâce à FOOTBALL DATAS<br/>\
                Base de données provenant de : https://www.football-data.co.uk/</font>')
            Story.append(Paragraph(ptext, styles["Normal"]))

        
        doc.build(Story)
        
        subprocess.Popen([f"saves/{user}/{doctitle}.pdf"],shell=True)
        return
    
    def deleter():    
        os.remove(clstsavepath)
        os.remove(matchssavepath)
        
    def Classementdefault():
        results = TeamsResults(championnat['text'])
        sorted_teams = sorted(results, key=operator.itemgetter(1,8,6,3), reverse=True) #tri par Points (si égalité, par Goal Average et si encore égalité par Buts Pour). ordre de priorité conservé par la suite
        taillechp = len(sorted_teams)
        dftable = pd.DataFrame(sorted_teams, columns =['TEAM', 'POINTS', 'J','V','N','D','BP','BC','+/-'],index=np.arange(len(sorted_teams))+1)
        return(dftable, taillechp)

    def ClassementOptions():    #utilisation du module 'operator' pour le tri en fonction de plusieurs données (et non une pour éviter le classement automatique alphabétique qui n'est pas celui utilisé dans le football)
        mouseclick2()
        a = 0
        print(championnat['text'])
        results = TeamsResults(championnat['text'])   
        if c41.get() == "Points":
            sorted_teams = sorted(results, key=operator.itemgetter(1,8,6,3), reverse=True) #tri par Points (si égalité, par Goal Average et si encore égalité par Buts Pour). ordre de priorité conservé par la suite
            a = 1
            title = ('Points')
        elif c41.get() == "Buts Pour":
            sorted_teams = sorted(results, key=operator.itemgetter(6,1,8,3), reverse=True) #tri par Buts marqués (si égalité, par nombre de pts...)
            a = 6
            title = ('Buts Pour')
        elif c41.get() == "Buts Contre (Best to Worst)":
            sorted_teams = sorted(results, key=operator.itemgetter(7,1,8,6), reverse=False) #tri par Buts encaissés, la pire défense étant classée 20e pour cohérence avec la plupart des autres tris disponibles
            a = 7
            title = ('Buts Contre')
        elif c41.get() == "Goal Average":
            sorted_teams = sorted(results, key=operator.itemgetter(8,1,6,3), reverse=True) #tri par différence de buts (si égalité, logique précédente)
            a = 8
            title = ('Goal Average')
        elif c41.get() == "Victoires":
            sorted_teams = sorted(results, key=operator.itemgetter(3,1,8,6), reverse=True) #tri par victoires puis logique précédente
            a = 3
            title = ('Victoires')
        elif c41.get() == "Matchs Nuls":
            sorted_teams = sorted(results, key=operator.itemgetter(4,1,8,6), reverse=True) #tri par matchs nuls
            a = 4
            title = ('Matchs Nuls')
        elif c41.get() == "Défaites":
            sorted_teams = sorted(results, key=operator.itemgetter(5,1,8,6), reverse=True) #tri par défaites
            a = 5
            title = ('Défaites')
        
        Btitle = ('Affichage ' + title + ' par Equipe')
        
        print()
        print("-"*(24 - len(str(c41.get())))," CLASSEMENT ", c41.get(),"-"*(24 - len(str(c41.get()))))
        print()
        print()
        dftable = pd.DataFrame(sorted_teams, columns =['TEAM', 'POINTS', 'J','V','N','D','BP','BC','+/-'],index=np.arange(len(sorted_teams))+1)
        print(dftable)

        #Graphes du championnat en fonction du 'a' sélectionné précédemment
    
        print("-"*(53))
        plt.xticks(rotation='vertical')
        plt.title(Btitle)
        plt.bar([r[0] for r in results], [r[a] for r in results], color = color_chp[championnat['text']])
        plt.show()
        
        #ENREGiSTREMENT AU FORMAT PDF
        
        # print("Enregistrer le tableau au format pdf [y/n] ?")
        # answer = input(">> ")
        
        # if answer == 'y':

        #https://stackoverflow.com/questions/33155776/export-pandas-dataframe-into-a-pdf-file-using-python
        
        fig, rank =plt.subplots(figsize=(18,6))
        rank.axis('tight')
        rank.axis('off')
        rank.table(cellText=dftable.values,colLabels=dftable.columns,loc='center')

        try :
            savepath = (f"saves/{user}")    #déifinition d'un chemin d'enregistrement
            os.mkdir(savepath)              #permet la création d'un nouveau répertoire si jamais nouvel utilisateur (même si non implémenté)   
        except:
            pass
        
        tabletitle = ("Table"+championnat['text']+"J"+str(maxmatchs)+"RankedBy"+title)
                    #nom du fichier se lit : 'Table NomDuChampionnat NombreDeMatchsJoués ClasséPar TypeDeClassement'
        tabletitle.replace(" ", "")     #permet de combler les espaces pour avoir un nom de fichier concaténé
        tableau = PdfPages(f"{savepath}/{tabletitle}.pdf")
        tableau.savefig(fig, bbox_inches='tight')
        tableau.close()

        # print("Document enregistré !")

    def fenetre_compo():        #permet l'affichage graphique des équipes sur le terrain dans un canevas tkinter. cet affichage prend notamment en compte :
                                #la position des joueurs, leur nom, leur numéro, leur note attribuée par le jeu 'FIFA 20'. Seuls les titulaires sont utilisés
        mouseclick2()
        c71.get()
        equipe = c71.get()
        pitch = lpitch['image']
        GKjersey = PhotoImage(file = r"Images/Jerseys/Gkjersey.png")
        titre = ("Composition type de : " + equipe)
        fenetre2 = Toplevel(fenetre)
        fenetre2.title(titre)
        fenetre2.iconphoto(False, PhotoImage(file='Images/icones/footballshirt.png'))
        fenetre2.resizable(0, 0) 
        can = Canvas(fenetre2, width=877,height=641)
        can.pack()
        can.create_image(0, 0, image = pitch, anchor = NW)
        
        tCompair = process.extractOne(equipe,TeamsName)[0]
        titu =(dfPlayers[np.logical_and(dfPlayers['club']== tCompair, (np.logical_and(dfPlayers['team_position'] != 'SUB', dfPlayers['team_position'] != 'RES')))][['club','short_name', 'team_position', 'team_jersey_number','overall']])


        if equipe == "Liverpool":
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/EasterEgg/You'll Never Walk Alone.wav"))
            l10_3['text'] = "Now Playing 'You'll Never Walk Alone'"
            
            Jurgen = can.create_image(795,565, image = Klopp)
            coach = can.create_text(715,555, text = "Coach :\nJurgen Klopp", fill = "white")

        jersey = ljersey['image']        
        #POSTES
        for i in range(len(titu)):
            posit = titu.iloc[i,:]['team_position'] #le iloc permet de sélectionner la donnée sans distinction entre str(), int()...
            name = titu.iloc[i,:]['short_name']     #le [i,:] : notation pour prendre la ligne entière (et non un unique élément), avec 'i' le call du 'for i in range'
            numero = int(titu.iloc[i,:]['team_jersey_number'])
            note = ("Note", titu.iloc[i,:]['overall'])
            club = titu.iloc[i,:]['club']

            
            if posit=='GK':
                jerseyGK = can.create_image(438,575, image = GKjersey)             #l'attribution d'un nom de variable du type 'jerseyGK' est dans l'optique d'améliorations futures post-rendu du Grand Projet
                numeroGK = can.create_text(438,575,text= numero ,fill="white", font = 25)   #l'attribution d'un nom de variable du type 'numeroGK' est dans l'optique d'améliorations futures post-rendu du Grand Projet
                joueurGK = can.create_text(438,610,text= name,fill="white")                 #l'attribution d'un nom de variable du type 'joueurGK' est dans l'optique d'améliorations futures post-rendu du Grand Projet
                noteGK = can.create_text(438,625,text= note ,fill="white")                  #l'attribution d'un nom de variable du type 'noteGK' est dans l'optique d'améliorations futures post-rendu du Grand Projet
                
            elif posit == 'LB':
                jerseyLB = can.create_image(100,400,image = jersey)
                numeroLB = can.create_text(100,400,text= numero ,fill="white", font = 25)
                joueurLB = can.create_text(100,435,text= name,fill="white")
                noteLB = can.create_text(100,450,text= note ,fill="white")
                
            elif posit == 'LCB':
                jerseyLCB = can.create_image(315,460,image = jersey)
                numeroLCB = can.create_text(315,460,text= numero ,fill="white", font = 25)
                joueurLCB = can.create_text(315,495,text= name,fill="white")
                noteLCB = can.create_text(315,510,text= note ,fill="white")
                
            elif posit == 'CB':
                jerseyCB = can.create_image(437,460,image = jersey)
                numeroCB = can.create_text(437,460,text= numero ,fill="white", font = 25)
                joueurCB = can.create_text(437,495,text= name,fill="white")
                noteCB = can.create_text(437,510,text= note ,fill="white")
                
            elif posit == 'RCB':
                jerseyRCB = can.create_image(560,460,image = jersey)
                numeroRCB = can.create_text(560,460,text= numero ,fill="white", font = 25)  
                joueurRCB = can.create_text(560,495,text= name,fill="white")
                noteRCB = can.create_text(560,510,text= note ,fill="white")

            elif posit == 'RB':
                jerseyRB = can.create_image(775,400,image = jersey)
                numeroRB = can.create_text(775,400,text= numero ,fill="white", font = 25)
                joueurRB = can.create_text(775,435,text= name,fill="white")
                noteRB = can.create_text(775,450,text= note ,fill="white")
                
            elif posit == 'LDM':
                jerseyLDM = can.create_image(315,320,image = jersey)
                numeroLDM = can.create_text(315,320,text= numero ,fill="white", font = 25)
                joueurLDM = can.create_text(315,355,text= name,fill="white")
                noteLDM = can.create_text(315,370,text= note ,fill="white")

            elif posit == 'LAM':
                jerseyLAM = can.create_image(275,200,image = jersey)
                numeroLAM = can.create_text(275,200,text= numero ,fill="white", font = 25)
                joueurLAM = can.create_text(275,235,text= name,fill="white")
                noteLAM = can.create_text(275,250,text= note ,fill="white")
                
            elif posit == 'LWB':
                jerseyLWB = can.create_image(80,340,image = jersey)
                numeroLWB = can.create_text(80,340,text= numero ,fill="white", font = 25)
                joueurLWB = can.create_text(80,375,text= name,fill="white")
                noteLWB = can.create_text(80,390,text= note ,fill="white")
                
            elif posit == 'LCM':       
                jerseyLCM = can.create_image(250,245,image = jersey)
                numeroLCM = can.create_text(250,245,text= numero ,fill="white", font = 25)
                joueurLCM = can.create_text(250,280,text= name,fill="white")
                noteLCM = can.create_text(250,295,text= note ,fill="white")
                
            elif posit == 'LM':
                jerseyLM = can.create_image(100,200,image = jersey)
                numeroLM = can.create_text(100,200,text= numero ,fill="white", font = 25)
                joueurLM = can.create_text(100,235,text= name,fill="white")
                noteLM = can.create_text(100,250,text= note ,fill="white")
                
            elif posit == 'CDM':   
                jerseyCDM = can.create_image(438,280,image = jersey)
                numeroCDM = can.create_text(438,280,text= numero ,fill="white", font = 25)
                joueurCDM = can.create_text(438,315,text= name,fill="white")
                noteCDM = can.create_text(438,330,text= note ,fill="white")
                
            elif posit == 'CM':           
                jerseyCM = can.create_image(438,245,image = jersey)
                numeroCM = can.create_text(438,245,text= numero ,fill="white", font = 25)
                joueurCM = can.create_text(438,280,text= name,fill="white")
                noteCM = can.create_text(438,295,text= note ,fill="white")
                
            elif posit == 'RDM':    
                jerseyRDM = can.create_image(560,320,image = jersey)
                numeroRDM = can.create_text(560,320,text= numero ,fill="white", font = 25)
                joueurRDM = can.create_text(560,355,text= name,fill="white")
                noteRDM = can.create_text(560,370,text= note ,fill="white")

            elif posit == 'RAM':
                jerseyRAM = can.create_image(600,200,image = jersey)
                numeroRAM = can.create_text(600,200,text= numero ,fill="white", font = 25)
                joueurRAM = can.create_text(600,235,text= name,fill="white")
                noteRAM = can.create_text(600,250,text= note ,fill="white")
                
            elif posit == 'RWB':   
                jerseyRWB = can.create_image(795,340,image = jersey)
                numeroRWB = can.create_text(795,340,text= numero ,fill="white", font = 25)
                joueurRWB = can.create_text(795,375,text= name,fill="white")
                noteRWB = can.create_text(795,390,text= note ,fill="white")
                
            elif posit == 'RCM':           
                jerseyRCM = can.create_image(625,245,image = jersey)
                numeroRCM = can.create_text(625,245,text= numero ,fill="white", font = 25)
                joueurRCM = can.create_text(625,280,text= name,fill="white")
                noteRCM = can.create_text(625,295,text= note ,fill="white")
                
            elif posit == 'RM':   
                jerseyRM = can.create_image(775,200,image = jersey)
                numeroRM = can.create_text(775,200,text= numero ,fill="white", font = 25)
                joueurRM = can.create_text(775,235,text= name,fill="white")
                noteRM = can.create_text(775,250,text= note ,fill="white")
                
            elif posit == 'CAM':           
                jerseyCAM = can.create_image(438,155,image = jersey)
                numeroCAM = can.create_text(438,155,text= numero ,fill="white", font = 25)
                joueurCAM = can.create_text(438,190,text= name,fill="white")
                noteCAM = can.create_text(438,205,text= note ,fill="white")
                
            elif posit == 'LW':           
                jerseyLW = can.create_image(210,100,image = jersey)
                numeroLW = can.create_text(210,100,text= numero ,fill="white", font = 25)
                joueurLW = can.create_text(210,135,text= name,fill="white")
                noteLW = can.create_text(210,150,text= note ,fill="white")
                
            elif posit == 'CF':           
                jerseyCF = can.create_image(438,80,image = jersey)
                numeroCF = can.create_text(438,80,text= numero ,fill="white", font = 25)
                joueurCF = can.create_text(438,115,text= name,fill="white")
                noteCF = can.create_text(438,130,text= note ,fill="white")
                
            elif posit == 'LS':   
                jerseyLS = can.create_image(306,70,image = jersey)
                numeroLS = can.create_text(306,70,text= numero ,fill="white", font = 25)
                joueurLS = can.create_text(306,105,text= name,fill="white")
                noteLS = can.create_text(306,120,text= note ,fill="white")
                
            elif posit == 'ST':           
                jerseyST = can.create_image(438,60,image = jersey)
                numeroST = can.create_text(438,60,text= numero ,fill="white", font = 25)
                joueurST = can.create_text(438,95,text= name,fill="white")
                noteST = can.create_text(438,110,text= note ,fill="white")
                
            elif posit == 'RS':           
                jerseyRS = can.create_image(570,70,image = jersey)
                numeroRS = can.create_text(570,70,text= numero ,fill="white", font = 25)
                joueurRS = can.create_text(570,105,text= name,fill="white")
                noteRS = can.create_text(570,120,text= note ,fill="white")
                
            elif posit == 'RW':           
                jerseyRW = can.create_image(675,100,image = jersey)
                numeroRW = can.create_text(675,100,text= numero ,fill="white", font = 25)
                joueurRW = can.create_text(675,135,text= name,fill="white")
                noteRW = can.create_text(675,150,text= note ,fill="white")
            
            elif posit == 'RF':
                jerseyRF = can.create_image(670,110,image = jersey)
                numeroRF = can.create_text(670,110,text= numero ,fill="white", font = 25)
                joueurRF = can.create_text(670,145,text= name,fill="white")
                noteRF = can.create_text(670,160,text= note ,fill="white")
            
            elif posit == 'LF':
                jerseyLF = can.create_image(205,110,image = jersey)
                numeroLF = can.create_text(205,110,text= numero ,fill="white", font = 25)
                joueurLF = can.create_text(205,145,text= name,fill="white")
                noteLF = can.create_text(205,160,text= note ,fill="white")

            #NB : toutes les équipes ont les mêmes couleurs de maillot car pas de données sur les couleurs de maillot dans le jeu 'FIFA 20'
            # et utilisation d'une image '.png' et non d'une forme créée directement dont nous pouvons modifier les options
        
        logo = process.extractOne(club, Llogos)[0]
        imlogo = Image.open(f'Ecussons/{logo}')
        imlogo = imlogo.resize((120,120))
        imagelogo = ImageTk.PhotoImage(imlogo)
        can.create_image(780,75, image = imagelogo)
        
        fenetre2.mainloop()


    def StatsPlayers():
        mouseclick2()
        c81.get()
        joueur = c81.get()
        
        j = (dfPlayers[dfPlayers['long_name']== joueur][['long_name','short_name','age','height_cm','weight_kg','nationality','club','overall','potential','value_eur','wage_eur','preferred_foot','skill_moves','team_position','team_jersey_number','contract_valid_until','pace','shooting','passing','dribbling','defending','physic','gk_diving','gk_handling','gk_kicking','gk_reflexes','gk_speed','gk_positioning']])

        for i in range(len(j)):
            #général
            club = j.iloc[i]['club']
            lname = j.iloc[i]['long_name']
            sname = j.iloc[i]['short_name']
            posit = str(j.iloc[i]['team_position'])
            numero = str(int(j.iloc[i]['team_jersey_number']))
            age = str(j.iloc[i]['age'])
            taille = str(j.iloc[i]['height_cm'])
            poids = str(j.iloc[i]['weight_kg'])
            country = j.iloc[i]['nationality']
            pied = str(j.iloc[i]['preferred_foot'])
            
            if pied == "Left":
                bpied = "Pied Gauche"
            elif pied == "Right":
                bpied = "Pied Droit"
            else:
                bpied = "Les Deux"

            try:
                valeur = str((j.iloc[i]['value_eur'])/1000000)
                contrat = str(int(j.iloc[i]['contract_valid_until']))
            except:
                valeur = str("N/C")
                contrat = str("N/C")
            
            #stats            
            note = j.iloc[i]['overall']
            potentiel = str(int(j.iloc[i]['potential']) - int(j.iloc[i]['overall']))
            
            if posit != 'GK':
                try :
                    vitesse = int(j.iloc[i]['pace'])
                    tir = int(j.iloc[i]['shooting'])
                    passe = int(j.iloc[i]['passing'])
                    dribble = int(j.iloc[i]['dribbling'])
                    defense = int(j.iloc[i]['defending'])     
                    physique = int(j.iloc[i]['physic'])   
                except:
                    vitesse = str('N/C')
                    tir = str('N/C')
                    passe = str('N/C')
                    dribble = str('N/C')
                    defense = str('N/C')
                    physique = str ('N/C')
            else:
                try :
                    diving = int(j.iloc[i]['gk_diving'])
                    handling = int(j.iloc[i]['gk_handling'])
                    kicking = int(j.iloc[i]['gk_kicking'])
                    reflexes = int(j.iloc[i]['gk_reflexes'])
                    speed = int(j.iloc[i]['gk_speed'])
                    positioning = int(j.iloc[i]['gk_positioning'])
                except:
                    diving = str('N/C')
                    handling = str('N/C')
                    kicking = str('N/C')
                    reflexes = str('N/C')
                    speed = str('N/C')
                    positioning = str ('N/C')
        try:
            if club != 'Liverpool':
                if (note < 65) and (posit == 'GK'):
                    card = bronzecardgk
                    colo = '#4F4000'
                elif (note < 65) and (posit != 'GK'):
                    card = bronzecardj
                    colo = '#4F4000'
                elif (note >= 65 and note < 80) and (posit == 'GK'):
                    card = silvercardgk
                    colo = '#4F4000'
                elif (note >= 65 and note < 80) and (posit != 'GK'):
                    card = silvercardj
                    colo = '#4F4000'
                elif (note >= 80 and note < 90) and (posit == 'GK'):
                    card = goldcardgk
                    colo = '#4F4000'
                elif (note >= 80 and note < 90) and (posit != 'GK'):
                    card = goldcardj
                    colo = '#4F4000'
                elif (note >= 90) and (posit == 'GK'):
                    card = topcardgk
                    colo = '#B7A866'
                elif (note >= 90) and (posit != 'GK'):
                    card = topcardj
                    colo = '#B7A866'
            else:
                if posit == 'GK':
                    card = uefacardgk
                    colo = '#ADA2FD'
                else :
                    card = uefacardj
                    colo = '#ADA2FD'
        except:
            pass
            

        flag = process.extractOne(country, Lflags)[0]
        imflag = Image.open(f'flags/{flag}')
        imflag = imflag.resize((60,60))   
        imageflag = ImageTk.PhotoImage(imflag)


        nameR = process.extractOne(sname, LPlayers)[1]
        if nameR >= 90:
            Player_Name = process.extractOne(sname, LPlayers)[0]
            imPlayer = Image.open(f'Images/Players/{Player_Name}')
            imPlayer = imPlayer.resize((280,280))
            imagePlayer = ImageTk.PhotoImage(imPlayer)                

        titre = ("Statistiques de : " + joueur)
        fenetre3 = Toplevel(fenetre)
        fenetre3.title(titre)
        fenetre3.iconphoto(False, PhotoImage(file='Images/icones/icone.png'))
        fenetre3.resizable(0, 0) 
        
        can = Canvas(fenetre3, width=1280,height=877)
        can.pack()
        can.create_image(0, 0, image = bgcard, anchor = NW)
        can.create_image(955, 440, image = card)
        
        
        #---------Infos Joueur display---------#
        
        
        #-----CARD-----#
        #displaygénéral
        can.create_text(958,520,text= sname ,fill= colo, font = ("Purisa", 48))
        can.create_text(810,190,text= str(int(note)) ,fill= colo, font = ("Purisa", 48, 'bold'))
        can.create_text(810,255,text= posit ,fill= colo, font = ("Purisa", 32))
        can.create_image(810,313, image = imageflag)
        
        try:
            can.create_image(1020,325, image = imagePlayer)
        except:
            can.create_image(1020,327, image = imagedefaultplayer)
        
        try :
            logo = process.extractOne(club, LlogosFIFA)[0]
            imlogo = Image.open(f'Ecussons/Ecussons FIFA/{logo}')
            imlogo = imlogo.resize((120,120))
            imagelogo = ImageTk.PhotoImage(imlogo)
            can.create_image(811,405, image = imagelogo)
        except:
            can.create_text(805,375,text= club ,fill= colo, font = ("Purisa", 42))
        
        #displaystats

        if posit != 'GK':  
            can.create_text(805,600,text= vitesse ,fill= colo, font = ("Purisa", 32))
            can.create_text(805,649,text= tir ,fill= colo, font = ("Purisa", 32))
            can.create_text(805,698,text= passe ,fill= colo, font = ("Purisa", 32))
            can.create_text(1005,600,text= dribble ,fill= colo, font = ("Purisa", 32))
            can.create_text(1005,649,text= defense ,fill= colo, font = ("Purisa", 32))
            can.create_text(1005,698,text= physique ,fill= colo, font = ("Purisa", 32))
        else:
            can.create_text(805,600,text= diving ,fill= colo, font = ("Purisa", 32))
            can.create_text(805,649,text= handling ,fill= colo, font = ("Purisa", 32))
            can.create_text(805,698,text= kicking ,fill= colo, font = ("Purisa", 32))
            can.create_text(1005,600,text= reflexes ,fill= colo, font = ("Purisa", 32))
            can.create_text(1005,649,text= speed ,fill= colo, font = ("Purisa", 32))
            can.create_text(1005,698,text= positioning ,fill= colo, font = ("Purisa", 32))
        
        #----Fiche Joueur----#
        
        can.create_text(324, 120, text = "Fiche de : " + sname, fill="snow", font = ("Purisa", 30, 'bold'))
        can.create_text(324, 180, text = "Nationalité : " + country, fill="snow", font = ("Purisa", 20))
        can.create_text(324, 240, text = "Club Actuel : " + club, fill="snow", font = ("Purisa", 20, 'bold'))
        can.create_text(324, 300, text = "Age : " + age +" ans", fill="snow", font = ("Purisa", 20))
        can.create_text(324, 360, text = "Position : " + posit, fill="snow", font = ("Purisa", 20))
        can.create_text(324, 420, text = "Numéro en Club : " + numero, fill="snow", font = ("Purisa", 20))
        can.create_text(324, 480, text = "Bon Pied : " + bpied, fill="snow", font = ("Purisa", 20))
        can.create_text(324, 540, text = "Taille et Poids : " + taille + " cm, " + poids + " kg", fill="snow", font = ("Purisa", 20))
        can.create_text(324, 600, text = "Note Globale : " + str(int(note)) + " sur 100", fill="snow", font = ("Purisa", 20, 'bold'))
        can.create_text(324, 660, text = "Potentiel de Progression : +" + potentiel, fill="snow", font = ("Purisa", 20))
        can.create_text(324, 720, text = "Valeur Actuelle : " + valeur + " Millions €", fill="snow", font = ("Purisa", 20))
        can.create_text(324, 780, text = "Contrat expire en : " + contrat, fill="snow", font = ("Purisa", 20))

        
        fenetre3.mainloop()

    #-------------------------PRONOSTICS----------------------------#
    
    # def dataprono():
    
    #----Display Prono----#

    def pronoGUI():
        mouseclick2()

        cpt1.get()
        cpt2.get()
        Team1 = str(cpt1.get())
        Team2 = str(cpt2.get())
        
        if Team1 != Team2:
            try:
                path = os.path.dirname(os.path.abspath(__file__))
                model = tf.keras.models.load_model(os.path.join(path,"models/all_model.h5"))
                # model.summary()
                probability_model = tf.keras.Sequential([model, 
                                                            tf.keras.layers.Softmax()])

            except :
                messagebox.showwarning("Erreur", "Le modèle n'est pas disponible. Mettez à jour le modèle.")
                return
        
            
            one_input = build_match_features(championnat['text'],Team1,Team2).values
            one_prediction = probability_model.predict(one_input)
            prediction = one_prediction[0]
            P = np.array(prediction)
            best = P.argmax()
            
            if best == 0:
                probmax = f'Victoire {Team1}'
            elif best ==1:
                probmax = 'Match Nul'
            else:
                probmax = f'Victoire {Team2}'
            
            HP = prediction[0]*100
            DP = prediction[1]*100
            AP = prediction[2]*100
            # print(HP, DP, AP)            
            
            tCompair = process.extractOne(Team1,TeamsName)[0]
            tituT1 =(dfPlayers[np.logical_and(dfPlayers['club']== tCompair, (np.logical_and(dfPlayers['team_position'] != 'SUB', dfPlayers['team_position'] != 'RES')))][['club','short_name', 'team_position', 'team_jersey_number']])
    
            tCompair = process.extractOne(Team2,TeamsName)[0]
            tituT2 =(dfPlayers[np.logical_and(dfPlayers['club']== tCompair, (np.logical_and(dfPlayers['team_position'] != 'SUB', dfPlayers['team_position'] != 'RES')))][['club','short_name', 'team_position', 'team_jersey_number']])
        
            titre = ("Pronostic de : " + Team1 + " vs " + Team2)
            fenetre4 = Toplevel(fenetre)
            fenetre4.title(titre)
            fenetre4.iconphoto(False, PhotoImage(file='Images/icones/icone.png'))
            fenetre4.resizable(0, 0) 
            
            can = Canvas(fenetre4, width=1280,height=877)
            can.pack()
            can.create_image(0, 0, image = lterrain['image'], anchor = NW)

            logoT1 = process.extractOne(Team1, Llogos)[0]
            imlogoT1 = Image.open(f'Ecussons/{logoT1}')
            imlogoT1 = imlogoT1.resize((175,175))
            imagelogoT1 = ImageTk.PhotoImage(imlogoT1)
            can.create_image(105,100, image = imagelogoT1)

            logoT2 = process.extractOne(Team2, Llogos)[0]
            imlogoT2 = Image.open(f'Ecussons/{logoT2}')
            imlogoT2 = imlogoT2.resize((175,175))
            imagelogoT2 = ImageTk.PhotoImage(imlogoT2)
            can.create_image(1175,100, image = imagelogoT2)
            
            jerseyR1 = process.extractOne(Team1, Dicjerseypro.keys())[1]
            if jerseyR1 >= 90:
                jerseyN1 = process.extractOne(Team1, Dicjerseypro.keys())[0]
                jersey = Dicjerseypro[jerseyN1]
            else:
                jersey = random.choice(Ljersey)
            jerseyR2 = process.extractOne(Team2, Dicjerseypro.keys())[1]
            if jerseyR2 >= 90:
                jerseyN2 = process.extractOne(Team2, Dicjerseypro.keys())[0]
                jersey2 = Dicjerseypro[jerseyN2]
            else:
                jersey2 = random.choice(Ljersey)
                
            while jersey == jersey2:
                jersey2 = random.choice(Ljersey)
                
            GKjersey = random.choice(LjerseyGK)
            GKjersey2 = random.choice(LjerseyGK)
            
            while GKjersey == GKjersey2 :
                GKjersey2 = random.choice(LjerseyGK)
            
            for i in range(len(tituT1)):
                posit = tituT1.iloc[i,:]['team_position']
                name = tituT1.iloc[i,:]['short_name']
            
                if posit == 'GK':
                    jerseyGK = can.create_image(65,425, image = GKjersey)
                    joueurGK = can.create_text(65,460,text= name,fill="white")
                    
                elif posit == 'LB':
                    jerseyLB = can.create_image(250,120,image = jersey)
                    joueurLB = can.create_text(250,155,text= name,fill="white")
                    
                elif posit == 'LCB':
                    jerseyLCB = can.create_image(170,300,image = jersey)
                    joueurLCB = can.create_text(170,335,text= name,fill="white")
                    
                elif posit == 'CB':
                    jerseyCB = can.create_image(170,430,image = jersey)
                    joueurCB = can.create_text(170,465,text= name,fill="white")
                    
                elif posit == 'RCB':
                    jerseyRCB = can.create_image(170,560,image = jersey)
                    joueurRCB = can.create_text(170,595,text= name,fill="white")
    
                elif posit == 'RB':
                    jerseyRB = can.create_image(250,740,image = jersey)
                    joueurRB = can.create_text(250,775,text= name,fill="white")
                    
                elif posit == 'LDM':
                    jerseyLDM = can.create_image(350,250,image = jersey)
                    joueurLDM = can.create_text(350,285,text= name,fill="white")
    
                elif posit == 'LAM':
                    jerseyLAM = can.create_image(430,200,image = jersey)
                    joueurLAM = can.create_text(430,235,text= name,fill="white")
                    
                elif posit == 'LWB':
                    jerseyLWB = can.create_image(280,100,image = jersey)
                    joueurLWB = can.create_text(280,135,text= name,fill="white")
                    
                elif posit == 'LCM':
                    jerseyLCM = can.create_image(370,290,image = jersey)
                    joueurLCM = can.create_text(370,325,text= name,fill="white")
                    
                elif posit == 'LM':
                    jerseyLM = can.create_image(435,205,image = jersey)
                    joueurLM = can.create_text(435,240,text= name,fill="white")
                    
                elif posit == 'CDM':   
                    jerseyCDM = can.create_image(310,430,image = jersey)
                    joueurCDM = can.create_text(310,465,text= name,fill="white")
                    
                elif posit == 'CM':           
                    jerseyCM = can.create_image(380,430,image = jersey)
                    joueurCM = can.create_text(380,465,text= name,fill="white")
                    
                elif posit == 'RDM':    
                    jerseyRDM = can.create_image(350,627,image = jersey)
                    joueurRDM = can.create_text(350,662,text= name,fill="white")
    
                elif posit == 'RAM':
                    jerseyRAM = can.create_image(430,670,image = jersey)
                    joueurRAM = can.create_text(430,705,text= name,fill="white")
                    
                elif posit == 'RWB':   
                    jerseyRWB = can.create_image(280,777,image = jersey)
                    joueurRWB = can.create_text(280,812,text= name,fill="white")
                    
                elif posit == 'RCM':           
                    jerseyRCM = can.create_image(370,570,image = jersey)
                    joueurRCM = can.create_text(370,605,text= name,fill="white")
                    
                elif posit == 'RM':
                    jerseyRM = can.create_image(435,665,image = jersey)
                    joueurRM = can.create_text(435,700,text= name,fill="white")
                    
                elif posit == 'CAM':      
                    jerseyCAM = can.create_image(440,430,image = jersey)
                    joueurCAM = can.create_text(440,465,text= name,fill="white")
                    
                elif posit == 'LW':           
                    jerseyLW = can.create_image(500,180,image = jersey)
                    joueurLW = can.create_text(500,215,text= name,fill="white")
                    
                elif posit == 'CF':           
                    jerseyCF = can.create_image(545,430,image = jersey)
                    joueurCF = can.create_text(545,465,text= name,fill="white")
                    
                elif posit == 'LS':   
                    jerseyLS = can.create_image(555,250,image = jersey)
                    joueurLS = can.create_text(555,285,text= name,fill="white")
                    
                elif posit == 'ST':           
                    jerseyST = can.create_image(600,430,image = jersey)
                    joueurST = can.create_text(600,465,text= name,fill="white")
                    
                elif posit == 'RS':           
                    jerseyRS = can.create_image(555,620,image = jersey)
                    joueurRS = can.create_text(555,655,text= name,fill="white")
                    
                elif posit == 'RW':           
                    jerseyRW = can.create_image(500,697,image = jersey)
                    joueurRW = can.create_text(500,732,text= name,fill="white")
                
                elif posit == 'RF': ##
                    jerseyRF = can.create_image(525,265,image = jersey)
                    joueurRF = can.create_text(525,300,text= name,fill="white")
                
                elif posit == 'LF': ##
                    jerseyLF = can.create_image(525,605,image = jersey)
                    joueurLF = can.create_text(525,640,text= name,fill="white")
            
        
        
            for i in range(len(tituT2)):
                posit = tituT2.iloc[i,:]['team_position']
                name = tituT2.iloc[i,:]['short_name']
                
                if posit == 'GK':
                    jerseyGK = can.create_image(1280-65,425, image = GKjersey2)
                    joueurGK = can.create_text(1280-65,460,text= name,fill="white")
                    
                elif posit == 'LB':
                    jerseyLB = can.create_image(1280-250,740,image = jersey2)
                    joueurLB = can.create_text(1280-250,775,text= name,fill="white")
                    
                elif posit == 'LCB':
                    jerseyLCB = can.create_image(1280-170,560,image = jersey2)
                    joueurLCB = can.create_text(1280-170,595,text= name,fill="white")
                    
                elif posit == 'CB':
                    jerseyCB = can.create_image(1280-170,430,image = jersey2)
                    joueurCB = can.create_text(1280-170,465,text= name,fill="white")
                    
                elif posit == 'RCB':
                    jerseyRCB = can.create_image(1280-170,310,image = jersey2)
                    joueurRCB = can.create_text(1280-170,345,text= name,fill="white")
    
                elif posit == 'RB':
                    jerseyRB = can.create_image(1280-250,120,image = jersey2)
                    joueurRB = can.create_text(1280-250,155,text= name,fill="white")
                    
                elif posit == 'LDM':
                    jerseyLDM = can.create_image(1280-350,627,image = jersey2)
                    joueurLDM = can.create_text(1280-350,662,text= name,fill="white")
    
                elif posit == 'LAM':
                    jerseyLAM = can.create_image(1280-430,670,image = jersey2)
                    joueurLAM = can.create_text(1280-430,705,text= name,fill="white")
                    
                elif posit == 'LWB':
                    jerseyLWB = can.create_image(1280-280,777,image = jersey2)
                    joueurLWB = can.create_text(1280-280,812,text= name,fill="white")
                    
                elif posit == 'LCM':
                    jerseyLCM = can.create_image(1280-370,290,image = jersey2)
                    joueurLCM = can.create_text(1280-370,325,text= name,fill="white")
                    
                elif posit == 'LM':
                    jerseyLM = can.create_image(1280-435,665,image = jersey2)
                    joueurLM = can.create_text(1280-435,700,text= name,fill="white")
                    
                elif posit == 'CDM':   
                    jerseyCDM = can.create_image(1280-310,430,image = jersey2)
                    joueurCDM = can.create_text(1280-310,465,text= name,fill="white")
                    
                elif posit == 'CM':           
                    jerseyCM = can.create_image(1280-380,430,image = jersey2)
                    joueurCM = can.create_text(1280-380,465,text= name,fill="white")
                    
                elif posit == 'RDM':    
                    jerseyRDM = can.create_image(1280-350,250,image = jersey2)
                    joueurRDM = can.create_text(1280-350,285,text= name,fill="white")
    
                elif posit == 'RAM':
                    jerseyRAM = can.create_image(1280-430,200,image = jersey2)
                    joueurRAM = can.create_text(1280-430,235,text= name,fill="white")
                    
                elif posit == 'RWB':   
                    jerseyRWB = can.create_image(1280-280,100,image = jersey2)
                    joueurRWB = can.create_text(1280-280,135,text= name,fill="white")
                    
                elif posit == 'RCM':           
                    jerseyRCM = can.create_image(1280-370,570,image = jersey2)
                    joueurRCM = can.create_text(1280-370,605,text= name,fill="white")
                    
                elif posit == 'RM':
                    jerseyRM = can.create_image(1280-435,205,image = jersey2)
                    joueurRM = can.create_text(1280-435,240,text= name,fill="white")
                    
                elif posit == 'CAM':      
                    jerseyCAM = can.create_image(1280-440,430,image = jersey2)
                    joueurCAM = can.create_text(1280-440,465,text= name,fill="white")
                    
                elif posit == 'LW':           
                    jerseyLW = can.create_image(1280-500,690,image = jersey2)
                    joueurLW = can.create_text(1280-500,725,text= name,fill="white")
                    
                elif posit == 'CF':           
                    jerseyCF = can.create_image(735,430,image = jersey2)
                    joueurCF = can.create_text(735,465,text= name,fill="white")
                    
                elif posit == 'LS':   
                    jerseyLS = can.create_image(1280-555,620,image = jersey2)
                    joueurLS = can.create_text(1280-555,655,text= name,fill="white")
                    
                elif posit == 'ST':           
                    jerseyST = can.create_image(1280-600,430,image = jersey2)
                    joueurST = can.create_text(1280-600,465,text= name,fill="white")
                    
                elif posit == 'RS':           
                    jerseyRS = can.create_image(1280-555,250,image = jersey2)
                    joueurRS = can.create_text(1280-555,285,text= name,fill="white")
                    
                elif posit == 'RW':           
                    jerseyRW = can.create_image(1280-500,180,image = jersey2)
                    joueurRW = can.create_text(1280-500,215,text= name,fill="white")
                
                elif posit == 'RF':
                    jerseyRF = can.create_image(1280-525,605,image = jersey2)
                    joueurRF = can.create_text(1280-525,640,text= name,fill="white")
                
                elif posit == 'LF':
                    jerseyLF = can.create_image(1280-525,265,image = jersey2)
                    joueurLF = can.create_text(1280-525,300,text= name,fill="white")
            
            # can.create_text(350,70,text= Team1 ,fill= 'snow', font = ("Purisa", 32))
            # can.create_text(950,70,text= Team2 ,fill= 'snow', font = ("Purisa", 32))

            can.create_image(630, 430, image = pronoBG)
                                 #x0,   y0,   x1, y1
            can.create_rectangle(400, 600, 440, 600 - HP*6, fill = '#99CC00')
            can.create_text(420,620, text = f"{HP:.2f}%")
            
            can.create_rectangle(620, 600, 660, 600 - DP*6, fill = '#FF9900')
            can.create_text(640,620, text = f"{DP:.2f}%")
            
            can.create_rectangle(840, 600, 880, 600 - AP*6, fill = '#FF3800')
            can.create_text(860,620, text = f"{AP:.2f}%")
            
            can.create_text(630,250,text= 'Résultat le plus probable :', fill = 'snow',font = ("Purisa", 24))
            can.create_text(630,300,text= probmax, fill = macouleur,font = ("Purisa", 36, 'bold'))
            
            fenetre4.mainloop()

        else:
            err = messagebox.showerror("Selections Invalides","Veuillez sélectionner deux équipes différentes pour pronostiquer.")
            if err == 'ok':
                mouseclick2()
    
    def randomteams():
        mouseclick2()
        clubs = Teams[championnat['text']]
        R1 = random.randint(0, len(clubs)-1)
        R2 = random.randint(0, len(clubs)-1)
        while R1 == R2:
            R2 = random.randint(0, len(clubs)-1)
        cpt1.current(R1)
        cpt2.current(R2)
    
    #--------------------SIMULATION CHAMPIONNAT-----------------------#
        
    def selectrank(event):
        poidsrank['text'] = (vr.get())/10
    def selectnote(event):
        poidsnote['text'] = (vn.get())/10        

    def simulation():
        mouseclick2()
        poidsrank.get()
        poidsnote.get()
        pr = float(poidsrank['text'])
        pn = float(poidsnote['text'])
        
        if (pr == 0 and pn == 0):
            messagebox.showerror("Poids Invalides","Veuillez mettre au moins l'une des deux valeurs à 1.")
            
        else:
            # HIGHER RATED TEAM
            higher = 1.148698355
            # LOWER RATED TEAM
            lower = 0.8705505633
            
            
            #Définition de la class Team
            class Team:
                def __init__(self, name, skill):
                    self.name = name
                    self.skill = skill
                    self.points = self.gf = self.ga = self.wins = self.draws = self.losses = 0
            
                def add_goals(self, goals):
                    self.gf += goals
            
            chp = championnat['text'] #récupération du championnat
            
            # Récupération des équipes et attribution d'un Team Skill
            teams = [] #initialisation de la liste qui va récupérer les noms et les skills
            results = TeamsResults(chp)   #appel de la fonction TeamsResults(chp)
            sorted_teams = sorted(results, key=operator.itemgetter(1,8,6,3)) #classement des équipes de la dernière à la première
            sorted_names = [t[0] for t in sorted_teams] #ou list(map(list, zip(*sorted_teams)))[0] #transformation sous forme de liste en ne gardant que le nom de l'équipe
    
            for t in Teams[chp]:
    
                tCompair = process.extractOne(t,TeamsName)[0]
                titu =(dfPlayers[np.logical_and(dfPlayers['club']== tCompair, (np.logical_and(dfPlayers['team_position'] != 'SUB', dfPlayers['team_position'] != 'RES')))][['club','overall']])
                note=titu['overall'].mean() #moyenne de tous les joueurs titulaires
                teams.append(Team(t, sorted_names.index(t)*pr+note*pn)) #rajout dans la liste teams les objets "Team"
    
            # système aléatoire pour les buts à domicile
            def home_score(home, away):
                homeSkill = home.skill / 3
                awaySkill = away.skill / 3
            
                if homeSkill == awaySkill:
                    raise ValueError
            
                if homeSkill > awaySkill:
                    homeGoals = 0
                    lambHome = higher ** (homeSkill - awaySkill)
                    z = random.random()
                    while z > 0:
                        z = z - (((lambHome ** homeGoals) * math.exp(-1 * lambHome)) /
                                 math.factorial(homeGoals))
                        homeGoals += 1
                    return (homeGoals - 1)
            
                if homeSkill < awaySkill:
                    homeGoals = 0
                    lambHome = higher ** (homeSkill - awaySkill)
                    z = random.random()
                    while z > 0:
                        z = z - (((lambHome ** homeGoals) * math.exp(-1 * lambHome)) /
                                 math.factorial(homeGoals))
                        homeGoals += 1
            
                    return (homeGoals - 1)
            
            #idem pour les buts à l'extérieur
            def away_score(home, away):
                homeSkill = home.skill / 3
                awaySkill = away.skill / 3
            
                if homeSkill == awaySkill:
                    return "Teams cannot play themselves!!!"
            
                if awaySkill > homeSkill:
                    awayGoals = 0
                    lambAway = lower ** (homeSkill - awaySkill)
                    x = random.random()
                    while x > 0:
                       x = x - (((lambAway ** awayGoals) * math.exp(-1 * lambAway)) /
                                math.factorial(awayGoals))
                       awayGoals += 1
                    return (awayGoals - 1)
            
                if awaySkill < homeSkill:
                    awayGoals = 0
                    lambAway = lower ** (homeSkill - awaySkill)
                    x = random.random()
                    while x > 0:
                       x = x - (((lambAway ** awayGoals) * math.exp(-1 * lambAway)) /
                                math.factorial(awayGoals))
                       awayGoals += 1
                    return (awayGoals - 1)
            
            # Taille de la ligue et paramétrage de la ligue 
            league_size = len(Teams[chp])
            POINTS = []
            BUTS_POUR = []
            BUTS_CONTRE = []
            VICS =[]
            NULS = []
            LOSSES = []
    
            for x in range(league_size):
                POINTS += [0]
                BUTS_POUR += [0]
                BUTS_CONTRE += [0]
                VICS += [0]
                NULS += [0]
                LOSSES += [0]
            
            # Rencontres entre équipes et MAJ des stats
            for x in range(league_size):
                print("========================================")
                print(teams[x].name + " à domicile : ")
                print("========================================")
                for y in range(league_size):
                    error = 0
                    try:
                        homeScore = home_score(teams[x], teams[y])
                    except ValueError:
                        pass
                        error += 1
                    try:
                        awayScore = away_score(teams[x], teams[y])
                    except ValueError:
                        pass
                    if error == 0:
                        print(teams[x].name, homeScore, ":", awayScore, teams[y].name)
                        BUTS_POUR[x] += homeScore
                        BUTS_POUR[y] += awayScore
                        BUTS_CONTRE[x] += awayScore
                        BUTS_CONTRE[y] += homeScore
                        if homeScore > awayScore:
                            VICS[x] += 1
                            LOSSES[y] += 1
                            POINTS[x] += 3
                        elif homeScore == awayScore:
                            NULS[x] += 1
                            NULS[y] += 1
                            POINTS[x] += 1
                            POINTS[y] += 1
                        else:
                            VICS[y] += 1
                            LOSSES[x] += 1
                            POINTS[y] += 3
                    else:
                        pass
            
            # ASSIGNEMENT DES STATISTIQUES A CHAQUE EQUIPE
            for x in range(league_size):
                teams[x].points = POINTS[x]
                teams[x].bp = BUTS_POUR[x]
                teams[x].bc = BUTS_CONTRE[x]
                teams[x].vics = VICS[x]
                teams[x].nuls = NULS[x]
                teams[x].losses = LOSSES[x]
                teams[x].db = BUTS_POUR[x] - BUTS_CONTRE[x]
            
            sorted_teams = sorted(teams, key=lambda t: (t.points,t.db, t.bp), reverse=True) #originalement seul t.points comptait
    
            # AFFICHAGE FINAL
            position = 0
            print()
            print("| Pos |          EQUIPE           | POINTS |  Vi  | NULS  | LOSSES | BUTS POUR |  BUTS CONTRE  |  Diff  |")
            resultats = {}
            for team in sorted_teams:
                
                resultats.update({team.name : [team.losses, team.nuls, team.vics]})
                
                position = position +1
                print("|", position," "*(2-len(str(position))), "|",team.name," "*(24 - len(team.name)),"|  ",team.points," "*(3 - len(str(team.points))),"| ",team.vics," "*(2 - len(str(team.vics))),"|  ",
                      team.nuls," "*(2 - len(str(team.nuls))),"|  ",team.losses," "*(3 - len(str(team.losses))),"|    ",team.bp," "*(4 - len(str(team.bp))),"|     ",
                      team.bc," "*(7 - len(str(team.bc))),"|  ", team.db, " "*(3 - len(str(team.db))), "|")
            print('\nPoids Classement Actuel :', pr, '| Poids Niveau Joueurs FIFA 20 :', pn)            
            whistle()
 
            resultats_names = ['Défaites', 'Nuls', 'Victoires']
            labels = list(resultats.keys())
            data = np.array(list(resultats.values()))
            data_cum = data.cumsum(axis=1)
            degrade_colors = ['red', 'orange', 'chartreuse']
            
            """
            Les lignes qui suivent ont en partie été comprises, mais pas en intégralité.
            Le code qui suit a en partie été extrait d'un example trouvé sur matplotlib
            qui a été modifié pour supporter notre simulation. Nous essayons au mieux
            d'interpréter et de nous approprier chaque ligne qui n'est pas originale.
            """
            
            fig, ax = plt.subplots(figsize=(10, 7.5))
            ax.invert_yaxis()
            ax.xaxis.set_visible(False)
            ax.set_xlim(0, np.sum(data, axis=1).max())
        
            for i, (colname, color) in enumerate(zip(resultats_names, degrade_colors)):
                widths = data[:, i]
                starts = data_cum[:, i] - widths
                ax.barh(labels, widths, left=starts, height=0.75,label=colname, color=color)
                xcenters = starts + widths / 2
                
                for y, (x, c) in enumerate(zip(xcenters, widths)):
                    ax.text(x, y, str(int(c)), ha='center', va='center', color= 'snow', weight = 'bold')
            ax.legend(ncol=len(resultats_names), bbox_to_anchor=(0, 1),loc='lower left', fontsize='14')
            plt.title("Classement avec détails des résultats", pad = 45)
            plt.show()
    
    #------------------------Fonctions Supplémentaires------------------------------#

    def Aide():                 #fonction permettant d'aider l'utilisateur dans la compréhension de chaque onglet du programme
        mouseclick()
        MsgBoxHelp = messagebox.askokcancel("Aide", "Choisis une section et regarde les options\n\nTu peux afficher les STATS de ton équipe préférée,\nPRONOSTIQUER un résultat ou SIMULER une ligue !")
        if MsgBoxHelp == True :
            mouseclick()
            MsgBoxHelp2 = messagebox.askokcancel('Aide Stats&Co',"Dans 'Stats & Co', tu as accès aux statistiques des équipes.\n\nIl te suffir de chosir un CHAMPIONNAT pour avoir accès à son CLASSEMENT. Sélectionne un CLUB pour afficher sa COMPOSITION classique, ou simplement voir ses STATS.")
            if MsgBoxHelp2 == True:
                mouseclick()
                MsgBoxHelp3 = messagebox.askokcancel('Aide Pronostics',"Dans 'Pronostics', tu peux sélectionner une équipe\net regarder nos conseils pour tes prochains PARIS (€) !")
                if MsgBoxHelp3 == True :
                    mouseclick()
                    MsgBoxHelp4 = messagebox.askokcancel('Aide Simulation', "Dans 'Simulation Championnat', tu peux simuler une saison entière d'un championnat en définissant tes propres paramètres de simulation !\n\nNB : Le poids du rang provient du classement réel actuel, le poids du niveau provient des notes des joueurs dans FIFA 20.\nSi les 2 paramètres sont à 0 le championnat est nul.")
                    if MsgBoxHelp4 == True:
                        mouseclick()
                        messagebox.showinfo('Fin Aide', "Tu peux désormais naviguer entre les différents onglets. Amuses toi bien !")
                        
    def ExitApplication():      #fonction permettant la fermeture de l'application avec confirmation de l'utilisateur. Le choix de redémarrer la musique du menu au début est volontaire.
        notif()
        MsgBox = messagebox.askquestion ('Exit Application',"Etes-vous sûr de vouloir quitter l'application ?", icon = 'warning', default = 'no', parent = fenetre)
        
        if MsgBox == 'yes':
            pygame.mixer.stop()
            cMusique.current(1)
            fenetre.destroy() #supprime les fichiers temporaires du répertoire saves
            for r in LtoRemove:
                os.remove(r)
        else:
            mouseclick()
            music()
    
    #-------- PARAMETRES INTERFACE --------#
    def param():
        global ROOTparam
        mouseclick2()
        titre = ("Paramètres")
        ROOTparam = Toplevel(fenetre)
        ROOTparam.title(titre)
        ROOTparam.iconphoto(False, PhotoImage(file='Images/icones/param.png'))
        x = fenetre.winfo_x()
        y = fenetre.winfo_y()
        ROOTparam.geometry("500x300+%d+%d" % (x + 200, y + 150))
        bgROOT = Label(ROOTparam, image= paramBG)
        bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
        ROOTparam.resizable(0, 0)
        
        BLook = Button(ROOTparam, text = "Modifier les Couleurs", command = Look, width = 30)
        BLook.place(x = 140, y = 20)
        Bjerseys = Button(ROOTparam, text = "Changer de Maillot", command = jerseys, width = 30)
        Bjerseys.place(x = 140, y = 50)
        Btheme = Button(ROOTparam, text = "Thème Spécial", command = theme, width = 30)
        Btheme.place(x = 140, y = 80)
        BReset = Button(ROOTparam, text = "Reset", command = Reset, width = 30)
        BReset.place(x = 140, y = 160)
        
        blearning = Button(ROOTparam, text = "Datas & Deep Learning", command = learning, width = 30)
        blearning.place(x = 140, y = 190)
        
        bcredits = Button(ROOTparam, text = "Crédits", command = creditsm, width = 30)
        bcredits.place(x = 140, y = 220)
        
        bpassword = Button(ROOTparam, text = "Reset Password", bg = 'darkgrey', command = resetpass, width = 30)
        bpassword.place(x = 140, y = 250)
        
        Bquit = Button(ROOTparam, text = "Retour", bg = "#E81123", fg = "white", activebackground = "darkred", activeforeground = "white" ,command = lambda:[ROOTparam.destroy(), mouseclick2()])
        Bquit.place(x = 0, y = 274)

        bal1 = tix.Balloon(ROOTparam,initwait=1000, bg = 'white')
        bal1.bind_widget(BLook, balloonmsg="Permet de changer la couleur des Widgets")
        for sub in bal1.subwidgets_all():
            sub.config(bg='white')

        bal2 = tix.Balloon(ROOTparam,initwait=1000, bg = 'white')
        bal2.bind_widget(Bjerseys, balloonmsg="Permet de changer le maillot utilisé dans 'Composition Type'")
        for sub in bal2.subwidgets_all():
            sub.config(bg='white')
            
        bal3 = tix.Balloon(ROOTparam,initwait=1000, bg = 'white')
        bal3.bind_widget(Btheme, balloonmsg="Permet de choisir un thème différent")
        for sub in bal3.subwidgets_all():
            sub.config(bg='white')
            
        bal4 = tix.Balloon(ROOTparam,initwait=1000, bg = 'white')
        bal4.bind_widget(BReset, balloonmsg="Permet de réinitialiser les paramètres")
        for sub in bal4.subwidgets_all():
            sub.config(bg='white')

        bal5 = tix.Balloon(ROOTparam,initwait=1000, bg = 'white')
        bal5.bind_widget(blearning, balloonmsg="Permet de modifier les fichiers.\nAttention, les actions sont irréversibles.")
        for sub in bal5.subwidgets_all():
            sub.config(bg='white')
            
        bal6 = tix.Balloon(ROOTparam,initwait=1000, bg = 'white')
        bal6.bind_widget(bcredits, balloonmsg="Permet d'afficher les musiques disponibles")
        for sub in bal6.subwidgets_all():
            sub.config(bg='white')
            
        bal7 = tix.Balloon(ROOTparam,initwait=1000, bg = 'white')
        bal7.bind_widget(bpassword, balloonmsg="Permet de réinitaliser le mot de passe")
        for sub in bal7.subwidgets_all():
            sub.config(bg='white')

        ROOTparam.attributes('-topmost', 'true')
        ROOTparam.mainloop()


    def color():
        colorbg = ccolor.get()
        colorfg = ctcolor.get()
        
        LLB = [l11, l31, b51, l61, b71, l81, b81, b91, lpt1, lpt2, bprono, brandomteams, l15, l35, b55]
        for LB in LLB:
            LB['bg'] = colorbg
            LB['fg'] = colorfg


    def Look():
        global ROOTlook
        def mycolor():
            #E0113A
            mouseclick2()
            couleur = colorchooser.askcolor(l11['bg'], parent = ROOTlook, title = "My Color")
            try:
                RVB, colorbg = couleur
                colorbg = colorbg.upper()
                dfConfig.loc[dfConfig["users"]== profil, "default_bg"] = colorbg
                dfConfig.to_csv("config.csv", index=False)
                msg = messagebox.showinfo('Redémarrage',"Changement de couleur sauvegardé. L'application va redémarrer  pour que ce dernier soit effectif.", parent = ROOTlook)
                fenetre.destroy()
                for r in LtoRemove:
                    os.remove(r)
                Launch()
            except:
                pass
            
        mouseclick2()
        ROOTlook = Toplevel(fenetre)
        ROOTlook.title("Couleurs")
        ROOTlook.iconphoto(False, PhotoImage(file='Images/icones/param.png'))
        ROOTlook.geometry("520x300")
        bgROOT = Label(ROOTlook, image= lookBG)
        bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
        ROOTlook.resizable(0, 0)
        
        bblack = Button(ROOTlook, bg = 'black', activebackground = 'black', command = lambda:[ccolor.current(1), ctcolor.current(0), color()], width = 10, height = 2)
        bblack.place(x = 20, y = 20)
        bdarkgrey = Button(ROOTlook, bg = '#333333', activebackground = '#333333', command = lambda:[ccolor.current(2), ctcolor.current(0),color()], width = 10, height = 2)
        bdarkgrey.place(x = 100, y = 20)
        bbleu1 = Button(ROOTlook, bg = '#333399', activebackground = '#333399', command = lambda:[ccolor.current(3), ctcolor.current(0),color()], width = 10, height = 2)
        bbleu1.place(x = 340, y = 20)        
        bbleu2 = Button(ROOTlook, bg = '#003366', activebackground = '#003366', command = lambda:[ccolor.current(4), ctcolor.current(0),color()], width = 10, height = 2)
        bbleu2.place(x = 260, y = 20)
        bbleu3 = Button(ROOTlook, bg = '#006B6B', activebackground = '#006B6B', command = lambda:[ccolor.current(5), ctcolor.current(0), color()], width = 10, height = 2)
        bbleu3.place(x = 180, y = 20)
        bvert1 = Button(ROOTlook, bg = '#008000', activebackground = '#008000', command = lambda:[ccolor.current(6), ctcolor.current(0),color()], width = 10, height = 2)
        bvert1.place(x = 20, y = 60)
        bvert2 = Button(ROOTlook, bg = '#99CC00', activebackground = '#99CC00', command = lambda:[ccolor.current(7), ctcolor.current(0),color()], width = 10, height = 2)
        bvert2.place(x = 100, y = 60)        
        bjaune = Button(ROOTlook, bg = '#FFFF00', activebackground = '#FFFF00', command = lambda:[ccolor.current(8), ctcolor.current(2),color()], width = 10, height = 2)
        bjaune.place(x = 20, y = 100)
        borange0 = Button(ROOTlook, bg = '#FFCC00', activebackground = '#FFCC00', command = lambda:[ccolor.current(9), ctcolor.current(2),color()], width = 10, height = 2)
        borange0.place(x = 100, y = 100)        
        borange1 = Button(ROOTlook, bg = '#FF9900', activebackground = '#FF9900', command = lambda:[ccolor.current(10), ctcolor.current(0),color()], width = 10, height = 2)
        borange1.place(x = 180, y = 100)
        borange2 = Button(ROOTlook, bg = '#FF6600', activebackground = '#FF6600', command = lambda:[ccolor.current(11), ctcolor.current(0),color()], width = 10, height = 2)
        borange2.place(x = 260, y = 100)        
        bmarron = Button(ROOTlook, bg = '#993300', activebackground = '#993300', command = lambda:[ccolor.current(12), ctcolor.current(0),color()], width = 10, height = 2)
        bmarron.place(x = 20, y = 140)
        bbrown = Button(ROOTlook, bg = '#800000', activebackground = '#800000', command = lambda:[ccolor.current(13), ctcolor.current(0),color()], width = 10, height = 2)
        bbrown.place(x = 100, y = 140)        
        brouge = Button(ROOTlook, bg = '#FF0000', activebackground = '#FF0000', command = lambda:[ccolor.current(14), ctcolor.current(0),color()], width = 10, height = 2)
        brouge.place(x = 20, y = 180)
        bfuscia = Button(ROOTlook, bg = '#FF00FF', activebackground = '#FF00FF', command = lambda:[ccolor.current(15), ctcolor.current(0),color()], width = 10, height = 2)
        bfuscia.place(x = 180, y = 180)        
        brose = Button(ROOTlook, bg = '#FF99CC', activebackground = '#FF99CC', command = lambda:[ccolor.current(16), ctcolor.current(0),color()], width = 10, height = 2)
        brose.place(x = 100, y = 180)
        bbeige = Button(ROOTlook, bg = '#FFCC99', activebackground = '#FFCC99', command = lambda:[ccolor.current(17), ctcolor.current(1),color()], width = 10, height = 2)
        bbeige.place(x = 340, y = 100)        
        bjaunepale = Button(ROOTlook, bg = '#FFFF99', activebackground = '#FFFF99', command = lambda:[ccolor.current(18), ctcolor.current(2),color()], width = 10, height = 2)
        bjaunepale.place(x = 420, y = 140)
        bvertpale = Button(ROOTlook, bg = '#CCFFCC', activebackground = '#CCFFCC', command = lambda:[ccolor.current(19), ctcolor.current(1),color()], width = 10, height = 2)
        bvertpale.place(x = 180, y = 60)        
        bbleupale = Button(ROOTlook, bg = '#CCFFFF', activebackground = '#CCFFFF', command = lambda:[ccolor.current(20), ctcolor.current(1),color()], width = 10, height = 2)
        bbleupale.place(x = 260, y = 60)
        bbleuciel = Button(ROOTlook, bg = '#99CCFF', activebackground = '#99CCFF', command = lambda:[ccolor.current(21), ctcolor.current(0),color()], width = 10, height = 2)
        bbleuciel.place(x = 340, y = 60)        
        bturquoise = Button(ROOTlook, bg = '#00CCFF', activebackground = '#00CCFF', command = lambda:[ccolor.current(22), ctcolor.current(0),color()], width = 10, height = 2)
        bturquoise.place(x = 420, y = 60)
        bbleu0 = Button(ROOTlook, bg = '#3366FF', activebackground = '#3366FF', command = lambda:[ccolor.current(23), ctcolor.current(0),color()], width = 10, height = 2)
        bbleu0.place(x = 420, y = 20)        
        bmauve = Button(ROOTlook, bg = '#CC99FF', activebackground = '#CC99FF', command = lambda:[ccolor.current(24), ctcolor.current(0),color()], width = 10, height = 2)
        bmauve.place(x = 340, y = 140)
        bblanc = Button(ROOTlook, bg = '#FFFFFF', activebackground = '#FFFFFF', command = lambda:[ccolor.current(25), ctcolor.current(2),color()], width = 10, height = 2)
        bblanc.place(x = 420, y = 100)        
        bpourpre = Button(ROOTlook, bg = '#993366', activebackground = '#993366', command = lambda:[ccolor.current(26), ctcolor.current(0),color()], width = 10, height = 2)
        bpourpre.place(x = 180, y = 140)
        bviolet = Button(ROOTlook, bg = '#800080', activebackground = '#800080', command = lambda:[ccolor.current(27), ctcolor.current(0),color()], width = 10, height = 2)
        bviolet.place(x = 260, y = 140)        
        bgold = Button(ROOTlook, bg = '#BDAB6D', activebackground = '#BDAB6D', command = lambda:[ccolor.current(28), ctcolor.current(0),color()], width = 10, height = 2)
        bgold.place(x = 260, y = 180)
        
        bdefault = Button(ROOTlook, text = "default", bg = 'darkgrey', activebackground = 'darkgrey', command = lambda:[ccolor.current(29), ctcolor.current(0),color()], width = 10, height = 2)
        bdefault.place(x = 420, y = 180)
        
        bmycolor = Button(ROOTlook, text = "My Color", command = lambda:[mycolor()], bg = l11['bg'], activebackground = 'darkgrey', width = 10, height = 2)
        bmycolor.place(x = 340, y = 180)

        Bquit = Button(ROOTlook, text = "Retour", bg = "#E81123", fg = "white", activebackground = "darkred", activeforeground = "white" ,command = lambda:[ROOTlook.destroy(), mouseclick2()])
        Bquit.place(x = 0, y = 274)
        
        ROOTlook.attributes('-topmost', 'true')
        ROOTlook.mainloop()

    def jerseyswitch():
        myjersey = cJC.get()
        ljersey['image'] = myjersey
        
    def jerseys():
        mouseclick2()
        ROOTjersey = Toplevel(fenetre)
        ROOTjersey.title("Maillot")
        ROOTjersey.iconphoto(False, PhotoImage(file='Images/icones/param.png'))
        ROOTjersey.geometry("500x300")
        bgROOT = Label(ROOTjersey, image= dressingroomBG)
        bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
        ROOTjersey.resizable(0, 0)
        
        bJ_ = Button(ROOTjersey, bg = 'black', command = lambda:[cJC.current(0),jerseyswitch(),mouseclick2()], image = jersey_)
        bJ_.place(x = 35, y = 170)
        bJA = Button(ROOTjersey, bg = 'black', command = lambda:[cJC.current(1),jerseyswitch(),mouseclick2()], image = jerseyA)
        bJA.place(x = 110, y = 170)
        bJB = Button(ROOTjersey, bg = 'black', command = lambda:[cJC.current(2),jerseyswitch(),mouseclick2()], image = jerseyB)
        bJB.place(x = 182, y = 170)
        bJC = Button(ROOTjersey, bg = 'black', command = lambda:[cJC.current(3),jerseyswitch(),mouseclick2()], image = jerseyC)
        bJC.place(x = 255, y = 170)
        bJD = Button(ROOTjersey, bg = 'black', command = lambda:[cJC.current(4),jerseyswitch(),mouseclick2()], image = jerseyD)
        bJD.place(x = 330, y = 170)
        bJE = Button(ROOTjersey, bg = 'black', command = lambda:[cJC.current(5),jerseyswitch(),mouseclick2()], image = jerseyE)
        bJE.place(x = 400, y = 170)

        Bquit = Button(ROOTjersey, text = "Retour", bg = "#E81123", fg = "white", activebackground = "darkred", activeforeground = "white" ,command = lambda:[ROOTjersey.destroy(), mouseclick2()])
        Bquit.place(x = 0, y = 274)
        
        ROOTjersey.attributes('-topmost', 'true')
        ROOTjersey.mainloop()        

    def themeswitch():
        notif()
        bgpitch = cpitch.get()
        lpitch['image'] = bgpitch
        bgterrain = cterrain.get()
        lterrain['image'] = bgterrain
        
    def theme():
        mouseclick2()
        ROOTtheme = Toplevel(fenetre)
        ROOTtheme.title("Theme")
        ROOTtheme.iconphoto(False, PhotoImage(file='Images/icones/param.png'))
        ROOTtheme.geometry("500x300")
        ROOTtheme.wm_attributes("-transparentcolor", 'grey')
        bgROOT = Label(ROOTtheme, image = paramlfcBG, bg = 'grey')
        bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
        ROOTtheme.resizable(0, 0)
        
        blfc = Button(ROOTtheme, bg = '#E0113A', activebackground = 'darkred', image = blasonlfc, command = lambda:[ cpitch.current(1), cterrain.current(1), ccolor.current(30), cJC.current(6),jerseyswitch(), color(), themeswitch(), mouseclick2(),ROOTtheme.destroy()])
        blfc.place(x = 70, y = 70)
        
        bmyt = Button(ROOTtheme, bg = 'darkblue', activebackground = '#0061B0', image = mythemeblason, command = lambda:[ cpitch.current(2), cterrain.current(2), ccolor.current(31), cJC.current(7),jerseyswitch(), color(), themeswitch(), mouseclick2(),ROOTtheme.destroy()])
        bmyt.place(x = 270, y = 70)
        ROOTtheme.attributes('-topmost', 'true')
        ROOTtheme.mainloop()

    def Reset():
        mouseclick()
        ask = messagebox.askokcancel("Reset","Etes-vous sûr de vouloir rétablir les paramètres par défaut ?", default = 'cancel', parent = ROOTparam)
        if ask == True:
            mouseclick()
            ccolor.current(29)
            ctcolor.current(0)
            cJC.current(0)
            cpitch.current(0)
            cterrain.current(0)
            color()
            jerseyswitch()
            themeswitch()

        
    def learning():
        mouseclick2()
        global ROOTlearning
        DicoLigues = {'Premier League' : 'E0', 'League Championship': 'E1', 'Scottish Premier League' :'SC0', 'Scottish First Division':'SC1', 'Ligue 1' :'F1', 'Ligue 2':'F2', 'Bundesliga 1':'D1', 'Bundesliga 2 ':'D2', 'Liga BBVA' :'SP1', 'Liga Adelante' : 'SP2', 'Serie A' :'I1', 'Serie B' : 'I2', 'Eredivisie' : 'N1', 'Liga Sagres' : 'P1', 'Jupiler League' :'B1', 'Süper Lig' : 'T1'}
        Divs = list(DicoLigues.keys())
        Ligues = DicoLigues.values()
        
        def updatemodel():
            mouseclick2()
            msg = messagebox.showinfo("En étude...","Cette option est en cours d'implémentation. Revenez bientôt pour l'utiliser.", parent = ROOTlearning)
            # msg = messagebox.askokcancel("ATTENTION","Cette action peut durer plusieurs plusieurs minutes et est irréversible", default = 'cancel',parent = ROOTlearning)
            if msg == 'ok':
                mouseclick2()
            #     ROOTlearning.destroy()
            
        def updateall():
            mouseclick2()
            msg = messagebox.askokcancel("ATTENTION","Cette action peut durer un certain temps et est irréversible", default = 'cancel', parent = ROOTlearning)
            if msg == True:
                mouseclick2()
                build_all_database(Div1, 4, .95)
                learn_model('all')

        def DataUpdate():
            for l in Ligues :
                req = requests.get(f'http://www.football-data.co.uk/mmz4281/1920/{l}.csv')
                url_content = req.content
                csv_file = open(f'Data/AllLeagues/{l}2020.csv', 'wb')
                
                csv_file.write(url_content)
                csv_file.close()
            msg = messagebox.showinfo("Redémarrage",f"Les ligues ont bien étés mises à jour. L'application va redémarrer.", parent = ROOTlearning)
            mouseclick2()
            fenetre.destroy()
            for r in LtoRemove:
                os.remove(r)
            Launch()       
        
        def LeagueUpdate():
            k = cligue.get()
            v = DicoLigues[k]
            req = requests.get(f'http://www.football-data.co.uk/mmz4281/1920/{v}.csv')
            url_content = req.content
            csv_file = open(f'Data/{v}2020.csv', 'wb')
            
            csv_file.write(url_content)
            csv_file.close()            
            msg = messagebox.showinfo("Redémarrage",f"La ligue {k} a bien été mise à jour. L'application va redémarrer.", parent = ROOTlearning)
            mouseclick2()
            fenetre.destroy()
            for r in LtoRemove:
                os.remove(r)
            Launch()       
            
        ROOTlearning = Toplevel(fenetre)
        ROOTlearning.title("Datas")
        ROOTlearning.iconphoto(False, PhotoImage(file='Images/icones/param.png'))
        ROOTlearning.geometry("800x550")
        bgROOT = Label(ROOTlearning, image = learningBG)
        bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
        ROOTlearning.resizable(0, 0)
        
        lscript = Label(ROOTlearning, bg = '#2B618F', fg = 'white', text = "Bienvenue dans le coeur du Programme !\nC'est ici que vous choisissez sur quel modèle reposent les pronostics.\nVous pouvez également mettre à jour vos fichiers (requiert internet)\nAttention, tous les championnats ne sont pas éligibles.")
        lscript.place(x =200, y = 50)

        cligue = ttk.Combobox(ROOTlearning, values = Divs, state= "readonly", width = 60)
        cligue.current(0)
        cligue.place(x=200, y=100)
        
        bupdate = Button(ROOTlearning,  text = "Update Selected Model", command = updatemodel, width = 53)
        bupdate.place(x =200, y = 150)

        bupdateall = Button(ROOTlearning, text = "Update All Models", command = updateall, width = 53)
        bupdateall.place(x =200, y = 180)
        
        bdata = Button(ROOTlearning,  text = "Update Selected League Data", command = LeagueUpdate, width = 53)
        bdata.place(x =200, y = 350)

        bdataall = Button(ROOTlearning, text = "Update All Data files", command = DataUpdate, width = 53)
        bdataall.place(x =200, y = 380)

        Bquit = Button(ROOTlearning, text = "Retour", bg = "#E81123", fg = "white", activebackground = "darkred", activeforeground = "white" ,command = lambda:[ROOTlearning.destroy(), mouseclick2()])
        Bquit.place(x = 0, y = 524)
        
        ROOTlearning.attributes('-topmost', 'true')
        ROOTlearning.mainloop()
        
    def creditsm():
        mouseclick2()
        def Atomic():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Atomic Drum Assembly - Island Life.wav"))
            l10_3['text'] = "Now Playing 'Atomic Drum Assembly - Island Life'"
            # bm1['image'] = pause
            
        def Bakermat():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Bakermat - Baiana.wav"))
            l10_3['text'] = "Now Playing 'Bakermat - Baiana'"
            # bm2['image'] = pause
            
        def Baloji():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Baloji - L'Hiver Indien.wav"))
            l10_3['text'] = "Now Playing 'Baloji - L'Hiver Indien'"
            # bm3['image'] = pause
            
        def Illenium():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Illenium - It's All On You.wav"))
            l10_3['text'] = "Now Playing 'Illenium - It's All On You'"
            # bm4['image'] = pause
            
        def MajorLazer():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Major Lazer - Que Calor.wav"))
            l10_3['text'] = "Now Playing 'Major Lazer - Que Calor'"
            # bm5['image'] = pause
            
        def PES():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/PES 2011 Soundtrack - UEFA.wav"))
            l10_3['text'] = "Now Playing 'PES 2011 Soundtrack - UEFA'"
            # bm6['image'] = pause
            
        def Mendes():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Sergio Mendes - Mas Que Nada.wav"))
            l10_3['text'] = "Now Playing 'Sergio Mendes - Mas Que Nada'"
            # bm7['image'] = pause
            
        def Selectah():
            # for b in Lb:
            #     b['image'] = play
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("Musics/Background Musics/Toy Selectah - Explotar.wav"))
            l10_3['text'] = "Now Playing 'Toy Selectah - Explotar'"
            # bm8['image'] = pause

        ROOTcredits = Toplevel(fenetre)
        ROOTcredits.title("Deep Learning")
        ROOTcredits.iconphoto(False, PhotoImage(file='Images/icones/param.png'))
        ROOTcredits.geometry("650x450")
        bgROOT = Label(ROOTcredits, image = creditsBG)
        bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
        ROOTcredits.resizable(0, 0)
        
        
        lm1 = Label(ROOTcredits, text = "Atomic Drum Assembly - Island Life", bg = '#330075', fg = 'snow', width=40, height = 2)
        lm1.place(x = 50, y = 100)
        lm2 = Label(ROOTcredits, text = "Bakermat - Baiana", bg = '#330070', fg = 'snow', width=40, height = 2)
        lm2.place(x = 50, y = 150)        
        lm3 = Label(ROOTcredits, text = "Baloji - L'Hiver Indien", bg = '#330065', fg = 'snow', width=40, height = 2)
        lm3.place(x = 50, y = 200)        
        lm4 = Label(ROOTcredits, text = "Illenium - It's All On You", bg = '#330060', fg = 'snow', width=40, height = 2)
        lm4.place(x = 50, y = 250)
        lm5 = Label(ROOTcredits, text = "Major Lazer - Que Calor", bg = '#330055', fg = 'snow', width=40, height = 2)
        lm5.place(x = 50, y = 300)
        lm6 = Label(ROOTcredits, text = "PES 2011 Soundtrack - UEFA", bg = '#330050', fg = 'snow', width=40, height = 2)
        lm6.place(x = 50, y = 350)        
        lm7 = Label(ROOTcredits, text = "Sergio Mendes - Mas Que Nada", bg = '#330045', fg = 'snow', width=40, height = 2)
        lm7.place(x = 50, y = 400)        
        lm8 = Label(ROOTcredits, text = "Toy Selectah - Explotar", bg = '#330040', fg = 'snow', width=40, height = 2)
        lm8.place(x = 50, y = 450)    
        
        bm1 = Button(ROOTcredits, bg = '#330075', image = play, command = Atomic)
        bm1.place(x = 400, y = 100)
        bm2 = Button(ROOTcredits, bg = '#330070', image = play, command = Bakermat)
        bm2.place(x = 400, y = 150)
        bm3 = Button(ROOTcredits, bg = '#330065', image = play, command = Baloji)
        bm3.place(x = 400, y = 200)
        bm4 = Button(ROOTcredits, bg = '#330060', image = play, command = Illenium)
        bm4.place(x = 400, y = 250)
        bm5 = Button(ROOTcredits, bg = '#330055', image = play, command = MajorLazer)
        bm5.place(x = 400, y = 300)
        bm6 = Button(ROOTcredits, bg = '#330050', image = play, command = PES)
        bm6.place(x = 400, y = 350)
        bm7 = Button(ROOTcredits, bg = '#330045', image = play, command = Mendes)
        bm7.place(x = 400, y = 400)
        bm8 = Button(ROOTcredits, bg = '#330040', image = play, command = Selectah)
        bm8.place(x = 400, y = 450)
        
        Lb = [bm1, bm2, bm3, bm4, bm5, bm6, bm7, bm8]
        
        Bquit = Button(ROOTcredits, text = "Retour", bg = "#E81123", fg = "white", activebackground = "darkred", activeforeground = "white" ,command = lambda:[ROOTcredits.destroy(), mouseclick2()])
        Bquit.place(x = 0, y = 424)

        ROOTcredits.attributes('-topmost', 'true')
        ROOTcredits.mainloop()


    def resetpass():
        global ROOTpass
        dprofil =(dfConfig[dfConfig['users']==user][['users','password']]) 
        profil = dprofil.iloc[0]['users']
        password = dprofil.iloc[0]['password']
            
        def newmdp():
            notif()
            oldpass = eOldPass.get()
            newpass = eNewPass.get()
            confpas = eConfirm.get()
            if oldpass == password:
                if (oldpass != newpass) and (len(newpass)>= 5):
                    if confpas == newpass:
                        dfConfig.loc[dfConfig["users"]== profil, "password"] = newpass
                        dfConfig.to_csv("config.csv", index=False)
                        msg = messagebox.askokcancel('Redémarrage',"Changement de mot de passe sauvegardé. L'application doit redémarrer pour que celui-ci soit effectif.", parent = ROOTpass)
                        fenetre.destroy()
                        for r in LtoRemove:
                            os.remove(r)
                        Launch()              
                    else:
                        messagebox.showerror("Mauvais Mot de Passe", "Veuillez rentrer le même mot de passe dans les deux entrées.", parent = ROOTpass)
                else:
                    messagebox.showerror("Nouveau Mot de Passe Incorrect", "Veuillez rentrer un mot de passe différent de l'ancien.\nLe nouveau mot de passe doit faire au minimum 5 caractères",parent = ROOTpass)
            else:
                messagebox.showerror("Mauvais Mot de Passe", "L'ancien mot de passe rentré n'est pas valide.",parent = ROOTpass)
        
        def valider(event):
            if bValid['bg'] == 'snow':
                mouseover0()
                bValid['bg'] = '#D9FFFF'
                bValid['fg'] = 'blue'
            else:
                bValid['bg'] = 'snow'
                bValid['fg'] = 'black' 
            
        mouseclick2()
        ROOTpass = Toplevel(fenetre)
        ROOTpass.title("New Password")
        ROOTpass.iconphoto(False, PhotoImage(file='Images/icones/param.png'))
        ROOTpass.geometry("650x450")
        bgROOT = Label(ROOTpass, image = passwordBG)
        bgROOT.place(x = 0, y = 0, relwidth=1, relheight=1)
        ROOTpass.resizable(0, 0)
        
        eOldPass = Entry(ROOTpass, width = 35, show='⦁')
        eOldPass.place(x = 300, y =150)

        eNewPass = Entry(ROOTpass, width = 35)
        eNewPass.place(x = 300, y =225)

        eConfirm = Entry(ROOTpass, width = 35)
        eConfirm.place(x = 300, y =300)
        
        bValid = Button(ROOTpass, text ='Confirmer Changement', bg ='snow', command = newmdp, width = 20)
        bValid.place(x = 365, y =350)
        bValid.bind("<Enter>",valider)
        bValid.bind("<Leave>",valider)
        
        tOldPass = Text(ROOTpass, width = 21, height = 1)
        tOldPass.insert('1.0','Ancien Mot de Passe :')
        tOldPass.place(x = 100, y = 150)

        tNewPass = Text(ROOTpass, width = 22, height = 1)
        tNewPass.insert('1.0','Nouveau Mot de Passe :')
        tNewPass.place(x = 100, y = 225)
        
        tConfirm = Text(ROOTpass, width = 24, height = 1)
        tConfirm.insert('1.0','Confirmer Mot de Passe :')
        tConfirm.place(x = 100, y = 300)
        
        Bquit = Button(ROOTpass, text = "Retour", bg = "#E81123", fg = "white", activebackground = "darkred", activeforeground = "white" ,command = lambda:[ROOTpass.destroy(), mouseclick2()])
        Bquit.place(x = 0, y = 424)
        
        ROOTpass.attributes('-topmost', 'true')
        ROOTpass.mainloop()

    #-----------SONS-----------#
    def ToggleSound():          #fonction permettant de désactiver le son ou de le réactiver. Cette option repose sur la gestion du volume des différents 'Channels'
        if b06['text'] == 'on':
            pygame.mixer.Channel(0).set_volume(0)
            pygame.mixer.Channel(1).set_volume(0)
            b06['image'] = SpeakerOffIcon
            b06['text'] = 'off'
            l10_3['text'] = "Music OFF"
            b06['relief'] = SUNKEN

        else:
            pygame.mixer.Channel(0).set_volume(1)
            pygame.mixer.Channel(1).set_volume(1)
            b06['image'] = SpeakerIcon
            b06['text'] = 'on'
            l10_3['text'] = "Music ON"
            b06['relief'] = FLAT


    def Erreur():               #fonction ne se déclenchant que lorsque l'utilisateur décide d'une action incohérente avec les donneés récupérées.
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/fail.wav"))
        messagebox.showinfo("Incohérence", "Attention, l'action que tu demandes\nn'est pas possible. Essaye autre chose.")
    
    def mouseoverb51(event):
        if b51['bg'] != '#E8FFFF':
            mouseover0()
            b51['bg'] = '#E8FFFF'
            b51['fg'] = 'blue'
        else:
            color()
        
    def mouseoverb55(event):
        if b55['bg'] != '#E8FFFF':
            mouseover0()
            b55['bg'] = '#E8FFFF'
            b55['fg'] = 'blue'
        else:
            color()
        
    def mouseoverb71(event):
        if b71['bg'] != '#E8FFFF':
            mouseover0()
            b71['bg'] = '#E8FFFF'
            b71['fg'] = 'blue'
        else:
            color()
        
    def mouseoverb81(event):
        if b81['bg'] != '#E8FFFF':
            mouseover0()
            b81['bg'] = '#E8FFFF'
            b81['fg'] = 'blue'
        else:
            color()
    
    def mouseoverb91(event):
        if b91['bg'] != '#E8FFFF':
            mouseover0()
            b91['bg'] = '#E8FFFF'
            b91['fg'] = 'blue'
        else:
            color()
    
    def mouseoverbrandomteams(event):
        if brandomteams['bg'] != '#E8FFFF':
            mouseover0()
            brandomteams['bg'] = '#E8FFFF'
            brandomteams['fg'] = 'blue'
        else:
            color()
    
    def mouseoverbprono(event):
        if bprono['bg'] != '#E8FFFF':
            mouseover0()
            bprono['bg'] = '#E8FFFF'
            bprono['fg'] = 'blue'
        else:
            color()
        
    def notif():
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/notif.wav"))
        
    def whistle():
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("Sounds/referee whistle.wav"))

    
    def music():
        Lsongs = ['Musics/Background Musics/Atomic Drum Assembly - Island Life.wav','Musics/Background Musics/Bakermat - Baiana.wav','Musics/Background Musics/Sergio Mendes - Mas Que Nada.wav',
                  "Musics/Background Musics/Baloji - L'Hiver Indien.wav", "Musics/Background Musics/Illenium - It's All On You.wav", "Musics/Background Musics/Major Lazer - Que Calor.wav",
                  "Musics/Background Musics/PES 2011 Soundtrack - UEFA.wav", "Musics/Background Musics/Toy Selectah - Explotar.wav"]

        song0 = random.choice(Lsongs)
        Lsongs.remove(song0)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(song0))
        songnumber = 0
        for s in Lsongs:
            songnumber = songnumber + 1
            songname = ("song"+ str(songnumber))
            songname = random.choice(Lsongs)
            Lsongs.remove(songname)
            pygame.mixer.Channel(0).queue(pygame.mixer.Sound(songname))

        l10_3['text'] = "Background Music"
                        
    def checkmusic():
        try:
            cMusique.get() 
            try:
                cMusique.get() == 'GO'
                if pygame.mixer.Channel(0).get_busy() == False and pygame.mixer.Channel(1).get_busy() == False:
                    music()   
                timer()
            except:
                pass
        except:
            pass
        
    def timer():        #Il faut qu'il accepte d'être lancé ssi fenetre est encore active         
        cMusique.get()    
        try: 
            cMusique.get() == 'GO'
            tim = threading.Timer(18.0, checkmusic)
            tim.start()
        except:
            pygame.mixer.stop()
            tim.cancel()
            
    #-------------------Coeur du Programme---------------------------------#


    #---------Fenetre & Interface Tkinter---------#

    ## A noté que nous sommes passés du .grid au .place durant la création de l'interface. Les noms ne sont plus nécessairement adéquates

    fenetre = tix.Tk()
    fenetre.title("FOOTBALL TOTAL")
    fenetre.iconphoto(False, PhotoImage(file='Images/icones/icone.png'))
    DW = int((fenetre.winfo_screenwidth())/4)
    DH = int((fenetre.winfo_screenheight())/5)
    fenetre.geometry(f"877x641+{DW}+{DH}")
    fenetre.resizable(0,0)

    #Backgrounds
    terrain = PhotoImage(file = r"Images/Backgrounds/Football_pitch.png")
    football_pitch = PhotoImage(file = r"Images/Backgrounds/footballpitch.png")
    pronoBG = ImageTk.PhotoImage(file="Images/Backgrounds/PronoBG.png")
    paramBG = PhotoImage(file = r"Images/Backgrounds/paramBG.png")
    lookBG = PhotoImage(file = r"Images/Backgrounds/lookBG.png")
    dressingroomBG = PhotoImage(file = r"Images/Backgrounds/dressing_room_BG.png")
    learningBG = PhotoImage(file = r"Images/Backgrounds/learningBG.png")
    creditsBG = PhotoImage(file = r"Images/Backgrounds/creditsBG.png")
    passwordBG =PhotoImage(file = r"Images/Backgrounds/resetpassBG.png")
    
    #---------Thèmes--------#
    
    #LFC
    blasonlfc = PhotoImage(file = r"Images/Backgrounds/themes/liverpool/Liverpool.png")
    lfcterrain = PhotoImage(file = r"Images/Backgrounds/themes/liverpool/lfcterrain.png")
    lfcpitch = PhotoImage(file = r"Images/Backgrounds/themes/liverpool/lfcpitch.png")
    paramlfcBG = PhotoImage(file = r"Images/Backgrounds/themes/liverpool/anfieldS.png")
    
    #my theme
    mythemeblason = PhotoImage(file = r"Images/Backgrounds/themes/my theme/mythemelogo.png")
    mythemeterrain = PhotoImage(file = r"Images/Backgrounds/themes/my theme/mythemeterrain.png")
    mythemepitch = PhotoImage(file = r"Images/Backgrounds/themes/my theme/mythemepitch.png")
    mythemejersey = PhotoImage(file = r"Images/Backgrounds/themes/my theme/mythemejersey.png")
    
    #-------#
    
    Lthemespitch = [football_pitch, lfcpitch, mythemepitch]    
    cpitch = ttk.Combobox(fenetre, values = Lthemespitch)
    cpitch.current(0)
    lpitch = Label(fenetre, image= football_pitch)
    lpitch.place(x = 0, y = 0, relwidth=1, relheight=1)
    
    Lthemesterrain = [terrain, lfcterrain, mythemeterrain]
    cterrain = ttk.Combobox(fenetre, values = Lthemesterrain)
    cterrain.current(0)
    lterrain = Label(fenetre, image = terrain)

    #Listes & Combobox paramètres
    Lcolors = [macouleur, "#000000", "#333333", "#333399", "#003366","#006B6B","#008000", "#99CC00", "#FFFF00", "#FFCC00", "#FF9900",
               "#FF6600", "#993300", "#800000", "#FF0000", "#FF00FF", "#FF99CC", "#FFCC99", "#FFFF99", "#CCFFCC", "#CCFFFF", "#99CCFF",
               "#00CCFF", "#3366FF", "#CC99FF", "#FFFFFF", "#993366", "#800080", "#BDAB6D","darkgrey","#E0113A", "#0061B0"]
    Ltextcolors = ["snow", "grey", "black"]    
    ccolor = ttk.Combobox(fenetre, values = Lcolors)
    ccolor.current(0) 
    ctcolor = ttk.Combobox(fenetre, values = Ltextcolors)
    ctcolor.current(0)
 
    
 
    
    ##-----------------------AFFICHAGE--------------------##
    #Boutons essentiels
    
    b10_0 = Button (fenetre, text = "Quitter", bg = "#E81123", fg = "white", activebackground = "darkred", activeforeground = "white" ,command = ExitApplication)
    b10_0.place(x=0, y=615)
    b10_6 = Button (fenetre, text = "Aide", bg = "snow", fg = "blue", activebackground = "silver", activeforeground = "navy", command = Aide)
    b10_6.place(x=842, y = 615)
    
    #Musique
    pygame.mixer.Channel(0).set_volume(1)
    pygame.mixer.Channel(1).set_volume(1) 
    
    l10_3 = Label(fenetre, text = "Background Music", bg = "#3C9C3C", fg = "white", width = 60)
    l10_3.place(x = 222, y = 615)
    
    Lcmusique = ["GO", "STOP"]
    cMusique = ttk.Combobox(fenetre, values = Lcmusique)
    cMusique.current(0)
    music()

    #Affichage initial ligue
    championnat = Label(fenetre, text = 'F1')
    
    #---------Stats & Co---------#
    l01 = Label (fenetre, text = "Stats & Co",fg = "black", width = 30, height = 2, relief = GROOVE)
    l01.place(x =50, y = 10)

    #Sélection Championnat 
    l11 = Label (fenetre, text = "Sélection Championnat", bg = macouleur,fg = "white", width = 30, height = 2)
    l11.place(x = 50, y = 60)

    c21 = ttk.Combobox(fenetre, values = Ligues, state= "readonly", width = 32)
    c21.bind("<<ComboboxSelected>>", LigueGet)
    c21.current(0)
    c21.place(x = 50, y = 98)

    #Commande Classement
    l31 = Label(fenetre, text = "Classer Par :", bg = macouleur,fg = "white", width = 30, height = 2)
    l31.place(x = 50, y = 170)

    c41 = ttk.Combobox(fenetre, values = Options, state= "readonly", width = 32)
    c41.current(0)
    c41.place(x = 50, y = 208)
    
    b51 = Button (fenetre, text = "Classement", bg = macouleur, fg = "white", activebackground = "grey", activeforeground = "snow", command = ClassementOptions, width = 29, height = 3, highlightcolor = 'snow', state = NORMAL)
    b51.place(x = 50, y = 235)
    b51.bind("<Enter>", mouseoverb51)
    b51.bind("<Leave>", mouseoverb51)


    #Commande Stats
    l61 = Label(fenetre, text = "Sélection Equipe", bg = macouleur,fg = "white", width = 30)
    l61.place(x = 50, y = 298)
    
    c71 = ttk.Combobox(fenetre, values = Teams[championnat['text']], state= "readonly", width = 32)
    c71.current(0)
    c71.bind("<<ComboboxSelected>>",GetPlayers)
    c71.place(x = 50, y = 320)
    
    b71 = Button(fenetre, text = "Stats du Club", bg = macouleur, fg = "white", activebackground = "grey", activeforeground = "snow", command = StatsTeam, width = 29, height = 3, highlightcolor = 'snow', state = NORMAL)
    b71.place(x = 50, y = 345)
    b71.bind("<Enter>", mouseoverb71)
    b71.bind("<Leave>", mouseoverb71)

    #Commande Compositions
    b91 = Button (fenetre, text = "Composition Type", command = fenetre_compo, bg = macouleur, fg = "white", width = 29, height = 3,activebackground = "grey", activeforeground = "snow")
    b91.place(x = 50, y = 405)
    b91.bind("<Enter>", mouseoverb91)
    b91.bind("<Leave>", mouseoverb91)
    

    #Commande Joueurs
    l81 = Label(fenetre, text = "Sélection Joueur", bg = macouleur,fg = "white", width = 30)
    l81.place(x = 50, y = 475)
    
    c81 = ttk.Combobox(fenetre, values = joueurs , state= "readonly", width = 32)
    c81.current(0)
    c81.place(x = 50, y = 497)
    
    b81 = Button (fenetre, text = "Fiche du Joueur", command = StatsPlayers, bg = macouleur, fg = "white", width = 29, height = 3,activebackground = "grey", activeforeground = "snow")
    b81.place(x = 50, y = 525)
    b81.bind("<Enter>", mouseoverb81)
    b81.bind("<Leave>", mouseoverb81)
    
    #---------Pronostics---------#

    l03 = Label (fenetre, text = "Pronostics", fg = "black", width = 30, height = 2, relief = GROOVE)
    l03.place(x = 332, y = 10)

    lpt1 = Label(fenetre, text = "Sélection Equipe 1", bg = macouleur,fg = "white", width = 30)
    lpt1.place(x = 332, y = 60)
    
    cpt1 = ttk.Combobox(fenetre, values = Teams[championnat['text']], state= "readonly", width = 32)
    cpt1.current(0)
    cpt1.place(x = 332, y = 80)

    lpt2 = Label(fenetre, text = "Sélection Equipe 2", bg = macouleur,fg = "white", width = 30)
    lpt2.place(x = 332, y = 110)
    
    cpt2 = ttk.Combobox(fenetre, values = Teams[championnat['text']], state= "readonly", width = 32)
    cpt2.current(1)
    cpt2.place(x = 332, y = 130)
    
    bprono = Button(fenetre, text = 'Lancer Pronostic', command = pronoGUI ,bg = macouleur, fg = "white", width = 29, height = 3,activebackground = "grey", activeforeground = "snow", state = NORMAL)
    bprono.place(x = 332, y = 220)
    if bprono['state'] == NORMAL:
        bprono.bind('<Enter>', mouseoverbprono)
        bprono.bind('<Leave>', mouseoverbprono)
        
    
    brandomteams = Button(fenetre, text = "Random Teams", command = randomteams, bg = macouleur, fg = "white", width = 15, height = 2,activebackground = "grey", activeforeground = "snow")
    brandomteams.place(x=385, y = 160)
    brandomteams.bind("<Enter>", mouseoverbrandomteams)
    brandomteams.bind("<Leave>", mouseoverbrandomteams)
    #---------Simu Premier League---------#
    
    l05 = Label (fenetre, text = "Simulation Championnat", fg = "black", width = 30, height = 2, relief = GROOVE)
    l05.place(x = 605, y = 10)
    
    l15 = Label (fenetre, text = "Poids du classement actuel :", bg = macouleur, fg = "white", activebackground = "grey", activeforeground = "snow", width = 30, height = 2)
    l15.place(x = 605, y = 60)
    
    vr = IntVar()
    vr.set('10')
    scale1 = Scale(fenetre, variable = vr, from_ =0, to = 10, orient = HORIZONTAL, len = 210)
    scale1.bind("<B1-Motion>", selectrank)
    scale1.place(x = 605, y = 90)
    
    l35 = Label (fenetre, text = "Poids du niveau des joueurs :", bg = macouleur, fg = "white", activebackground = "grey", activeforeground = "snow", width = 30, height = 2)
    l35.place(x = 605, y = 145)
    
    vn = IntVar()
    vn.set('2')
    scale2 = Scale(fenetre, variable = vn, from_ = 0, to = 10, orient = HORIZONTAL, len = 210)
    scale2.bind("<B1-Motion>", selectnote)
    scale2.place(x = 605, y = 180)
    
    poidsrank = Entry(fenetre, textvariable = "1.0")
    poidsnote = Entry(fenetre, textvariable = "0.2")
    
    b55 = Button (fenetre, text = "Lancer Simulation", command = simulation, bg = macouleur,fg = "white", activebackground = "green", activeforeground = "snow", width = 30, height = 3, highlightcolor = 'snow')
    b55.place(x = 605, y = 235)
    b55.bind("<Enter>", mouseoverb55)
    b55.bind("<Leave>", mouseoverb55)
    
    ##-----------DATA SUPPLEMENTAIRE------------------##
    
    #---------Images---------#
    
    #-----JERSEYS-----#
    
    #fictive jerseys
    jerseyGK = PhotoImage(file = r"Images/Jerseys/jerseyGK.png")
    jerseyGK2 = PhotoImage(file = r"Images/Jerseys/jerseyGK2.png")    
    
    jersey0 = PhotoImage(file = r"Images/Jerseys/jersey0.png")
    jersey1 = PhotoImage(file = r"Images/Jerseys/jersey1.png")
    jersey2 = PhotoImage(file = r"Images/Jerseys/jersey2.png")
    jersey3 = PhotoImage(file = r"Images/Jerseys/jersey3.png")
    jersey4 = PhotoImage(file = r"Images/Jerseys/jersey4.png")
    jersey5 = PhotoImage(file = r"Images/Jerseys/jersey5.png")
    jersey6 = PhotoImage(file = r"Images/Jerseys/jersey6.png")
    jersey7 = PhotoImage(file = r"Images/Jerseys/jersey7.png")
    jersey10 = PhotoImage(file = r"Images/Jerseys/jersey10.png")
    jersey11 = PhotoImage(file = r"Images/Jerseys/jersey11.png")

    #real Jerseys
    Arsenal = PhotoImage(file = r"Images/Jerseys/Pros/Arsenal.png")
    ASSE = PhotoImage(file = r"Images/Jerseys/Pros/AS Saint-Etienne.png")
    Aston_Villa = PhotoImage(file = r"Images/Jerseys/Pros/Aston Villa.png")
    Bournemouth = PhotoImage(file = r"Images/Jerseys/Pros/Bournemouth.png")
    Burnley = PhotoImage(file = r"Images/Jerseys/Pros/Burnley.png")
    Brighton = PhotoImage(file = r"Images/Jerseys/Pros/Brighton.png")
    Chelsea = PhotoImage(file = r"Images/Jerseys/Pros/Chelsea.png")
    Crystal_Palace = PhotoImage(file = r"Images/Jerseys/Pros/Crystal Palace.png")
    Everton = PhotoImage(file = r"Images/Jerseys/Pros/Everton.png")
    Leicester = PhotoImage(file = r"Images/Jerseys/Pros/Leicester.png")
    Liverpool = PhotoImage(file = r"Images/Jerseys/Pros/Liverpool.png")
    Lyon = PhotoImage(file = r"Images/Jerseys/Pros/Lyon.png")
    Man_City = PhotoImage(file = r"Images/Jerseys/Pros/Man City.png")
    Man_United = PhotoImage(file = r"Images/Jerseys/Pros/Man United.png")
    Marseille = PhotoImage(file = r"Images/Jerseys/Pros/Marseille.png")
    Newcastle = PhotoImage(file = r"Images/Jerseys/Pros/Newcastle.png")
    Norwich = PhotoImage(file = r"Images/Jerseys/Pros/Norwich.png")
    Paris_SG = PhotoImage(file = r"Images/Jerseys/Pros/Paris SG.png")
    Sheffield = PhotoImage(file = r"Images/Jerseys/Pros/Sheffield United.png")
    Southampton = PhotoImage(file = r"Images/Jerseys/Pros/Southampton.png")
    Tottenham = PhotoImage(file = r"Images/Jerseys/Pros/Tottenham.png")
    Watford = PhotoImage(file = r"Images/Jerseys/Pros/Watford.png")
    West_Ham = PhotoImage(file = r"Images/Jerseys/Pros/West Ham.png")
    Wolves = PhotoImage(file = r"Images/Jerseys/Pros/Wolves.png")

    Ljersey = [jersey0, jersey1, jersey2, jersey3, jersey4, jersey5, jersey6, jersey7, jersey10,jersey11]
    
    Dicjerseypro = {"Liverpool":Liverpool, "Chelsea":Chelsea, "Wolves" : Wolves, "Paris SG":Paris_SG, "Arsenal" : Arsenal,
                    "Crystal Palace" : Crystal_Palace, "Lyon" : Lyon, "Man City": Man_City, "Man United" : Man_United,
                    "Marseille" : Marseille, "Burnley Ham" : Burnley, "AS Saint-Etienne": ASSE, "Bournemouth" : Bournemouth,
                    "Aston Villa" : Aston_Villa, "Norwich": Norwich, "Brighton Hove Albion" : Brighton, "Newcastle": Newcastle,
                    "West Ham" : West_Ham, "Sheffield United" : Sheffield, "Watford" : Watford, "Southampton" : Southampton,
                    "Leicester" : Leicester, "Tottenham" : Tottenham, "Everton" : Everton}
    LjerseyGK = [jerseyGK, jerseyGK2]
    
    jersey_ = PhotoImage(file = r"Images/Jerseys/Compo/jersey.png")
    jerseyA = PhotoImage(file = r"Images/Jerseys/Compo/jerseyA.png")
    jerseyB = PhotoImage(file = r"Images/Jerseys/Compo/jerseyB.png")
    jerseyC = PhotoImage(file = r"Images/Jerseys/Compo/jerseyC.png")
    jerseyD = PhotoImage(file = r"Images/Jerseys/Compo/jerseyD.png")
    jerseyE = PhotoImage(file = r"Images/Jerseys/Compo/jerseyE.png")

    
    LjerseyCompo = [jersey_, jerseyA, jerseyB, jerseyC, jerseyD, jerseyE, Liverpool, mythemejersey]
    
    cJC = ttk.Combobox(fenetre, values = LjerseyCompo)
    cJC.current(0)
    
    ljersey = Label(fenetre, image = jersey_)
    
    #----Fiche Joueur-----# 
    
    bgcard = PhotoImage(file = r"Images/cards/bgcard.png")
    goldcardj = PhotoImage(file = r"Images/cards/goldcardj.png")
    goldcardgk = PhotoImage(file = r"Images/cards/goldcardgk.png")
    silvercardj = PhotoImage(file = r"Images/cards/silvercardj.png")
    silvercardgk = PhotoImage(file = r"Images/cards/silvercardgk.png")
    bronzecardj = PhotoImage(file = r"Images/cards/bronzecardj.png")
    bronzecardgk = PhotoImage(file = r"Images/cards/bronzecardgk.png")
    topcardj = PhotoImage(file = r"Images/cards/topcardj.png")
    topcardgk = PhotoImage(file = r"Images/cards/topcardgk.png")
    uefacardj = PhotoImage(file = r"Images/cards/uefacardj.png")
    uefacardgk = PhotoImage(file = r"Images/cards/uefacardgk.png")
    
    imagedefaultplayer = PhotoImage(file = r"Images/Players/defaultplayer.png")

    #---Easter Egg Liverpool---#
    Klopp = PhotoImage(file = r"Images/EasterEgg/JurgenKlopp.png")
    
    #Drapeaux
    drapeauFR = PhotoImage(file = r"Images/Drapeaux/drapeauFR2.png")
    drapeauEN = PhotoImage(file = r"Images/Drapeaux/drapeauEN2.png")
    drapeauES = PhotoImage(file = r"Images/Drapeaux/drapeauES2.png")
    drapeauAL = PhotoImage(file = r"Images/Drapeaux/drapeauAL2.png")
    drapeauIT = PhotoImage(file = r"Images/Drapeaux/drapeauIT2.png")
    drapeauNL = PhotoImage(file = r"Images/Drapeaux/drapeauNL2.png")
    drapeauPT = PhotoImage(file = r"Images/Drapeaux/drapeauPT2.png")
    drapeauBG = PhotoImage(file = r"Images/Drapeaux/drapeauBG2.png")
    drapeauBR = PhotoImage(file = r"Images/Drapeaux/drapeauBR2.png")
    drapeauSC = PhotoImage(file = r"Images/Drapeaux/drapeauSC2.png")
    drapeauTU = PhotoImage(file = r"Images/Drapeaux/drapeauTU2.png")
    drapeauARG = PhotoImage(file = r"Images/Drapeaux/drapeauARG2.png")
    drapeauMX = PhotoImage(file = r"Images/Drapeaux/drapeauMX2.png")
    drapeauIRL = PhotoImage(file = r"Images/Drapeaux/drapeauIRL2.png")
    drapeauSU = PhotoImage(file = r"Images/Drapeaux/drapeauSU2.png")
    
    l20 = Label(fenetre, image = drapeauFR)
    l20.place(x = 8, y = 100)
    
    #Logos Championnats

    Ligue1 = PhotoImage(file = r"Images/Ligues/Ligue1.png")
    Ligue2 =PhotoImage(file = r"Images/Ligues/Ligue2.png")
    PremierLeague = PhotoImage(file = r"Images/Ligues/PremierLeague.png")
    LeagueChampi = PhotoImage(file = r"Images/Ligues/LeagueChampionship.png")
    LigaBBVA = PhotoImage(file = r"Images/Ligues/LigaBBVA.png")
    LigaAdelante = PhotoImage(file = r"Images/Ligues/LigaAdelante.png")
    Bundes1 = PhotoImage(file = r"Images/Ligues/Bundes1.png")
    Bundes2 = PhotoImage(file = r"Images/Ligues/Bundes2.png")
    SerieA = PhotoImage(file = r"Images/Ligues/SerieA.png")
    SerieB = PhotoImage(file = r"Images/Ligues/SerieB.png")
    LigaNOS = PhotoImage(file = r"Images/Ligues/LigaNOS.png")
    Jupi = PhotoImage(file = r"Images/Ligues/BEL.png")
    Eredi = PhotoImage(file = r"Images/Ligues/NL1.png")
    Eco1 = PhotoImage(file = r"Images/Ligues/SC1.png")
    Eco2 = PhotoImage(file = r"Images/Ligues/SC2.png")
    Suis = PhotoImage(file = r"Images/Ligues/SWZ.png")
    Turq = PhotoImage(file = r"Images/Ligues/TUR.png")
    Bras = PhotoImage(file = r"Images/Ligues/BRA.png")
    Arge = PhotoImage(file = r"Images/Ligues/ARG.png")
    Mexi = PhotoImage(file = r"Images/Ligues/MEX.png")
    Irla = PhotoImage(file = r"Images/Ligues/IRL.png")
    
    lLigue = Label(fenetre, image = Ligue1)
    lLigue.place(x = 570, y = 300, width = "299", height = "299")  
    
    
    #Icones
    Stats = PhotoImage(file = r"Images/icones/stats.png")
    l00 = Label(fenetre, image = Stats, width = "40", height = "40")
    l00.place(x = 0, y = 10)

    Euro = PhotoImage(file = r"Images/icones/euro.png")
    l02 = Label(fenetre, bg ="#3C9C3C", image = Euro, width = "30", height = "30")
    l02.place(x = 285, y = 10)
    
    Manette = PhotoImage(file = r"Images/icones/manette.png")
    l04 = Label(fenetre,  bg ="#3C9C3C", image = Manette, width = "30", height = "30")
    l04.place(x = 560, y = 10)
    
    Cup = PhotoImage(file = r"Images/icones/cup.png")
    l50 = Label(fenetre, image = Cup, width = "40", height = "40")
    l50.place(x = 0, y = 240)
    
    PieChart = PhotoImage(file = r"Images/icones/PieChart.png")
    l80 = Label(fenetre,  bg ="#3C9C3C", image = PieChart, width = "40", height = "36")
    l80.place(x = 0, y = 355)

    CompoIcon = PhotoImage(file = r"Images/icones/compoicon.png")
    l90 = Label(fenetre,  bg ="#3C9C3C", image = CompoIcon, width = "40", height = "36")
    l90.place(x = 0, y = 415)
    
    CardIcon = PhotoImage(file = r"Images/icones/card.png")
    l90 = Label(fenetre,  bg ="#3C9C3C", image = CardIcon, width = "40", height = "40")
    l90.place(x = 0, y = 530)
    
    SpeakerIcon = PhotoImage(file = r"Images/icones/SpeakerIcon.png")
    SpeakerOffIcon = PhotoImage(file = r"Images/icones/SpeakerOffIcon.png")
    
    b06 = Button(fenetre, bg ="#3C9C3C", activebackground = "#349834", text = 'on', image = SpeakerIcon, command = ToggleSound, relief = FLAT)
    b06.place (x = 843, y = 10)

    settings = PhotoImage(file = r"Images/icones/settings.png")    
    bparam = Button(fenetre, bg ="#3C9C3C", activebackground = "#349834", image = settings, command = param, relief = FLAT)
    bparam.place (x = 843, y = 50)
    
    play = PhotoImage(file = r"Images/icones/play.png")  
    pause = PhotoImage(file = r"Images/icones/pause.png")  

    
    timer()
    fenetre.protocol("WM_DELETE_WINDOW", ExitApplication)
    fenetre.mainloop()

Launch()
