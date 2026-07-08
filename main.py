from Database.Connexion import DatabaseConnection
from menu.Authentification import Menu_Authentification
from menu.Interface import Interface


def main():
    # Connexion à la base de données
    db = DatabaseConnection()
    if not db.connect():
        print("Impossible de se connecter à la base de données !")
        return

    # Boucle principale
    while True:
        auth = Menu_Authentification()
        utilisateur = auth.se_connecter()

        if utilisateur:
            interface = Interface(utilisateur)
            interface.afficher_menu()

        print("Voulez-vous vous reconnecter ? (oui/non)")
        choix = input().strip().lower()
        if choix != "oui":
            print("Au revoir !")
            db.disconnect()
            break


if __name__ == "__main__":
    main()