import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.environnement import *

def tests_environnement():
    environnement = Environnement(1)
    assert environnement.value == 1 
    assert environnement.__str__() == "V"
    environnement = Environnement(2)
    assert environnement.value == 2
    assert environnement.__str__() == "H"
    environnement = Environnement(3)
    assert environnement.value == 3 
    assert environnement.__str__() == "M"
    try : 
        environnement = Environnement(0)
        assert False
    except ValueError as e : pass 
    try :
        environnement = Environnement(4)
        assert False 
    except ValueError as e : pass