from dao.Utilisateur_dao import UtilisateurDao
from dao.Incident_dao import Incident_dao
from dao.Intervention_dao import InterventionDao
from dao.Statistiques_dao import StatistiquesDAO
from models.Utilisateur import Utilisateur
from models.Incidents import Incidents
from models.Intervention import Intervention
import os

class Interface:
    def __init__(self, utilisateur):
        self.utilisateur = utilisateur  # utilisateur connecté
        self.util_dao = UtilisateurDao()
        self.incident_dao = Incident_dao()
        self.intervention_dao = InterventionDao()
        self.stats_dao = StatistiquesDAO()

    def cls(self):
        os.system("cls")

    def pause(self):
        input("Tapez entrer pour continuer ...")

    def afficher_menu(self):
        if self.utilisateur.est_admin():
            self.menu_admin()
        elif self.utilisateur.est_technicien():
            self.menu_technicien()
        else:
            self.menu_utilisateur()

    def creer_incident(self):
        self.cls()
        print("======= CRÉER UN INCIDENT =======")
        titre = input("Titre : ").strip()
        description = input("Description : ").strip()
        print("Priorité : ")
        print("1. BASSE")
        print("2. MOYENNE")
        print("3. HAUTE")
        print("4. CRITIQUE")
        choix = input("Votre choix : ").strip()
        priorites = {"1": "BASSE", "2": "MOYENNE", "3": "HAUTE", "4": "CRITIQUE"}
        if choix not in priorites:
            print("Choix invalide !")
            self.pause()
            return
        priorite = priorites[choix]
        incident = Incidents(
            titre=titre,
            description=description,
            priorite=priorite,
            statut="OUVERT",
            utilisateur_id=self.utilisateur.id
        )
        ok = self.incident_dao.ajouter_Incident(incident)
        if ok:
            print("Incident créé avec succès !")
        else:
            print("Erreur lors de la création de l'incident !")
        self.pause()

    def mes_incidents(self):
        self.cls()
        print("======= MES INCIDENTS =======")
        incidents = self.incident_dao.get_by_utilisateur(self.utilisateur.id)
        if not incidents:
            print("Vous n'avez aucun incident.")
        else:
            for incident in incidents:
                print(incident)
        self.pause()

    def detail_incident(self):
        self.cls()
        print("======= DÉTAIL D'UN INCIDENT =======")
        try:
            incident_id = int(input("ID de l'incident : ").strip())
        except ValueError:
            print("ID invalide !")
            self.pause()
            return

        resultats = self.incident_dao.detail(incident_id)

        if not resultats:
            print("Incident introuvable !")
        else:
            # Afficher les infos de l'incident (première ligne)
            print(f"\nTitre : {resultats[0][1]}")
            print(f"Description : {resultats[0][2]}")
            print(f"Priorité : {resultats[0][3]}")
            print(f"Statut : {resultats[0][4]}")
            print(f"Date création : {resultats[0][5]}")

            # Afficher les interventions
            print("\n--- Interventions ---")
            for ligne in resultats:
                if ligne[7]:  # si commentaire existe
                    print(f"Commentaire : {ligne[7]}")
                    print(f"Durée : {ligne[8]} minutes")
                    print(f"Date : {ligne[9]}")
                    print("---")
                else:
                    print("Aucune intervention pour le moment.")
                    break

        self.pause()

    def filtrer_par_statut(self):
        self.cls()
        print("======= FILTRER PAR STATUT =======")
        print("1. OUVERT")
        print("2. EN_COURS")
        print("3. RESOLU")
        print("4. FERME")
        choix = input("Votre choix : ").strip()

        statuts = {"1": "OUVERT", "2": "EN_COURS", "3": "RESOLU", "4": "FERME"}

        if choix not in statuts:
            print("Choix invalide !")
            self.pause()
            return

        statut = statuts[choix]
        incidents = self.incident_dao.filtrer_Statut(self.utilisateur.id, statut)

        if not incidents:
            print(f"Aucun incident avec le statut {statut}")
        else:
            for incident in incidents:
                print(incident)
        self.pause()

    def filtrer_par_priorite(self):
        self.cls()
        print("======= FILTRER PAR PRIORITÉ =======")
        print("1. BASSE")
        print("2. MOYENNE")
        print("3. HAUTE")
        print("4. CRITIQUE")
        choix = input("Votre choix : ").strip()

        priorites = {"1": "BASSE", "2": "MOYENNE", "3": "HAUTE", "4": "CRITIQUE"}

        if choix not in priorites:
            print("Choix invalide !")
            self.pause()
            return

        priorite = priorites[choix]
        incidents = self.incident_dao.filtrer_priorite(self.utilisateur.id, priorite)

        if not incidents:
            print(f"Aucun incident avec la priorité {priorite}")
        else:
            for incident in incidents:
                print(incident)
        self.pause()


    def menu_utilisateur(self):
        while True:
            self.cls()
            print("======= MENU UTILISATEUR =======")
            print(f"Connecté : {self.utilisateur.prenom} {self.utilisateur.nom}")
            print("1. Créer un nouvel incident")
            print("2. Consulter mes incidents")
            print("3. Consulter le détail d'un incident")
            print("4. Filtrer mes incidents par statut")
            print("5. Filtrer mes incidents par priorité")
            print("0. Se déconnecter")
            print("================================")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                self.creer_incident()
            elif choix == "2":
                self.mes_incidents()
            elif choix == "3":
                self.detail_incident()
            elif choix == "4":
                self.filtrer_par_statut()
            elif choix == "5":
                self.filtrer_par_priorite()
            elif choix == "0":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide !")
                self.pause()