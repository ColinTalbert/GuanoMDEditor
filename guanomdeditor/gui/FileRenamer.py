import sys
import os
from pathlib import Path
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt
from PyQt5.Qt import QModelIndex
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QFileSystemModel

from guanomdeditor.gui.ui_files import UI_file_renamer
from guanomdeditor.core import utils

from guano import GuanoFile
import nabatpy

class FileRenamer(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.help_text = ''

        self.in_context = False

        self.build_ui()
        self.connect_events()

    def build_ui(self):
        self.ui = UI_file_renamer.Ui_Form()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        self.original_model = QFileSystemModel()
        self.original_model.setNameFilters(["*.wav", "*.zc"])
        self.original_model.setNameFilterDisables(False)
        self.original_model.setRootPath(r'C:\temp\to_rename')
        self.ui.treeview_original.setModel(self.original_model)
        for i in range(6, 0, -1):
            self.ui.treeview_original.setColumnHidden(i, True)

        self.changed_model = RenamedFileSystemModel(rename_function=self.change_fname_function)
        self.changed_model.setNameFilters(["*.wav", "*.zc"])
        self.changed_model.setNameFilterDisables(False)
        self.changed_model.setRootPath(r'C:\temp\to_rename')
        self.ui.treeview_changed.setModel(self.changed_model)
        for i in range(6, 0, -1):
            self.ui.treeview_changed.setColumnHidden(i, True)
        # self.ui.scrollArea.setAcceptDrops(True)
        # self.installEventFilter(self)
        # self.setMouseTracking(True)
        # self.setAcceptDrops(True)

        icon = QIcon(utils.resource_path('../resources/icons/nabat_circle_color.ico'))
        self.setWindowIcon(icon)

        self.ui.progressBar.setVisible(False)

    def connect_events(self):
        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.directory_name.textChanged.connect(self.load_directory)
        self.ui.btn_save.clicked.connect(self.save)

        self.ui.treeview_original.expanded.connect(self.expand_changed)
        self.ui.treeview_original.collapsed.connect(self.collapse_changed)
        self.ui.treeview_changed.expanded.connect(self.expand_original)
        self.ui.treeview_changed.collapsed.connect(self.collapse_original)

        self.ui.chk_auto_rename.stateChanged.connect(self.update_filenames)
        self.ui.chk_replace.stateChanged.connect(self.update_filenames)

        self.ui.replace_from.textChanged.connect(self.update_filenames)
        self.ui.replace_to.textChanged.connect(self.update_filenames)

    def update_filenames(self):
        self.load_directory()

    def expand_changed(self, index):
        self.ui.treeview_changed.setExpanded(self.changed_model.index(self.original_model.filePath(index)), True)

    def collapse_changed(self, index):
        self.ui.treeview_changed.setExpanded(self.changed_model.index(self.original_model.filePath(index)), False)

    def expand_original(self, index):
            self.ui.treeview_original.setExpanded(self.original_model.index(self.changed_model.filePath(index)), True)

    def collapse_original(self, index):
        self.ui.treeview_original.setExpanded(self.original_model.index(self.changed_model.filePath(index)), False)

    def browse(self):
        settings = QSettings('USGS', 'guanoeditor')
        last_data_fname = settings.value('lastDataDname', '')

        dname = QFileDialog.getExistingDirectory(self, "Open a folder", last_data_fname)
        if dname:
            settings.setValue('lastDataDname', dname)

            self.ui.directory_name.setText(dname)

            self.load_directory()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls() and e.mimeData().urls()[0].isLocalFile():
            url = e.mimeData().urls()[0].toLocalFile()
            if url.endswith('.wav'):
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Updates the form with the contents of an xml node dropped onto it.
        Parameters
        ----------
        e : qt event
        Returns
        -------
        None
        """
        try:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            url = e.mimeData().urls()[0].toLocalFile()
            self.ui.file_name.setText(url)

            # self.from_xml(element)
        except:
            e = sys.exc_info()[0]
            print('problem drop', e)

    def change_fname_function(self, fname):
        renamed = fname

        if self.ui.chk_auto_rename.isChecked():
            try:
                renamed = nabatpy.utils.parse_nabat_fname(fname)['correct_fname']
            except:
                renamed = fname

        if self.ui.chk_replace.isChecked():
            renamed = renamed.replace(self.ui.replace_from.text(), self.ui.replace_to.text())

        return renamed

    def load_directory(self):
        self.ui.treeview_original.setRootIndex(self.original_model.index(self.ui.directory_name.text()))
        self.original_model.setRootPath(self.ui.directory_name.text())

        self.ui.treeview_changed.setRootIndex(self.changed_model.index(self.ui.directory_name.text()))
        self.changed_model.setRootPath(self.ui.directory_name.text())

    def save(self):

        d = Path(self.ui.directory_name.text())
        wavs = list(d.glob('**\*.wav'))

        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setMinimum(1)
        self.ui.progressBar.setMaximum(len(wavs))
        self.ui.progressBar.setVisible(1)


        for f in wavs:
            original_fname = f.name
            new_fname = self.change_fname_function(original_fname)

            if original_fname != new_fname:
                f.rename(f.parent.joinpath(new_fname))
                g = GuanoFile(f.parent.joinpath(new_fname))
                g['Original Filename'] = original_fname
                g.write(make_backup=False)

            self.ui.progressBar.setValue(self.ui.progressBar.value()+1)

        self.ui.progressBar.setMinimum(self.ui.progressBar.maximum())
        



class RenamedFileSystemModel(QFileSystemModel):
    def __init__(self, rename_function=None, *args, **kwargs):
        super(RenamedFileSystemModel, self).__init__(*args, **kwargs)

        self.original_data = {}

        self.rename_function = rename_function

    def data(self, index, role=Qt.DisplayRole):

        if role == Qt.TextColorRole:
            fname = index.data(Qt.DisplayRole)
            renamed = self.rename_function(fname)
            if super(RenamedFileSystemModel, self).data(index) != renamed:
                return QColor("#ef1c25")
        else:
            data = super(RenamedFileSystemModel, self).data(index, role)
            self.original_data[index] = data
            try:
                return self.rename_function(data)
            except:
                return data


if __name__ == "__main__":
    app = QApplication([])
    app.title = 'NABat File Renamer'
    widget = FileRenamer()
    widget.setWindowTitle(app.title)
    widget.show()
    sys.exit(app.exec_())
