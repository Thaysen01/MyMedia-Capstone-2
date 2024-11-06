import socket
import threading
import sys, os
import pickle
sys.path.append(os.path.abspath(os.path.join('..', 'config')))

import Database.DatabaseFunctions as db

serverRunning = True
def runServer():
    global serverRunning

    serverRunning = True
    host='127.0.0.1'
    port=12345
    # Create a TCP/IP socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(1)
    serverSocket.settimeout(1)
    
    print(f'Server listening on {host}:{port}')

    while serverRunning:
        connection = None
        try:
            connection, clientAddress = serverSocket.accept()
            clientChoice = 'getMovies'
            clientChoice = (connection.recv(1024).decode().strip())

            # Handle a get movie list/picture request
            if clientChoice == 'getMovies':
                print('Sending Movie list')
                # this will be retrieved from the database
                movieIDList = db.getMovieIDList()
                movieList = db.getMovieList()
                movieImageList = db.getMovieImageList()
                connection.sendall(pickle.dumps(movieIDList))
                connection.sendall(pickle.dumps(movieList))

                # Send each movie image file
                for movieImage in movieImageList:
                    with open(movieImage, 'rb') as f:
                        # Send the file size first
                        fileSize = os.path.getsize(movieImage)
                        connection.sendall(str(fileSize).encode() + b'\n')

                        # Wait until receive ready to send
                        while connection.recv(1024) != b'a':
                            pass

                        # Send the file data
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            connection.sendall(data)         

            # Handle a get movie video/audio request
            elif clientChoice == 'getMovieVideo':
                movieID = int(connection.recv(1024).decode())
                print(f'Connection from {clientAddress}, sending movie id {movieID}')

                # Get filepath from database where movie id == movieID
                filename = db.getMoviePath(movieID)
                with open(filename, 'rb') as f:
                    # Send the file size first
                    fileSize = os.path.getsize(filename)
                    connection.sendall(str(fileSize).encode() + b'\n')

                    # Send the file data
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        connection.sendall(data)
        except Exception as e:
            print(e)
        finally:
            if connection is not None:
                connection.close()

def startServer():
    serverThread = threading.Thread(target=runServer)
    serverThread.start()

def stopServer():
    global serverRunning
    serverRunning = False