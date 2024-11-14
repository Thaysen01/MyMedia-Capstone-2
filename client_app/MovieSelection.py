from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import math
import Constants
import socket
import pickle
from PIL import Image
import io
import os

MOVIE_TABLE_COLUMN_COUNT = 5

class MovieSelectionScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/movieSelection.ui", self)

        self.movieInfo = {}

    def updateMovies(self):
        # Updates the displayed movie table
        self.movieInfo = self.getMovies()
        movieList = self.movieInfo['movies']
        movieImages = self.movieInfo['coverImages']
        movieTable = self.tabWidget.widget(0).children()[0]
        movieTable.setRowCount(math.ceil(len(movieList) / MOVIE_TABLE_COLUMN_COUNT))
        movieTable.setColumnCount(MOVIE_TABLE_COLUMN_COUNT)

        for i in range(len(movieList)):
            # Implement movie poster
            image = QLabel()
            image.setScaledContents(True)
            pixmap = QPixmap('movie_images/' + movieImages[i])
            image.setPixmap(pixmap)
            image.setStyleSheet('padding :3px')

            # Implement movie title
            text = QLabel()
            if len(movieList[i]) > Constants.MAX_MOVIE_TITLE_LENGTH:
                text.setText(movieList[i][0:Constants.MAX_MOVIE_TITLE_LENGTH - 3] + '...')
            else:
                text.setText(movieList[i])
            
            # Combine title with poster
            imageWithTextLayout = QVBoxLayout()
            imageWithTextLayout.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)
            imageWithTextLayout.addWidget(text, alignment=Qt.AlignmentFlag.AlignCenter)
            imageWithText = QWidget()
            imageWithText.setLayout(imageWithTextLayout)

            # set the table to show the poster and title
            movieTable.setCellWidget(i // MOVIE_TABLE_COLUMN_COUNT, i % MOVIE_TABLE_COLUMN_COUNT, imageWithText)            

    def getMovies(self):
        # Gets the list of uploaded movies from the host app

        # Create image folder if it does not already exist
        if not os.path.exists("movie_images"):
            os.makedirs("movie_images")

        # Set connection variables    
        host='127.0.0.1'
        port=12345

        # Create a TCP/IP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        clientSocket.sendall(b'getMovies\n')
        data = clientSocket.recv(1024)
        movieIDList = pickle.loads(data)
        data = clientSocket.recv(1024)
        movies = pickle.loads(data)

        coverImages = []

        # Receive the movie image files and store them locally
        for movie in movies:
            data = clientSocket.recv(1024)
            print(data)
            fileSize = int(data.decode().strip())
            receivedData = bytearray()

            # Send ready to receive signal
            clientSocket.send(b'a')

            # receive image
            while len(receivedData) < fileSize:
                data = clientSocket.recv(1024)
                if not data:
                    break
                receivedData.extend(data)
                
            # set up image file/file list
            fileName = movie.replace(' ', '_') + '.png'
            coverImages.append(fileName)
            filePath = 'movie_images/' + fileName
            print(len(receivedData))
            image = Image.open(io.BytesIO(receivedData))
            image.save(filePath)
        clientSocket.close()
        retVal = {'movies': movies, 'coverImages': coverImages, 'movieIDList': movieIDList}
        return retVal

    def getSelectedMovieID(self):
        movieTable = self.tabWidget.widget(0).children()[0]
        movieIndex = movieTable.currentRow() * movieTable.columnCount() + movieTable.currentColumn()
        if movieIndex >= 0:
            return self.movieInfo['movieIDList'][movieIndex]
        return -1
