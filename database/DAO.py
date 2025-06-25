from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select year(datetime) as year 
                    from sighting
                    group by year(`datetime`)
                    order by `datetime` desc """
        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getShapes(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select shape 
                    from sighting s 
                    where shape != ''
                    and year(`datetime`) = %s
                    group by shape 
                    order by shape asc """
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(anno, shape):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                from sighting s 
                where year(`datetime`)=%s and shape = %s"""
        cursor.execute(query, (anno, shape))
        for row in cursor:
            result.append(Sighting(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(anno, shape, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT s1.id AS id1, s2.id AS id2
                FROM sighting s1, sighting s2
                WHERE s1.state = s2.state
                  AND s1.id != s2.id
                  AND YEAR(s1.datetime) = %s
                  AND YEAR(s2.datetime) = %s
                  AND s1.shape = %s
                  AND s2.shape = %s
                  AND s1.datetime < s2.datetime"""
        cursor.execute(query, (anno, anno, shape, shape))
        for row in cursor:
            result.append((idMap[row["id1"]], idMap[row["id2"]]))
        cursor.close()
        conn.close()
        return result

