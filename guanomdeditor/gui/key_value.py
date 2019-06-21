import sys
import os
from collections import OrderedDict
from pathlib import Path

import pandas as pd

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QIcon

from guanomdeditor.gui.ui_files import UI_key_value


class KeyValue(QWidget):

    def __init__(self, tag, description='', required=False, parent=None):
        QWidget.__init__(self, parent=parent)
        self.tag = tag
        self.help_text = ''
        self.required = required

        # for standalone testing and debugging
        if __name__ == "__main__":
            QMainWindow.__init__(self, parent)

        self.in_context = False
        self.ui = None
        self.build_ui()
        self.ui.key_label.setText(tag)
        from textwrap import wrap
        self.setToolTip("\n".join(wrap(description)))
        self.ui.key_label.setToolTip("\n".join(wrap(description)))

    def build_ui(self):
        self.ui = UI_key_value.Ui_Form()
        self.ui.setupUi(self)

        if self.required:
            self.setStyleSheet("""QLabel {
                                                font: bold;
                                            }
                                  QFrame {
                                  background-color: rgb(117, 186, 202)
                                  }""")

    def load_data(self, content):
        self.ui.value_edit.setText(str(content))

    def get_data(self):
        if self.tag == 'Timestamp' and self.ui.value_edit.text().strip() != '':
            try:
                return pd.to_datetime(self.ui.value_edit.text())
            except:
                return ''
        elif self.tag == 'Length':
            try:
                return float(self.ui.value_edit.text())
            except:
                return ''
        elif self.tag == 'Loc Position':
            try:
                value = self.ui.value_edit.text()
                values = value.split()
                if len(values) == 2:
                    return tuple(float(v) for v in values)
                else:
                    return ''
            except:
                return ''
        else:
            return self.ui.value_edit.text()


if __name__ == "__main__":
    # from utils import launch_widget
    # widget = launch_widget(KeyValue, 'tesing key_value', tag='test_label', description='test')
    app = QApplication([])
    app.title = 'NABat Guano MD Editor'
    widget = KeyValue(tag='test_label', description='test')
    widget.load_data('test_value')
    widget.setWindowTitle(app.title)
    widget.show()
    sys.exit(app.exec_())
