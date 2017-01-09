import ctypes

import vlc
ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]

from PySide.QtCore import *
from PySide.QtGui import *

from ..VideoPos import VideoPos
from ..SequencePos import SequencePos
from ..VideoFile import VideoFile
from ..VideoSequence import VideoSequence
from .SourceFileChooserDialog import SourceFileChooserDialog
from .VideoFileLoaderThread import VideoFileLoaderThread

from .VideoTrimMainWindow_UI import Ui_VideoTrimMainWindow_UI
from .VideoTimelineWidget import VideoTimelineWidget

class VideoTrimMainWindow(QMainWindow, Ui_VideoTrimMainWindow_UI):

    current_video_file_finished = Signal()
    current_video_file_changed = Signal()

    def __init__(self, parent=None):
        super(VideoTrimMainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        # Init Vars
        self.source_chooser = SourceFileChooserDialog(parent=self)
        self.vid_sequence = None
        self.vid_sequence_idx = None
        self._vlc = vlc.Instance()
        self._vlc_player = None
        self._vlc_playlist = None
        self._vlc_event_mgr = None
        self._vid_loader = None

        self._init_vlc()

        # Replace the Timeline Widget
        if self.timeline is not None:
            self.timeline.deleteLater()
        self.timeline = VideoTimelineWidget(parent=self.timeline_frame)
        self.timeline.setObjectName("timeline")
        self.timeline_frame.layout().insertWidget(1, self.timeline)

        # Connect signals/slots
        self.play_btn.clicked.connect(self.play_pause)
        self.pushButton_5.clicked.connect(self.jump)
        self.current_video_file_finished.connect(self._start_next_video_in_seq)
        self.timeline.timeline_clicked.connect(self.handle_timeline_click)

        # Begin
        QTimer.singleShot(200, self.choose_source_files)

        self.playback_status_update_timer = QTimer(self)
        self.connect(self.playback_status_update_timer, SIGNAL("timeout()"),
                     self.update_playback_status)
        self.playback_status_update_timer.start(0.25 * 1000)    # 1000 msec = 1 second


    def _init_vlc(self):

        # Init player
        self._vlc_player = self._vlc.media_player_new()

        # https://forum.videolan.org/viewtopic.php?t=109408
        self._vlc_event_mgr = self._vlc_player.event_manager()
        event=vlc.EventType()
        self._vlc_event_mgr.event_attach(event.MediaPlayerEndReached, self._video_finished_vlc_event)

        # https://forum.videolan.org/viewtopic.php?t=72360
        hwnd = self.video_widget.winId()
        # https://srinikom.github.io/pyside-bz-archive/523.html (2011-11-03 comment)
        try:
            int_hwnd = ctypes.pythonapi.PyCObject_AsVoidPtr(hwnd)
            hwnd = int_hwnd
            self._vlc_player.set_hwnd(hwnd)
        except AttributeError:
            pass



    def update_playback_status(self):
        playing = False
        if self._vlc_player is not None:
            playing = self._vlc_player.is_playing()

        if playing:
            self.play_btn.setText('Pause')

            seq_pos = self.play_pos
            if seq_pos is not None:
                self.seq_pos_lbl.setText(seq_pos.timecode)
                self.timeline.updatePlayingPlayhead(seq_pos)

                video_pos = seq_pos.video_pos
                self.video_position_lbl.setText(video_pos.timecode)

        else:
            self.play_btn.setText('Play')

        if self.vid_sequence is not None and self.vid_sequence_idx is not None:
            cur_video = self.vid_sequence[self.vid_sequence_idx]
            self.current_video_lbl.setText(cur_video.filename)





    def choose_source_files(self):
        # Check loading thread running
        if self._vid_loader is not None:
            msgBox = QMessageBox()
            msgBox.setText("Video files still being loaded.")
            msgBox.exec_()
            return

        # Have user select videos to load
        self.source_chooser.exec_()

        # Start loader thread
        self.vid_sequence = VideoSequence()
        paths = [src.path for src in self.source_chooser.sources]
        self._vid_loader = VideoFileLoaderThread(paths, self.vid_sequence, parent=self)
        self._vid_loader.loading_file.connect(self.loader_loading_file)
        self._vid_loader.finished.connect(self.loader_finished)
        self._vid_loader.start()

        # Setup VLC to play video list
        # http://stackoverflow.com/questions/38650544/media-list-in-python-vlc
        # self._vlc_player = self._vlc.media_list_player_new()
        # self._vlc_playlist = self._vlc.media_list_new()
        # for src in self.source_chooser.sources:
        #     self._vlc_playlist.add_media(self._vlc.media_new(src.path))
        # self._vlc_player.set_media_list(self._vlc_playlist)


    def loader_loading_file(self, path):
        self.statusbar.showMessage("Loading " + path)


    def loader_finished(self):
        self.statusbar.showMessage("Ready to play")
        self._vid_loader = None
        self.project_length_timecode.setText(self.vid_sequence.duration.timecode)
        self.timeline.setSequence(self.vid_sequence)
        self.restart_video()


    def restart_video(self):
        if len(self.source_chooser.sources) > 0:
            self.vid_sequence_idx = 0
            self._vlc_player.set_media(self._vlc.media_new(self.source_chooser.sources[0].path))



    def play_pause(self):
        if self._vlc_player is not None:
            if self._vlc_player.is_playing:
                self.play()
            else:
                self.pause()

    def play(self):
        self._vlc_player.play()

    def pause(self):
        self._vlc_player.pause()


    @property
    def play_pos(self):

        '''Playhead'''
        if self.vid_sequence is None:
            return None
        if self.vid_sequence_idx is None:
            return None
        if self._vlc_player is None:
            return None

        # Video Pos
        cur_video = self.vid_sequence[self.vid_sequence_idx]
        vlc_pos = self._vlc_player.get_position()
        vlc_pos_sec = cur_video.duration.seconds * vlc_pos
        cur_video_pos = VideoPos(cur_video, sec=vlc_pos_sec)

        # Sequence Pos
        seq_pos_sec = sum([v.duration.seconds for v in self.vid_sequence.videos[:self.vid_sequence_idx]])
        seq_pos_sec += cur_video_pos.seconds

        return SequencePos(self.vid_sequence, sec=seq_pos_sec)


    def _video_finished_vlc_event(self, arg):
        self.current_video_file_finished.emit()


    def _start_next_video_in_seq(self):
        # Load next video in sequence
        if len(self.source_chooser.sources) >= self.vid_sequence_idx + 2:
            self._load_video_at_index_to_vlc(self.vid_sequence_idx + 1)
            self._vlc_player.play()


    def _load_video_at_index_to_vlc(self, idx):
        '''
        Start playing the video at the given index in the sequence

        :param idx: Index within sequence
        '''
        # Sanity check
        if self.vid_sequence is not None and idx >= 0 and idx < len(self.vid_sequence):
            if idx != self.vid_sequence_idx:
                self.vid_sequence_idx = idx
                video = self._vlc.media_new(self.source_chooser.sources[self.vid_sequence_idx].path)
                self._vlc_player.set_media(video)
                self.current_video_file_changed.emit()


    def handle_timeline_click(self, sec):
        '''
        React to user clicking on timeline to scrub video

        :param sec: Number of seconds into sequence
        '''
        seq_pos = SequencePos(self.vid_sequence, sec=sec)
        video_index, video_pos = self.vid_sequence.calc_video_pos(seq_pos)

        # Change playing video if needed
        if self.vid_sequence_idx != video_index:
            self._load_video_at_index_to_vlc(video_index)

        self._vlc_player.play()

        # Seek to pos in video
        video = self.vid_sequence[self.vid_sequence_idx]
        vlc_pos = float(video_pos.seconds) / float(video.duration.seconds)
        self._vlc_player.set_position(vlc_pos)



    def jump(self):
        self._vlc_player.set_position(0.9)
