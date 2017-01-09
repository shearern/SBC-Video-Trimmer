import os

from vidtrim.ffmpeg.ffprobe import get_file_data
from VideoPos import VideoPos


class VideoFile(object):
    '''A video file'''


    def __init__(self, path, data):
        self.__path = path
        self.__data = data


    @property
    def path(self):
        return self.__path


    @property
    def filename(self):
        return os.path.basename(self.path)

    def __str__(self):
        return self.filename


    @property
    def data(self):
        '''Data about this file'''
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
        return VideoPos(self, sec = self.data.duration_sec)
    @property
    def dur(self):
        return self.duration


def load_video_file(path):
    '''Use ffprobe to get information about a video file'''
    data = get_file_data(path)
    return VideoFile(path, data)


