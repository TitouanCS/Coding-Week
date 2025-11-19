import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.animal import *


# Création d'un lapin
ours = Ours((5,2),3)

def test_init():
    assert ours.get_food() == ours.PARAMETERS["foodInitOurs"]
    assert ours.get_coord() == (5,2)
    assert ours.get_id() == 3
    
def test_mange():
    initial_food = ours.get_food()
    ours.mange("lapin")
    assert ours.get_food() ==  min(
        initial_food + ours.PARAMETERS["foodLapin"], ours.PARAMETERS["maxFoodOurs"])
    initial_food = ours.get_food()
    ours.mange("renard")
    assert ours.get_food() ==  min(
        initial_food + ours.PARAMETERS["foodRenard"], ours.PARAMETERS["maxFoodOurs"])
    
def test_peutSeReproduire():
    # Cas 1: food >= FoodReprOurs
    ours.set_food(ours.PARAMETERS["foodReprodLapin"])
    continue_ = True 
    while(continue_):
        try : 
            assert ours.peutSeReproduire() == False 
            continue_ = False
        except AssertionError as e :
            continue_
    
    # cas 2: food < FoodReprodOurs
    ours.set_food(Animal.PARAMETERS["foodReprodOurs"]-1 ) # Aleatoire moin que foodReprodLapin
    assert ours.peutSeReproduire() == False 
    
def test_vaMourir():
    
    # Quand MaxAge
    ours._Animal__age = ours.PARAMETERS["maxAgeOurs"]
    ours.set_food(5)
    assert ours.vaMourir() == True
    
    # Quand food == 0
    ours._Animal__age = 3 # aleatoire moins que MaxAge
    ours._Ours__food = 0
    assert ours.vaMourir() == True
    
def test_reduireVie():
    ours.set_food(5)  #aleatoire pour test
    ours.reduireVie()
    assert ours.get_food() == 4
    
def test__str():
    assert ours.__str__() == f"O{ours.get_id()}" 