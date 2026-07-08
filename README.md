# Gestion des Tickets d'Incidents

Application console de gestion des incidents informatiques (Help Desk) développée en Python avec MySQL.

## Auteurs
- Diallo Salamata - Chef de projet
- Ndeye laamine Dieng
- Ndeye Astou Camara
- Dieynaba Fall

## Technologies utilisées
- Python 3.14
- MySQL 8.4
- mysql-connector-python

## Architecture
gestion_incidents/
- Database/ → Connexion et configuration BD
- dao/ → Couche d'accès aux données (DAO)
- models/ → Classes métier
- menu/ → Interface utilisateur console
- main.py → Point d'entrée

## Installation

### Prérequis
- Python 3.x installé
- MySQL installé (Laragon ou autre)
- HeidiSQL (optionnel)

### Étapes

**1. Cloner le projet**

git clone https://github.com/diallosalamata93/gestion_incidents.git
cd gestion_incidents

**2. Installer les dépendances**

pip install mysql-connector-python

**3. Configurer la base de données**

Créer un fichier Database/config.py avec vos informations de connexion MySQL.

**4. Créer la base de données**

Dans HeidiSQL, créer une base nommée gestionIncident et créer les 3 tables : utilisateur, incident, intervention.

**5. Créer un utilisateur admin**

INSERT INTO utilisateur (login, password, nom, prenom, email, role, service, date_creation)
VALUES ('admin', 'admin123', 'Diallo', 'Salamata', 'admin@test.com', 'ADMIN', 'Informatique', CURDATE());

**6. Lancer l'application**

python main.py

## Utilisation

### Rôles disponibles
- ADMIN : gestion complète (utilisateurs, incidents, statistiques)
- TECHNICIEN : prise en charge et résolution des incidents
- UTILISATEUR : création et suivi de ses propres incidents

### Workflow des incidents
OUVERT → EN_COURS → RESOLU → FERME

## Fonctionnalités
- Authentification par rôle
- CRUD complet des utilisateurs
- Création et suivi des incidents
- Gestion des interventions
- Statistiques et rapports pour ADMIN