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
        if self.utilisateur.verif_admin():
            self.menu_admin()
        elif self.utilisateur.verif_technicien():
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

        incident = self.incident_dao.get_by_id(incident_id)

        if not incident:
            print("Incident introuvable !")
            self.pause()
            return

        # Vérifier que c'est bien l'incident de l'utilisateur connecté
        # (sauf technicien et admin qui peuvent tout voir)
        if self.utilisateur.verif_utilisateur():
            if incident.utilisateur_id != self.utilisateur.id:
                print("Accès refusé ! Vous ne pouvez voir que vos propres incidents.")
                self.pause()
                return

        resultats = self.incident_dao.detail(incident_id)

        if not resultats:
            print("Incident introuvable !")
        else:
            print(f"\nTitre : {resultats[0][1]}")
            print(f"Description : {resultats[0][2]}")
            print(f"Priorité : {resultats[0][3]}")
            print(f"Statut : {resultats[0][4]}")
            print(f"Date création : {resultats[0][5]}")

            print("\n--- Interventions ---")
            for ligne in resultats:
                if ligne[7]:
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
                #Fonction pour menu technicien

    def voir_incidents_ouverts(self):
                self.cls()
                print("======= INCIDENTS OUVERTS / EN COURS =======")
                incidents = self.incident_dao.ouvert_Encours()
                if not incidents:
                    print("Aucun incident ouvert ou en cours.")
                else:
                    for incident in incidents:
                        print(incident)
                self.pause()
        #*************************************************************
    def prendre_en_charge(self):
        self.cls()
        print("======= PRENDRE EN CHARGE UN INCIDENT =======")
        try:
            incident_id = int(input("ID de l'incident : ").strip())
        except ValueError:
            print("ID invalide !")
            self.pause()
            return

        incident = self.incident_dao.get_by_id(incident_id)

        if not incident:
            print("Incident introuvable !")
            self.pause()
            return

        if not incident.statut_ouvert():
            print(f"Impossible ! L'incident est déjà en statut {incident.statut}")
            self.pause()
            return

        ok = self.incident_dao.prendre_en_charge(incident_id)
        if ok:
            print("Incident pris en charge avec succès !")
        else:
            print("Erreur lors de la prise en charge !")
        self.pause()
    #*************************************************************
    def ajouter_intervention(self):
        self.cls()
        print("======= AJOUTER UNE INTERVENTION =======")
        try:
            incident_id = int(input("ID de l'incident : ").strip())
        except ValueError:
            print("ID invalide !")
            self.pause()
            return

        incident = self.incident_dao.get_by_id(incident_id)

        if not incident:
            print("Incident introuvable !")
            self.pause()
            return

        if not incident.statut_ouvert() and not incident.statut_en_cours():
            print(f"Impossible ! L'incident est en statut {incident.statut}")
            self.pause()
            return

        commentaire = input("Commentaire : ").strip()
        try:
            duree = int(input("Durée (en minutes) : ").strip())
            if duree < 0:
                print("La durée ne peut pas être négative !")
                self.pause()
                return
        except ValueError:
            print("Durée invalide !")
            self.pause()
            return

        intervention = Intervention(
            commentaire=commentaire,
            duree_minutes=duree,
            incident_id=incident_id,
            technicien_id=self.utilisateur.id
        )

        ok = self.intervention_dao.ajouter_Intervention(intervention)
        if ok:
            print("Intervention ajoutée avec succès !")
        else:
            print("Erreur lors de l'ajout de l'intervention !")
        self.pause()
        #**************************************
    def resoudre_incident(self):
            self.cls()
            print("======= RÉSOUDRE UN INCIDENT =======")
            try:
                incident_id = int(input("ID de l'incident : ").strip())
            except ValueError:
                print("ID invalide !")
                self.pause()
                return

            incident = self.incident_dao.get_by_id(incident_id)

            if not incident:
                print("Incident introuvable !")
                self.pause()
                return

            if not incident.statut_en_cours():
                print(f"Impossible ! L'incident doit être EN_COURS pour être résolu. Statut actuel : {incident.statut}")
                self.pause()
                return

            ok = self.incident_dao.changer_statut(incident_id, "RESOLU")
            if ok:
                print("Incident résolu avec succès !")
            else:
                print("Erreur lors de la résolution !")
            self.pause()
            #*********************************************************
    def fermer_incident(self):
                self.cls()
                print("======= FERMER UN INCIDENT =======")
                try:
                    incident_id = int(input("ID de l'incident : ").strip())
                except ValueError:
                    print("ID invalide !")
                    self.pause()
                    return

                incident = self.incident_dao.get_by_id(incident_id)

                if not incident:
                    print("Incident introuvable !")
                    self.pause()
                    return

                if not incident.statut_resolu():
                    print(
                        f"Impossible ! L'incident doit être RESOLU pour être fermé. Statut actuel : {incident.statut}")
                    self.pause()
                    return

                ok = self.incident_dao.changer_statut(incident_id, "FERME")
                if ok:
                    print("Incident fermé avec succès !")
                else:
                    print("Erreur lors de la fermeture !")
                self.pause()

        #******************************************************
    def supprimer_incident(self):
        self.cls()
        print("======= SUPPRIMER UN INCIDENT =======")
        try:
            id = int(input("ID de l'incident : ").strip())
        except ValueError:
            print("ID invalide !")
            self.pause()
            return

        incident = self.incident_dao.get_by_id(id)
        if not incident:
            print("Incident introuvable !")
            self.pause()
            return

        # Vérifier s'il a des interventions
        interventions = self.intervention_dao.get_by_incident(id)
        if interventions:
            print("Impossible ! Cet incident a des interventions associées.")
            self.pause()
            return

        print(f"Voulez-vous supprimer l'incident '{incident.titre}' ? (oui/non)")
        confirmation = input().strip().lower()
        if confirmation != "oui":
            print("Suppression annulée !")
            self.pause()
            return

        ok = self.incident_dao.get_delete_by(id)
        if ok:
            print("Incident supprimé avec succès !")
        else:
            print("Erreur lors de la suppression !")
        self.pause()
        #******************************************************

    def historique_technicien(self):
        self.cls()
        print("======= MON HISTORIQUE =======")
        incidents = self.incident_dao.get_historique_technicien(self.utilisateur.id)
        if not incidents:
            print("Vous n'avez traité aucun incident.")
        else:
            for incident in incidents:
                print(incident)
        self.pause()
               #MENU TECHNICIEN

    def menu_technicien(self):
        while True:
            self.cls()
            print("======= MENU TECHNICIEN =======")
            print(f"Connecté : {self.utilisateur.prenom} {self.utilisateur.nom}")
            print("1. Consulter incidents OUVERTS ou EN_COURS")
            print("2. Prendre en charge un incident")
            print("3. Ajouter une intervention")
            print("4. Résoudre un incident")
            print("5. Fermer un incident")
            print("6. Consulter mon historique")
            print("0. Se déconnecter")
            print("================================")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                self.voir_incidents_ouverts()
            elif choix == "2":
                self.prendre_en_charge()
            elif choix == "3":
                self.ajouter_intervention()
            elif choix == "4":
                self.resoudre_incident()
            elif choix == "5":
                self.fermer_incident()
            elif choix == "6":
                self.historique_technicien()
            elif choix == "0":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide !")
                self.pause()
                #***********************************************
                #Fonction admin
    def ajouter_utilisateur(self):
                    self.cls()
                    print("======= AJOUTER UN UTILISATEUR =======")
                    login = input("Login : ").strip()
                    password = input("Mot de passe : ").strip()
                    nom = input("Nom : ").strip()
                    prenom = input("Prénom : ").strip()
                    email = input("Email : ").strip()
                    service = input("Service : ").strip()
                    print("Rôle : ")
                    print("1. UTILISATEUR")
                    print("2. TECHNICIEN")
                    print("3. ADMIN")
                    choix = input("Votre choix : ").strip()
                    roles = {"1": "UTILISATEUR", "2": "TECHNICIEN", "3": "ADMIN"}
                    if choix not in roles:
                        print("Choix invalide !")
                        self.pause()
                        return
                    role = roles[choix]

                    utilisateur = Utilisateur(
                        login=login,
                        password=password,
                        nom=nom,
                        prenom=prenom,
                        email=email,
                        role=role,
                        service=service
                    )
                    ok = self.util_dao.ajouter_Utilisateur(utilisateur)
                    if ok:
                        print("Utilisateur ajouté avec succès !")
                    else:
                        print("Erreur lors de l'ajout !")
                    self.pause()
        #*********************************************************
    def lister_utilisateurs(self):
        self.cls()
        print("======= LISTE DES UTILISATEURS =======")
        utilisateurs = self.util_dao.get_all()
        if not utilisateurs:
            print("Aucun utilisateur trouvé.")
        else:
            for utilisateur in utilisateurs:
                print(utilisateur)
        self.pause()
        #****************************************
    def modifier_utilisateur(self):
            self.cls()
            print("======= MODIFIER UN UTILISATEUR =======")
            try:
                id = int(input("ID de l'utilisateur : ").strip())
            except ValueError:
                print("ID invalide !")
                self.pause()
                return

            utilisateur = self.util_dao.get_by_id(id)
            if not utilisateur:
                print("Utilisateur introuvable !")
                self.pause()
                return

            print(f"Utilisateur actuel : {utilisateur}")
            print("Laissez vide pour garder la valeur actuelle")

            login = input(f"Login [{utilisateur.login}] : ").strip() or utilisateur.login
            password = input(f"Mot de passe [{utilisateur.password}] : ").strip() or utilisateur.password
            nom = input(f"Nom [{utilisateur.nom}] : ").strip() or utilisateur.nom
            prenom = input(f"Prénom [{utilisateur.prenom}] : ").strip() or utilisateur.prenom
            email = input(f"Email [{utilisateur.email}] : ").strip() or utilisateur.email
            service = input(f"Service [{utilisateur.service}] : ").strip() or utilisateur.service

            print("Rôle : ")
            print("1. UTILISATEUR")
            print("2. TECHNICIEN")
            print("3. ADMIN")
            choix = input(f"Votre choix [{utilisateur.role}] : ").strip()
            roles = {"1": "UTILISATEUR", "2": "TECHNICIEN", "3": "ADMIN"}
            role = roles.get(choix, utilisateur.role)

            utilisateur.login = login
            utilisateur.password = password
            utilisateur.nom = nom
            utilisateur.prenom = prenom
            utilisateur.email = email
            utilisateur.role = role
            utilisateur.service = service

            ok = self.util_dao.modifier_Utilisateur(utilisateur)
            if ok:
                print("Utilisateur modifié avec succès !")
            else:
                print("Erreur lors de la modification !")
            self.pause()
            #*******************************************

    def supprimer_utilisateur(self):
        self.cls()
        print("======= SUPPRIMER UN UTILISATEUR =======")
        try:
            id = int(input("ID de l'utilisateur : ").strip())
        except ValueError:
            print("ID invalide !")
            self.pause()
            return

        utilisateur = self.util_dao.get_by_id(id)
        if not utilisateur:
            print("Utilisateur introuvable !")
            self.pause()
            return

        # Vérifier s'il a des incidents
        incidents = self.incident_dao.get_by_utilisateur(id)
        if incidents:
            print("Impossible ! Cet utilisateur a des incidents associés.")
            self.pause()
            return

        # Vérifier s'il a des interventions
        interventions = self.intervention_dao.get_historique_technicien_Intervention(id)
        if interventions:
            print("Impossible ! Cet utilisateur a des interventions associées.")
            self.pause()
            return

        print(f"Voulez-vous supprimer {utilisateur} ? (oui/non)")
        confirmation = input().strip().lower()
        if confirmation != "oui":
            print("Suppression annulée !")
            self.pause()
            return

        ok = self.util_dao.get_delete_by(id)
        if ok:
            print("Utilisateur supprimé avec succès !")
        else:
            print("Erreur lors de la suppression !")
        self.pause()
                #***************************

    def rechercher_utilisateur(self):
                self.cls()
                print("======= RECHERCHER UN UTILISATEUR =======")
                mot_cle = input("Rechercher (nom, login ou service) : ").strip()
                utilisateurs = self.util_dao.rechercher_Utilisateur(mot_cle)
                if not utilisateurs:
                    print("Aucun utilisateur trouvé.")
                else:
                    for utilisateur in utilisateurs:
                        print(utilisateur)
                self.pause()
                #******************************************

    def tous_les_incidents(self):
                self.cls()
                print("======= TOUS LES INCIDENTS =======")
                incidents = self.incident_dao.get_all()
                if not incidents:
                    print("Aucun incident trouvé.")
                else:
                    for incident in incidents:
                        print(incident)
                self.pause()
                # ******************************************

    def voir_statistiques(self):
                self.cls()
                print("======= STATISTIQUES =======")

                print("\n--- Incidents par statut ---")
                stats = self.stats_dao.total_Incidents_statut()
                for ligne in stats:
                    print(f"{ligne[0]} : {ligne[1]}")

                print("\n--- Incidents par priorité ---")
                stats = self.stats_dao.incident_Priorite()
                for ligne in stats:
                    print(f"{ligne[0]} : {ligne[1]}")

                print("\n--- Temps moyen de résolution ---")
                temps = self.stats_dao.temps_moyen_resolution()
                if temps and temps[0]:
                    print(f"{round(temps[0], 2)} heures")
                else:
                    print("Pas de données disponibles")

                print("\n--- Top 3 techniciens ---")
                top = self.stats_dao.technicien_plus_actif()
                for ligne in top:
                    print(f"{ligne[0]} {ligne[1]} : {ligne[2]} interventions")

                print("\n--- Stats par technicien ---")
                stats = self.stats_dao.incident_traite_Temps()
                if not stats:
                    print("Pas de données disponibles")
                else:
                   for ligne in stats:
                     print(f"{ligne[0]} {ligne[1]} : {ligne[2]} incidents, {round(ligne[3], 2)}h en moyenne")

                print("\n--- Taux de résolution 48h ---")
                taux = self.stats_dao.taux_resolution_48h()
                if not taux:
                    print("Pas de données disponibles")
                else:

                    print(f"Total : {ligne[0]}, Dans 48h : {ligne[1]},Pourcentage:{round(ligne[2], 2)}%")

                self.pause()


                #MENU ADMIN

    def menu_admin(self):
        while True:
            self.cls()
            print("======= MENU ADMIN =======")
            print(f"Connecté : {self.utilisateur.prenom} {self.utilisateur.nom}")
            print("=== GESTION UTILISATEURS ===")
            print("1. Ajouter un utilisateur")
            print("2. Lister tous les utilisateurs")
            print("3. Modifier un utilisateur")
            print("4. Supprimer un utilisateur")
            print("5. Rechercher un utilisateur")
            print("=== INCIDENTS ===")
            print("6. Consulter tous les incidents")
            print("7. Prendre en charge un incident")
            print("8. Résoudre un incident")
            print("9. Fermer un incident")
            print("10. Supprimer un incident")
            print("11. Ajouter une intervention")
            print("=== STATISTIQUES ===")
            print("12. Voir les statistiques")
            print("0. Se déconnecter")
            print("==========================")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                self.ajouter_utilisateur()
            elif choix == "2":
                self.lister_utilisateurs()
            elif choix == "3":
                self.modifier_utilisateur()
            elif choix == "4":
                self.supprimer_utilisateur()
            elif choix == "5":
                self.rechercher_utilisateur()
            elif choix == "6":
                self.tous_les_incidents()
            elif choix == "7":
                self.prendre_en_charge()
            elif choix == "8":
                self.resoudre_incident()
            elif choix == "9":
                self.fermer_incident()
            elif choix == "10":
                self.supprimer_incident()
            elif choix == "11":
                self.ajouter_intervention()
            elif choix == "12":
                self.voir_statistiques()
            elif choix == "0":
                print("Déconnexion...")
                break
            else:
                print("Choix invalide !")
                self.pause()
