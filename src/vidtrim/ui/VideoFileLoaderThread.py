from PySide.QtCore import QThread, QObject, Signal, QTimer, Slot

from ..VideoFile import load_video_file


class VideoFileLoaderThread(QThread):
    '''Thread to load video file data and add to sequence'''

    loading_file = Signal(str)
    finished = Signal()

    def __init__(self, paths, sequence, parent=None):
        super(VideoFileLoaderThread, self).__init__(parent)

        self.__paths = paths
        self.__seq = sequence


    def run(self):
        for path in self.__paths:
            self.loading_file.emit(path)
            file = load_video_file(path)
            self.__seq.add(file)
        self.finished.emit()



