from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from time import sleep
import socket
import tempfile

class WatchMovieScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/watchMovie.ui", self)

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.moviePlayer)
        self.playButton.clicked.connect(self.playButtonClicked)
        self.fullScreenButton.setShortcut(QKeySequence(Qt.Key.Key_Escape))
        self.fullScreenButton.clicked.connect(self.fullScreenButtonClicked)

        # Movie slider things
        self.player.durationChanged.connect(self.durationChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.movieSlider.sliderMoved.connect(self.setPosition)

        

    def fullScreenButtonClicked(self):
        if self.moviePlayer.isFullScreen():
            self.moviePlayer.setFullScreen(False)
        else:
            self.moviePlayer.setFullScreen(True)

    def playButtonClicked(self):
        # Handles the pause/play button functionality
        if self.player.isPlaying():
            self.player.pause()
            self.playButton.setText('Play')
        else:
            self.player.play()
            self.playButton.setText('Pause')

    def getMovie(self, movieID):
        # Retrieves the selected movie
        
        host='127.0.0.1'
        port=12345

        # Create a TCP/IP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        clientSocket.sendall(b'getMovieVideo')
        clientSocket.send(str(movieID).encode())
        # Read file size
        fileSize = int(clientSocket.recv(1024).decode().strip())
        receivedData = bytearray()

        while len(receivedData) < fileSize:
            data = clientSocket.recv(1024)
            if not data:
                break
            receivedData.extend(data)

        # Save the received data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tempFile:
            tempFile.write(receivedData)
            tempFilePath = tempFile.name
        
        self.player.setSource(QUrl.fromLocalFile(tempFilePath))

    def setPosition(self, position):
        # Sets the movie position based on the slider
        self.player.setPosition(position)

    def positionChanged(self, position):
        # Sets the slider position based on the movie position
        self.movieSlider.setValue(position)
    
    def durationChanged(self, duration):
        # Changes the movie slider range based on the movie's duration
        self.movieSlider.setRange(0, duration)

    def stopMovie(self):
        self.player.stop()


        