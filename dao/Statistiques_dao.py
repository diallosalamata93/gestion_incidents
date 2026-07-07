from dao.base_dao import BaseDAO


class StatistiquesDao(BaseDAO):
    def __init__(self):
        super().__init__()
    def total_Incidents_statut(self):
        sql="""
        SELECT statut, COUNT(*) as total FROM incident GROUP BY statut
        """
        self.bd.execute(sql)
        return self.bd.fetchall()

    def incident_Priorite(self):
        sql="""
        SELECT priorite, COUNT(*) as priori FROM incident GROUP BY priorite """
        self.bd.execute(sql)
        return self.bd.fetchall()

    def temps_moyen_resolution(self):
        sql = """
        SELECT AVG(iv.duree_minutes) / 60
        FROM intervention iv
        JOIN incident i ON i.id = iv.incident_id
        WHERE i.statut IN ('RESOLU', 'FERME')
        """
        self.bd.execute(sql)
        return self.bd.fetchone()
    def technicien_plus_actif(self):
        sql = """
        SELECT u.nom, u.prenom, COUNT(iv.id) as nb_interventions
        FROM utilisateur u
        JOIN intervention iv ON iv.technicien_id = u.id 
        WHERE u.role='TECHNICIEN'
        GROUP BY u.id,u.nom,u.prenom
        ORDER BY nb_interventions DESC
        LIMIT 3
        """
        self.bd.execute(sql)
        return self.bd.fetchall()
    def incident_traite_Temps(self):
        sql = """
        SELECT u.nom, u.prenom, COUNT(DISTINCT i.id) as nb_incidents,
        AVG(v.duree_minutes) as temps_moyen
        FROM utilisateur u
        JOIN intervention v ON v.technicien_id = u.id
        JOIN incident i ON i.id = v.incident_id
        WHERE u.role='TECHNICIEN'
        GROUP BY u.id,u.nom,u.prenom
         """
        self.bd.execute(sql)
        return self.bd.fetchall()

    def taux_resolution_48h(self):
        sql = """SELECT 
                 COUNT(*) AS total,
                 SUM(CASE WHEN SUM(iv.duree_minutes) <= 2880 
                 THEN 1 ELSE 0 END) AS dans_48h,
                 SUM(CASE WHEN SUM(iv.duree_minutes) <= 2880 
                 THEN 1 ELSE 0 END) * 100 / COUNT(*) AS pourcentage
                 FROM incident i
                 JOIN intervention iv ON iv.incident_id = i.id
                 WHERE i.statut IN ('RESOLU', 'FERME')
                 GROUP BY i.id"""
        self.bd.execute(sql)
        return self.bd.fetchall()


