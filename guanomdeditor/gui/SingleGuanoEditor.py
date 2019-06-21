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
from PyQt5.QtGui import QIcon

from guanomdeditor.gui.ui_files import UI_simple_viewer2
from guanomdeditor.gui.namespace_group import NamespaceGroup
from guanomdeditor.core import utils

from guano import GuanoFile


class SingleGuanoEditor(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.help_text = ''

        self.in_context = False
        self.ui = None

        self.guano_content = None

        self.namespaces = OrderedDict()
        self.namespace_chks = OrderedDict()

        self.build_ui()
        self.connect_events()

    def build_ui(self):
        self.ui = UI_simple_viewer2.Ui_Form()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)
        self.ui.scrollArea.setAcceptDrops(True)
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        icon = QIcon(utils.resource_path('../resources/icons/nabat_circle_color.ico'))
        self.setWindowIcon(icon)

        self.header_layout = self.ui.header_layout
        self.namespace_layout = self.ui.scrollAreaWidgetContents_2.layout()

        self.load_namespaces()

    def connect_events(self):
        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.file_name.textChanged.connect(self.load_file)
        self.ui.btn_save.clicked.connect(self.save)

    def browse(self):
        settings = QSettings('USGS', 'guanoeditor')
        last_data_fname = settings.value('lastDataFname', '')
        if last_data_fname:
            dname, fname = os.path.split(last_data_fname)
        else:
            fname, dname = "", ""

        fname = QFileDialog.getOpenFileName(self, fname, dname,
                                            filter="Wave files (*.wav)")
        if fname[0]:
            settings.setValue('lastDataFname', fname[0])

            self.ui.file_name.setText(fname[0])

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

    def load_namespaces(self):
        namespace_d = Path(utils.resource_path("../resources/specs"))
        namespace_csvs = namespace_d.glob("*.csv")
        for namespace_csv in namespace_csvs:
            namespace = namespace_csv.name.replace(".csv", "")
            namespace_chk = QCheckBox(namespace.replace("_", " "))
            self.header_layout.addWidget(namespace_chk)
            namespace_chk.stateChanged.connect(self.namespace_changed)
            self.namespace_chks[namespace] = namespace_chk

    def namespace_changed(self, int):
        this_namespace_sender = self.sender()
        namespace = this_namespace_sender.text().replace(" ", "_")

        if int == 0:  # remove this namespace
            if namespace in self.namespaces:
                self.namespaces[namespace].hide()

        else: # show this namespace
            if namespace in self.namespaces:
                self.namespaces[namespace].show()
            else:
                namespace_fname = utils.resource_path(f"../resources/specs/{namespace}.csv")
                spec = utils.read_namespace(namespace_fname)

                this_namespace = NamespaceGroup(namespace, spec)
                this_namespace.load_data({})

                index = self.ui.scrollAreaWidgetContents_2.layout().count()-1
                self.ui.scrollAreaWidgetContents_2.layout().insertWidget(index, this_namespace)
                self.namespaces[namespace] = this_namespace

    def load_file(self):
        for i in reversed(range(self.namespace_layout.count()-1)):
            self.namespace_layout.itemAt(i).widget().setParent(None)

        for namespce_chk in self.namespace_chks.values():
            namespce_chk.setChecked(False)

        self.namespaces = OrderedDict()

        fname = self.ui.file_name.text()
        f = Path(fname)
        try:
            exists = f.exists()
        except:
            exists = False

        if exists:
            try:
                g = GuanoFile(fname)
            except:
                msg = f"There was a problem loading the Guano MD from:\n{fname}\n\nPlease verify that it is a valid wav file"
                QMessageBox.warning(self, "File Error", msg)
                return None

            self.guano_content = {key:{} for key in g.get_namespaces()}

            for item in g.items_namespaced():
                self.guano_content[item[0]][item[1]] = item[2]

            for namespace in g.get_namespaces():

                if namespace == '':
                    namespace = 'guano_base'
                namespace_fname = utils.resource_path(f"../resources/specs/{namespace}.csv")

                if Path(namespace_fname).exists():
                    spec = utils.read_namespace(namespace_fname)
                else:
                    # if we have a namespace we've never seen, load it up as if it was a complete spec
                    spec = [{'tag':tag} for tag in self.guano_content[namespace].keys()]

                this_namespace = NamespaceGroup(namespace, spec)

                if namespace == 'guano_base':
                    this_namespace.load_data(self.guano_content[''])
                else:
                    this_namespace.load_data(self.guano_content[namespace])

                index = self.ui.scrollAreaWidgetContents_2.layout().count()-1
                self.ui.scrollAreaWidgetContents_2.layout().insertWidget(index, this_namespace)
                self.namespaces[namespace] = this_namespace
                try:
                    self.namespace_chks[namespace].setChecked(True)
                except KeyError:
                    pass

    def save(self):
        fname = self.ui.file_name.text()
        try:
            g = GuanoFile(fname)
        except:
            msg = f"There was a problem loading the Guano MD from:\n{fname}\n\nPlease verify that it is a valid wav file"
            QMessageBox.warning(self, "File Error", msg)
            return None

        for namespace_name, namespace_group in self.namespaces.items():
            print(namespace_name)
            namespace_data = namespace_group.get_data()

            if namespace_name == 'guano_base':
                namespace_name = ''

            for k, v in namespace_data.items():
                if v == '':
                    try:
                        del g[f"{namespace_name}|{k}"]
                    except KeyError:
                        pass
                else:
                    g[f"{namespace_name}|{k}"] = v

        g.write(make_backup=False)


if __name__ == "__main__":
    app = QApplication([])
    app.title = 'Guano MD Editor'
    widget = SingleGuanoEditor()
    widget.setWindowTitle(app.title)
    widget.show()
    sys.exit(app.exec_())
