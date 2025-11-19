import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.animal import *

# Création d'un lapin
lap = Lapin((5,5),1)

def test_init():
    assert lap.get_food() == lap.PARAMETERS["foodInitLapin"]
    assert lap.get_coord() == (5,5)
    assert lap.get_id() == 1
    
def test_mange():
    initial_food = lap.get_food()
    lap.mange()
    assert lap.get_food() ==  min(
        initial_food + lap.PARAMETERS["foodHerbe"]+lap._genes[Genes.MANGE], lap.PARAMETERS["maxFoodLapin"]) + 2*lap._genes[Genes.MANGE]
    
def test_peutSeReproduire():
    # Création d'un lapin
    lap = Lapin((5,5),1)
    # Cas 1: food >= FoodReprLapin
    lap._Lapin__food = lap.PARAMETERS["foodReprodLapin"]
    # Sexe True 
    assert lap.peutSeReproduire() == True
    
    # cas 2: food < FoodReprodR
    lap._Lapin__food = Animal.PARAMETERS["foodReprodLapin"]-1 # Aleatoire moin que foodReprodLapin
    # Sexe False
    assert lap.peutSeReproduire() == False 
    
def test_vaMourir():
    
    # Quand MaxAge
    lap._Animal__age = lap.PARAMETERS["maxAge"]
    lap._Lapin__food = 5 # aleatoire plus que 0
    assert lap.vaMourir() == True
    
    # Quand food == 0
    lap._Animal__age = 3 # aleatoire moin que MaxAge
    lap._Lapin__food = 0
    assert lap.vaMourir() == True
    
def test_reduireVie():
    lap._Lapin__food = 5 #aleatoire pour test
    lap.reduireVie()
    assert lap._Lapin__food == 4 - (lap.get_genes()[Genes.ESQUIVE] * (Animal.PARAMETERS["CoeffGeneE"]/10))
    
def test__str():
    assert lap.__str__() == f"L{lap.get_id()}" 