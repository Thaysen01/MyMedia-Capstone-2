from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import math

MOVIE_TABLE_COLUMN_COUNT = 5

class MovieSelectionScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/movieSelection.ui", self)

    def updateMovies(self):
        # Updates the displayed movie table
        movieList = self.getMovies()
        movieTable = self.tabWidget.widget(0).children()[0]
        movieTable.setRowCount(math.ceil(len(movieList) / MOVIE_TABLE_COLUMN_COUNT))
        movieTable.setColumnCount(MOVIE_TABLE_COLUMN_COUNT)

        for i in range(len(movieList)):
            print(i)
            movieTable.setItem(i // MOVIE_TABLE_COLUMN_COUNT, i % MOVIE_TABLE_COLUMN_COUNT, QTableWidgetItem())
            movieTable.item(i // MOVIE_TABLE_COLUMN_COUNT, i % MOVIE_TABLE_COLUMN_COUNT).setText(movieList[i])
        

    def getMovies(self):
        # Gets the list of uploaded movies from the host app
        return ['Spiderman', 'Spiderman 2', 'Spiderman 3', 'Batman Begins', 'The Dark Knight', 'The Dark Knight Rises']

