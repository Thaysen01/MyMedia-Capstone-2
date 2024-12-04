import socket
import threading
import sys, os
import pickle
sys.path.append(os.path.abspath(os.path.join('..')))
import Database.DatabaseFunctions as db

serverRunning = True
def runServer():
    global serverRunning

    serverRunning = True
    host='0.0.0.0'
    port=12345
    #Currently need to convert mp4 file to mp3 and have both in the folder. These should be stored on the device outside of these folders ig, 
    #...Filename="..\..\..\..\Videos\Created Videos\FirstCastedRLSnT.mp4" #location on device
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
            clientChoice = ''
            data = b''
            while data != b'\n':
                data = connection.recv(1)
                if data != b'\n':
                    clientChoice += data.decode().strip()
            # clientChoice = (connection.recv(1024).decode().strip())

            # Handle a get movie list/picture request
            if clientChoice == 'getMovies':
                print('Sending Movie list')
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

            # Handle a get movie list/picture request
            elif clientChoice == 'getMusic':
                print('Sending Movie list')
                songIDList = db.getSongIDList()
                songList = db.getSongList()
                connection.sendall(pickle.dumps(songIDList))
                connection.sendall(pickle.dumps(songList))

            # Handle a get movie video/audio request
            elif clientChoice == 'getMovieVideo':
                print(f'Connection from {clientAddress} requesting movie')
                movieID = int(connection.recv(1024).decode())
                print(movieID)
                videoFilename = db.getMovieVideoPath(movieID)
                # Send video file
                send_file(connection, videoFilename)
            
            elif clientChoice == 'getSong':
                print(f'Connection from {clientAddress}')
                songID = int(connection.recv(1024).decode())
                audioFilename = db.getSongAudioPath(songID)
                songImageName = db.getSongImage(songID)
                # Send audio file
                send_file(connection, audioFilename)    
                send_file(connection, songImageName)   

        except Exception as e:
            print(e)
        finally:
            if connection is not None:
                connection.close()

def send_file(connection, filename):
    """Helper function to send a file over a socket connection."""
    with open(filename, 'rb') as f:
        fileSize = os.path.getsize(filename)
        print(f"Sending '{filename}' with size {fileSize}")
        
        # Send the file size as a 4-byte integer (big-endian)
        connection.sendall(fileSize.to_bytes(4, byteorder='big'))

        # Send the file data
        while True:
            data = f.read(1024)
            if not data:
                break
            connection.sendall(data)

def startServer():
    serverThread = threading.Thread(target=runServer)
    serverThread.start()

def stopServer():
    global serverRunning
    serverRunning = False