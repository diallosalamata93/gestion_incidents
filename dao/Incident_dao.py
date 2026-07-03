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
