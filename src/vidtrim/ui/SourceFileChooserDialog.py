import os

from PySide.QtCore import *
from PySide.QtGui import *

from .SourceFileChooserDialog_UI import Ui_SourceFileChooserDialog_UI


class SourceFile(object):
    def __init__(self):
        self.name = None
        self.path = None
        self.selected = True
        self.pos = None


class SourceFileChooserDialog(QDialog, Ui_SourceFileChooserDialog_UI):

    def __init__(self, parent=None):
        super(SourceFileChooserDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.settings = QSettings()

        # Signals and Slots
        self.browse_btn.clicked.connect(self.browse_for_source_folder)
        self.source_files_tbl.cellClicked.connect(self._file_row_clicked)

        # Initialize Variables
        self.path = self.settings.value('last_source_dir_path')
        self._files = list()

        # Begin
        self.refresh_source_file_list()

    @property
    def path(self):
        return self.source_dir_input.text()
    @path.setter
    def path(self, value):
        self.source_dir_input.setText(value)
    
    
    @property
    def sources(self):
        return [f for f in self._files[:] if f.selected]


    def browse_for_source_folder(self):
        '''Open file browser to select input folder'''
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select folder to read source files from",
            dir=self.path)

        # Store value
        self.path = path

        # Save as default for next run
        QSettings().setValue('last_source_dir_path', path)

        # Update source file list
        self.refresh_source_file_list()


    def refresh_source_file_list(self):

        # Check that current path exists
        if not os.path.exists(self.path):
            self.path = os.path.expanduser('~')

        # Find files
        try:
            self._files = list()
            for filename in sorted(os.listdir(self.path)):
                try:
                    ext = os.path.splitext(filename)[1]
                    if ext.lower() in ('.avi', '.mp4'):
                        f = SourceFile()
                        f.name = filename
                        f.path = os.path.join(self.path, filename)
                        f.pos = len(self._files)

                        self._files.append(f)
                except:
                    pass
        except OSError, e:
            msgBox = QMessageBox()
            msgBox.setText(str(e))
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.exec_()

            self._files = list()

        # Setup Table
        self.source_files_tbl.clear()
        self.source_files_tbl.setRowCount(len(self._files))
        self.source_files_tbl.setColumnCount(1)
        self.source_files_tbl.setHorizontalHeaderLabels(('Filename', ))
        self.source_files_tbl.horizontalHeader().setStretchLastSection(True)
        self.source_files_tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Use row headers to designate selected
        self._refresh_table_selected_indicators()

        # Populate Table
        for i, file in enumerate(self._files):
            self.source_files_tbl.setItem(i, 0, QTableWidgetItem(file.name))


    def _file_row_clicked(self, row, col):

        # Update selection flag
        self._files[row].selected = not self._files[row].selected

        # Re-calc positions
        pos = 0
        for file in self._files:
            if file.selected:
                file.pos = pos
                pos += 1

        # Use row headers to designate selected
        self._refresh_table_selected_indicators()


    def _refresh_table_selected_indicators(self):
        # Update selected indicators
        row_heads = list()
        for file in self._files:
            if file.selected:
                row_heads.append('%02d' % (file.pos))
            else:
                row_heads.append('--')
        self.source_files_tbl.setVerticalHeaderLabels(row_heads)
