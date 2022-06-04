import sqlalchemy
from sqlalchemy import create_engine
from pprint import pprint
engine = sqlalchemy.create_engine('postgresql://polina1:555@localhost:5432/singeralbum')
engine
con = engine.connect()

pprint(con.execute(
    """

    SELECT genre_id, COUNT(singer_id) FROM singergenre
    GROUP BY genre_id 
    ORDER BY genre_id
       

    """).fetchall())

pprint(con.execute(
    """

    SELECT COUNT(id) FROM track
    WHERE album_id = (
    SELECT id FROM album
    WHERE year IN (2019, 2021))
     


    """).fetchall())

pprint(con.execute(
    """

    SELECT album_id, ROUND(AVG(duration), 2) FROM track
    GROUP BY album_id
    ORDER BY album_id
    


    """).fetchall())

pprint(con.execute(
    """

    SELECT singer.name FROM singer
    RIGHT JOIN singeralbum
    ON singer.id = singeralbum.singer_id
    RIGHT JOIN album
    ON album.id = singeralbum.album_id
    WHERE NOT album.year = 2020
    

    """).fetchall())

pprint(con.execute(
    """

    SELECT collection.name FROM collection
    RIGHT JOIN collectiontrack
    ON collection.id = collectiontrack.collection_id
    RIGHT JOIN track
    ON track.id = collectiontrack.track_id
    RIGHT JOIN album
    ON album.id = track.album_id
    RIGHT JOIN singeralbum
    ON album.id = singeralbum.album_id
    RIGHT JOIN singer
    ON singer.id = singeralbum.singer_id
    WHERE singer.name iLIKE '%%NIRVANA%%'


    """).fetchall())

pprint(con.execute(
    """

    SELECT album.name FROM album
    LEFT JOIN singeralbum
    ON album.id = singeralbum.album_id
    LEFT JOIN singer
    ON singer.id = singeralbum.singer_id
    LEFT JOIN singergenre
    ON singer.id = singergenre.singer_id
    LEFT JOIN genre
    ON genre.id = singergenre.genre_id
    GROUP BY album.name
    HAVING COUNT(genre.name) > 1
    
    """).fetchall())

pprint(con.execute(
    """

    SELECT track.name FROM track
    RIGHT JOIN collectiontrack
    ON track.id = collectiontrack.track_id
    WHERE collectiontrack.track_id IS NULL

    """).fetchall())

pprint(con.execute(
    """

    SELECT singer.name FROM singer
    LEFT JOIN singeralbum
    ON singer.id = singeralbum.singer_id
    LEFT JOIN album
    ON album.id = singeralbum.album_id
    LEFT JOIN track 
    ON album.id = track.album_id
    GROUP BY singer.name, track.duration
    HAVING track.duration = (
    SELECT MIN(duration) FROM track)

    """).fetchall())


pprint(con.execute(
    """

    SELECT album.name FROM album
    RIGHT JOIN track
    ON album.id = track.album_id
    WHERE track.album_id IN (
    SELECT album_id FROM track
    GROUP BY album_id
    HAVING COUNT(id) = (
    SELECT COUNT(id) FROM track
    GROUP BY album_id
    ORDER BY COUNT LIMIT 1 ))
    ORDER BY album.name
    

    """).fetchall())