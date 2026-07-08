from abc import ABC

from dao.base_dao import BaseDAO
from models.Intervention import Intervention


class InterventionDao(BaseDAO):
    def __init__(self):
        super().__init__()
    def get_all(self):
             self.bd.execute("select * from intervention")
             return self.bd.fetchall()

    def get_by_id(self, id):
            sql = "SELECT * FROM intervention WHERE id=%s"
            params = (id,)
            self.bd.execute(sql, params)
            ligne = self.bd.fetchone()
            if ligne:
                return Intervention(
                    id=ligne[0],
                    commentaire=ligne[1],
                    duree_minutes=ligne[2],
                    date_intervention=ligne[3],
                    incident_id=ligne[4],
                    technicien_id=ligne[5],

                )
            return None

    def get_delete_by(self, id):
            sql = "DELETE FROM intervention WHERE id=%s"
            params = (id,)
            ok = self.bd.execute(sql, params)
            if ok:
                self.bd.commit()
            else:
                self.bd.rollback()
            return ok

    def ajouter_Intervention(self, intervention):
        sql = """
               insert into intervention(commentaire,duree_minutes,date_intervention,incident_id,technicien_id) 
               values(%s,%s,%s,%s,%s)
               """
        params = (intervention.commentaire, intervention.duree_minutes, intervention.date_intervention, intervention.incident_id, intervention.technicien_id,
                  )
        ok = self.bd.execute(sql, params)
        if ok:
            self.bd.commit()
        else:
            self.bd.rollback()
        return ok
    def modifier_Intervention(self, intervention,id):
        sql = """UPDATE intervention 
        SET commentaire=%s,duree_minutes=%s,date_intervention=%s,incident_id=%s,technicien_id=%s 
         WHERE id=%s  
        """
        params = (intervention.commentaire, intervention.duree_minutes, intervention.date_intervention, intervention.incident_id, intervention.technicien_id,
                  id
                  )
        ok = self.bd.execute(sql, params)
        if ok:
            self.bd.commit()
        else:
            self.bd.rollback()
        return ok
    def get_historique_technicien_Intervention(self, technicien_id):
        sql = """SELECT * FROM intervention WHERE technicien_id = %s"""
        params = (technicien_id,)
        self.bd.execute(sql, params)
        lignes = self.bd.fetchall()
        interventions = []
        for ligne in lignes:
            interventions.append(Intervention(
                id=ligne[0],
                commentaire=ligne[1],
                duree_minutes=ligne[2],
                date_intervention=ligne[3],
                incident_id=ligne[4],
                technicien_id=ligne[5]
            ))
        return interventions
    def get_by_incident(self, incident_id):
        sql = """SELECT * FROM intervention WHERE incident_id = %s"""
        params = (incident_id,)
        self.bd.execute(sql, params)
        lignes = self.bd.fetchall()
        interventions = []
        for ligne in lignes:
            interventions.append(Intervention(
                id=ligne[0],
                commentaire=ligne[1],
                duree_minutes=ligne[2],
                date_intervention=ligne[3],
                incident_id=ligne[4],
                technicien_id=ligne[5]
            ))
        return interventions
