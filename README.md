# Projet NAS - Network Automation System

## Description

Le projet NAS (Network Automation System) est une solution d'automatisation réseau conçue pour configurer et gérer des topologies complexes de routeurs. Il permet de générer des configurations pour des protocoles tels que RIP, OSPF, et BGP, tout en prenant en charge les interconnexions entre différents systèmes autonomes (AS). Ce projet est particulièrement utile pour les environnements de simulation réseau comme GNS3.

## Features

- Génération automatique de configurations pour les routeurs.
- Support des protocoles RIP, OSPF, et BGP.
- Gestion des interconnexions entre AS.
- Scripts pour déplacer et organiser les fichiers de configuration.
- Compatible avec les environnements de simulation réseau.

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/projet_NAS.git
   cd projet_NAS
   ```

2. Assurez-vous d'avoir Python 3.x installé.

3. Installez les dépendances nécessaires :

   ```bash
   pip install -r requirements.txt
   ```

4. Configurez votre environnement GNS3 pour utiliser les fichiers générés.

## Usage

1. Modifiez le fichier `intends.json` pour définir votre topologie réseau.
2. Exécutez le script principal pour générer les configurations :

   ```bash
   python GNS_code/main.py
   ```

3. Déplacez les fichiers générés vers les dossiers de configuration GNS3 :

   ```bash
   jupyter nbconvert --to script GNS_code/move_files.ipynb
   python GNS_code/move_files.py
   ```

4. Chargez les configurations dans GNS3 et démarrez vos routeurs.

## Project Structure

- `GNS_code/`: Contient les scripts principaux pour la génération et la gestion des configurations.
- `intends.json`: Fichier de définition de la topologie réseau.
- `README.md`: Documentation du projet.
- `design.md`: Documentation technique et architecture du projet.

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes :

1. Forkez ce dépôt.
2. Créez une branche pour vos modifications :

   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```

3. Soumettez une pull request avec une description claire de vos changements.

## License

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

## Acknowledgments

Merci à tous les contributeurs et aux outils open-source qui ont rendu ce projet possible.
