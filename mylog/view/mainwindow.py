from PySide6.QtWidgets import QMainWindow
from .mainwindow_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    '''
    
    '''

    def __init__(self, parent=None):
        '''
        
        '''

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
