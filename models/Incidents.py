from datetime import datetime
class Incidents:
    def __init__(self, id=None,titre="",description="",priorite="",statut="OUVERT",date_creation=None,utilisateur_id=None):
        self.id = id
        self.titre = titre
        self.description = description
        self.priorite = priorite
        self.statut = statut
        self.date_creation = date_creation if date_creation else datetime.now()
        self.utilisateur_id = utilisateur_id
    def __str__(self):
        return f"{self.id} - {self.titre}-{self.description}-Priorité:{self.priorite}- statut:{self.statut}"
    def statut_overt(self):
        return self.statut=="OUVERT"

    def statut_en_cours(self):
        return self.statut=="En_COURS"

    def statut_resolu(self):
        return self.statut=="RESOLU"

    def statut_ferme(self):
        return self.statut=="FERME"

    def priorite_basse(self):
        return self.priorite=="BASSE"

    def priorite_moyenne(self):
        return self.statut=="MOYENNE"

    def priorite_haute(self):
        return self.statut=="HAUTE"

    def priorite_critique(self):
        return self.statut=="CRITIQUE"