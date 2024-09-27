from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import math

#MUSIC_TABLE_COLUMN_COUNT = 1

class MusicSelectionScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/musicSelection.ui", self)

    def updateMusic(self):
        # Updates the displayed music table
        musicList = self.getMusic()
        musicTable = self.tabWidget.widget(0).children()[0]
        musicTable.setRowCount(math.ceil(len(musicList)))
        musicTable.setColumnCount(1)

        for i in range(len(musicList)):
            print(i)
            musicTable.setItem(i, 0, QTableWidgetItem())
            musicTable.item(i, 0).setText(musicList[i])
        

    def getMusic(self):
        # Gets the list of uploaded music from the host app
        return ['Flowers', 'Greedy', 'Die for You', 'Birds of a Feather', 'Dancing in the Flames', 'Taste']