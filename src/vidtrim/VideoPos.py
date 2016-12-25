from .TimePos import TimePos

class VideoPos(TimePos):
    '''Position within a video'''

    def __init__(self, video, sec=None, ms=None):
        self.__video = video
        super(VideoPos, self).__init__(sec, ms)


    def __add__(self, other):
        try:
            return VideoPos(self.__video, sec=self.seconds + other.seconds)
        except AttributeError:
            raise Exception("Can't add %s to %s" % (
                other.__class__.__name__,
                self.__class__.__name__))


    def __str__(self):
        return "%s of %s" % (self.timecode, self.__video.filename)