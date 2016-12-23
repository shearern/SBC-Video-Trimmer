

class VideoTS(object):
    '''Represent a time in a video'''

    def __init__(self, framerate, time_sec):
        '''
        :param framerate: Number of frames per second
        :param time_sec: Number of seconds into file
        '''
        self.__framerate = framerate
        self.__sec = time_sec


    @property
    def ms(self):
        '''Number of miliseconds'''
        return float(self.__sec) * 1000


    @property
    def frames(self):
        '''Number of frames into file'''
        return int(float(self.__framerate) * float(self.__sec))

    @property
    def timecode(self):
        '''Time in format: HH:MM:SS.MMMM'''
        hours = self.__sec // (60 * 60)
        minutes = (self.__sec // 60) % 60
        seconds = self.__sec % 60
        return "%02d:%02d:%02.2f" % (hours, minutes, seconds)
