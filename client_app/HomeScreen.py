from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from MovieSelection import MovieSelectionScreen
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


        # Connect buttons
        self.moviesButton.clicked.connect(self.showMovies)
        self.musicButton.clicked.connect(self.showMusic)
        self.refreshButton.clicked.connect(self.updateContent)

    def showMovies(self):
        self.movieSelection.tabWidget.setCurrentIndex(Constants.LIBRARY_INDEX)
        self.stackedWidget.setCurrentIndex(Constants.MOVIE_SELECTION_SCREEN_INDEX)

    def showMusic(self):
        self.musicSelection.tabWidget.setCurrentIndex(Constants.LIBRARY_INDEX)
        self.stackedWidget.setCurrentIndex(Constants.MUSIC_SELECTION_SCREEN_INDEX)


    def updateContent(self):
        self.movieSelection.updateMovies()
        self.musicSelection.updateMusic()

    def getSelectedItemID(self):
        selectedItemID = -1
        if self.stackedWidget.currentIndex() == Constants.MOVIE_SELECTION_SCREEN_INDEX:
            selectedItemID = self.movieSelection.getSelectedMovieID()
        elif self.stackedWidget.currentIndex() == Constants.MUSIC_SELECTION_SCREEN_INDEX:
            selectedItemID = self.musicSelection.getSelectedSongID()
        if selectedItemID >= 0:
            return selectedItemID
        return -1
