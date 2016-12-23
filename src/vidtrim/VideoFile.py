import os

from .ffprobe import get_file_data
from .VideoTS import VideoTS

class VideoFile(object):
    '''A vido file'''


    def __init__(self, path):
        self.__path = path
        self.__data = None


    @property
    def path(self):
        return self.__path


    @property
    def filename(self):
        return os.path.basename(self.path)


    @property
    def data(self):
        '''Data about this file'''
        if self.__data is None:
            self.__data = get_file_data(self.path)
        return self.__data


    @property
    def framerate(self):
        return self.data.framerate


    @property
    def duration(self):
        '''
        Duration of this video clip

        :return: VideoTS
        '''
        return VideoTS(
            framerate = self.framerate,
            time_sec = self.data.duration_sec)