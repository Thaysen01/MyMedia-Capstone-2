from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import os, sys
sys.path.append(os.path.abspath(os.path.join('..')))
import Database.DatabaseFunctions as db


class HomeScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/homeScreen.ui", self)

        self.media_type_dropdown.addItem("Song")
        self.media_type_dropdown.addItem("Movie")
        self.select_media_btn.clicked.connect(self.selectMediaFile)
        self.select_image_btn.clicked.connect(self.selectImageFile)
        self.upload_btn.clicked.connect(self.uploadFile)

    def selectMediaFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, filter="*.mp4")
        if file_path:
            self.media_path.setText(file_path)

    def selectImageFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, filter="*.png")
        if file_path:
            self.image_path.setText(file_path)

    def uploadFile(self):
        if self.media_type_dropdown.currentText() == 'Song':
            pass
        else:
            pass