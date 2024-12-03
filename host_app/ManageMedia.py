from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import os, sys
sys.path.append(os.path.abspath(os.path.join('..')))
import Database.DatabaseFunctions as db

class ViewMedia(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/viewMedia.ui", self)

        self.mediaInfoList = []
        self.mediaList.setHorizontalHeaderLabels(['Type', 'Title'])
        self.mediaList.horizontalHeader().resizeSection(0,50)
        self.mediaList.horizontalHeader().resizeSection(1,578)
        self.mediaList.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.mediaList.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.remove_btn.clicked.connect(self.removeMedia)

    def removeMedia(self):
        if len(self.mediaList.selectedItems()) > 0:
            mediaIndexToRemove = self.mediaInfoList[self.mediaList.currentRow()][0]
            print(mediaIndexToRemove)
            db.removeMedia(mediaIndexToRemove)
            self.updateMediaList()

    def updateMediaList(self):
        self.mediaInfoList = db.getMediaList()
        self.mediaList.setRowCount(len(self.mediaInfoList))
        for i in range(len(self.mediaInfoList)):
            self.mediaList.setItem(i, 0, QTableWidgetItem())
            self.mediaList.setItem(i, 1, QTableWidgetItem())
            self.mediaList.item(i, 0).setText(self.mediaInfoList[i][1])
            self.mediaList.item(i, 1).setText(self.mediaInfoList[i][2])