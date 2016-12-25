import ctypes

import vlc
ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]

from PySide.QtCore import *
from PySide.QtGui import *

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


    def _video_finished(self, arg):
        print 'Playback Finished'
        print str(arg)


    def jump(self):
        self._vlc_player.set_position(0.9)
