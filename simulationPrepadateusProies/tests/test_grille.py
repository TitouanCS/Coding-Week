import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.grille import *

grille = Grille(10)
TAILLE = grille.get_TAILLE()

def tests_init():
    for i in range(TAILLE):
        for j in range(TAILLE):
            assert grille.get_id(Coordonnee(i,j)) == -1
            assert grille.get_environnement(Coordonnee(i,j)) == Environnement.VIDE

def tests_set_animalId_and_removeId():

    grille.set_animalId(Coordonnee(0,0),0)
    grille.set_animalId(Coordonnee(3,4),10)

    assert grille.get_id(Coordonnee(0,0)) == 0
    grille.removeId(Coordonnee(0,0))
    assert grille.get_id(Coordonnee(0,0)) == -1

    assert grille.get_id(Coordonnee(3,4)) == 10
    grille.removeId(Coordonnee(3,4))
    assert grille.get_id(Coordonnee(3,4)) == -1

def tests_case_vide():
    grille.case_Vide() == [Coordonnee(i,j) for i in range(TAILLE) for j in range(TAILLE)]
    grille.set_environnement(Coordonnee(0,0),Environnement.HERBE)
    grille.case_Vide() == [Coordonnee(i,j) for i in range(TAILLE) for j in range(TAILLE) if i!=0 and j!=0]
    grille.set_environnement(Coordonnee(0,0),Environnement.VIDE)

def tests_coord_hasard():
    c = grille.coord_hasard()
    x,y = c.get_coord()
    assert 0 <= x < TAILLE
    assert 0 <= y < TAILLE
    
def tests_str():

    # Représentation attendue pour une grille vide
    assert str(grille) == "".join(
        f"| {' | '.join('-1 V' for _ in range(TAILLE))} |\n" for _ in range(TAILLE)
    )

    # Ajout d'identifiants à quelques cases
    grille.set_animalId(Coordonnee(0, 0), 42)
    grille.set_animalId(Coordonnee(1, 3), 99)
    grille.set_animalId(Coordonnee(4, 7), 7)

    # Ajout d'un environnement en (0,0)
    grille.set_environnement(Coordonnee(0,0),Environnement.HERBE)
    
    expected = ""
    for i in range(TAILLE):
        expected += "|"
        for j in range(TAILLE):
            if (i, j) == (0, 0):
                expected += " 42 H |"
            elif (i, j) == (1, 3):
                expected += " 99 V |"
            elif (i, j) == (4, 7):
                expected += " 7 V |"
            else:
                expected += " -1 V |"
        expected += "\n"

    assert str(grille) == expected

    # Suppression d'un identifiant
    grille.removeId(Coordonnee(1, 3))
    
    expected_bis = ""
    for i in range(TAILLE):
        expected_bis += "|"
        for j in range(TAILLE):
            if (i, j) == (0, 0):
                expected_bis += " 42 H |"
            elif (i, j) == (4, 7):
                expected_bis += " 7 V |"
            else:
                expected_bis += " -1 V |"
        expected_bis += "\n"

    assert str(grille) == expected_bis

def tests_set_environnement():
    grille.set_environnement(Coordonnee(0,0),Environnement.HERBE)
    assert grille.get_environnement(Coordonnee(0,0)) == Environnement.HERBE
    try : 
        grille.set_environnement(Coordonnee(0,TAILLE),Environnement.HERBE)
        assert False
    except ValueError as e : pass
    try : 
        grille.set_environnement(Coordonnee(TAILLE,0),Environnement.HERBE)
        assert False
    except ValueError as e : pass  