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