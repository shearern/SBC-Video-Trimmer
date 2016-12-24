

class VideoSequence(object):
    '''A sequence of video files'''

    def __init__(self):
        self.__videos = list()


    def add(self, video):
        self.__videos.append(video)