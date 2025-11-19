import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.animal import *
    
# Création d'un renard
ren = Renard((5,5),1)

def test_init():
    assert ren._Renard__food == ren.PARAMETERS["foodInitRenard"]
    assert ren.get_coord() == (5,5)
    assert ren.get_id() == 1
    
def test_mange():
    initial_food = ren.get_food()
    ren.mange()
    assert ren.get_food() ==  min(
        initial_food + ren.PARAMETERS["foodLapin"]+ ren._genes[Genes.MANGE], ren.PARAMETERS["maxFoodRenard"] + 2 * ren._genes[Genes.MANGE]) 
    
def test_peutSeReproduire():
    # Cas 1: food >= FoodReprodR
    ren._Renard__food = ren.PARAMETERS["foodReprodRenard"]
    continue_ = True 
    while(continue_):
        try : 
            assert ren.peutSeReproduire() == False 
            continue_ = False
        except AssertionError as e :
            continue_
    
    # cas 2: food < FoodReprodR
    ren._Renard__food = ren.PARAMETERS["foodReprodRenard"] - 1 # Aleatoire moin que foodReprodRenard
    assert ren.peutSeReproduire() == False 
    
def test_vaMourir():
    
    # Quand MaxAge
    ren._Animal__age = ren.PARAMETERS["maxAge"]
    ren._Renard__food = 5 # aleatoire plus que 0
    assert ren.vaMourir() == True
    
    # Quand food == 0
    ren._Animal__age = 3 # aleatoire moin que MaxAge
    ren._Renard__food = 0
    assert ren.vaMourir() == True
    
def test_reduireVie():
    ren._Renard__food = 5 #aleatoire pour test
    ren.reduireVie()
    
    assert ren._Renard__food == 4 - (ren.get_genes()[Genes.ESQUIVE] * (Animal.PARAMETERS["CoeffGeneE"]/10))
    
def test__str():
    assert ren.__str__() == f"R{ren.get_id()}"