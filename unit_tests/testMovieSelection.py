import unittest
import sys, os
from unittest.mock import patch
from PyQt6.QtWidgets import *
from PIL import Image
sys.path.append('../client_app')
from MovieSelection import MovieSelectionScreen

class TestMovieSelection(unittest.TestCase):
    app = QApplication(sys.argv)
    @patch('socket.socket.connect')
    @patch('socket.socket.sendall')
    @patch('socket.socket.send')
    @patch('socket.socket.recv')
    @patch('pickle.loads')
    @patch('PIL.Image.open')
    @patch('PIL.Image.Image.save')
    def testGetMovies(self, mockImageSave, mockImageOpen, mockPickleLoad, mockRecv, mockSend, mockSendAll, mockConnect):
        # Change the directory to help with ui file issues
        os.chdir('../client_app')
        
        # Mock functions
        mockConnect.return_value = None
        mockSendAll.return_value = None
        mockSend.return_value = None
        mockRecv.return_value = b'10'
        mockPickleLoad.return_value = ['a']
        mockImageOpen.return_value = Image.Image()
        mockImageSave.return_value = None
        print(mockPickleLoad)

        # Set up object
        movieSelectionObj = MovieSelectionScreen()

        # Verify return value
        self.assertEqual(movieSelectionObj.getMovies(), {'movies': ['a'], 'coverImages': ['a.png']})

        
    def testUpdateMovies(self):
        pass

if __name__ == '__main__':
    unittest.main()