import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'MyMediaData.db')

def getMovieVideoPath(movieID):
    # Gets the filepath of a movie given its id
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute(f'SELECT videoPath FROM coreInfo WHERE ID={movieID}')
    path = res.fetchall()[0]
    con.close()
    return path[0]

def getMovieAudioPath(movieID):
    # Gets the filepath of a movie given its id
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute(f'SELECT audioPath FROM coreInfo WHERE ID={movieID}')
    path = res.fetchall()[0]
    con.close()
    return path[0]

def getMovieList():
    # Returns a list of movie names from the database

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute(f'SELECT title FROM coreInfo WHERE type="movie"')
    movieList = res.fetchall()
    con.close()
    return [movie[0] for movie in movieList]

def getMovieIDList():
    # Returns a list of movie ids from the database

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute(f'SELECT ID FROM coreInfo WHERE type="movie"')
    movieIDList = res.fetchall()
    con.close()
    return [movieID[0] for movieID in movieIDList]
    
def getMovieImageList():
    # Returns a list of movie image paths from the database
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute(f'SELECT imagePath FROM coreInfo WHERE type="movie"')
    movieImageList = res.fetchall()
    con.close()
    return [movieImage[0] for movieImage in movieImageList]
