from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from MovieSelection import MovieSelectionScreen
from BookSelection import BookSelectionScreen
from MusicSelection import MusicSelectionScreen
import Constants

class HomeScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/homeScreen.ui", self)

        # Add pages to stacked widget / last to be run = starting screen
        self.movieSelection = MovieSelectionScreen()
        self.stackedWidget.addWidget(self.movieSelection) 

        self.musicSelection = MusicSelectionScreen()
        self.stackedWidget.addWidget(self.musicSelection)

        self.bookSelection = BookSelectionScreen()
        self.stackedWidget.addWidget(self.bookSelection)

        # Connect buttons
        self.moviesButton.clicked.connect(self.showMovies)
        self.musicButton.clicked.connect(self.showMusic)
        self.booksButton.clicked.connect(self.showBooks)

    def showMovies(self):
        self.movieSelection.tabWidget.setCurrentIndex(Constants.LIBRARY_INDEX)
        self.stackedWidget.setCurrentIndex(Constants.MOVIE_SELECTION_SCREEN_INDEX)

    def showMusic(self):
        self.musicSelection.tabWidget.setCurrentIndex(Constants.LIBRARY_INDEX)
        self.stackedWidget.setCurrentIndex(Constants.MUSIC_SELECTION_SCREEN_INDEX)

    def showBooks(self):
        self.bookSelection.tabWidget.setCurrentIndex(Constants.LIBRARY_INDEX)
        self.stackedWidget.setCurrentIndex(Constants.BOOK_SELECTION_SCREEN_INDEX)

    def updateContent(self):
        self.movieSelection.updateMovies()
        self.musicSelection.updateMusic()

    def getSelectedItemID(self):
        selectedItemID = -1
        if self.stackedWidget.currentIndex() == Constants.MOVIE_SELECTION_SCREEN_INDEX:
            selectedItemID = self.movieSelection.getSelectedMovieID()
        if selectedItemID >= 0:
            return selectedItemID
        return -1
