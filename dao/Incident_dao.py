from abc import ABC

from dao.base_dao import BaseDAO
from models.Incidents import Incidents


class Incident_dao(BaseDAO, ABC):
    def __init__(self):
        super().__init__()

    def get_all(self):
            self.bd.execute("select * from incident")
            return self.bd.fetchall()

    def get_by_id(self, id):
            sql = "SELECT * FROM incident WHERE id=%s"
            params = (id,)
            self.bd.execute(sql, params)
            ligne = self.bd.fetchone()
            if ligne:
                return Incidents(
                    id=ligne[0],
                    titre=ligne[1],
                    description=ligne[2],
                    priorite=ligne[3],
                    statut=ligne[4],
                    date_creation=ligne[5],
                    utilisateur_id=ligne[6],
                )
            return None

    def delete_by_id(self, id):
            sql = "DELETE FROM incident WHERE id=%s"
            params = (id,)
            ok = self.bd.execute(sql, params)
            if ok:
                self.bd.commit()
            else:
                self.bd.rollback()
            return ok
    def ajouter_Incident(self,incident):
            sql="""
            insert into incident(titre,description,priorite,statut,date_creation,utilisateur_id) 
            values(%s,%s,%s,%s,%s,%s)
            """
            params=(incident.titre,incident.description,incident.priorite,incident.statut,incident.date_creation,incident.utilisateur_id)
            ok=self.bd.execute(sql,params)
            if ok:
                self.bd.commit()
            else:self.bd.rollback()
            return ok
    def filtrer_Statut(self,utilisateur_id,statut):
        sql="""
        SELECT * FROM incident WHERE utilisateur_id=%s AND statut=%s
        
        """
        params=(utilisateur_id,statut)
        self.bd.execute(sql,params)
        lignes= self.bd.fetchall()
        incidents=[]
        for ligne in lignes:
            incidents.append(Incidents(
                id=ligne[0],
                titre=ligne[1],
                description=ligne[2],
                priorite=ligne[3],
                statut=ligne[4],
                date_creation=ligne[5],
                utilisateur_id=ligne[6],
            ))
        return incidents
    def filtrer_priorite(self,utilisateur_id,priorite):
        sql="""
        SELECT * FROM incident WHERE utilisateur_id=%s AND priorite=%s
        """
        params=(utilisateur_id,priorite)
        self.bd.execute(sql,params)
        ligne= self.bd.fetchall()
        incidents=[]
        for ligne in ligne:
            incidents.append(Incidents(
                id=ligne[0],
                titre=ligne[1],
                description=ligne[2],
                priorite=ligne[3],
                statut=ligne[4],
                date_creation=ligne[5],
                utilisateur_id=ligne[6],
            ))
        return incidents
    def detail(self,incident_id):
        sql=""" 
        SELECT i.*, inter.commentaire,v.duree_minute,inter.date_intervention,inter.technicien_id
         FROM incident i
        LEFT JOIN intervention inter on  i.id=inter.incident_id
        WHERE i.id=%s
        """
        params=(incident_id,)
        self.bd.execute(sql,params)
        return self.bd.fetchall()
    def ouvert_Encours(self):
        sql="""
            SELECT * FROM incident
            WHERE statut='OUVERT' OR statut='EN_COURS'
        """
        self.bd.execute(sql)
        ligne= self.bd.fetchall()
        incidents=[]
        for ligne in ligne:
            incidents.append(Incidents(
                id=ligne[0],
                titre=ligne[1],
                description=ligne[2],
                priorite=ligne[3],
                statut=ligne[4],
                date_creation=ligne[5],
                utilisateur_id=ligne[6],

            ))
        return incidents
    def changer_statut(self,id,nouveau_statut):
        sql="""
        UPDATE incident SET statut=%s WHERE id=%s
        """
        params=(id,nouveau_statut)
        ok=self.bd.execute(sql,params)
        if ok:
            self.bd.commit()
        else:
            self.bd.rollback()
        return ok
    def prendre_en_charge(self,id):
        return self.changer_statut(id,"EN_COURS")

    def get_historique_technicien(self, technicien_id):
        sql = """SELECT DISTINCT i.* FROM incident i
                 JOIN intervention v ON i.id = v.incident_id
                 WHERE v.technicien_id = %s"""
        params = (technicien_id,)
        self.bd.execute(sql, params)
        lignes = self.bd.fetchall()
        incidents = []
        for ligne in lignes:
            incidents.append(Incidents(
                id=ligne[0],
                titre=ligne[1],
                description=ligne[2],
                priorite=ligne[3],
                statut=ligne[4],
                date_creation=ligne[5],
                utilisateur_id=ligne[6]
            ))
        return incidents

    def modifier_Incident(self, incident,id):
        sql = """UPDATE incident 
        SET titre=%s,description=%s,priorite=%s,date_creation=%s
         WHERE id=%s  
        """
        params = (incident.titre, incident.description, incident.priorite, incident.date_creation,
                  id
                  )
        ok = self.bd.execute(sql, params)
        if ok:
            self.bd.commit()
        else:
            self.bd.rollback()
        return ok