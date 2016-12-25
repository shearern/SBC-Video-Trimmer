from .SequencePos import SequencePos

class VideoSequence(object):
    '''A sequence of video files'''

    def __init__(self):
        self.__videos = list()


    def add(self, video):
        self.__videos.append(video)



    @property
    def duration(self):
        if len(self.__videos) == 0:
            return None
        dur = SequencePos(self, 0)
        for video in self.__videos:
            dur += video.duration
        return dur