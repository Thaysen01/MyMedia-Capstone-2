from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from time import sleep
import socket
import tempfile
from PIL import Image
import io
import os

class AudioPlayer(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/audioPlayer.ui", self)

        self.audioPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.audioPlayer.setAudioOutput(self.audioOutput)
        self.playButton.clicked.connect(self.playButtonClicked)

        # Movie slider things
        self.audioPlayer.durationChanged.connect(self.durationChanged)
        self.audioPlayer.positionChanged.connect(self.positionChanged)
        self.movieSlider.sliderMoved.connect(self.setPosition)

        

    def playButtonClicked(self):
        # Handles the pause/play button functionality
        if self.audioPlayer.isPlaying():
            self.audioPlayer.pause()
            self.playButton.setText('Play')
        else:
            self.audioPlayer.play()
            self.playButton.setText('Pause')

    def getSong(self, songID):
        # Retrieves the selected movie and audio
        
        host='127.0.0.1'
        port=12345

        # Create a TCP/IP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        clientSocket.sendall(b'getSong\n')
        clientSocket.sendall((str(songID) + '\n').encode())
        
        # Receive audio file
        audio_file_data = self.receive_file(clientSocket)
        album_file_data = self.receive_file(clientSocket)
        audio_temp_path = self.save_file_to_temp(audio_file_data, '.mp3')
        album_temp_path = self.save_file_to_temp(album_file_data, '.png')
        
        # Set album cover
        self.albumCover.setScaledContents(True)
        self.albumCover.setPixmap(QPixmap(album_temp_path))

        # Set audio source
        audio_url = QUrl.fromLocalFile(audio_temp_path)
        if audio_url.isValid():
            self.audioPlayer.setSource(audio_url)

    def setPosition(self, position):
        # Sets the movie position based on the slider
        self.audioPlayer.setPosition(position)

    def positionChanged(self, position):
        # Sets the slider position based on the movie position
        self.movieSlider.setValue(position)
    
    def durationChanged(self, duration):
        # Changes the movie slider range based on the movie's duration
        self.movieSlider.setRange(0, duration)

    def stopMovie(self):
        self.audioPlayer.stop()

    def receive_file(self, clientSocket):
        # Helper function to receive a file from the server
        # Receive the file size (assuming it's sent as a 4-byte integer)
        file_size_data = clientSocket.recv(4)  # Receive the first 4 bytes for the file size
        if len(file_size_data) < 4:
            raise ValueError("Failed to receive file size")
        
        fileSize = int.from_bytes(file_size_data, byteorder='big')  # Convert the 4 bytes to an integer
        
        receivedData = bytearray()

        # Receive the actual file data
        while len(receivedData) < fileSize:
            data = clientSocket.recv(1024)
            if not data:
                break
            receivedData.extend(data)

        return receivedData

    def save_file_to_temp(self, file_data, extension):
        # Helper function to save the received file data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tempFile:
            tempFile.write(file_data)
            tempFilePath = tempFile.name
        
        return tempFilePath