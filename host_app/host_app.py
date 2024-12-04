import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from HomeScreen import HomeScreen
from addMedia import AddMedia
from ManageMedia import ViewMedia
import Server
import Constants
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/pages.ui', self)

        self.setWindowTitle("MyMedia Host")
        self.setFixedSize(QSize(900, 600))
    
        
        # Add widgets to stacked widget
        self.homeScreen = HomeScreen()
        self.stackedWidget.addWidget(self.homeScreen) # add each screen to the QStackedWidget

        self.addMedia = AddMedia()
        self.stackedWidget.addWidget(self.addMedia)

        self.manageMediaScreen = ViewMedia()
        self.stackedWidget.addWidget(self.manageMediaScreen)

        # Connect buttons
        self.homeScreen.addMediaButton.clicked.connect(self.addMediaButtonClicked) # clicking add media button takes you to add media screen
        self.addMedia.back_btn.clicked.connect(self.goToHomeScreen)
        self.homeScreen.manageMediaButton.clicked.connect(self.goToManageMedia)
        self.manageMediaScreen.back_btn.clicked.connect(self.goToHomeScreen)

    def goToHomeScreen(self):
        self.stackedWidget.setCurrentIndex(Constants.HOME_SCREEN_INDEX)

    def goToAddMedia(self):
        self.stackedWidget.setCurrentIndex(Constants.ADD_MEDIA_SCREEN_INDEX)
    
    def addMediaButtonClicked(self):
        self.goToAddMedia()

    def goToManageMedia(self):
        self.manageMediaScreen.updateMediaList()
        self.stackedWidget.setCurrentIndex(Constants.MANAGE_MEDIA_SCREEN_INDEX)
    
if __name__ == '__main__': 
    Server.startServer()
    app = QApplication(sys.argv)
    w = MainWindow() # Create main window
    w.show() # displays the window
    app.exec() # execute the app
    Server.stopServer()