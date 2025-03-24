# Design Document - Projet NAS

## Overview

Le projet NAS est conçu pour automatiser la configuration des réseaux complexes en utilisant des fichiers JSON pour définir la topologie et des scripts Python pour générer les configurations. Ce document décrit l'architecture, les composants, et le flux de travail du projet.

## Architecture

### Components

1. **intends.json** :
   - Définit la topologie réseau, les routeurs, les interfaces, et les protocoles.
   - Structure hiérarchique avec des informations sur les AS et leurs voisins.

2. **Scripts Python** :
   - `main.py` : Point d'entrée principal pour générer les configurations.
   - `protocols.py` : Gère l'activation des protocoles RIP, OSPF, et BGP.
   - `tools.py` : Fournit des fonctions utilitaires pour manipuler les fichiers de configuration.
   - `move_files.ipynb` : Script pour organiser et déplacer les fichiers générés.

3. **GNS3 Integration** :
   - Les fichiers générés sont compatibles avec les projets GNS3 pour une simulation réseau.

### Data Flow

1. **Input** :
   - L'utilisateur modifie `intends.json` pour définir la topologie réseau.

2. **Processing** :
   - `main.py` lit `intends.json` et génère les fichiers de configuration pour chaque routeur.
   - Les protocoles sont activés en fonction des spécifications dans `intends.json`.

3. **Output** :
   - Les fichiers de configuration sont générés dans le format attendu par GNS3.

## Workflow

1. **Définition de la topologie** :
   - L'utilisateur configure les AS, routeurs, interfaces, et protocoles dans `intends.json`.

2. **Génération des configurations** :
   - `main.py` génère les fichiers de configuration en appelant les fonctions des modules `protocols.py` et `tools.py`.

3. **Organisation des fichiers** :
   - `move_files.ipynb` déplace les fichiers générés vers les dossiers de configuration GNS3.

4. **Simulation dans GNS3** :
   - L'utilisateur importe les fichiers dans GNS3 et démarre la simulation.

## Future Improvements

- Support pour d'autres protocoles comme EIGRP.
- Interface utilisateur pour simplifier la définition de la topologie.
- Tests unitaires pour valider les scripts.

## Conclusion

Le projet NAS offre une solution robuste pour l'automatisation des configurations réseau. Son architecture modulaire permet une extensibilité facile pour répondre à des besoins futurs.
