from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import math
import Constants

MOVIE_TABLE_COLUMN_COUNT = 5

class MovieSelectionScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/movieSelection.ui", self)

    def updateMovies(self):
        # Updates the displayed movie table
        movieInfo = self.getMovies()
        movieList = movieInfo['movies']
        movieImages = movieInfo['coverImages']
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
        return {'movies':['Spiderman', 'Transformers', 'Harry Potter and the Sorcerer\'s Stone', 'Jurassic Park', 'The Dark Knight', 'Cars', 'Cars 2', 'Interstellar', 'Airbud', 'The Princess Bride'], 
                'coverImages': ['spiderman.png', 'transformers.png', 'harry_potter.png', 'jurassic_park.png', 'dark_knight.png', 'cars.png', 'cars_2.png', 'interstellar.png', 'airbud.jpg', 'princess_bride.jpg']}

