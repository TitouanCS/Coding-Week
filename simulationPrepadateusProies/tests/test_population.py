import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.coordonnee import *
from source.population import *

population = Population(10)
TAILLE = population.getTAILLE()


def tests_init():
    animauxPopulation = population.getAnimauxPopulation()
    idsUtilisables = population.getIdsUtilisables()
    assert len(animauxPopulation) == TAILLE*TAILLE
    assert len(idsUtilisables) == TAILLE*TAILLE
    for i in range(TAILLE*TAILLE):
        assert animauxPopulation[i] == -1
        assert idsUtilisables[i] == i


def tests_add_and_delete_animal():

    # Ajout d'un Renard à la case(0,0)
    population.addAnimal(0, Coordonnee(0, 0))
    assert 0 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[0].get_id() == 0
    # Ajout d'un Renard à la case(2,3)
    population.addAnimal(0, Coordonnee(2, 3))
    assert 1 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[1].get_id() == 1
    # Ajout d'un Renard à la case(0,0)
    population.addAnimal(0, Coordonnee(5, 4))
    assert 2 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[2].get_id() == 2

    animauxPopulation = population.getAnimauxPopulation()
    idsUtilisables = population.getIdsUtilisables()

    for i in range(3, TAILLE*TAILLE):
        assert animauxPopulation[i] == -1
        assert idsUtilisables[i-3] == i

    assert population.renard_ids() == [0, 1, 2]
    assert population.lapin_ids() == []
    assert population.ours_ids() == []

    # Ajout d'un Lapin à la case(1,1)
    population.addAnimal(1, Coordonnee(1, 1))
    assert 3 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[3].get_id() == 3
    # Ajout d'un Lapin à la case(6,5)
    population.addAnimal(1, Coordonnee(6, 5))
    assert 4 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[4].get_id() == 4
    # Ajout d'un Lapin à la case(5,5)
    population.addAnimal(1, Coordonnee(5, 5))
    assert 5 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[5].get_id() == 5

    animauxPopulation = population.getAnimauxPopulation()
    idsUtilisables = population.getIdsUtilisables()

    for i in range(6, TAILLE*TAILLE):
        assert animauxPopulation[i] == -1
        assert idsUtilisables[i-6] == i

    assert population.renard_ids() == [0, 1, 2]
    assert population.lapin_ids() == [3, 4, 5]
    assert population.ours_ids() == []

    # Ajout d'un Ours à la case(9,1)
    population.addAnimal(2, Coordonnee(9, 1))
    assert 6 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[6].get_id() == 6
    # Ajout d'un Ours à la case(3,9)
    population.addAnimal(2, Coordonnee(3, 9))
    assert 7 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[7].get_id() == 7
    # Ajout d'un Ours à la case(6,7)
    population.addAnimal(2, Coordonnee(6, 7))
    assert 8 not in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[8].get_id() == 8

    animauxPopulation = population.getAnimauxPopulation()
    idsUtilisables = population.getIdsUtilisables()

    for i in range(9, TAILLE*TAILLE):
        assert animauxPopulation[i] == -1
        assert idsUtilisables[i-9] == i

    assert population.renard_ids() == [0, 1, 2]
    assert population.lapin_ids() == [3, 4, 5]
    assert population.ours_ids() == [6, 7, 8]

    # Suppression du Renard en (0,0)
    population.deleteAnimal(population.getAnimal(0))
    assert 0 in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[0] == -1
    # Suppression du Renard en (2,3)
    population.deleteAnimal(population.getAnimal(1))
    assert 1 in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[1] == -1
    # Suppression du Lapin en (5,5)
    population.deleteAnimal(population.getAnimal(5))
    assert 5 in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[5] == -1
    # Suppression de l'Ours en (3,9)
    population.deleteAnimal(population.getAnimal(7))
    assert 7 in population.getIdsUtilisables()
    assert population.getAnimauxPopulation()[7] == -1

    assert population.renard_ids() == [2]
    assert population.lapin_ids() == [3, 4]
    assert population.ours_ids() == [6, 8]


def test_allele_frequencies():
    """Test la méthode de calcul des fréquences des allèles avec des gènes spécifiques sur une grille de 10x10"""

    population = Population(10)
    TAILLE = population.getTAILLE()

    # Ajouter un renard avec des gènes spécifiques (par exemple, Gène1 : A, Gène2 : B)
    coord1 = Coordonnee(0, 0)
    # Gène1 : A (0), Gène2 : B (1)
    genes_renard = {Genes.MANGE: 0, Genes.ESQUIVE: 1}
    population.addAnimal(sexe=0, coord=coord1, genes=genes_renard)

    coord2 = Coordonnee(6, 3)
    # Gène1 : A (0), Gène2 : B (1)
    genes_renard = {Genes.MANGE: 0, Genes.ESQUIVE: 4}
    population.addAnimal(sexe=0, coord=coord2, genes=genes_renard)

    allele_frequencies = population.alleleFrequenciesByGeneByAnimal()

    assert allele_frequencies["Renard"][Genes.MANGE] == {0: 1}
    assert allele_frequencies["Renard"][Genes.ESQUIVE] == {1: 1/2, 4: 1/2}

    coord3 = Coordonnee(7, 3)
    # Gène1 : A (0), Gène2 : B (1)
    genes_lapin = {Genes.MANGE: 4, Genes.ESQUIVE: 4}
    population.addAnimal(sexe=1, coord=coord3 ,genes=genes_lapin)

    allele_frequencies = population.alleleFrequenciesByGeneByAnimal()
    
    assert allele_frequencies["Renard"][Genes.MANGE] == {0: 1}
    assert allele_frequencies["Renard"][Genes.ESQUIVE] == {1: 1/2, 4: 1/2}
    assert allele_frequencies["Lapin"][Genes.MANGE] == {4: 1}
    assert allele_frequencies["Lapin"][Genes.ESQUIVE] == {4: 1}

    # Vérifications
    assert "Renard" in allele_frequencies
    assert "Lapin" in allele_frequencies

    # Vérifie que les fréquences des allèles sont bien des dictionnaires
    assert isinstance(allele_frequencies["Renard"], dict)
    assert isinstance(allele_frequencies["Lapin"], dict)

