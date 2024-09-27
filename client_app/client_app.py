import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Login import LoginScreen
from HomeScreen import HomeScreen
import Constants


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

        # Connect buttons
        self.loginScreen.loginButton.clicked.connect(self.loginButtonClicked) # clicking login button takes you to movie selection screen
        self.homeScreen.logoutButton.clicked.connect(self.logoutButtonClicked)

    def goToHome(self):
        self.stackedWidget.setCurrentIndex(Constants.HOME_SCREEN_INDEX)

    def goToLogin(self):
        self.stackedWidget.setCurrentIndex(Constants.LOGIN_SCREEN_INDEX)

    def loginButtonClicked(self):
        # This will eventually handle accounts and whatnot
        self.loginScreen.usernameEdit.clear()
        self.loginScreen.passwordEdit.clear()
        self.homeScreen.showMovies()
        self.homeScreen.showMusic()
        self.homeScreen.updateContent()
        self.goToHome()
    
    def logoutButtonClicked(self):
        self.goToLogin()

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    w = MainWindow() # Create main window
    w.show() # displays the window
    app.exec() # execute the app