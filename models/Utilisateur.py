from datetime import date
class Utilisateur:
    #ROLES=["Utilisateur","Technicien","Admin"]
    def __init__(self, id=None,login="",password="",nom="",prenom="",email="",role="",service="",date_creation=None):
        self.id = id
        self.login = login
        self.password = password
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.role = role
        self.service = service
        self.date_creation = date_creation.today()
    def __str__(self):
            return f"{self.id}-{self.nom}-{self.prenom}-{self.email}-{self.login}-{self.role}-{self.service}-{self.date_creation}"
    def verif_admin(self):
        return self.role=="Admin"
    def verif_technicien(self):
        return self.role=="Technicien"
    def verif_utilisateur(self):
        return self.role=="Utilisateur"
