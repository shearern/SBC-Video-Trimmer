
class TimePos(object):
    '''The time representation of a position in or duration of a video'''

    def __init__(self, sec = None, ms = None):
        '''
        :param sec: Number of seconds
        :param ms: Number of miliseconds
        '''
        if sec is None and ms is None:
            raise Exception("Specify sec or ms")
        if sec is not None and ms is not None:
            raise Exception("Specify sec or ms, not both.")
        if sec is not None:
            self.__sec = sec
        else:
            self.__sec = float(ms) / 1000.0


    def __str__(self):
        return self.timecode

    def __repr__(self):
        return "TimePos(sec=%.02f)" % (self.sec)


    @property
    def seconds(self):
        '''Number of seconds'''
        return self.__sec
    @property
    def sec(self):
        return self.seconds


    @property
    def ms(self):
        '''Number of miliseconds'''
        return float(self.__sec) * 1000.0


    @property
    def timecode(self):
        '''Time in format: HH:MM:SS.MMMM'''

        # Round to the nearest hundredth of a second
        total_sec = round(self.__sec, 2)

        hours = total_sec // (60 * 60)
        minutes = (total_sec // 60) % 60
        seconds = total_sec % 60
        sec_hundredths = (seconds % 1)
        return "%02d:%02d:%02d.%02d" % (hours, minutes, seconds, sec_hundredths)


    def __add__(self, other):
        try:
            return TimePos(sec=self.seconds + other.seconds)
        except AttributeError:
            raise TypeError("Can't add %s to %s" % (
                other.__class__.__name__,
                self.__class__.__name__))


    def __lt__(self, other):
        try:
            return self.seconds < other.seconds
        except AttributeError:
            raise TypeError("Can't compare %s and %s" % (
                other.__class__.__name__,
                self.__class__.__name__))

    def __le__(self, other):
        return self < other or self == other


    def __gt__(self, other):
        try:
            return self.seconds > other.seconds
        except AttributeError:
            raise TypeError("Can't compare %s and %s" % (
                other.__class__.__name__,
                self.__class__.__name__))

    def __ge__(self, other):
        return self > other or self == other


    FLOAT_COMPARE_TOLERANCE = 0.0001

    def __eq__(self, other):
        try:
            if other.seconds > self.seconds - self.FLOAT_COMPARE_TOLERANCE:
                if other.seconds < self.seconds + self.FLOAT_COMPARE_TOLERANCE:
                    return True
            return False
        except AttributeError:
            raise TypeError("Can't compare %s and %s" % (
                other.__class__.__name__,
                self.__class__.__name__))


    def __ne__(self, other):
        return not self == other