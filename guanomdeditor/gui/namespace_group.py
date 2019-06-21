import sys
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout

from guanomdeditor.gui.key_value import KeyValue
from guanomdeditor.gui.key_value_picklist import KeyValuePicklist
from guanomdeditor.gui.ui_files.CollapsibleBox import CollapsibleBox


class NamespaceGroup(CollapsibleBox):

    def __init__(self, namespace_name, items={}, parent=None):

        CollapsibleBox.__init__(self, parent=parent)

        self.namespace_name = namespace_name
        self.items = OrderedDict()

        self.setMinimumWidth(250)
        self.lay = QVBoxLayout()
        self.lay.setSpacing(1)

        self.toggle_button.setText(namespace_name)

        for item in items:
            if item.get('picklist', ''):
                kv = KeyValuePicklist(item['tag'], item['picklist'],
                                      description=item.get('description', ''),
                                      required=item.get('required', 0))
            else:
                kv = KeyValue(item['tag'], description=item.get('description', ''),
                              required=item.get('required', 0))
                kv.load_data('')

            self.items[item['tag']] = kv
            self.lay.addWidget(kv)
        self.setContentLayout(self.lay)

    def load_data(self, items_dict):

        for k, v in items_dict.items():
            if k in self.items:
                self.items[k].load_data(v)
            else:
                kv = KeyValue(k, description='Item not in spec')
                kv.ui.key_label.setStyleSheet("""QLabel {
                                                color:red;
                                            }""")
                kv.load_data(v)
                self.items[k] = kv
                self.lay.addWidget(kv)
                print(f"missing key in spec:{k}")

        self.on_pressed()
        self.toggle_button.setChecked(True)

    def get_data(self):

        data = OrderedDict()
        for k, v in self.items.items():
            data[k] = v.get_data()

        return data


if __name__ == "__main__":
    app = QApplication([])
    app.title = 'NABat Guano MD Editor'
    nabat_ns = load_nabat_namespace()
    widget = NamespceGroup( 'test namespace name', nabat_ns )


    data = {'Site Name':'test_1',
            'Latitude':'111'}

    widget.load_data(data)
    widget.setWindowTitle(app.title)
    widget.show()
    sys.exit(app.exec_())
