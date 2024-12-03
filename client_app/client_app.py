import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Login import LoginScreen
from HomeScreen import HomeScreen
from WatchMovie import WatchMovieScreen
from audio_player import AudioPlayer
import Constants
from time import sleep


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/pages.ui', self)

        self.setWindowTitle("MyMedia Client")
        self.setFixedSize(QSize(900, 600))

        # Add widgets to stacked widget
        self.loginScreen = LoginScreen()
        self.stackedWidget.addWidget(self.loginScreen) # add each screen to the QStackedWidget

        self.homeScreen = HomeScreen()
        self.stackedWidget.addWidget(self.homeScreen)

        self.watchMovieScreen = WatchMovieScreen()
        self.stackedWidget.addWidget(self.watchMovieScreen)

        self.audioPlayerScreen = AudioPlayer()
        self.stackedWidget.addWidget(self.audioPlayerScreen)

        # Connect buttons
        self.loginScreen.loginButton.clicked.connect(self.loginButtonClicked) # clicking login button takes you to movie selection screen
        self.homeScreen.logoutButton.clicked.connect(self.logoutButtonClicked)
        self.watchMovieScreen.homeButton.clicked.connect(self.homeButtonClicked)
        self.audioPlayerScreen.homeButton.clicked.connect(self.homeButtonClicked)
        self.homeScreen.playButton.clicked.connect(self.playButtonClicked)
        

    def goToHome(self):
        # Sets the current page to the home page
        self.stackedWidget.setCurrentIndex(Constants.HOME_SCREEN_INDEX)

    def goToLogin(self):
        # Sets the current page to the login page
        self.stackedWidget.setCurrentIndex(Constants.LOGIN_SCREEN_INDEX)
    
    def goToWatchMovie(self):
        # Sets the current page to the watch movie page
        self.stackedWidget.setCurrentIndex(Constants.WATCH_MOVIE_SCREEN_INDEX)

    def goToAudioPlayer(self):
        # Sets the current page to the watch movie page
        self.stackedWidget.setCurrentIndex(Constants.AUDIO_PLAYER_SCREEN_INDEX)

    def loginButtonClicked(self):
        # This will eventually handle accounts and whatnot
        self.loginScreen.usernameEdit.clear()
        # Show the movies selection screen upon logging in
        self.homeScreen.showMovies()
        self.homeScreen.updateContent()
        self.goToHome()
    
    def logoutButtonClicked(self):
        # Logs out
        self.goToLogin()

    def playButtonClicked(self):
        # Retrieves selected movie and goes to watch movie screen
        selectedItemID = self.homeScreen.getSelectedItemID()
        if selectedItemID >= 0: 
            if self.homeScreen.stackedWidget.currentIndex() == Constants.MOVIE_SELECTION_SCREEN_INDEX:
                self.watchMovieScreen.getMovie(selectedItemID)
                self.watchMovieScreen.playButton.setText('Play')
                sleep(1)
                self.goToWatchMovie()
            elif self.homeScreen.stackedWidget.currentIndex() == Constants.MUSIC_SELECTION_SCREEN_INDEX:
                self.audioPlayerScreen.getSong(selectedItemID)
                self.watchMovieScreen.playButton.setText('Play')
                sleep(1)
                self.goToAudioPlayer()

    def homeButtonClicked(self):
        self.goToHome()

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    w = MainWindow() # Create main window
    w.show() # displays the window
    app.exec() # execute the app