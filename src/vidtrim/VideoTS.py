

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

        # Round to the nearest hundredth of a second
        total_sec = round(self.__sec, 2)

        hours = total_sec // (60 * 60)
        minutes = (total_sec // 60) % 60
        seconds = total_sec % 60
        frames = (seconds % 1) * self.__framerate
        return "%02d:%02d:%02d.%02d" % (hours, minutes, seconds, frames)
