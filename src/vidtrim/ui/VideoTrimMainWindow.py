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

class VideoTrimMainWindow(QMainWindow, Ui_VideoTrimMainWindow_UI):

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

        # Connect signals/slots
        self.play_btn.clicked.connect(self.play_pause)
        self.pushButton_5.clicked.connect(self.jump)

        # Begin
        QTimer.singleShot(200, self.choose_source_files)

        self.playback_status_update_timer = QTimer(self)
        self.connect(self.playback_status_update_timer, SIGNAL("timeout()"),
                     self.update_playback_status)
        self.playback_status_update_timer.start(0.25 * 1000)    # 1000 msec = 1 second


    def _init_vlc(self):

        # Init player
        self._vlc_player = self._vlc.media_player_new()
        self._vlc_player.set_media(self._vlc.media_new(self.source_chooser.sources[0].path))

        # https://forum.videolan.org/viewtopic.php?t=109408
        self._vlc_event_mgr = self._vlc_player.event_manager()
        event=vlc.EventType()
        self._vlc_event_mgr.event_attach(event.MediaPlayerEndReached, self._video_finished)

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
        self.statusbar.showMessage("TODO: Loading finished")
        self._vid_loader = None
        self.vid_sequence_idx = 0
        self.project_length_timecode.setText(self.vid_sequence.duration.timecode)


    def play_pause(self):
        if self._vlc_player is not None:
            if self._vlc_player.is_playing:
                self.play()
            else:
                self.pause()

    def play(self):
        self._vlc_player.play()
        self.play_btn.setText('Pause')

    def pause(self):
        self._vlc_player.pause()
        self.play_btn.setText('Play')


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
        vlc_pos_ms = self._vlc_player.get_time()
        if vlc_pos_ms == -1:
            return None
        cur_video_pos = VideoPos(cur_video, ms=vlc_pos_ms)

        # Sequence Pos
        seq_pos_ms = sum([v.duration for v in self.vid_sequence.videos[:self.vid_sequence_idx]])
        seq_pos_ms += cur_video_pos.ms

        return SequencePos(self.vid_sequence, ms=seq_pos_ms)


    def _video_finished(self, arg):
        print 'Playback Finished'
        print str(arg)


    def jump(self):
        self._vlc_player.set_position(0.9)
