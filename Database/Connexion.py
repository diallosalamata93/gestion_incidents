import mysql.connector
import psycopg2
from Database.config import TYPE_BD, POSTGRES, MYSQL


class DatabaseConnection:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection=None
            cls._instance.cursor=None

        return cls._instance


    def connect(self):
         try:
            if TYPE_BD == "postgres":
                self.connection = psycopg2.connect(
                    host=POSTGRES["host"],
                    port=POSTGRES["port"],
                    database=POSTGRES["database"],
                    user=POSTGRES["user"],
                    password=POSTGRES["password"],
                )
                print("connection reussi à postgres")
            elif TYPE_BD == "mysql":
                self.connection= mysql.connector.connect(
                    host=MYSQL["host"],
                    port=MYSQL["port"],
                    database=MYSQL["database"],
                    user=MYSQL["user"],
                    password=MYSQL["password"],
                )
                print("connection reussi à mysql")
            else:
                print("type de base de donnee introuvable")
                return False
            self.cursor = self.connection.cursor()
            return True
         except Exception as e:
            print(f"Erreur de connexion a la base de donnee:{e}")
            return False


    def disconnect(self):
    #fermer la connexion
        if self.cursor:
            self.cursor.close()
        self.cursor = None
        if self.connection:
           self.connection.close()
           self.connection = None
           print("Connexion fermée")



    def commit(self):
         #Valider les modifications
         if self.connection:
           self.connection.commit()

    def rollback(self):
        #retour ou Annule les modifications
        if self.connection:
          self.connection.rollback()

    def execute(self,query,params=None):
        #execute une requete sql
        try:
            self.cursor.execute(query,params or ())
            return True
        except Exception as e:
            print(f"Erreur de requette SQL:{e}")
            return False

    def fetchall(self):
        #recupere tout les resultats
        return self.cursor.fetchall()


    def fetchone(self):
        #recupère un seul résultat
        return self.cursor.fetchone()












