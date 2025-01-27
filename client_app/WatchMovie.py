from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QEvent, QUrl
from PyQt6 import uic
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
import socket
import tempfile
import Constants
import os

class WatchMovieScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/watchMovie.ui", self)

        # Video player setup
        self.video_player = QMediaPlayer()
        self.video_player.setVideoOutput(self.moviePlayer)
        self.playButton.clicked.connect(self.playButtonClicked)
        self.fullScreenButton.clicked.connect(self.fullScreenButtonClicked)

        # Install event filter on both moviePlayer and self
        self.moviePlayer.installEventFilter(self)
        self.installEventFilter(self)

        # Movie slider setup
        self.video_player.durationChanged.connect(self.durationChanged)
        self.video_player.positionChanged.connect(self.positionChanged)
        self.movieSlider.sliderMoved.connect(self.setPosition)

        # Audio output setup
        self.audio_output = QAudioOutput()
        self.video_player.setAudioOutput(self.audio_output)

        # Volume slider setup (changed to align with UI)
        self.audioSlider.valueChanged.connect(self.changeVolume)
        self.audioSlider.setRange(0, 100)  # Slider range: 0 to 100
        self.audioSlider.setValue(int(self.audio_output.volume() * 100))  # Set initial volume

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        # Initialize fullscreen video widget
        self.fullscreenPlayer = None

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            if self.fullscreenPlayer is not None:
                self.exitFullScreen()
                return True  # Event handled
        return super().eventFilter(source, event)

    def fullScreenButtonClicked(self):
        if self.fullscreenPlayer is None:
            self.enterFullScreen()
        else:
            self.exitFullScreen()

    def enterFullScreen(self):
        # Create a new video widget for fullscreen
        self.fullscreenPlayer = QVideoWidget()
        self.fullscreenPlayer.setWindowFlags(Qt.WindowType.Window)
        self.fullscreenPlayer.showFullScreen()
        self.fullscreenPlayer.installEventFilter(self)
        # Switch the video output to the fullscreen widget
        self.video_player.setVideoOutput(self.fullscreenPlayer)
        # Ensure the audio output remains set
        self.video_player.setAudioOutput(self.audio_output)

    def exitFullScreen(self):
        # Switch the video output back to the original widget
        self.video_player.setVideoOutput(self.moviePlayer)
        # Remove the fullscreen widget
        self.fullscreenPlayer.hide()
        self.fullscreenPlayer.deleteLater()
        self.fullscreenPlayer = None

    def playButtonClicked(self):
        # Handles the pause/play button functionality
        if self.video_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.video_player.pause()
            self.playButton.setText('Play')
        else:
            self.video_player.play()
            self.playButton.setText('Pause')

    def getMovie(self, movieID):
        # Retrieves the selected movie

        host = Constants.host
        port = 12345

        # Create a TCP/IP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        clientSocket.sendall(b'getMovieVideo\n')
        clientSocket.sendall((str(movieID) + '\n').encode())

        # Receive video file
        video_file_data = self.receive_file(clientSocket)
        video_temp_path = self.save_file_to_temp(video_file_data, '.mp4')

        # Set media source
        self.video_player.setSource(QUrl.fromLocalFile(video_temp_path))

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

    def setPosition(self, position):
        # Sets the movie position based on the slider
        self.video_player.setPosition(position)

    def positionChanged(self, position):
        # Sets the slider position based on the movie position
        self.movieSlider.setValue(position)

    def durationChanged(self, duration):
        # Changes the movie slider range based on the movie's duration
        self.movieSlider.setRange(0, duration)

    def changeVolume(self, value):
        # Adjust the volume of the audio output
        self.audio_output.setVolume(value / 100.0)

    def stopMovie(self):
        self.video_player.stop()
