from PyQt5 import QtCore, QtWidgets


class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QtWidgets.QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.DownArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self.content_area, b"maximumHeight"))

    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.toggle_animation.setDirection(QtCore.QAbstractAnimation.Forward if not checked else QtCore.QAbstractAnimation.Backward)
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height )
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


# if __name__ == '__main__':
#     import sys
#     import random
#
#     app = QtWidgets.QApplication(sys.argv)
#
#     w = QtWidgets.QMainWindow()
#     w.setCentralWidget(QtWidgets.QWidget())
#     dock = QtWidgets.QDockWidget("Collapsible Demo")
#     w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
#     scroll = QtWidgets.QScrollArea()
#     dock.setWidget(scroll)
#     content = QtWidgets.QWidget()
#     scroll.setWidget(content)
#     scroll.setWidgetResizable(True)
#     vlay = QtWidgets.QVBoxLayout(content)
#
#     nabat_ns = load_nabat_namespace()
#
#     # for i in range(10):
#     #     box = CollapsibleBox("Collapsible Box Header-{}".format(i))
#     #     vlay.addWidget(box)
#     #     lay = QtWidgets.QVBoxLayout()
#     #     for j in range(8):
#     #         label = QtWidgets.QLabel("{}".format(j))
#     #         color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
#     #         label.setStyleSheet("background-color: {}; color : white;".format(color.name()))
#     #         label.setAlignment(QtCore.Qt.AlignCenter)
#     #         lay.addWidget(label)
#     #
#     #     box.setContentLayout(lay)
#
#     box = CollapsibleBox("NABat")
#     box.setMinimumWidth(250)
#     lay = QtWidgets.QVBoxLayout()
#     lay.setSpacing(1)
#     vlay.addWidget(box)
#     for k,v in nabat_ns.items():
#         kv = KeyValue()
#         kv.load_data((k, v))
#         lay.addWidget(kv)
#         # self.items.append(kv)
#         # self.ui.namespace_group.layout().addWidget(kv)
#     box.setContentLayout(lay)
#
#     box2 = CollapsibleBox("NABat2")
#     lay2 = QtWidgets.QVBoxLayout()
#     vlay.addWidget((box2))
#     for k,v in nabat_ns.items():
#         kv = KeyValue()
#         kv.load_data((k, v))
#         lay2.addWidget(kv)
#         # self.items.append(kv)
#         # self.ui.namespace_group.layout().addWidget(kv)
#     box2.setContentLayout(lay2)
#
#     vlay.addStretch()
#     w.resize(640, 1480)
#     w.show()
#     sys.exit(app.exec_())