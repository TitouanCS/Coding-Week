import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.gameRules import *
from source.coordonnee import *

def tests_init():
    # Paramètres principaux
    GameRules.PARAMETERS["Renards"] = 100
    GameRules.PARAMETERS["Lapins"] = 50
    GameRules.PARAMETERS["Taille"] = 20
    GameRules.PARAMETERS["Apparition herbe (%)"] = 10

    gameRules = GameRules()
    TAILLE =  GameRules.PARAMETERS["Taille"] = 20

    renardsVus = 0
    lapinVus = 0
    for i in range(TAILLE):
        for j in range(TAILLE):
            if isinstance(gameRules.get_population().getAnimauxPopulation()[gameRules.get_id(Coordonnee(i,j))],Lapin) : lapinVus +=1
            if isinstance(gameRules.get_population().getAnimauxPopulation()[gameRules.get_id(Coordonnee(i,j))],Renard) : renardsVus +=1
    
    gameRules.checkInvariant()
    
    assert lapinVus ==  GameRules.PARAMETERS["Lapins"]
    assert renardsVus == GameRules.PARAMETERS["Renards"]           
        
    assert len(gameRules.get_population().renard_coord()) == gameRules.PARAMETERS["Renards"]
    assert len(gameRules.get_population().lapin_coord()) == gameRules.PARAMETERS["Lapins"]

    assert gameRules.get_population().renard_ids() == [i for i in range(gameRules.PARAMETERS["Renards"])]
    assert gameRules.get_population().lapin_ids() == [i for i in range(gameRules.PARAMETERS["Renards"],gameRules.PARAMETERS["Lapins"]+gameRules.PARAMETERS["Renards"])]
    assert gameRules.get_population().getIdsUtilisables() == [i for i in range(gameRules.PARAMETERS["Lapins"]+gameRules.PARAMETERS["Renards"],TAILLE**2)]