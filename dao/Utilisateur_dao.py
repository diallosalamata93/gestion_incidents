from Database.Connexion import DatabaseConnection
from dao.base_dao import BaseDAO
from models.Utilisateur import Utilisateur


class UtilisateurDao(BaseDAO):
    def __init__(self):
        super().__init__()

    def get_all(self):
       self.bd.execute("select * from utilisateur")
       return self.bd.fetchall()
    def get_by_id(self,id):
        sql = "SELECT * FROM utilisateur WHERE id=%s"
        params = (id,)
        self.bd.execute(sql, params)
        ligne= self.bd.fetchone()
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
        ok=self.bd.execute(sql, params)
        if ok:
            self.bd.commit()
        else:
            self.bd.rollback()
        return ok
    def ajouter_Utilisateur(self,utilisateur):
            sql="""
            insert into utilisateur(login,password,nom,prenom,email,role,service,date_creation) 
            values(%s,%s,%s,%s,%s,%s,%s,%s)
            """
            params=(utilisateur.login,utilisateur.password,utilisateur.nom,utilisateur.prenom,utilisateur.email,utilisateur.role,utilisateur.service,utilisateur.date_creation)
            ok=self.bd.execute(sql,params)
            if ok:
                self.bd.commit()
            else:self.bd.rollback()
            return ok

    def rechercher_Utilisateur(self, mot_cle):  # soit nom,login ou bien service


        sql = "SELECT * FROM utilisateur WHERE nom LIKE %s OR login Like %s OR service Like %s"
        motif = f"%{mot_cle}%"
        params = (motif, motif,motif)
        self.bd.execute(sql, params)
        resultats=self.bd.fetchall()
        utilisateurs=[]
        for ligne in resultats:
            utilisateurs.append(Utilisateur(
                id = ligne[0],
                login = ligne[1],
                password = ligne[2],
                nom = ligne[3],
                prenom = ligne[4],
                email = ligne[5],
                role = ligne[6],
                service = ligne[7],
                date_creation = ligne[8]
            ))
            return utilisateurs

    def modifier_Utilisateur(self, utilisateur):
        sql = """UPDATE utilisateur 
        SET login=%s,password=%s,nom=%s,prenom=%s,email=%s,role=%s,service=%s,date_creation=%s 
         WHERE id=%s  
        """
        params = (utilisateur.login, utilisateur.password, utilisateur.nom, utilisateur.prenom,
                  utilisateur.email,utilisateur.role,utilisateur.service,utilisateur.date_creation,utilisateur.id)
        ok = self.bd.execute(sql, params)
        if ok:
            self.bd.commit()
        else:
            self.bd.rollback()
        return ok
    def authentifier(self,login,password):
        sql="SELECT * FROM utilisateur WHERE login=%s AND password=%s"
        params=(login,password)
        self.bd.execute(sql, params)
        ligne=self.bd.fetchone()
        if ligne:
            return Utilisateur(
                id = ligne[0],
                login = ligne[1],
                password = ligne[2],
                nom = ligne[3],
                prenom = ligne[4],
                email = ligne[5],
                role = ligne[6],
                service = ligne[7],
                date_creation = ligne[8]
            )
        return None

