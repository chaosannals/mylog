import sys
from multiprocessing import freeze_support
from PySide6.QtWidgets import QApplication
from mylog.view.mainwindow import MainWindow

def init_log():
    '''
    
    '''

def main():
    '''
    
    '''

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec()

if __name__ == '__main__':
    freeze_support()
    init_log()
    main()
    