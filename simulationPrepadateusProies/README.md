# Simulation proies,prédateurs

## Description 
Simulation d'un écosystème contenant une chaîne de proies et de prédateurs. L'objectif est d'observer à travers une simulation des comportements semblables à ceux présent dans la nature. Pour cela, différents graphiques se forment parallèlement à la simulation.

## Comment utiliser ?
Se placer à la racine de l'archive puis : 
- pour lancer les tests
``` pytest --cov=./ --cov-report=term ./tests/ ```
- pour lancer la simulation 
```python3 main.py```

## What does the fox say ?
- Quentin DILET
- Juefei YUAN
- Christian ABOU HAMAD
- Guglielmo LUKSCH
- Joseph LEGER
- Titouan GAY-CORTIJO

## Attentes 
```
Pour chaque fonctionnalité :

Chaque membre du groupe travaille, de son côté,  sur son dépôt local. Attention, dans ce cas, il est préférable de ne pas travailler sur la branche master mais sur des branches de travail, qui vous seront propres, et que vous devrez créer.

Il faudra alors prévoir un temps de mise en commun et de revue entre vous de chacune des foncionnalités. C'est un procédé que l'on pourrait assimilé à de la revue de code

Après ce travail de revue, vous pourrez alors décidé de la version de la foncionnalité à mettre sur la branche master qui devra contenir à tout moment la version stable de votre projet.

Et bien évidemment, il sera nécessaire de pusher sur le depôt distant pour vous permettre de partager cette version stable entre vous.

Le passage et le travail à une nouvelle fonctionnalité se fera donc sur la base d'une branche master synchronisée entre vous tous
```

```
Pour toute la suite du projet, il vous est demandé de :

- Faire un commit dès que la réalisation d'une fonctionnalité ou d'une sous-fonctionnalité est finie.
- Tagger à la fin de chaque journée votre dernier commit et à la fin de chaque split
- Faire une revue de code au sein de l'équipe pour chaque fonctionnalité.
- Mettre le code stable sur la branche master.
- Push le code vers votre dépôt distant sur GitLab.
- Faire un test de couverture de code à la fin de chaque journée et de chaque split et de pousser le bilan obtenu vers votre dépôt distant sur GitLab.
```

## Règles de développement
- Pour chaque cycle de conception, lister et prioriser les fonctionnalités manquante puis découper le travail en splits.
- Ne jamais travailler localement sur sa branche `main`
- Réaliser des tests pour chaque fonction, classe ou méthode implémentées. 
Le sujet suggère de réaliser une approche TDD. Le sujet suggère d'utiliser `Pytest`
- Pour chaque méthode ou fonction, faire la docstring. ChatGPT la génère très bien.
- Commenter raisonnablement le code

## Tests

Les tests doivent être réalisés dans le fichier `tests` afin de ne pas saturer le répertoire de travail. 

Si vous souhaitez effectuer des tests sur la classe `A`, vous devez introduire les lignes suivantes au début du fichier :

```python
import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from A import *
```

### MVP1 : Implémentation fondamentale du jeu avec interface élémentaire en terminal

- Sprint 1.1 : Initialisation technique et réflexions autour du projet
    - Fonctionnalité 1.1.1 Trouver un nom au projet et un nom d'équipe
    - Fonctionnalité 1.1.2 Expliciter les premières règles de reproduction et de disparition
    - Fonctionnalité 1.1.3 Initialisation du git et du README.md
    - Fonctionnalité 1.1.4 S'accorder pour la représentation informatique des objets manipulés et le formuler dans le WorkingDocs
    - Fonctionnalité 1.1.5 Réaliser un diagrammes de classe, expliciter les pemières méthodes de classes, ses arguments et ses invariants

- Sprint 1.2 : Mise en place des données du projet
    - Fonctionnalité 1.2.1 : Représentation de grille avec l'état initial généré aléatoirement
    - Fonctionnalité 1.2.2 : Implémentation de la classe Case
    - Fonctionnalité 1.2.3 : Implémentation de la classe Entité et de ses classes filles
    - Fonctionnalité 1.2.4 : Appliquer les règles à toutes les Entités de la grille

- Sprint 1.3 : Premier affichage
    - Fonctionnalité 1.3.1 : Implémenter les fonctions d'affichage pour chaque classe dérivée de la classe Entité
    - Fonctionnalité 1.3.2 : Implémentation de la fonction d'affichage de la classe Grille
    - Fonctionnalité 1.3.3 : Gestion des paramètres avec argparse

Avant de continuer au MVP2:
- Réaliser pour chaque méthode implémentées plusieurs tests, en particulier ceux gérant les cas limites
- Retour utilisateur : Lister et prioriser les fonctionnalités manquantes dans le TODO.md
 
 
### MVP2 : Implémentation de l’ interface graphique avec pygame

- Sprint 2.1 : Configuration et structure de base
    - Fonctionnalité 2.1.1 : Initialisation de l'interface graphique : Configurer pygame.
    - Fonctionnalité 2.1.2 : Créer une classe principale InterfaceGraphique.
    - Fonctionnalité 2.1.3 : Définir les constantes de couleur, tailles, et FPS.
 
- Sprint 2.2 : Gestion de l’écran de paramètres:
    - Fonctionnalité 2.2.1 : Afficher les paramètres utilisateurs de la simulation
    - Fonctionnalité 2.2.2 : Gestion de ces paramètres par l’utilisateur
 
- Sprint 2.3 : Intégration de la simulation
    - Fonctionnalité 2.3.1 : Fonction de mise à jour de la grille
    - Fonctionnalité 2.3.2 : Lecture des données de la grille
    - Fonctionnalité 2.3.3 : Représentation des entités sur la grille
    - Fonctionnalité 2.3.4 : Ajouter une boucle principale pour animer la simulation
 
 
### MVP 3 : Enregistrement avec matplotlib et de courbes avec matplotlib

- Sprint 3.1 : Mise en place des données nécessaires pour le graphique
    - Fonctionnalité : 3.1.1 Initialisation des listes pour les populations et les stocker dans la boucle principale
    - Fonctionnalité : 3.1.2 : Adapter « run » pour mettre à jour les listes à chaque génération

- Sprint 3.2 : Génération du graphique des populations
    - Fonctionnalité 3.2.1 : Appel à plotSurface avec les listes à jour
    - Fonctionnalité 3.2.2 : Création d’une surface Pygame avec plotSurface, afficher le graphique
    - Fonctionnalité 3.2.3 : Dimensionner le graphique, les échelles et le positionnement
    - Fonctionnalité 3.2.4 : Tests pour différentes configurations
 
### MVP 4 : Finitions et optimisations

- Sprint 4.1 : Ajout d’un super-prédateur
    - Fonctionnalité 4.1.1 : Création de la classe associée
    - Fonctionnalité 4.1.2 : Modification de gameRules en conséquence
    - Fonctionnalité 4.1.3 : Ajout du super-prédateur pendant la simulation

- Sprint 4.2 : Ajout de paramètres génétiques
    - Fonctionnalité 4.2.1 : Implémentation des gênes et allèles
    - Fonctionnalité 4.2.2 : Adaptation de gameRules à l’hérédité
    - Fonctionnalité 4.2.3 : Afficher histogramme des gênes durant la simulation
    
- Sprint 4.3 : Améliorations interfaces
    - Fonctionnalité 4.3.1 : Amélioration de l’interface graphique
 