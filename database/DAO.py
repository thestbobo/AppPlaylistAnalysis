from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbumsDur(min_dur):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """SELECT a.AlbumId, a.Title , sum(t.Milliseconds) as totDurata
                    FROM track t, album a 
                    WHERE t.AlbumId = a.AlbumId 
                    group by a.AlbumId
                    HAVING totDurata > %s
        """

        cursor.execute(query, (min_dur,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAlbumsPlaylist(idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """SELECT DISTINCTROW t.AlbumId as a1, t2.AlbumId as a2
                    FROM track t, playlisttrack p, track t2, playlisttrack p2
                    WHERE t.AlbumId < t2.AlbumId 
                    and t.TrackId = p.TrackId
                    and t2.TrackId = p2.TrackId 
                    and p.PlaylistId = p2.PlaylistId 
            """

        cursor.execute(query)

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]], idMap[row["a2"]]))

        cursor.close()
        conn.close()

        return result