import sqlite3

def getMoviePath(movieID):
    # Gets the filepath of a movie given its id

    con = sqlite3.connect('MyMediaData.db')
    cur = con.cursor()
    res = cur.execute(f'SELECT filePath FROM coreInfo WHERE ID={movieID}')
    path = res.fetchall()[0]
    con.close()
    return path

def getMovieList():
    # Returns a list of movie names from the database

    con = sqlite3.connect('MyMediaData.db')
    cur = con.cursor()
    res = cur.execute(f'SELECT movieName FROM movies')
    movieList = res.fetchall()[0]
    con.close()
    return list(movieList[0])

def getMovieIDList():
    # Returns a list of movie ids from the database

    con = sqlite3.connect('MyMediaData.db')
    cur = con.cursor()
    res = cur.execute(f'SELECT ID FROM movies')
    movieIDList = res.fetchall()[0]
    con.close()
    return list(movieIDList[0])
    
def getMovieImageList():
    # Returns a list of movie image paths from the database
    
    con = sqlite3.connect('MyMediaData.db')
    cur = con.cursor()
    res = cur.execute(f'SELECT imagePath FROM movies')
    movieImageList = res.fetchall()[0]
    con.close()
    return list(movieImageList[0])
