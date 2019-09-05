import sys
import os
from pathlib import Path
from collections import OrderedDict
import shutil
import tarfile
import re

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


class FileRenamer(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.help_text = ''

        self.in_context = False

        self.build_ui()
        self.connect_events()

        self.cache = {}

    def build_ui(self):
        self.ui = UI_file_renamer.Ui_Form()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        self.original_model = QFileSystemModel()
        self.original_model.setNameFilters(["*.wav", "*.zc"])
        self.original_model.setNameFilterDisables(False)
        self.ui.treeview_original.setModel(self.original_model)
        for i in range(6, 0, -1):
            self.ui.treeview_original.setColumnHidden(i, True)

        self.changed_model = RenamedFileSystemModel(rename_function=self.change_fname_function)
        self.changed_model.setNameFilters(["*.wav", "*.zc"])
        self.changed_model.setNameFilterDisables(False)
        self.ui.treeview_changed.setModel(self.changed_model)
        for i in range(6, 0, -1):
            self.ui.treeview_changed.setColumnHidden(i, True)

        icon = QIcon(utils.resource_path('../resources/icons/nabat_circle_color.ico'))
        self.setWindowIcon(icon)

        self.ui.progressBar.setVisible(False)
        self.ui.progressBar_tarball.setVisible(False)

    def connect_events(self):
        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.btn_browse_output.clicked.connect(self.browse_output)
        self.ui.directory_name.textChanged.connect(self.load_directory)
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_tarball.clicked.connect(self.tarball)

        self.ui.treeview_original.expanded.connect(self.expand_changed)
        self.ui.treeview_original.collapsed.connect(self.collapse_changed)
        self.ui.treeview_changed.expanded.connect(self.expand_original)
        self.ui.treeview_changed.collapsed.connect(self.collapse_original)
        self.sb_original = self.ui.treeview_original.verticalScrollBar()
        self.sb_original.valueChanged.connect(self.sync_scroll_right)
        self.sb_changed = self.ui.treeview_changed.verticalScrollBar()
        self.sb_changed.valueChanged.connect(self.sync_scroll_left)

        self.ui.chk_auto_rename.stateChanged.connect(self.update_filenames)
        self.ui.chk_replace.stateChanged.connect(self.update_filenames)

        self.ui.replace_from.textChanged.connect(self.update_filenames)
        self.ui.replace_to.textChanged.connect(self.update_filenames)

        self.ui.chk_replace.stateChanged.connect(self.enable_chk_replace)
        self.ui.chk_replace2.stateChanged.connect(self.enable_chk_replace2)
        self.ui.chk_folderGRTS.stateChanged.connect(self.enable_chk_grtsfolder)
        self.ui.chk_sitename_folder.stateChanged.connect(self.enable_chk_sitefolder)

        self.ui.site_text.textChanged.connect(self.update_filenames)
        self.ui.grts_txt.textChanged.connect(self.update_filenames)
        self.ui.replace_from.textChanged.connect(self.update_filenames)
        self.ui.replace_to.textChanged.connect(self.update_filenames)
        self.ui.replace_from2.textChanged.connect(self.update_filenames)
        self.ui.replace_to2.textChanged.connect(self.update_filenames)
        self.ui.grts_folder.toggled.connect(self.grts_parent_change)
        self.ui.grts_folder2x.toggled.connect(self.grts_parent_change)
        self.ui.site_folder.toggled.connect(self.site_parent_change)
        self.ui.site_folder2x.toggled.connect(self.site_parent_change)

    def grts_parent_change(self):
        self.ui.grts_txt.setText('')
        self.update_filenames()

    def site_parent_change(self):
        self.ui.site_text.setText('')
        self.update_filenames()

    def enable_chk_replace(self):
        checked = self.ui.chk_replace.isChecked()
        self.ui.replace_from.setEnabled(checked)
        self.ui.replace_to.setEnabled(checked)
        self.ui.chk_use_re.setEnabled(checked)
        self.ui.label_2.setEnabled(checked)
        self.update_filenames()

    def enable_chk_replace2(self):
        checked = self.ui.chk_replace2.isChecked()
        self.ui.replace_from2.setEnabled(checked)
        self.ui.replace_to2.setEnabled(checked)
        self.ui.chk_use_re2.setEnabled(checked)
        self.ui.label_3.setEnabled(checked)
        self.update_filenames()

    def enable_chk_grtsfolder(self):
        checked = self.ui.chk_folderGRTS.isChecked()
        self.ui.grts_folder.setEnabled(checked)
        self.ui.grts_folder2x.setEnabled(checked)
        self.ui.grts_folder3x.setEnabled(checked)
        self.ui.grts_txt.setEnabled(checked)
        self.update_filenames()

    def enable_chk_sitefolder(self):
        checked = self.ui.chk_sitename_folder.isChecked()
        self.ui.site_folder.setEnabled(checked)
        self.ui.site_folder2x.setEnabled(checked)
        self.ui.site_folder3x.setEnabled(checked)
        self.ui.site_text.setEnabled(checked)
        self.update_filenames()

    def sync_scroll_right(self, int):
        self.sb_changed.setValue(self.sb_original.value())

    def sync_scroll_left(self, int):
        self.sb_original.setValue(self.sb_changed.value())

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
        last_data_fname = str(Path(settings.value('lastDataDname', '')).parent)

        dname = QFileDialog.getExistingDirectory(self, "Open a folder", last_data_fname)
        if dname:
            settings.setValue('lastDataDname', dname)

            self.ui.directory_name.setText(dname)

            self.load_directory()

    def browse_output(self):
        settings = QSettings('USGS', 'guanoeditor')
        last_data_fname = str(Path(settings.value('lastDataDname', '')).parent)

        dname = QFileDialog.getExistingDirectory(self, "Select an output folder", last_data_fname)
        if dname:
            settings.setValue('lastDataDname', dname)

            self.ui.directory_name_output.setText(dname)

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

    def change_fname_function(self, fname, index=None, f=None):

        renamed = fname

        if self.ui.chk_auto_rename.isChecked():
            try:
                renamed = utils.clean_name(fname)
            except:
                renamed = fname

        try:
            if self.ui.chk_replace.isChecked():
                if self.ui.chk_use_re.isChecked():
                    renamed = re.sub(self.ui.replace_from.text(), self.ui.replace_to.text(), renamed)
                else:
                    renamed = renamed.replace(self.ui.replace_from.text(), self.ui.replace_to.text())
        except:
            pass

        try:
            if self.ui.chk_replace2.isChecked():
                if self.ui.chk_use_re2.isChecked():
                    renamed = re.sub(self.ui.replace_from2.text(), self.ui.replace_to2.text(), renamed)
                else:
                    renamed = renamed.replace(self.ui.replace_from2.text(), self.ui.replace_to2.text())
        except:
            pass

        if not self.ui.chk_folderGRTS.isChecked() and \
            not self.ui.chk_sitename_folder.isChecked():
            return renamed

        try:
            parts = renamed.split('_')
            time_str = parts[-1]
            date_str = parts[-2]

            if len(parts) == 4:
                grts_str, site_str = parts[:2]
            elif len(parts) == 3:
                grts_str = parts[0]
                site_str = 'UnknownSiteName'
        except:
            return renamed

        if self.ui.chk_folderGRTS.isChecked():
            grts_str = self.ui.grts_txt.text()
            if not grts_str:
                if self.ui.grts_folder.isChecked():
                    if index is not None:
                        grts_str = self.changed_model.parent(index).data()
                    elif f is not None:
                        grts_str = f.parent()
                elif self.ui.grts_folder2x.isChecked():
                    if index is not None:
                        grts_str = self.changed_model.parent(index).parent().data()
                    elif f is not None:
                        grts_str = f.parent().parent()
                elif self.ui.grts_folder3x.isChecked():
                    if index is not None:
                        grts_str = self.changed_model.parent(index).parent().parent().data()
                    elif f is not None:
                        grts_str = f.parent().parent().parent()

        if self.ui.chk_sitename_folder.isChecked():
            site_str = self.ui.site_text.text()
            if not site_str:
                if self.ui.site_folder.isChecked():
                    if index is not None:
                        site_str = self.changed_model.parent(index).data()
                    elif f is not None:
                        site_str = f.parent()
                elif self.ui.site_folder2x.isChecked():
                    if index is not None:
                        site_str = self.changed_model.parent(index).parent().data()
                    elif f is not None:
                        site_str = f.parent().parent()
                elif self.ui.site_folder3x.isChecked():
                    if index is not None:
                        site_str = self.changed_model.parent(index).parent().parent().data()
                    elif f is not None:
                        site_str = f.parent().parent().parent()

        try:
            parts = [grts_str, site_str, date_str, time_str]
            renamed = "_".join(parts)
        except:
            return renamed

        return renamed

    def load_directory(self):
        self.ui.treeview_original.setRootIndex(self.original_model.index(self.ui.directory_name.text()))
        self.original_model.setRootPath(self.ui.directory_name.text())

        self.ui.treeview_changed.setRootIndex(self.changed_model.index(self.ui.directory_name.text()))
        self.changed_model.setRootPath(self.ui.directory_name.text())

    def save(self):

        d = Path(self.ui.directory_name.text())
        wavs = list(d.glob('**\*.wav'))
        wavs += list(d.glob('**\*.zc'))

        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setMinimum(1)
        self.ui.progressBar.setMaximum(len(wavs))
        self.ui.progressBar.setVisible(1)

        if self.ui.directory_name_output.text():
            if not Path(self.ui.directory_name_output.text()).exists():
                msq = r"The output directory specified does not exist!  Please point to an existing directory."
                QMessageBox.warning(self, "Output directory does not exist", msg)
                return None
            out_dir = Path(self.ui.directory_name_output.text())
            make_copy = True
        else:
            out_dir = Path(self.ui.directory_name.text())
            make_copy = False

        for f in wavs:
            original_fname = f.name

            new_fname = self.change_fname_function(original_fname, f=f)

            full_name = f.parent.joinpath(new_fname)
            full_name = str(full_name).replace(str(Path(self.ui.directory_name.text())), \
                                                   str(out_dir))
            if not Path(full_name).exists():
                Path(full_name).parent.mkdir(parents=True, exist_ok=True)
                if make_copy:
                    shutil.copy(str(f), full_name)
                else:
                    f.rename(full_name)

            if original_fname != new_fname:
                try:
                    g = GuanoFile(full_name)
                    g['Original Filename'] = original_fname
                    g.write(make_backup=False)
                except:
                    pass

            self.ui.progressBar.setValue(self.ui.progressBar.value()+1)

        msg = f"Finished renaming files in directory:\n\n{out_dir}"
        QMessageBox.information(self, "Renaming Process Complete", msg)

        self.ui.progressBar.setVisible(False)

    def tarball(self):
        if self.ui.directory_name_output.text():
            if not Path(self.ui.directory_name_output.text()).exists():
                msq = r"The output directory specified does not exist!  Please point to an existing directory."
                QMessageBox.warning(self, "Output directory does not exist", msg)
                return None
            out_dir = Path(self.ui.directory_name_output.text())
        else:
            out_dir = Path(self.ui.directory_name.text())

        wavs = list(out_dir.glob('**\*.wav'))
        wavs += list(out_dir.glob('**\*.zc'))

        self.ui.progressBar_tarball.setVisible(True)
        self.ui.progressBar_tarball.setMinimum(1)
        self.ui.progressBar_tarball.setMaximum(len(wavs))
        self.ui.progressBar_tarball.setVisible(1)

        tar_name = out_dir.joinpath(out_dir.name + '.tar.gz')

        with tarfile.open(tar_name, "w:gz") as tar_handle:
            for f in wavs:
                tar_handle.add(str(f), arcname=f.name)
                self.ui.progressBar_tarball.setValue(self.ui.progressBar.value()+1)

        self.ui.progressBar_tarball.setValue(self.ui.progressBar_tarball.maximum())

        msg = f"Finished creating tar.gz archive of directory contents.:\n\n{tar_name}"
        QMessageBox.information(self, "Tarball Process Complete", msg)

        self.ui.progressBar_tarball.setVisible(False)


class RenamedFileSystemModel(QFileSystemModel):
    def __init__(self, rename_function=None, *args, **kwargs):
        super(RenamedFileSystemModel, self).__init__(*args, **kwargs)

        self.original_data = {}

        self.rename_function = rename_function

    def data(self, index, role=Qt.DisplayRole):

        # parent3x = self.parent(index).parent().parent().data()
        # parent2x = self.parent(index).parent().data()
        # parent = self.data(index).parent(index).data()
        fname = super(RenamedFileSystemModel, self).data(index)

        if role == Qt.TextColorRole:
            # parent3x = super(RenamedFileSystemModel, self).parent(index).parent().parent().data()
            # parent2x = super(RenamedFileSystemModel, self).parent(index).parent().data()
            # parent = super(RenamedFileSystemModel, self).parent(index).data()
            # fname = super(RenamedFileSystemModel, self).data(index)
            #
            # renamed = self.rename_function(parent3x.joinpath(fname, [parent, parent2x, parent3x]))
            # if fname != renamed and \
            #
            if Path(fname).suffix.lower() in ['.wav', '.zc']:
                # renamed = self.rename_function(fname, [parent, parent2x, parent3x])
                renamed = self.rename_function(fname, index=index)
                if fname != renamed:
                    return QColor("#ef1c25")
        else:
            data = super(RenamedFileSystemModel, self).data(index, role)
            self.original_data[index] = data
            try:
                if not Path(fname).suffix.lower() in ['.wav', '.zc']:
                    return data

                return self.rename_function(data, index=index)
            except:
                return data


if __name__ == "__main__":
    app = QApplication([])
    app.title = 'NABat File Renamer'
    widget = FileRenamer()
    widget.setWindowTitle(app.title)
    widget.show()
    sys.exit(app.exec_())
