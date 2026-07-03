from Database.Connexion import DatabaseConnection
from dao.base_dao import BaseDAO
from models.Utilisateur import Utilisateur


class UtilisateurDao(BaseDAO):
    def __init__(self):
        super().__init__()

    def get_all(self):
       self.db.execute("select * from utilisateur")
       return self.db.fetchall()
    def get_by_id(self,id):
        sql = "SELECT * FROM utilisateur WHERE id=%s"
        params = (id,)
        self.db.execute(sql, params)
        ligne= self.db.fetchone()
        if ligne:
            return Utilisateur(
                id = ligne[0],
                login = ligne[1],
                password = ligne[2],
                nom = ligne[3],
                prenom = ligne[4],
                email = ligne[5],
                role = ligne[6],
                service= ligne[7],
                date_creation= ligne[8]
            )
        return None
    def delete_by_id(self,id):
        sql = "DELETE FROM utilisateur WHERE id=%s"
        params = (id,)
        ok=self.db.execute(sql, params)
        if ok:
            self.db.commit()
        else:
            self.db.rollback()
        return ok
