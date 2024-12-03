from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import os, sys
sys.path.append(os.path.abspath(os.path.join('..')))
import Database.DatabaseFunctions as db


class AddMedia(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/addMedia.ui", self)

        self.media_type_dropdown.addItem("Song")
        self.media_type_dropdown.addItem("Movie")
        self.select_media_btn.clicked.connect(self.selectMediaFile)
        self.select_image_btn.clicked.connect(self.selectImageFile)
        self.upload_btn.clicked.connect(self.uploadFile)

    def selectMediaFile(self):
        if self.media_type_dropdown.currentText() == 'Song':
            file_path, _ = QFileDialog.getOpenFileName(self, filter="*.mp3")
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, filter="*.mp4")
        if file_path:
            self.media_path.setText(file_path)

    def selectImageFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, filter="*.png *.jpg")
        if file_path:
            self.media_image_path.setText(file_path)

    def uploadFile(self):
        mediaTitle = self.media_title.text()
        filePath = self.media_path.text()
        fileImagePath = self.media_image_path.text()

        if  (
            len(mediaTitle) > 0 and len(filePath) > 0 and len(fileImagePath) > 0
            and os.path.isfile(filePath) and os.path.isfile(fileImagePath)
            ):
            if self.media_type_dropdown.currentText() == 'Song':
                db.addSong(mediaTitle, filePath, fileImagePath)
                dlg = QDialog(self)
                l1 = QLabel(dlg)
                l1.setText("Successfully uploaded a song!")
                l1.move(20,50)
                b1 = QPushButton("OK", dlg)
                b1.move(60,75)
                b1.clicked.connect(dlg.accept)
                dlg.setFixedWidth(200)
                dlg.exec()
            else:
                db.addMovie(mediaTitle, filePath, fileImagePath)
                dlg = QDialog(self)
                l1 = QLabel(dlg)
                l1.setText("Successfully uploaded a movie!")
                l1.move(20,50)
                b1 = QPushButton("OK", dlg)
                b1.move(60,75)
                b1.clicked.connect(dlg.accept)
                dlg.setFixedWidth(200)
                dlg.exec()