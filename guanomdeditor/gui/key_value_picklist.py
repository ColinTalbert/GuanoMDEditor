import sys
import os
from collections import OrderedDict
from pathlib import Path

import pandas as pd

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QIcon

from guanomdeditor.gui.ui_files import UI_key_value_picklist


class KeyValuePicklist(QWidget):

    def __init__(self, tag, picklist, description='', required=False, parent=None):
        QWidget.__init__(self, parent=parent)
        self.tag = tag

        self.help_text = description
        self.setToolTip(description)
        self.required = required

        # for standalone testing and debugging
        if __name__ == "__main__":
            QMainWindow.__init__(self, parent)

        self.in_context = False
        self.ui = None
        self.build_ui()

        self.ui.key_label.setText(tag)
        self.ui.value_box.clear()
        self.ui.value_box.addItems(picklist)
        self.ui.value_box.setEditText('')
        self.ui.value_box.editTextChanged.connect(self.check_on_list)
        self.ui.value_box.wheelEvent = self.wheelEvent

        from textwrap import wrap
        self.setToolTip("\n".join(wrap(description)))
        self.ui.value_box.setToolTip("\n".join(wrap(description)))
        self.ui.key_label.setToolTip("\n".join(wrap(description)))

    def build_ui(self):
        self.ui = UI_key_value_picklist.Ui_Form()
        self.ui.setupUi(self)

    def wheelEvent(self, *args, **kwargs):
        pass

    def load_data(self, content):
        self.ui.value_box.setEditText(str(content))
        self.check_on_list()

    def get_data(self):
        return self.ui.value_box.currentText()

    def check_on_list(self):
        content = self.ui.value_box.currentText()
        if self.ui.value_box.findText(str(content)) == -1 and content != '':

            stylesheet = """QComboBox {
                                                padding: 1px 18px 1px 15px;
                                                color:red;
                                            }
                                            """

        else:
            stylesheet = """QComboBox {
                                                padding: 1px 18px 1px 15px;
                                            }"""

        if self.required:
            stylesheet += """\nQLabel {
                                                font: bold;
                                            }
                               QFrame {
                                  background-color: rgb(117, 186, 202)
                                  }"""

        self.setStyleSheet(stylesheet)


if __name__ == "__main__":
    app = QApplication([])
    app.title = 'NABat Guano MD Editor'
    widget = KeyValuePicklist('test_key', ['item1', 'item2', 'item3'], description='testing')
    widget.load_data('test_value')
    widget.setWindowTitle(app.title)
    widget.show()
    sys.exit(app.exec_())
