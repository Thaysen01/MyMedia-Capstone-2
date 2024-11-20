from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import math
import socket
import pickle

#MUSIC_TABLE_COLUMN_COUNT = 1

class MusicSelectionScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/musicSelection.ui", self)

        self.musicInfo = {}

    def updateMusic(self):
        # Updates the displayed music table
        self.musicInfo = self.getMusic()
        musicList = self.musicInfo["songs"]
        musicTable = self.tabWidget.widget(0).children()[0]
        musicTable.setRowCount(math.ceil(len(musicList)))
        musicTable.setColumnCount(1)

        for i in range(len(musicList)):
            musicTable.setItem(i, 0, QTableWidgetItem())
            musicTable.item(i, 0).setText(musicList[i])
        
    def getMusic(self):
        # Gets the list of uploaded music from the host app

        # Set connection variables    
        host='127.0.0.1'
        port=12345

        # Create a TCP/IP socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        clientSocket.sendall(b'getMusic\n')
        data = clientSocket.recv(1024)
        songIDList = pickle.loads(data)
        data = clientSocket.recv(1024)
        songs = pickle.loads(data)
                
        clientSocket.close()
        retVal = {'songs': songs, 'songIDList': songIDList}
        return retVal