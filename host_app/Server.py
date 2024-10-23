import socket
import threading
import os

serverRunning = True
def runServer():
    global serverRunning

    serverRunning = True
    host='127.0.0.1'
    port=12345
    filename='movie.mp4'
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
            print(f'Connection from {clientAddress}')
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
        except:
            pass
        finally:
            if connection is not None:
                connection.close()

def startServer():
    serverThread = threading.Thread(target=runServer)
    serverThread.start()

def stopServer():
    global serverRunning
    serverRunning = False