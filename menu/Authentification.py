from dao.Utilisateur_dao import UtilisateurDao
import os

class Menu_Authentification:
    def __init__(self):
        self.util_dao = UtilisateurDao()

    def cls(self):
        os.system("cls")

    def pause(self):
        input("Tapez entrer pour continuer ...")

    def se_connecter(self):
        while True:
            self.cls()
            print("=======  CONNEXION  =========")
            login = input("Login: ").strip()
            password = input("Password: ").strip()
            utilisateur = self.util_dao.authentifier(login, password)
            if utilisateur:
                print(f"Bienvenue {utilisateur.nom} {utilisateur.prenom} {utilisateur.role}")
                self.pause()
                return utilisateur
            else:
                print("identifiant ou mot de passe incorrect")
                self.pause()