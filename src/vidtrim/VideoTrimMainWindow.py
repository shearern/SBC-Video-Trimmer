from PySide.QtCore import *
from PySide.QtGui import *

from .SourceFileChooserDialog import SourceFileChooserDialog

from .VideoTrimMainWindow_UI import Ui_VideoTrimMainWindow_UI

class VideoTrimMainWindow(QMainWindow, Ui_VideoTrimMainWindow_UI):

    def __init__(self, parent=None):
        super(VideoTrimMainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.source_chooser = SourceFileChooserDialog(parent=self)

        self.choose_source_files()


    def choose_source_files(self):
        self.source_chooser.exec_()