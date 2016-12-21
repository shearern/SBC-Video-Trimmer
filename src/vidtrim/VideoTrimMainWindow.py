from PySide.QtCore import *
from PySide.QtGui import *

from VideoTrimMainWindow_UI import Ui_VideoTrimMainWindow_UI

class VideoTrimMainWindow(QMainWindow, Ui_VideoTrimMainWindow_UI):

    def __init__(self, parent=None):
        super(VideoTrimMainWindow, self).__init__(parent=parent)
        self.setupUi(self)
