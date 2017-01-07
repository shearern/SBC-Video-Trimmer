import sys
from PySide import QtGui, QtCore

from ..TimePos import TimePos

class VideoTimelineWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(VideoTimelineWidget, self).__init__(parent=parent)

        # Config Parameters
        self.__sequence = None
        self.__playhead = None

        # Init UI
        self.setMinimumSize(50, 20) # W, H


    def setSequence(self, seq):
        '''Change the sequence being displayed'''
        self.__sequence = seq
        self.update()



    @property
    def sequnce_length(self):
        if self.__sequence is not None:
            return self.__sequence.duration


    def _calc_x_for_time(self, t):
        '''Given a TimePos, calculate the x position of the timeline'''
        total_dur = self.sequnce_length
        if total_dur is not None:
            w = self.size().width()
            p = t.ms / total_dur.ms
            return int(p * w)


    def paintEvent(self, e):

        # Qt Boilerplate to begin
        qp = QtGui.QPainter()
        qp.begin(self)

        # Some metrics
        size = self.size()
        w = size.width()
        h = size.height()

        # Colors
        background = QtGui.QColor(83, 83, 83) # Not used?
        track_color = QtGui.QColor(87, 111, 155)
        track_sep_color = QtGui.QColor(117, 141, 179)
        playhead_color = QtGui.QColor(255, 141, 179)

        # Draw background
        qp.setPen(background)
        qp.setBrush(background)
        qp.drawRect(0, 0, w-1, h-1)

        if self.__sequence is not None:

            # Draw line at 1 minute
            x = self._calc_x_for_time(TimePos(sec=60))
            if x is not None:
                qp.setPen(track_sep_color)
                qp.setBrush(track_sep_color)
                qp.drawLine(x, 0, x, h-1)

            # Outline tracks
            qp.setPen(track_sep_color)
            qp.setBrush(track_color)
            pos = TimePos(0)
            for video in self.__sequence.videos:
                start_x = self._calc_x_for_time(pos)
                pos += video.duration
                end_x = self._calc_x_for_time(pos)
                qp.drawRect(start_x, 0, end_x, h-1)

            # Draw playhead
            if self.__playhead is not None:
                qp.setPen(playhead_color)
                qp.setBrush(playhead_color)
                x = self._calc_x_for_time(self.__playhead)
                qp.drawLine(x, 0, x, h-1)

        # Qt Boilerplate to commit
        qp.end()


    def updatePlayingPlayhead(self, ts):
        '''Set the position in the sequence'''
        self.__playhead = ts
        self.update()


    def drawWidget(self, qp):
        print "DRAW"