from .SequencePos import SequencePos
from .VideoPos import VideoPos

class VideoSequence(object):
    '''A sequence of video files'''

    def __init__(self):
        self.__videos = list()


    def add(self, video):
        self.__videos.append(video)


    @property
    def videos(self):
        return self.__videos[:]

    def __len__(self):
        return len(self.__videos)


    def video_segments(self):
        '''
        Return the segments each video file occupies in the segment

        :return: generator: video index, start pos in sequence, end pos in sequence
        '''
        start_pos = SequencePos(self, 0)
        for i, video in enumerate(self.__videos):
            end_pos = start_pos + video.duration
            yield i, start_pos, end_pos
            start_pos = end_pos



    @property
    def duration(self):
        last_end = None
        for i, start, end in self.video_segments():
            last_end = end
        return last_end


    def calc_video_pos(self, seq_pos):
        '''
        Given a position in the sequence, calculate the position in the video file

        :param seq_pos: Position in the whole sequence
        :return: Index of video, VideoPos within that video
        '''
        for i, start, end in self.video_segments():
            if seq_pos >= start and seq_pos <= end:
                return i, VideoPos(self.__videos[i], sec = seq_pos.sec - start.sec)


    def __getitem__(self, i):
        return self.__videos[i]