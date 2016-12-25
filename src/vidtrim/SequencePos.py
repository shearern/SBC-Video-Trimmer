from .TimePos import TimePos
from .VideoPos import VideoPos

class SequencePos(TimePos):
    '''Position within a sequence of videos'''

    def __init__(self, sequence, sec=None, ms=None):
        self.__seq = sequence
        super(SequencePos, self).__init__(sec, ms)


    def __add__(self, other):
        try:
            return SequencePos(self.__seq, sec=self.seconds + other.seconds)
        except AttributeError:
            raise Exception("Can't add %s to %s" % (
                other.__class__.__name__,
                self.__class__.__name__))


    @property
    def video_pos(self):
        '''Position in the video'''

        offset = self.seconds

        # TODO: Cold probably speed this up
        # Find which video we're in
        for video in self.__seq.videos:
            if video.duration.seconds < offset:
                offset -= video.duration.seconds
            else:
                return VideoPos(video, sec=offset)